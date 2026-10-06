#!/usr/bin/env python3
"""Extract interfaced project codes from interfaces-text and add them to json_files.

For each ``interfaces-text/<code>-text.txt`` the script finds project codes with
a regex, corrects codes whose written name points to a different registry
project, asks Gemma 4 (through the local Ollama API) to judge the candidates and
resolve name-only references, then validates the answer against the registry in
``json_files``. Results are cached per project in ``interfaces-out/raw`` so
projects can be run one at a time. Projects with empty text are cached
automatically without calling Gemma.

Manual fixes go in ``interfaces-out/overrides.json``, keyed by project code:

    {"SRP8-186": {"add": ["SRP8-094"], "remove": ["SRP8-130"], "note": "why"}}

"add" links the two projects; "remove" vetoes the link in both directions, even
if the other project's text lists it. Overrides survive re-runs.

Once every project has a result, ``write`` makes links symmetric, applies the
overrides and gives each project JSON an ``"interfaces"`` array. Every command
refreshes the review report at ``interfaces-out/report.md``.

Usage:
    python3 extract_interfaces.py status
    python3 extract_interfaces.py run SRP8-186 [SRP8-130 ...] [--force]
    python3 extract_interfaces.py next [--count 3]
    python3 extract_interfaces.py report
    python3 extract_interfaces.py write
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
JSON_DIR = DIRECTORY / "json_files"
TEXT_DIR = DIRECTORY / "interfaces-text"
OUT_DIR = DIRECTORY / "interfaces-out"
RAW_DIR = OUT_DIR / "raw"
REPORT_PATH = OUT_DIR / "report.md"
OVERRIDES_PATH = OUT_DIR / "overrides.json"

OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "gemma4:12b"
PROMPT_VERSION = "1"

CODE_PATTERN = re.compile(r"\bSRP\s*8?\s*[-\u2013\u2014]?\s*(\d{2,3})(?!\d)", re.IGNORECASE)
# Shorthand for further codes straight after one, e.g. the "/ 012 / 013" in "SRP8-011 / 012 / 013 Lamps".
CONTINUATION_PATTERN = re.compile(r"\s*/\s*(\d{2,3})(?!\d)")
SEPARATORS = " \t:-\u2013\u2014|(),."

# A written name must match another registry project at least this well, and
# beat the written code's own registry name by at least NAME_MARGIN, before the
# code is corrected.
NAME_MATCH_MIN = 0.85
NAME_MARGIN = 0.3


@dataclass(frozen=True)
class Project:
    code: str
    name: str
    path: Path


def normalise_code(number: str) -> str:
    return f"SRP8-{int(number):03d}"


def parse_code(value: str) -> str | None:
    match = CODE_PATTERN.fullmatch(value.strip())
    return normalise_code(match.group(1)) if match else None


def normalise_text(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.lower()).split())


def load_registry() -> dict[str, Project]:
    registry: dict[str, Project] = {}
    for path in sorted(JSON_DIR.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        match = CODE_PATTERN.search(record.get("project_id") or "")
        if not match:
            print(f"warning: {path.name} has no usable project_id, skipped", file=sys.stderr)
            continue
        code = normalise_code(match.group(1))
        registry[code] = Project(code, (record.get("project_name") or "").strip(), path)
    return registry


def find_text_files(registry: dict[str, Project]) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for path in sorted(TEXT_DIR.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        code = parse_code(re.sub(r"-text$", "", path.stem, flags=re.IGNORECASE))
        if code not in registry:
            print(f"warning: {path.name} does not match any project JSON, skipped", file=sys.stderr)
            continue
        files[code] = path
    return files


def read_text(path: Path | None) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path else ""


# ---------------------------------------------------------------------------
# Regex candidates and code-name check
# ---------------------------------------------------------------------------


def written_names(text: str, matches: list[re.Match], index: int) -> tuple[str, str]:
    """Return the text before and after a code on its line, stopping at neighbouring codes and "|".

    Tables put the name before the code ("Door Handles SRP-002"), lists and
    paragraphs often put it after ("SRP-011 - Taillights"), and some tables put
    the code alone on a line with the name on the next non-empty line.
    """
    match = matches[index]
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.end())
    line_end = len(text) if line_end == -1 else line_end
    if index > 0:
        line_start = max(line_start, matches[index - 1].end())
    if index + 1 < len(matches):
        line_end = min(line_end, matches[index + 1].start())
    before = text[line_start : match.start()].rpartition("|")[2].strip(SEPARATORS)[-80:]
    after_start = match.end()
    while continuation := CONTINUATION_PATTERN.match(text, after_start):
        after_start = continuation.end()
    after = text[after_start : max(after_start, line_end)].partition("|")[0].strip(SEPARATORS)[:80]
    if not before and not after:
        for line in text[line_end:].splitlines():
            if line.strip():
                if not CODE_PATTERN.search(line):
                    after = line.strip(SEPARATORS)[:80]
                break
    return before, after


def name_similarity(before: str, after: str, registry_name: str) -> float:
    """Compare a registry name with the same number of words right before or right after a code."""
    target = normalise_text(registry_name)
    if not target:
        return 0.0
    size = len(target.split())
    scores = [0.0]
    if words := normalise_text(after).split():
        scores.append(difflib.SequenceMatcher(None, " ".join(words[:size]), target).ratio())
    if words := normalise_text(before).split():
        scores.append(difflib.SequenceMatcher(None, " ".join(words[-size:]), target).ratio())
    return max(scores)


def best_name_match(
    before: str, after: str, registry: dict[str, Project], exclude: set[str]
) -> tuple[str | None, float]:
    best_code, best_score = None, 0.0
    for code, project in registry.items():
        if code in exclude:
            continue
        score = name_similarity(before, after, project.name)
        if score > best_score:
            best_code, best_score = code, score
    return best_code, best_score


def regex_candidates(text: str, registry: dict[str, Project], source: str) -> list[dict]:
    matches = list(CODE_PATTERN.finditer(text))
    candidates = []
    for index, match in enumerate(matches):
        code = normalise_code(match.group(1))
        before, after = written_names(text, matches, index)
        own_score = name_similarity(before, after, registry[code].name) if code in registry else 0.0
        best_code, best_score = best_name_match(before, after, registry, exclude={code, source})
        corrected = None
        if best_code and best_score >= NAME_MATCH_MIN and best_score - own_score >= NAME_MARGIN:
            corrected = best_code
        candidates.append(
            {
                "written": match.group(0),
                "code": code,
                "text_before": before,
                "text_after": after,
                "corrected_to": corrected,
                "final": corrected or code,
            }
        )
        position = match.end()
        while continuation := CONTINUATION_PATTERN.match(text, position):
            position = continuation.end()
            extra = normalise_code(continuation.group(1))
            candidates.append(
                {
                    "written": text[match.start() : position].strip(),
                    "code": extra,
                    "text_before": before,
                    "text_after": after,
                    "corrected_to": None,
                    "final": extra,
                }
            )
    return candidates

# Gemma

SYSTEM_PROMPT = (
    "You extract project interface links from excerpts of engineering design reports. "
    "Respond only with JSON that matches the given schema."
)


def build_prompt(source: Project, text: str, candidates: list[str], registry: dict[str, Project]) -> str:
    registry_lines = "\n".join(
        f"{code}: {project.name}" for code, project in sorted(registry.items()) if code != source.code
    )
    candidate_lines = (
        "\n".join(f"{code}: {registry[code].name}" for code in candidates) if candidates else "(none)"
    )
    return f"""Source project: {source.code} ({source.name})

