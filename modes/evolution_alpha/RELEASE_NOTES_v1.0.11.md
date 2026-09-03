# CBA Hero: Ascendants v1.0.11 candidate

> Superseded by v1.0.12, which removes the unwanted hidden Goth Palisade HP
> mechanic. Keep this candidate only as the ownership-fix comparison point.

This candidate fixes the engine-reported cross-owned Castle spawns in shuffled
lobbies and removes the obsolete Palisade/Saboteur clutter from all four map corners.
It supersedes v1.0.10; the sole historical comparison baseline remains v1.0.3.

## Gameplay fixes

- **Armies now belong to the color whose Castle row creates them.** The v1.0.8–v1.0.10
  implementation incorrectly reused a trigger-derived player selector as an XS world
  player. Those are different custom-scenario identity domains. Every XS system now
  converts the scenario color with the engine's
  `xsGetWorldPlayerId(scenarioPlayer)` function before reading civilization, population,
  kills/deaths/razings, player state, or creating units. This is the official API for
  obtaining the lobby slot from a scenario player index.
- **The corners no longer contain staging clutter.** All 56 static submerged Palisade
  Walls and all 8 static Saboteurs are removed. They had no condition, effect, garrison,
  or gameplay references. The Goth Palisade reward remains because it is a separate
  trigger-created civilization bonus inside the playable base.

## Ownership invariant

- Trigger conditions/effects continue to use the Castle-row resolver and its
  `p#worldplayer` variables.
- XS player APIs never read those trigger-derived variables. They use
  `xsGetWorldPlayerId` at one explicit boundary.
- Source comments, repository agent guidance, and regression tests now document and
  enforce that split. The earlier test that merely enumerated 8! Python permutations
  was removed because it did not execute or model the DE engine and falsely certified
  the broken implementation.

The API contract is documented by Forgotten Empires' XS reference and the official
Age of Empires II Update 169123 notes:

- https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/xs-scripting-in-age-of-empires-ii-definitive-edition
- https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-169123/

## Verification

Produces 3,383 uniquely named non-empty triggers, 1,012 objects, 11,640 conditions,
10,871 effects, 113 variables, and 613 generated XS lines. The strict parser audit
passes with 0 errors and 0 warnings.

Focused tests: 69 passed

Repository tests: 114 passed

Ruff: clean

All six modes: build successfully

File size: 125,040 bytes

SHA-256:
`d516f9d9c472c8f650d590830788e5f62f21e28666c7c51bdc99f245413394c5`

## Required in-game acceptance

Start a shuffled full lobby with Red and Green in reversed lobby order, then repeat
with Yellow before Green. Each Castle territory must spawn units in its own color,
using that color's selected civilization; its HUD, Sheep route, milestone heroes,
builders, resignation cleanup, and victory result must stay attached to the same
color. Also reveal all four outer corners and confirm there are no Palisade Walls or
Saboteurs there. Parser checks cannot execute the multiplayer engine, so this focused
run is the final behavioral proof.
