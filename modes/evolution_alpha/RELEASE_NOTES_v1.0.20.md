# CBA Hero: Ascendants v1.0.20

## Closed lobby slots: participation must not depend on XS identity

The reported six-player match used Blue/Green against Teal/Purple/Gray/Orange,
with two lobby slots explicitly closed before starting. Gray and Orange had no
custom score values, kept buildings after losing their Castles, and prevented
victory. Both v1.0.18 and v1.0.19 failed this live case.

The source had a shared failure path: only XS identity detection could latch
participation. HUD activation and cleanup required that latch. Replacing the
converter with Castle-reference reads in v1.0.19 did not remove this dependency.
Earlier cleanup tests pre-filled participation and therefore missed it.

## Changed

- Native Castle-owner detectors now establish persistent participation and reset
  cleanup state after lobby settling. Defeated/closed player selectors cannot bind.
- Native owner-resolved triggers copy kills, deaths, and razings directly into
  HUD variables. HUD activation requires native occupancy, not XS detection.
- XS active state is derived only from occupied/not-eliminated latches. Native
  defeat/resignation and Castle-loss conditions drive elimination. Cleanup and
  victory do not require an XS identity token.
- Spawning and builder rewards use a separate resource handshake. XS stamps its
  API index plus 1000 into reserved unused resource 10. A trigger reads that value
  from the same owner whose Castles established the territory, copying it into
  variables 137–144. The resolver decodes only valid 1001–1008 tokens; late tokens
  retry, and successful bindings persist. Trigger selectors are never passed
  directly to XS player APIs.
- Removed the converter, Castle-reference identity cache, and debug-chat request.
- Preserved owner-wide protected-object cleanup, timed retries, empty-owner
  victory gates, and direct elimination guards on production.

Resource 10 is reserved for this handshake and must not be reused by economy,
score or civilization code. The current [resource reference](https://ugc.aoe2.rocks/general/resources/resources/)
identifies it as unused; resource 8 is not an interchangeable alternative.

## Validation

- 83 Ascendants tests and 60 other repository tests: **143 passing**.
- Emitted resolver and serialized resource bridge tested across all 255 nonempty
  occupied-color subsets in two seat orders, independently permuted trigger/XS
  identities, delayed and invalid tokens, and retained bindings.
- Seven lobby shapes, including the exact reported occupied colors: start with
  zero participation, detect native owners, activate/read HUD rows, then require
  cleanup and victory with every XS identity binding still zero.
- The zero-participation regression distinguishes the installed v1.0.19 artifact
  from v1.0.20: only v1.0.20 natively detects all six occupied colors.
- Repository Ruff checks, embedded XS validation (624 lines), and strict serialized
  audit pass: **0 errors, 0 warnings**.
- Readback comparison against installed v1.0.19: all 956 objects, all 20,736 terrain
  cells/elevations/layers, player settings, roster restrictions, and lobby options
  unchanged. Hero L1 and Scorpion lifetime are unchanged.

Artifact: `CBA Hero Ascendants v1.0.20.aoe2scenario`, 166,787 bytes.

SHA-256: `ec30a64b496f12504ca1af44a6a430dc047b2b547b3c0a820821cb8134a6f40d`.

3,911 triggers (3,451 initially enabled, 3,902 conservatively reachable),
17,449 conditions, 15,584 effects, 956 objects, 145 variables (0–144).

These are code and serialized-state tests, not a claim that a live DE match was
executed. Native closed-slot acceptance remains unobserved. The exact earlier XS
return values remain unknown; the shared dependency is removed without requiring
the user to collect debug output. Start a new match with v1.0.20: existing matches
and old saves retain their embedded scenario logic.