The text below is the interfaces section of the source project's detailed design report. List every OTHER project that the source project interfaces with.

Rules:
- Include every project listed in an interface table or list, even when no explanation is given.
- Include projects that paragraphs describe as exchanging data, signals, power, mechanical mounting, space, or otherwise depending on the source project.
- The text may refer to projects by code (formats vary, e.g. SRP8-012, SRP-012) or by name only. Resolve name-only references to codes using the registry. If a name does not clearly match a registry project, leave it out.
- The codes already found in the text are listed below. Include them unless the text clearly says there is no interface with that project.
- Never include the source project itself. Only use codes from the registry.
- For each project, "evidence" is a short snippet copied exactly from the text (at most 15 words) that mentions that project.

Registry (code: name):
{registry_lines}

Codes found in the text (code: registry name):
{candidate_lines}

Text:
\"\"\"
{text.strip()}
\"\"\"
"""


def response_schema(allowed_codes: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "interfaces": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "enum": allowed_codes},
                        "evidence": {"type": "string"},
                    },
                    "required": ["code", "evidence"],
                },
            }
        },
        "required": ["interfaces"],
    }


def check_ollama(model: str) -> None:
    try:
        with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=10) as response:
            tags = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as error:
        sys.exit(f"error: cannot reach Ollama at {OLLAMA_HOST} ({error}). Start it with `ollama serve` or the Ollama app.")
    names = {entry.get("name") for entry in tags.get("models", [])}
    if model not in names and f"{model}:latest" not in names:
        sys.exit(f"error: model {model} is not installed in Ollama. Run `ollama pull {model}`.")


def call_gemma(model: str, prompt: str, schema: dict, retries: int = 2) -> dict:
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "format": schema,
            "stream": False,
            "think": False,
            "options": {"temperature": 0, "seed": 0, "num_ctx": 16384},
        }
    ).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(
                f"{OLLAMA_HOST}/api/chat", data=payload, headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(request, timeout=900) as response:
                body = json.loads(response.read().decode("utf-8"))
            return json.loads(body["message"]["content"])
        except (urllib.error.URLError, json.JSONDecodeError, KeyError, TimeoutError) as error:
            last_error = error
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Ollama request failed after {retries + 1} attempts: {last_error}")


# ---------------------------------------------------------------------------
# Extraction, validation and cache
# ---------------------------------------------------------------------------


def evidence_in_text(evidence: str, text: str) -> bool:
    needle, haystack = normalise_text(evidence), normalise_text(text)
    if not needle:
        return False
    if needle in haystack:
        return True
    matcher = difflib.SequenceMatcher(None, haystack, needle, autojunk=False)
    match = matcher.find_longest_match(0, len(haystack), 0, len(needle))
    return match.size >= 0.85 * len(needle)


def extract(source: Project, text: str, registry: dict[str, Project], model: str) -> dict:
    candidates = regex_candidates(text, registry, source.code)
    known = sorted({c["final"] for c in candidates if c["final"] in registry and c["final"] != source.code})
    unknown = sorted({c["final"] for c in candidates if c["final"] not in registry})

    allowed = [code for code in sorted(registry) if code != source.code]
    raw = call_gemma(model, build_prompt(source, text, known, registry), response_schema(allowed))

    accepted: dict[str, dict] = {}
    rejected_gemma: list[dict] = []
    for item in raw.get("interfaces", []):
        code, evidence = item.get("code"), (item.get("evidence") or "").strip()
        if code not in registry or code == source.code:
            rejected_gemma.append({"code": code, "evidence": evidence, "reason": "not a valid other project"})
        elif code in known:
            accepted.setdefault(code, {"code": code, "via": "regex", "evidence": evidence})
        elif evidence_in_text(evidence, text):
            accepted.setdefault(code, {"code": code, "via": "name", "evidence": evidence})
        else:
            rejected_gemma.append({"code": code, "evidence": evidence, "reason": "evidence not found in text"})

    return {
        "candidates": candidates,
        "unknown_dropped": unknown,
        "gemma_raw": raw,
        "accepted": sorted(accepted.values(), key=lambda item: item["code"]),
        "rejected_regex": [code for code in known if code not in accepted],
        "rejected_gemma": rejected_gemma,
    }


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cache_path(code: str) -> Path:
    return RAW_DIR / f"{code}.json"


def load_cache(code: str) -> dict | None:
    path = cache_path(code)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def is_fresh(cached: dict | None, digest: str) -> bool:
    return bool(cached and cached.get("text_sha256") == digest and cached.get("prompt_version") == PROMPT_VERSION)


def save_cache(record: dict) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache_path(record["project_id"]).write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def base_record(source: Project, text_path: Path | None, text: str) -> dict:
    return {
        "project_id": source.code,
        "project_name": source.name,
        "source_file": text_path.name if text_path else None,
        "text_sha256": text_hash(text),
        "prompt_version": PROMPT_VERSION,
    }


def cache_empty_projects(registry: dict[str, Project], text_files: dict[str, Path]) -> None:
    """Empty-text projects need no Gemma call, so give them an empty result straight away."""
    for code, source in sorted(registry.items()):
        text = read_text(text_files.get(code))
        if text.strip() or is_fresh(load_cache(code), text_hash(text)):
            continue
        record = base_record(source, text_files.get(code), text)
        record.update(
            model=None, candidates=[], unknown_dropped=[], gemma_raw=None,
            accepted=[], rejected_regex=[], rejected_gemma=[],
        )
        save_cache(record)


def run_gemma(source: Project, text_path: Path, registry: dict[str, Project], model: str) -> dict:
    text = read_text(text_path)
    record = base_record(source, text_path, text)
    print(f"{source.code} ({source.name}): asking {model}...", flush=True)
    started = time.monotonic()
    record["model"] = model
    record.update(extract(source, text, registry, model))
    record["seconds"] = round(time.monotonic() - started, 1)
    save_cache(record)
    return record


def project_state(code: str, text_files: dict[str, Path]) -> tuple[str, dict | None]:
    """Return ("empty" | "done" | "stale" | "pending", cached record)."""
    text = read_text(text_files.get(code))
    cached = load_cache(code)
    if not text.strip():
        return "empty", cached
    if cached is None:
        return "pending", None
    return ("done" if is_fresh(cached, text_hash(text)) else "stale"), cached


# ---------------------------------------------------------------------------
# Overrides
# ---------------------------------------------------------------------------


def load_overrides(registry: dict[str, Project]) -> dict[str, dict[str, list[str]]]:
    if not OVERRIDES_PATH.exists():
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OVERRIDES_PATH.write_text("{}\n", encoding="utf-8")
        return {}
    try:
        data = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        sys.exit(f"error: {OVERRIDES_PATH} is not valid JSON: {error}")

    overrides: dict[str, dict[str, list[str]]] = {}
    for key, entry in data.items():
        source = parse_code(key)
        if source not in registry:
            sys.exit(f"error: overrides.json key {key!r} is not a project in {JSON_DIR}")
        cleaned: dict[str, list[str]] = {}
        for action in ("add", "remove"):
            codes = []
            for value in entry.get(action, []):
                code = parse_code(value)
                if code not in registry or code == source:
                    sys.exit(f"error: overrides.json {key} {action} {value!r} is not another project in {JSON_DIR}")
                codes.append(code)
            cleaned[action] = sorted(set(codes))
        overrides[source] = cleaned
    return overrides


# ---------------------------------------------------------------------------
# Symmetrise, write, report
# ---------------------------------------------------------------------------


def combine(
    results: dict[str, dict], overrides: dict[str, dict[str, list[str]]]
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Symmetrise extracted links, then apply overrides. Returns (final, added_by_symmetry)."""
    links = {code: {item["code"] for item in record["accepted"]} for code, record in results.items()}
    final = {code: set(codes) for code, codes in links.items()}
    for source, targets in links.items():
        for target in targets:
            final.setdefault(target, set()).add(source)
    reverse_only = {code: sorted(final[code] - links.get(code, set())) for code in final}

    for source, entry in overrides.items():
        for target in entry["add"]:
            final.setdefault(source, set()).add(target)
            final.setdefault(target, set()).add(source)
    for source, entry in overrides.items():
        for target in entry["remove"]:
            final.setdefault(source, set()).discard(target)
            final.setdefault(target, set()).discard(source)
    return {code: sorted(codes) for code, codes in final.items()}, reverse_only


