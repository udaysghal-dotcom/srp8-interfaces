# Interface extraction report

- Projects in registry: 91 (42 with interface text, 49 empty)
- Projects run through Gemma: 41 of 42
- Projects still to run: 1 (SRP8-192)
- Text changed since last run (stale): SRP8-192
- Links extracted from text: 260
- Links after symmetry and overrides: 482
- Regex codes rejected by Gemma: 1
- Gemma answers rejected by validation: 0
- Code-name corrections: 2
- Projects with manual overrides: 0

## SRP8-001 (Doors)

- Status: done
- Source file: `srp8-001-text.txt`
- Final interfaces: SRP8-002, SRP8-037, SRP8-059, SRP8-065, SRP8-083, SRP8-084, SRP8-085, SRP8-092, SRP8-111, SRP8-112, SRP8-130, SRP8-167, SRP8-173
- Added only through symmetry: SRP8-037, SRP8-059, SRP8-083, SRP8-130, SRP8-167, SRP8-173
- Codes not in json_files (dropped): SRP8-006, SRP8-102, SRP8-122

## SRP8-002 (Door Handles)

- Status: done
- Source file: `srp8-002-text.txt`
- Final interfaces: SRP8-001, SRP8-032, SRP8-059, SRP8-065, SRP8-092, SRP8-111, SRP8-112, SRP8-130, SRP8-173
- Added only through symmetry: SRP8-032, SRP8-059, SRP8-112, SRP8-130, SRP8-173
- Codes not in json_files (dropped): SRP8-006, SRP8-102, SRP8-122

## SRP8-003 (Windscreen)

- Status: done
- Source file: `srp8-003-text.txt`
- Final interfaces: SRP8-023, SRP8-037, SRP8-065, SRP8-082, SRP8-167
- Added only through symmetry: SRP8-023, SRP8-037, SRP8-167
- Codes not in json_files (dropped): SRP8-122

## SRP8-004 (Boot)

- Status: done
- Source file: `srp8-004-text.txt`
- Final interfaces: SRP8-011, SRP8-020, SRP8-130, SRP8-167, SRP8-172, SRP8-173
- Added only through symmetry: SRP8-130, SRP8-167, SRP8-172, SRP8-173
- Codes not in json_files (dropped): SRP8-006, SRP8-122

## SRP8-005 (Bonnet)

- Status: done
- Source file: `srp8-005-text.txt`
- Final interfaces: SRP8-010, SRP8-012, SRP8-020, SRP8-065, SRP8-066, SRP8-130, SRP8-167
- Added only through symmetry: SRP8-010, SRP8-012, SRP8-130, SRP8-167
- Codes not in json_files (dropped): SRP8-067

## SRP8-010 (Ventilation)

- Status: done
- Source file: `srp8-010-text.txt`
- Final interfaces: SRP8-005, SRP8-016, SRP8-037, SRP8-038, SRP8-045, SRP8-083, SRP8-085, SRP8-093, SRP8-094, SRP8-167
- Added only through symmetry: SRP8-037, SRP8-085, SRP8-094, SRP8-167
- Name-only references added by Gemma:
  - SRP8-005 (Bonnet): "Cooling of bonnet"
  - SRP8-016 (Battery): "battery"
  - SRP8-038 (Motors): "Motor Cooling"
  - SRP8-045 (Front Brakes): "front brakes"
  - SRP8-083 (Active Aero): "Active Aero"
  - SRP8-093 (Air Conditioning): "Air conditioning function"

## SRP8-011 (Tailights)

- Status: done
- Source file: `srp8-011-text.txt`
- Final interfaces: SRP8-004, SRP8-013, SRP8-014, SRP8-017, SRP8-022, SRP8-026, SRP8-059, SRP8-077, SRP8-092, SRP8-099, SRP8-124, SRP8-130, SRP8-132
- Added only through symmetry: SRP8-004, SRP8-013, SRP8-022, SRP8-059, SRP8-077, SRP8-092, SRP8-130, SRP8-132
- Codes not in json_files (dropped): SRP8-006

