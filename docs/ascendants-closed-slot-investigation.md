# Live follow-up: v1.0.1.0

The v1.0.20 candidate also failed the private P1/P3/P5/P8 reproduction on
2026-09-06. Native Objects in Area and token conditions did not recognize high
colors, while native effects continued to address the correct scenario players.
Isolated XS-condition probes restored P5/P8. The final fix converts candidate
selectors, verifies actual starting Castle references and retains native effects.
The production build initialized all four colors and displayed only those four
Objectives rows. See [v1.0.1.0 notes](../modes/evolution_alpha/RELEASE_NOTES_v1.0.1.0.md).

The earlier investigation below is retained as historical evidence.

# Closed-slot failure: live evidence, 2026-09-06

Historical status: **v1.0.19 failed live acceptance. v1.0.20 replaces the shared detection
failure path in code; native acceptance has not yet been observed.**
The user reports lobby slots 3 and 4 were explicitly closed. Occupied colors are
P1/P3 versus P5/P6/P7/P8. Lobby slot numbers must not be confused with color numbers.
P7/P8 have blank custom score rows, retain buildings after Castle loss, and prevent
the match from resolving. Do not describe the previous resolver changes as verified
fixes for this report.

## Verified locally

- The game's generated `default0.xs` identifies v1.0.19 and contains the Castle-
  reference resolver and one-shot identity diagnostic. This is not merely an older
  scenario selected by mistake.
- The current recording identifies v1.0.19, DE build 180059, save format 68.0.
- Its initial lobby/player table contains the following compacted entries. This is
  recording evidence, not an observation of XS function return values.

| Color/territory | Recorded world player | Starting Castle reference ids |
| --- | ---: | --- |
| P1 Blue | 1 | 9761, 22013, 22014, 22015 |
| P3 Green | 2 | 35043, 35044, 35045, 35046 |
| P5 Teal | 3 | 35047, 35048, 35049, 35050 |
| P6 Purple | 4 | 22023, 22024, 22025, 22026 |
| P7 Gray | 5 | 79333, 79334, 79335, 79336 |
| P8 Orange | 6 | 35055, 35056, 35057, 35058 |

- Actual initial world objects retain those references. Gray's Castles are at
  `(48/52/56/60,125)` and Orange's at `(84/88/92/96,125)`, matching the built rows.
- The recording includes the expected candidate owner detectors, including
  `Color Owner Detect S7 W5` and `Color Owner Detect S8 W6`. Their saved conditions
  test Castle type 82 in those correct rows; the corresponding variable writes are
  `(variable 46, value 5)` and `(variable 47, value 6)`. Candidate W7/W8 variants
  also exist. Saved definitions do not establish which trigger actually fires.

## Code correction without requiring manual diagnostics

The recording reader does not expose later XS arrays or trigger-variable state.
Initial object ownership cannot prove the return domain of `xsGetUnitOwner` or
`xsGetPlayerInGame`. The exact native failure is therefore not claimed as proven.

Source inspection nevertheless establishes the shared failure path: only the XS
lookup could latch participation, while HUD activation and cleanup required it.
v1.0.20 removes that dependency. Native Castle-owner detection latches participation;
native HUD triggers read that same owner's counters. XS active state is only
occupied AND not eliminated. A separate reserved-resource identity token supports
spawning/rewards; its absence cannot hide a HUD row or prevent cleanup/victory.

The diagnostic chat and collection request have been removed. Regression tests
start with zero occupancy and verify native detection/HUD/cleanup with no XS binding,
plus resource translation across different trigger and XS index permutations.
See [v1.0.20 notes](../modes/evolution_alpha/RELEASE_NOTES_v1.0.20.md).

## Replay reader note

Read-only extraction used mgz 1.8.51 in an isolated temporary package directory.
For this save-68 header, its DE player-record reader needed to consume an extra
`de_string(data)` after the save>=64.3 four-byte trailer. With that local diagnostic
adjustment, the eight lobby records and seven world records (including Gaia) parse.
Some unrelated fields in the fast world-player parser are not valid for save 68;
do not use those civilization/color fields as evidence. The lobby colors and
world names/object reference rows independently agree. No game files were edited.
