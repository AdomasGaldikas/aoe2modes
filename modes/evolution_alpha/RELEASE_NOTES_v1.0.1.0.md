# CBA Hero: Ascendants v1.0.1.0

Sparse lobbies in v1.0.20 left P5/P8 without custom scores or working elimination.
This release replaces failing native player conditions with embedded XS guards
that verify stable Castle references, HP and converted ownership. Native effects
still copy counters and perform owner-wide cleanup. The spawning identity token
remains separate from participation, cleanup and victory.

The final release number is **1.0.1.0**, as requested. Live test copies were
labeled v1.0.21 during development; renumbering adds no gameplay changes.

## Changes

- Objectives show only colors that started, with no closed-slot placeholders.
  Eliminated participants retain their final counters.
- Full Tech Tree is embedded in the scenario, independent of the lobby checkbox.
  Technologies still require their normal prerequisites and research.
- Each of the 32 army spawn pads checks its own Castle before creating a wave unit.
  Missing, dead or captured Castles stop their lane; surviving lanes continue.
- Runtime regression tests execute serialized guards across independent identity
  mappings, missing/dead/wrong-owner Castles and all eight colors' survival masks.

## Validation and limits

All 146 repository tests pass; Ruff passes. The embedded XS compiles and the strict serialized audit reports 0 errors and
0 warnings. The artifact has 3,903 triggers (3,443 initially enabled), 17,441
conditions, 15,520 effects, 956 objects and 145 variables.

Live DE testing on 2026-09-06:

- An uninstrumented P1/P3 vs P5/P8 match displayed all four counters, updated them
  during combat, cleaned up defeated opponents and reached normal victory at 31:14.
  This tested the runtime-guard/HUD changes before the final two additions.
- A diagnostic copy of the final build initialized all eight players. It destroyed
  one P1 Castle at 35 seconds: that lane stopped at 2 waves while the others reached
  13. Timed enemy Castle removal then reached victory.
- With the lobby Full Tech Tree checkbox explicitly unchecked, the Persian probe
  read Bracer and Siege Onager as tech state 0 (enabled, prerequisites not ready).

The diagnostic counters and timed destruction are not in the release artifact.
Every civilization, shuffled-seat arrangement, controller level, Hero tier and
resignation/vote-kick combination has not been exhaustively played. Keep those
checks in the [acceptance matrix](../../docs/ascendants-issue-register.md).

Artifact: `CBA Hero Ascendants v1.0.1.0.aoe2scenario`

SHA-256: `1e5870939b49aa3ddaf61c381ecd9a57c71c5703bc2f5a801f444e6fe83a424e`