## SRP8-012 (Headlights)

- Status: done
- Source file: `srp8-012-text.txt`
- Final interfaces: SRP8-005, SRP8-013, SRP8-022, SRP8-059, SRP8-092, SRP8-130, SRP8-132, SRP8-167
- Added only through symmetry: SRP8-013, SRP8-022, SRP8-059, SRP8-092, SRP8-130, SRP8-132

## SRP8-013 (Indicators)

- Status: done
- Source file: `srp8-013-text.txt`
- Final interfaces: SRP8-011, SRP8-012, SRP8-022, SRP8-092, SRP8-130, SRP8-132, SRP8-167
- Added only through symmetry: SRP8-092, SRP8-130, SRP8-132, SRP8-167
- Codes not in json_files (dropped): SRP8-006

## SRP8-014 (Regen Braking)

- Status: done
- Source file: `srp8-014-text.txt`
- Final interfaces: SRP8-011, SRP8-016, SRP8-022, SRP8-026, SRP8-038, SRP8-039, SRP8-058, SRP8-077, SRP8-092, SRP8-130
- Added only through symmetry: SRP8-011, SRP8-022, SRP8-026, SRP8-077, SRP8-092, SRP8-130

## SRP8-016 (Battery)

- Status: done
- Source file: `srp8-016-text.txt`
- Final interfaces: SRP8-010, SRP8-014, SRP8-017, SRP8-018, SRP8-021, SRP8-029, SRP8-039, SRP8-094
- Added only through symmetry: SRP8-010, SRP8-014, SRP8-029, SRP8-039

## SRP8-017 (Auxillary Power Distribution)

- Status: done
- Source file: `srp8-017-text.txt`
- Final interfaces: SRP8-011, SRP8-016, SRP8-020, SRP8-022, SRP8-026, SRP8-077, SRP8-133, SRP8-189
- Added only through symmetry: SRP8-011, SRP8-016, SRP8-022, SRP8-026, SRP8-077
- Name-only references added by Gemma:
  - SRP8-020 (Solar Array): "receiving power from the solar system"
  - SRP8-133 (Hydrogen Fuel Cell): "receiving power from the hydrogen fuel cell source"
  - SRP8-189 (Bidirectional DCDC): "Auxiliary Battery ↔ DC-DC"

## SRP8-018 (Energy Control)

- Status: done
- Source file: `srp8-018-text.txt`
- Final interfaces: SRP8-016, SRP8-019, SRP8-020, SRP8-021, SRP8-055, SRP8-083, SRP8-130, SRP8-133, SRP8-175
- Added only through symmetry: SRP8-020, SRP8-083, SRP8-130
- Name-only references added by Gemma:
  - SRP8-016 (Battery): "Main battery voltage is routed through the rest of SR8"
  - SRP8-019 (MPPTs): "We are dependent upon MPPT parameters in designing the protections"
  - SRP8-021 (Charging): "Charging will be routed through the ECS"
  - SRP8-055 (Unified Embedded Node): "We are dependent upon the design of the UEN"
  - SRP8-133 (Hydrogen Fuel Cell): "We are dependent upon Hydrogen's electrical parameters"
  - SRP8-175 (Vehicle States Project): "ECS is dependent on vehicle states project"

## SRP8-019 (MPPTs)

- Status: empty
- Source file: `srp8-019-text.txt`
- Final interfaces: SRP8-018, SRP8-020, SRP8-130
- Added only through symmetry: SRP8-018, SRP8-020, SRP8-130

## SRP8-020 (Solar Array)

- Status: done
- Source file: `srp8-020-text.txt`
- Final interfaces: SRP8-004, SRP8-005, SRP8-017, SRP8-018, SRP8-019, SRP8-027, SRP8-167
- Added only through symmetry: SRP8-167
- Codes not in json_files (dropped): SRP8-006

