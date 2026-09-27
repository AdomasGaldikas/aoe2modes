# Ascendants v1.0.1.1 — DE 185872 load fix

DE update 185872 renamed `xsGetLocalPlayerId` to `xsUnsyncGetLocalPlayerId`.
The old call caused an XS compile error after starting from the lobby. Dismissing
that error left the match without initialized runtime logic or army spawning.
The local builder-goal announcement now uses the renamed API.

Source: https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-185872/

The pinned checker predates this API. A mode-local `--extra-prelude-path` supplies
its signature for validation; this file is never embedded in the scenario.
Regression coverage checks that the old call and the validator stub are absent
from the embedded XS. Validation remains enabled.

Validation on 2026-09-27:
- 147 automated tests passed initially; the sole failure was the updated version
  missing from the mode README. Corrected the label and reran that test: passed.
- Ruff passed; strict artifact audit: zero errors, zero warnings.
- Private eight-player lobby on DE 185872: P1 Khmer plus seven standard AI,
  Full Tech Tree checkbox off, cheats off. Loaded without XS error; all eight
  objective rows initialized; Khmer army spawned and population rose from 3 to 31.
- This is a load/spawning smoke test, not a new full gameplay or sparse-slot audit.

Start a new match using `CBA Hero Ascendants v1.0.1.1.aoe2scenario`.
Already-running matches do not pick up changes to scenario files.