def write_json_files(registry: dict[str, Project], final: dict[str, list[str]]) -> None:
    for code, project in sorted(registry.items()):
        record = json.loads(project.path.read_text(encoding="utf-8"))
        record.pop("interfaces", None)
        record["interfaces"] = final.get(code, [])
        project.path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote interfaces to {len(registry)} project JSON files in {JSON_DIR}")


def label(registry: dict[str, Project], code: str) -> str:
    return f"{code} ({registry[code].name})" if code in registry else str(code)


def describe_candidate(registry: dict[str, Project], candidate: dict) -> str:
    context = " | ".join(part for part in (candidate["text_before"], candidate["text_after"]) if part)
    return f"`{candidate['written']}` near \"{context}\" -> {label(registry, candidate['corrected_to'])}"


def write_report(
    registry: dict[str, Project],
    text_files: dict[str, Path],
    results: dict[str, dict],
    overrides: dict[str, dict[str, list[str]]],
) -> None:
    final, reverse_only = combine(results, overrides)
    states = {code: project_state(code, text_files)[0] for code in registry}
    pending = [code for code, state in sorted(states.items()) if state in ("pending", "stale")]
    stale = [code for code, state in sorted(states.items()) if state == "stale"]
    with_text = [code for code, state in states.items() if state != "empty"]
    done = [code for code in with_text if states[code] == "done"]

    lines = [
        "# Interface extraction report",
        "",
        f"- Projects in registry: {len(registry)} ({len(with_text)} with interface text, "
        f"{len(registry) - len(with_text)} empty)",
        f"- Projects run through Gemma: {len(done)} of {len(with_text)}",
        f"- Projects still to run: {len(pending)}" + (f" ({', '.join(pending)})" if pending else ""),
        f"- Text changed since last run (stale): {', '.join(stale) or 'none'}",
        f"- Links extracted from text: {sum(len(r['accepted']) for r in results.values())}",
        f"- Links after symmetry and overrides: {sum(len(v) for v in final.values())}",
        f"- Regex codes rejected by Gemma: {sum(len(r['rejected_regex']) for r in results.values())}",
        f"- Gemma answers rejected by validation: {sum(len(r['rejected_gemma']) for r in results.values())}",
        f"- Code-name corrections: {sum(1 for r in results.values() for c in r['candidates'] if c['corrected_to'])}",
        f"- Projects with manual overrides: {len(overrides)}",
        "",
    ]

    for code in sorted(registry):
        record = results.get(code)
        state = states[code]
        if state == "empty" and not final.get(code) and code not in overrides:
            continue
        lines.append(f"## {label(registry, code)}")
        lines.append("")
        lines.append(f"- Status: {state}")
        lines.append(f"- Source file: `{text_files[code].name}`" if code in text_files else "- Source file: none")
        lines.append(f"- Final interfaces: {', '.join(final.get(code, [])) or 'none'}")
        if reverse_only.get(code):
            lines.append(f"- Added only through symmetry: {', '.join(reverse_only[code])}")
        if code in overrides:
            entry = overrides[code]
            lines.append(
                f"- Manual overrides: add {', '.join(entry['add']) or 'none'}; remove {', '.join(entry['remove']) or 'none'}"
            )
        if record is None:
            lines.append("")
            continue
        name_refs = [item for item in record["accepted"] if item["via"] == "name"]
        if name_refs:
            lines.append("- Name-only references added by Gemma:")
            lines.extend(f"  - {label(registry, item['code'])}: \"{item['evidence']}\"" for item in name_refs)
        corrections = [c for c in record["candidates"] if c["corrected_to"]]
        if corrections:
            lines.append("- Code-name corrections (registry wins):")
            lines.extend(f"  - {describe_candidate(registry, c)}" for c in corrections)
        if record["unknown_dropped"]:
            lines.append(f"- Codes not in json_files (dropped): {', '.join(record['unknown_dropped'])}")
        if record["rejected_regex"]:
            rejected = ", ".join(label(registry, c) for c in record["rejected_regex"])
            lines.append(f"- Codes found by regex but rejected by Gemma: {rejected}")
        if record["rejected_gemma"]:
            lines.append("- Gemma answers rejected by validation:")
            lines.extend(
                f"  - {item['code']}: {item['reason']} (\"{item['evidence']}\")" for item in record["rejected_gemma"]
            )
        lines.append("")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def print_review(registry: dict[str, Project], record: dict, overrides: dict[str, dict[str, list[str]]]) -> None:
    code = record["project_id"]
    print(f"\n{label(registry, code)}  [{record.get('model')}, {record.get('seconds', '?')}s]")
    if not record["accepted"]:
        print("  Accepted: none")
    else:
        print("  Accepted:")
        for item in record["accepted"]:
            print(f"    {label(registry, item['code'])}  [{item['via']}]  \"{item['evidence']}\"")
    corrections = [c for c in record["candidates"] if c["corrected_to"]]
    if corrections:
        print("  Code-name corrections:")
        for candidate in corrections:
            print(f"    {describe_candidate(registry, candidate)}")
    if record["unknown_dropped"]:
        print(f"  Codes not in json_files (dropped): {', '.join(record['unknown_dropped'])}")
    if record["rejected_regex"]:
        print(f"  Regex codes Gemma rejected: {', '.join(label(registry, c) for c in record['rejected_regex'])}")
    for item in record["rejected_gemma"]:
        print(f"  Rejected by validation: {item['code']} ({item['reason']}) \"{item['evidence']}\"")
    if code in overrides:
        entry = overrides[code]
        print(f"  Overrides: add {', '.join(entry['add']) or 'none'}; remove {', '.join(entry['remove']) or 'none'}")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@dataclass