## SRP8-021 (Charging)

- Status: empty
- Source file: `srp8-021-text.txt`
- Final interfaces: SRP8-016, SRP8-018, SRP8-167, SRP8-173
- Added only through symmetry: SRP8-016, SRP8-018, SRP8-167, SRP8-173

## SRP8-022 (Steering Wheel)

- Status: done
- Source file: `srp8-022-text.txt`
- Final interfaces: SRP8-011, SRP8-012, SRP8-013, SRP8-014, SRP8-017, SRP8-026, SRP8-029, SRP8-032, SRP8-037, SRP8-048, SRP8-049, SRP8-057, SRP8-059, SRP8-065, SRP8-082, SRP8-084, SRP8-130, SRP8-132
- Added only through symmetry: SRP8-059, SRP8-130, SRP8-132
- Name-only references added by Gemma:
  - SRP8-065 (Occupant Cell): "065

Occupant cell"
- Codes not in json_files (dropped): SRP8-015, SRP8-098

## SRP8-023 (Interior Lights)

- Status: done
- Source file: `srp8-023-text.txt`
- Final interfaces: SRP8-003, SRP8-027, SRP8-037, SRP8-130
- Added only through symmetry: SRP8-037, SRP8-130
- Codes not in json_files (dropped): SRP8-107

## SRP8-024 (Rear Vision System)

- Status: empty
- Source file: `srp8-024-text.txt`
- Final interfaces: SRP8-027, SRP8-037, SRP8-092, SRP8-130, SRP8-132
- Added only through symmetry: SRP8-027, SRP8-037, SRP8-092, SRP8-130, SRP8-132

## SRP8-025 (Side Vision System)

- Status: empty
- Source file: `srp8-025-text.txt`
- Final interfaces: SRP8-037, SRP8-092, SRP8-130, SRP8-132
- Added only through symmetry: SRP8-037, SRP8-092, SRP8-130, SRP8-132

## SRP8-026 (Pedals)

- Status: done
- Source file: `srp8-026-text.txt`
- Final interfaces: SRP8-011, SRP8-014, SRP8-017, SRP8-022, SRP8-032, SRP8-038, SRP8-045, SRP8-046, SRP8-065, SRP8-077, SRP8-130, SRP8-192
- Added only through symmetry: SRP8-022, SRP8-077, SRP8-130, SRP8-192

## SRP8-027 (Ceiling)

- Status: done
- Source file: `srp8-027-text.txt`
- Final interfaces: SRP8-020, SRP8-023, SRP8-024, SRP8-065
- Added only through symmetry: SRP8-023
- Name-only references added by Gemma:
  - SRP8-020 (Solar Array): "The roof solar subsystem may interface with the ceiling"
  - SRP8-024 (Rear Vision System): "mounting provisions for the high voltage cut off as well as the rear vision system"
  - SRP8-065 (Occupant Cell): "headliner interfaces directly with the occupant cell"

## SRP8-028 (Central Display)

- Status: empty
- Source file: `srp8-028-text.txt`
- Final interfaces: SRP8-029, SRP8-037, SRP8-092, SRP8-132
- Added only through symmetry: SRP8-029, SRP8-037, SRP8-092, SRP8-132

## SRP8-029 (Driver Display)

- Status: done
- Source file: `srp8-029-text.txt`
- Final interfaces: SRP8-016, SRP8-022, SRP8-028, SRP8-037, SRP8-055, SRP8-059, SRP8-092, SRP8-130, SRP8-132
- Added only through symmetry: SRP8-022, SRP8-092, SRP8-130, SRP8-132
- Codes not in json_files (dropped): SRP8-015, SRP8-060, SRP8-062, SRP8-095, SRP8-108, SRP8-121

## SRP8-032 (Front Seats)