class Context:
    registry: dict[str, Project]
    text_files: dict[str, Path]
    overrides: dict[str, dict[str, list[str]]]


def all_results(registry: dict[str, Project]) -> dict[str, dict]:
    return {code: cached for code in registry if (cached := load_cache(code)) is not None}


def to_run(context: Context) -> list[str]:
    return [
        code for code in sorted(context.registry)
        if project_state(code, context.text_files)[0] in ("pending", "stale")
    ]


def print_progress(context: Context) -> None:
    remaining = to_run(context)
    with_text = sum(1 for code in context.registry if read_text(context.text_files.get(code)).strip())
    print(f"\nProgress: {with_text - len(remaining)}/{with_text} projects with text done.", end=" ")
    print(f"Next: {remaining[0]} ({context.registry[remaining[0]].name})" if remaining else "All done; run `write`.")
    print(f"Report: {REPORT_PATH}")


def run_projects(context: Context, codes: list[str], model: str, force: bool) -> None:
    for code in codes:
        state, cached = project_state(code, context.text_files)
        if state == "empty":
            print(f"{label(context.registry, code)}: text is empty, nothing to run (interfaces = [] unless linked from others)")
            continue
        if state == "done" and not force:
            print(f"{code}: already done with {cached.get('model')}; showing cached result (use --force to re-run)")
            print_review(context.registry, cached, context.overrides)
            continue
        check_ollama(model)
        record = run_gemma(context.registry[code], context.text_files[code], context.registry, model)
        print_review(context.registry, record, context.overrides)
        write_report(context.registry, context.text_files, all_results(context.registry), context.overrides)


def command_run(context: Context, args: argparse.Namespace) -> None:
    codes = []
    for value in args.codes:
        code = parse_code(value)
        if code not in context.registry:
            sys.exit(f"error: {value} is not a project in {JSON_DIR}")
        codes.append(code)
    run_projects(context, codes, args.model, args.force)
    print_progress(context)


def command_next(context: Context, args: argparse.Namespace) -> None:
    codes = to_run(context)[: args.count]
    if not codes:
        print("Nothing left to run.")
    run_projects(context, codes, args.model, force=False)
    print_progress(context)


def command_status(context: Context, args: argparse.Namespace) -> None:
    print(f"{'code':<9} {'state':<8} {'chars':>5} {'links':>5} {'name':>4} {'rej':>3} {'ovr':>3}  name")
    for code, project in sorted(context.registry.items()):
        state, cached = project_state(code, context.text_files)
        if state == "empty" and not args.all:
            continue
        chars = len(read_text(context.text_files.get(code)).strip())
        accepted = cached["accepted"] if cached else []
        rejected = len(cached["rejected_regex"]) + len(cached["rejected_gemma"]) if cached else 0
        name_refs = sum(1 for item in accepted if item["via"] == "name")
        counts = [len(accepted), name_refs, rejected] if state in ("done", "stale") else ["-", "-", "-"]
        override = "yes" if code in context.overrides else ""
        print(
            f"{code:<9} {state:<8} {chars:>5} {counts[0]:>5} {counts[1]:>4} "
            f"{counts[2]:>3} {override:>3}  {project.name}"
        )
    if not args.all:
        print("(empty-text projects hidden; use --all to show them)")
    print_progress(context)