- Status: done
- Source file: `srp8-032-text.txt`
- Final interfaces: SRP8-002, SRP8-022, SRP8-026, SRP8-034, SRP8-036, SRP8-037, SRP8-190
- Name-only references added by Gemma:
  - SRP8-002 (Door Handles): "occupants can access their respective door card controls."
  - SRP8-022 (Steering Wheel): "The driver side seat indirectly interfaces with the steering wheel."
  - SRP8-026 (Pedals): "This is covered in the pedals and seat mount"
  - SRP8-034 (Front Seatbelts): "While the seatbelts do not directly interface with the seats"
  - SRP8-037 (Dashboard): "placed on the dashboard and centre console."
  - SRP8-190 (Centre Console): "placed on the dashboard and centre console."

## SRP8-034 (Front Seatbelts)

- Status: empty
- Source file: `srp8-034-text.txt`
- Final interfaces: SRP8-032, SRP8-059, SRP8-132
- Added only through symmetry: SRP8-032, SRP8-059, SRP8-132

## SRP8-036 (Front Seat Mount)

- Status: empty
- Source file: `srp8-036-text.txt`
- Final interfaces: SRP8-032, SRP8-192
- Added only through symmetry: SRP8-032, SRP8-192

## SRP8-037 (Dashboard)

- Status: done
- Source file: `srp8-037-text.txt`
- Final interfaces: SRP8-001, SRP8-003, SRP8-010, SRP8-022, SRP8-023, SRP8-024, SRP8-025, SRP8-028, SRP8-029, SRP8-032, SRP8-048, SRP8-055, SRP8-065, SRP8-093
- Codes not in json_files (dropped): SRP8-062

## SRP8-038 (Motors)

- Status: empty
- Source file: `srp8-038-text.txt`
- Final interfaces: SRP8-010, SRP8-014, SRP8-026, SRP8-039, SRP8-059, SRP8-094, SRP8-130
- Added only through symmetry: SRP8-010, SRP8-014, SRP8-026, SRP8-039, SRP8-059, SRP8-094, SRP8-130

## SRP8-039 (Powertrain Electronics)

- Status: done
- Source file: `srp8-039-text.txt`
- Final interfaces: SRP8-014, SRP8-016, SRP8-038, SRP8-058, SRP8-094, SRP8-132
- Added only through symmetry: SRP8-014, SRP8-094, SRP8-132

## SRP8-043 (Front Suspension)

- Status: empty
- Source file: `srp8-043-text.txt`
- Final interfaces: SRP8-059, SRP8-167
- Added only through symmetry: SRP8-059, SRP8-167

## SRP8-044 (Rear Suspension)

- Status: empty
- Source file: `srp8-044-text.txt`
- Final interfaces: SRP8-059
- Added only through symmetry: SRP8-059

## SRP8-045 (Front Brakes)

- Status: empty
- Source file: `srp8-045-text.txt`
- Final interfaces: SRP8-010, SRP8-026, SRP8-167
- Added only through symmetry: SRP8-010, SRP8-026, SRP8-167

## SRP8-046 (Rear Brakes)

- Status: empty
- Source file: `srp8-046-text.txt`
- Final interfaces: SRP8-026
- Added only through symmetry: SRP8-026

## SRP8-047 (Handbrake)

- Status: empty
- Source file: `srp8-047-text.txt`
- Final interfaces: SRP8-130
- Added only through symmetry: SRP8-130

## SRP8-048 (Steering Column)

- Status: empty
- Source file: `srp8-048-text.txt`
- Final interfaces: SRP8-022, SRP8-037, SRP8-059
- Added only through symmetry: SRP8-022, SRP8-037, SRP8-059

## SRP8-049 (Steering Rack)

- Status: empty
- Source file: `srp8-049-text.txt`
- Final interfaces: SRP8-022, SRP8-167
- Added only through symmetry: SRP8-022, SRP8-167

## SRP8-050 (Front Wheels)

- Status: empty
- Source file: `srp8-050-text.txt`
- Final interfaces: SRP8-059
- Added only through symmetry: SRP8-059

## SRP8-051 (Rear Wheels)

- Status: empty
- Source file: `srp8-051-text.txt`
- Final interfaces: SRP8-059
- Added only through symmetry: SRP8-059

## SRP8-055 (Unified Embedded Node)

- Status: empty
- Source file: `srp8-055-text.txt`
- Final interfaces: SRP8-018, SRP8-029, SRP8-037, SRP8-130, SRP8-132
- Added only through symmetry: SRP8-018, SRP8-029, SRP8-037, SRP8-130, SRP8-132

## SRP8-057 (Horn)

- Status: empty
- Source file: `srp8-057-text.txt`
- Final interfaces: SRP8-022, SRP8-092
- Added only through symmetry: SRP8-022, SRP8-092

## SRP8-058 (Drive Control Systems)

- Status: empty
- Source file: `srp8-058-text.txt`
- Final interfaces: SRP8-014, SRP8-039, SRP8-130
- Added only through symmetry: SRP8-014, SRP8-039, SRP8-130

## SRP8-059 (Sensors)

- Status: done
- Source file: `srp8-059-text.txt`
- Final interfaces: SRP8-001, SRP8-002, SRP8-011, SRP8-012, SRP8-022, SRP8-029, SRP8-034, SRP8-038, SRP8-043, SRP8-044, SRP8-048, SRP8-050, SRP8-051, SRP8-061, SRP8-093, SRP8-115, SRP8-130, SRP8-167, SRP8-170, SRP8-173
- Added only through symmetry: SRP8-029, SRP8-061, SRP8-093, SRP8-130, SRP8-173

## SRP8-061 (Telemetry)

- Status: done
- Source file: `srp8-061-text.txt`
- Final interfaces: SRP8-059, SRP8-130, SRP8-132
- Added only through symmetry: SRP8-130, SRP8-132
- Codes not in json_files (dropped): SRP8-054, SRP8-102

## SRP8-064 (Wiring Harnesses)

- Status: empty
- Source file: `srp8-064-text.txt`
- Final interfaces: SRP8-083, SRP8-085
- Added only through symmetry: SRP8-083, SRP8-085

## SRP8-065 (Occupant Cell)

- Status: empty
- Source file: `srp8-065-text.txt`
- Final interfaces: SRP8-001, SRP8-002, SRP8-003, SRP8-005, SRP8-022, SRP8-026, SRP8-027, SRP8-037, SRP8-085, SRP8-093, SRP8-094, SRP8-167, SRP8-192
- Added only through symmetry: SRP8-001, SRP8-002, SRP8-003, SRP8-005, SRP8-022, SRP8-026, SRP8-027, SRP8-037, SRP8-085, SRP8-093, SRP8-094, SRP8-167, SRP8-192

## SRP8-066 (Front Crash Structures)

- Status: empty
- Source file: `srp8-066-text.txt`
- Final interfaces: SRP8-005, SRP8-085, SRP8-167, SRP8-173
- Added only through symmetry: SRP8-005, SRP8-085, SRP8-167, SRP8-173

## SRP8-077 (Central Stop Lamp)

- Status: done
- Source file: `srp8-077-text.txt`
- Final interfaces: SRP8-011, SRP8-014, SRP8-017, SRP8-026, SRP8-099

## SRP8-082 (Windscreen Wipers)

- Status: empty
- Source file: `srp8-082-text.txt`
- Final interfaces: SRP8-003, SRP8-022, SRP8-092
- Added only through symmetry: SRP8-003, SRP8-022, SRP8-092

## SRP8-083 (Active Aero)

- Status: done
- Source file: `srp8-083-text.txt`
- Final interfaces: SRP8-001, SRP8-010, SRP8-018, SRP8-064, SRP8-094, SRP8-130, SRP8-167, SRP8-188
- Added only through symmetry: SRP8-010, SRP8-094, SRP8-130, SRP8-167