def command_report(context: Context, args: argparse.Namespace) -> None:
    print(f"Wrote report to {REPORT_PATH}")


def command_write(context: Context, args: argparse.Namespace) -> None:
    remaining = to_run(context)
    if remaining:
        sys.exit(f"error: not writing project JSONs; {len(remaining)} projects still need a run: {', '.join(remaining)}")
    final, _ = combine(all_results(context.registry), context.overrides)
    write_json_files(context.registry, final)
    print(f"Wrote report to {REPORT_PATH}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="Run Gemma on specific projects and print the result for review")
    run.add_argument("codes", nargs="+", help="Project codes, e.g. SRP8-186 srp8-023")
    run.add_argument("--force", action="store_true", help="Re-run even if a cached result exists")
    run.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    run.set_defaults(handler=command_run)

    next_ = commands.add_parser("next", help="Run Gemma on the next project(s) that have no result yet")
    next_.add_argument("--count", type=int, default=1, help="How many projects to run (default: 1)")
    next_.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    next_.set_defaults(handler=command_next)

    status = commands.add_parser("status", help="Show which projects are done, pending or stale")
    status.add_argument("--all", action="store_true", help="Also list projects with empty text")
    status.set_defaults(handler=command_status)

    commands.add_parser("report", help="Regenerate interfaces-out/report.md").set_defaults(handler=command_report)
    commands.add_parser(
        "write", help="Symmetrise, apply overrides and write interfaces into json_files (needs every project done)"
    ).set_defaults(handler=command_write)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    registry = load_registry()
    text_files = find_text_files(registry)
    context = Context(registry, text_files, load_overrides(registry))
    cache_empty_projects(registry, text_files)
    args.handler(context, args)
    write_report(registry, text_files, all_results(registry), context.overrides)


if __name__ == "__main__":
    main()