## SRP8-084 (Audio)

- Status: empty
- Source file: `srp8-084-text.txt`
- Final interfaces: SRP8-001, SRP8-022, SRP8-085, SRP8-092, SRP8-130
- Added only through symmetry: SRP8-001, SRP8-022, SRP8-085, SRP8-092, SRP8-130

## SRP8-085 (NVH)

- Status: done
- Source file: `srp8-085-text.txt`
- Final interfaces: SRP8-001, SRP8-010, SRP8-064, SRP8-065, SRP8-066, SRP8-084, SRP8-192
- Added only through symmetry: SRP8-001
- Name-only references added by Gemma:
  - SRP8-010 (Ventilation): "HVAC (Heating, ventilation and air conditioning)"
  - SRP8-064 (Wiring Harnesses): "wiring"
  - SRP8-065 (Occupant Cell): "occupation cell"
  - SRP8-066 (Front Crash Structures): "crash structures"
  - SRP8-084 (Audio): "audio"
  - SRP8-192 (Interior Floor Lining): "interior floor"

## SRP8-086 (Transmission)

- Status: empty
- Source file: `srp8-086-text.txt`
- Final interfaces: SRP8-172
- Added only through symmetry: SRP8-172

## SRP8-089 (Rear Uprights)

- Status: empty
- Source file: `srp8-089-text.txt`
- Final interfaces: SRP8-172
- Added only through symmetry: SRP8-172

## SRP8-092 (Auxiliary Systems Logic)

- Status: done
- Source file: `srp8-092-text.txt`
- Final interfaces: SRP8-001, SRP8-002, SRP8-011, SRP8-012, SRP8-013, SRP8-014, SRP8-024, SRP8-025, SRP8-028, SRP8-029, SRP8-057, SRP8-082, SRP8-084, SRP8-093, SRP8-111
- Added only through symmetry: SRP8-001, SRP8-002
- Codes not in json_files (dropped): SRP8-015, SRP8-060, SRP8-063, SRP8-095

## SRP8-093 (Air Conditioning)

- Status: done
- Source file: `srp8-093-text.txt`
- Final interfaces: SRP8-010, SRP8-037, SRP8-059, SRP8-065, SRP8-092, SRP8-094, SRP8-130
- Added only through symmetry: SRP8-092, SRP8-130
- Name-only references added by Gemma:
  - SRP8-010 (Ventilation): "Ventilation"
  - SRP8-037 (Dashboard): "Dashboard"
  - SRP8-059 (Sensors): "Sensors – Main Loop"
  - SRP8-065 (Occupant Cell): "Occupant Cell"
  - SRP8-094 (Thermal management): "Thermal management"

## SRP8-094 (Thermal management)

- Status: done
- Source file: `srp8-094-text.txt`
- Final interfaces: SRP8-010, SRP8-016, SRP8-038, SRP8-039, SRP8-065, SRP8-083, SRP8-093, SRP8-130
- Added only through symmetry: SRP8-093, SRP8-130
- Codes not in json_files (dropped): SRP8-006

## SRP8-099 (Traction Control)

- Status: empty
- Source file: `srp8-099-text.txt`
- Final interfaces: SRP8-011, SRP8-077, SRP8-130
- Added only through symmetry: SRP8-011, SRP8-077, SRP8-130

## SRP8-101 (Trip Energy Prediction)

- Status: empty
- Source file: `srp8-101-text.txt`
- Final interfaces: SRP8-132
- Added only through symmetry: SRP8-132

## SRP8-111 (Central Locking)

- Status: empty
- Source file: `srp8-111-text.txt`
- Final interfaces: SRP8-001, SRP8-002, SRP8-092, SRP8-130
- Added only through symmetry: SRP8-001, SRP8-002, SRP8-092, SRP8-130

## SRP8-112 (Electric Windows)

- Status: done
- Source file: `srp8-112-text.txt`
- Final interfaces: SRP8-001, SRP8-002, SRP8-130, SRP8-173
- Added only through symmetry: SRP8-130, SRP8-173
- Codes not in json_files (dropped): SRP8-006, SRP8-107

## SRP8-115 (Tyre Pressure Monitoring System)

- Status: empty
- Source file: `srp8-115-text.txt`
- Final interfaces: SRP8-059, SRP8-130
- Added only through symmetry: SRP8-059, SRP8-130

## SRP8-124 (Hydrogen Energy System)

- Status: empty
- Source file: `SRP8-124-text.txt`
- Final interfaces: SRP8-011, SRP8-130, SRP8-131, SRP8-133, SRP8-179, SRP8-186
- Added only through symmetry: SRP8-011, SRP8-130, SRP8-131, SRP8-133, SRP8-179, SRP8-186

## SRP8-128 (ABS Brakes)

- Status: empty
- Source file: `SRP8-128-text.txt`
- Final interfaces: SRP8-130
- Added only through symmetry: SRP8-130

## SRP8-129 (Embedded Low Level Code)

- Status: done
- Source file: `SRP8-129-text.txt`
- Final interfaces: none
- Codes not in json_files (dropped): SRP8-104

## SRP8-130 (Embedded High Level Software Archictecture)

- Status: done
- Source file: `SRP8-130-text.txt`
- Final interfaces: SRP8-001, SRP8-002, SRP8-004, SRP8-005, SRP8-011, SRP8-012, SRP8-013, SRP8-014, SRP8-018, SRP8-019, SRP8-022, SRP8-023, SRP8-024, SRP8-025, SRP8-026, SRP8-029, SRP8-038, SRP8-047, SRP8-055, SRP8-058, SRP8-059, SRP8-061, SRP8-083, SRP8-084, SRP8-093, SRP8-094, SRP8-099, SRP8-111, SRP8-112, SRP8-115, SRP8-124, SRP8-128, SRP8-132, SRP8-179
- Name-only references added by Gemma:
  - SRP8-093 (Air Conditioning): "Thermal Management System"
  - SRP8-094 (Thermal management): "Thermal Management System"
- Code-name corrections (registry wins):
  - `SRP8-025` near "Interior Lights" -> SRP8-023 (Interior Lights)
- Codes not in json_files (dropped): SRP8-015, SRP8-060, SRP8-062, SRP8-095, SRP8-096, SRP8-102, SRP8-140, SRP8-155, SRP8-177

## SRP8-131 (Hydrogen Pressure Vessel)

- Status: done
- Source file: `SRP8-131-text.txt`
- Final interfaces: SRP8-124, SRP8-133
- Added only through symmetry: SRP8-133

## SRP8-132 (Infotainment)

- Status: done
- Source file: `SRP8-132-text.txt`
- Final interfaces: SRP8-011, SRP8-012, SRP8-013, SRP8-022, SRP8-024, SRP8-025, SRP8-028, SRP8-029, SRP8-034, SRP8-039, SRP8-055, SRP8-061, SRP8-101, SRP8-130, SRP8-175
- Added only through symmetry: SRP8-130
- Name-only references added by Gemma:
  - SRP8-055 (Unified Embedded Node): "SRP8-055 Sensors"
- Code-name corrections (registry wins):
  - `SRP8-055` near "Sensors" -> SRP8-059 (Sensors)
- Codes found by regex but rejected by Gemma: SRP8-059 (Sensors)

## SRP8-133 (Hydrogen Fuel Cell)

- Status: done
- Source file: `SRP8-133-text.txt`
- Final interfaces: SRP8-017, SRP8-018, SRP8-124, SRP8-131, SRP8-172, SRP8-179, SRP8-182
- Added only through symmetry: SRP8-017, SRP8-018, SRP8-172

## SRP8-167 (Front Structure)

- Status: done
- Source file: `SRP8-167-text.txt`
- Final interfaces: SRP8-001, SRP8-003, SRP8-004, SRP8-005, SRP8-010, SRP8-012, SRP8-013, SRP8-020, SRP8-021, SRP8-043, SRP8-045, SRP8-049, SRP8-059, SRP8-065, SRP8-066, SRP8-083
- Added only through symmetry: SRP8-059
- Codes not in json_files (dropped): SRP8-006

## SRP8-170 (Rear Quarters)

- Status: empty
- Source file: `SRP8-170-text.txt`
- Final interfaces: SRP8-059, SRP8-172
- Added only through symmetry: SRP8-059, SRP8-172

## SRP8-172 (Rear Support Structure)

- Status: done
- Source file: `SRP8-172-text.txt`
- Final interfaces: SRP8-004, SRP8-086, SRP8-089, SRP8-133, SRP8-170, SRP8-176
- Name-only references added by Gemma:
  - SRP8-004 (Boot): "Boot (hinges)"
  - SRP8-086 (Transmission): "PWT gearboxes"
  - SRP8-089 (Rear Uprights): "VD rear wishbones and uprights"
  - SRP8-133 (Hydrogen Fuel Cell): "ALT hydrogen assembly"
  - SRP8-170 (Rear Quarters): "Rear quarters"
  - SRP8-176 (Rear Crash Structures): "Rear crash structure"

## SRP8-173 (Underbody)

- Status: done
- Source file: `SRP8-173-text.txt`
- Final interfaces: SRP8-001, SRP8-002, SRP8-004, SRP8-021, SRP8-059, SRP8-066, SRP8-112, SRP8-192
- Added only through symmetry: SRP8-192
- Codes not in json_files (dropped): SRP8-122

## SRP8-175 (Vehicle States Project)

- Status: empty
- Source file: `SRP8-175-text.txt`
- Final interfaces: SRP8-018, SRP8-132
- Added only through symmetry: SRP8-018, SRP8-132

## SRP8-176 (Rear Crash Structures)

- Status: empty
- Source file: `SRP8-176-text.txt`
- Final interfaces: SRP8-172
- Added only through symmetry: SRP8-172

## SRP8-179 (Hydrogen Airflow and Venting)

- Status: done
- Source file: `SRP8-179-text.txt`
- Final interfaces: SRP8-124, SRP8-130, SRP8-133
- Added only through symmetry: SRP8-130, SRP8-133

## SRP8-182 (Hydrogen Power Electronics System)

- Status: empty
- Source file: `SRP8-182-text.txt`
- Final interfaces: SRP8-133, SRP8-186
- Added only through symmetry: SRP8-133, SRP8-186

## SRP8-186 (Hydrogen Control System)

- Status: done
- Source file: `SRP8-186-text.txt`
- Final interfaces: SRP8-124, SRP8-182

## SRP8-188 (Computer)

- Status: empty
- Source file: `SRP8-188-text.txt`
- Final interfaces: SRP8-083
- Added only through symmetry: SRP8-083

## SRP8-189 (Bidirectional DCDC)

- Status: empty
- Source file: `SRP8-189-text.txt`
- Final interfaces: SRP8-017
- Added only through symmetry: SRP8-017

## SRP8-190 (Centre Console)

- Status: empty
- Source file: `SRP8-190-text.txt`
- Final interfaces: SRP8-032
- Added only through symmetry: SRP8-032

## SRP8-192 (Interior Floor Lining)

- Status: stale
- Source file: `SRP8-192-text.txt`
- Final interfaces: SRP8-026, SRP8-036, SRP8-065, SRP8-085, SRP8-173
- Name-only references added by Gemma:
  - SRP8-026 (Pedals): "Pedals"
  - SRP8-036 (Front Seat Mount): "the Front Seat Mount"
  - SRP8-065 (Occupant Cell): "Occupant Cell"
  - SRP8-085 (NVH): "Noise, Vibration and Harshness"
  - SRP8-173 (Underbody): "Underbody"
