# CBA Hero: Ascendants v1.0.1.0

Ascendants is a 144×144, eight-color CBA Hero scenario with automatic Castle armies,
kill-based Hero tiers, free development, four Castles per color, protected team routes,
center rewards, vote-kicks, and a compact K/D/R display. The maintained Python source is
authoritative; v1.0.3 is the sole historical comparison baseline.

## Start here

This file is the release summary. The reference documentation lives in `docs/`:

| Document | Read it when you want |
| --- | --- |
| [Gameplay](../../docs/ascendants-gameplay.md) | The rules, as a player or lobby host |
| [Architecture](../../docs/ascendants-architecture.md) | To change `build.py` |
| [XS runtime](../../docs/ascendants-xs-runtime.md) | To change spawning, the HUD, or anything touching player identity |
| [Data tables and runbooks](../../docs/ascendants-data-tables.md) | To add a civilization, a variable, or a hero tier |
| [Arena geometry](../../docs/ascendants-map.md) | To move anything on the map |
| [Testing](../../docs/ascendants-testing.md) | To know what is proven and what still needs a game check |
| [Control map](../../docs/ascendants-control-map.md) | Exact cells, pads, lanes and wall roles |
| [Development](../../docs/ascendants-development.md) · [Issue register](../../docs/ascendants-issue-register.md) | The release loop and the open acceptance matrix |

## Current build

| Metric | v1.0.1.0 |
| --- | ---: |
| Triggers | 3,903 (3,443 initially enabled) |
| Conditions | 17,441 |
| Effects | 15,520 |
| Units | 956 |
| Runtime variables | 145 (ids 0–144) |
| Scenario format | DE v1.58 |

The serialized artifact is `dist/CBA Hero Ascendants v1.0.1.0.aoe2scenario`.
`tests/test_evolution_alpha.py::test_evolution_alpha_readme_tracks_the_built_version`
keeps this file's version in step with `mode.toml`.

## Two independent spawn controls

Every color has two movable, protected controllers on separate rear tracks:

- **Sheep — Castle armies.** Its snowy HOLD pad (level 0) sends each new
  Castle wave (one unit per surviving Castle) one tile back toward its own Castle row. Levels 1–5 send each
  new wave progressively farther toward the battle.
- **War Penguin — Heroes.** Its snowy OFF pad (level 0) switches Hero
  production off. Levels 1–5 switch it on and send each newly spawned Hero
  progressively farther toward the battle.

Both controllers begin at level 3. The snowy pad is exactly the HOLD/OFF zone; stepping
onto the road activates the first forward level. Each track has its own HOLD/OFF and
FAR Signs. Short names explain the rule: `Army range - snow = HOLD` and
`Hero range - snow = OFF`. HOLD does not stop Castle production, and neither slider
changes units already fighting. The old five Relic/Rug targets, central Torches, shared
Sheep behavior, and shoreline blocker toggle are removed.

Each two-tile-wide track is surrounded by water, with a three-tile Deep Water gap
between the tracks. This keeps each controller inside its own selector line without
repeatedly overriding movement orders. The Signs leave one row clear for travel, and
every dry track tile belongs to one of its controller's six levels. The protected
Penguin's one real population slot is excluded from custom gameplay ceilings; the
scenario cap is 251 to preserve 250 ordinary gameplay slots.

The sliders latch color-local variables; they do not continuously order existing
units. A creation pulse is armed only after a Castle wave, Hero, or builder pair is
created. Exactly one owner-correct movement trigger consumes that pulse. Returning units keep orders between births; an old unit sharing the capture pad
during a later birth can still be retasked (open issue ASC-037).

Army waves are created at transformed cell centres and selected only on that exact
cell. The 32 decorative Hay Stack creates are removed: their two-by-two footprints had
overlapped 16 wave pads and eight level-0 destinations despite separate anchor points.

The exact lane rectangles, level variables, spawn pads, and destinations are recorded
in [`../../docs/ascendants-control-map.md`](../../docs/ascendants-control-map.md).

## Hero production

The Penguin controls all automatic Hero tiers:

| Kills | Unit | Active band |
| ---: | --- | --- |
| 200 | Robin Hood | 200–399 |
| 400 | Theodoric the Goth | 400–599 |
| 600 | Charles Martel | 600–799 |
| 800 | Subotai | 800–999 |
| 1,000 | Genghis Khan | 1,000–1,999 |
| 2,000 | Super Genghis | 2,000–3,499 |
| 3,500 | boosted Genghis loop | 3,500–4,999 |
| 5,000 | two boosted Genghis loops | 5,000+ |

These bands are mutually exclusive. Leaving the Penguin at Hero OFF pauses production;
moving it forward later starts only the tier appropriate to the current kill count, so
lower tiers cannot burst-spawn after re-enabling Heroes.

## Lobby ownership

The fixed scenario color and the runtime lobby player are separate identities in DE.
XS guards resolve each Castle row from stable references, positive hitpoints and
actual ownership. Native effects latch participation and read HUD counters. XS
stamps its API index into reserved resource 10; native effects copy that token for
spawning and builder rewards. v1.0.20's native conditions failed for high colors in
sparse lobbies; v1.0.1.0 passed a live P1/P3 versus P5/P8 match through natural victory.
Only colors that started have an Objectives row; final stats survive elimination.
The guards cover Castle, defeat and token conditions; hero tiers, age gates, center
rewards, vote markers and wall caps still resolve their owner natively (open ASC-053).
See [v1.0.1.0 notes](RELEASE_NOTES_v1.0.1.0.md) for the precise acceptance scope.

Full Tech Tree is enabled inside the scenario. Hosts do not need to enable its lobby
checkbox. Each army spawn point stops producing units when its own Castle is razed;
surviving Castles continue on the normal wave timer.

Blue, Red, Green, and Yellow form one side; Teal, Purple, Gray, and Orange form the
other. At least one occupied color is required on each side. A resigned or defeated
runtime player's remaining units and buildings are removed from the entire map.

## Match resolution

A color is alive after XS-guarded Castle-owner detection latches participation and until elimination.
`p#coloractive` has exactly **one** writer, `cbaUpdateColorRuntime` in XS; triggers
write occupancy and elimination, and XS derives the active bit within a second.
A second trigger-side writer used to be silently reverted unless every defeat path also
remembered to set the elimination bit.

Elimination is a **map state, not an event**. Each `Color Defeat Resolve S# W#` is live
from the start and fires from its own "no Castle of this owner in this color's Castle
row" condition, so any way those Castles leave the map resolves the color. The legacy
`castle (p#)` chain — four `Destroy Object` conditions on four exact references — is
kept only as a redundant fast path; it cannot become true for a Castle that was
*removed* rather than destroyed, so nothing depends on it.

`Color Castle Row Empty S#` is the last line: eight triggers, one per color, asking
only whether *any* candidate owner still holds a Castle in that row. The owner-resolved
resolvers use the native trigger-owner latch and persistent occupancy.
The row-empty fallback is redundant protection if an owner-specific Castle condition
does not fire. Neither path requires an XS identity token.

`Color Team Victory S# W#` ships disabled and is armed by the one owner detector whose
latch it can match, so seven of every eight candidates leave the tick loop at start-up.

## Arena and cleanup

All eight territories derive from one canonical sector and an eight-way transform.
The scenario retains the corrected walls, oriented gates, buildable milestone shores,
dry technology routes, Castle-relative spawn pads, protected allied routes, and
mirrored anti-Trebuchet areas. It contains no Transport Ships, submerged corner
Palisades, corner Saboteurs, decorative selector Relics/Rugs/Torches, or hidden Goth
Palisade HP bonus.

v1.0.18 cleanup is eligible after active=0 because occupancy is latched separately.
Castle loss, resignation and vote-kick share an owner-only purge without area/type/state
limits, including protected buildings and foundations. Timed retries remain active
after elimination, and victory waits for owner-empty confirmation. New object
production stops as soon as elimination is set. All 64 mappings are covered.

Every color shares one roster: 159 banned units, 16 banned buildings, one banned
technology. The unit ban is derived from `CIV_SPAWN_RULES` rather than the imported
per-color lists, so no civilization can hand-train the unique unit its own Castles
already produce for free — adding a civilization to that table also bans its unit, and
both the Elite and non-Elite forms. Castle, Krepost and Donjon are all banned together:
nobody adds a fifth castle-class fortification.

Deleting the side/rear Castle-yard switch gate removes the short shoulders **and the
long side walls**. The complete front gate/wall row and rear University walls/gate
stay in place. Two small front end posts per color prevent a route around the front
gates after the side walls disappear. The University access gate is not the removal
switch. Exact-reference removal and owner resolution keep this scoped to the correct
color in full, sparse, and shuffled lobbies.

The **wall-limit wipe remains active**: a one-shot warning at 200 owned WALL-class
objects arms the wipe at 220. The count includes preplaced walls. The wipe removes
that player's walls across the map except inside protected permanent barrier
footprints; the front row, University boundary, and teammate access gates remain.
Permanent walls/gates also reject manual deletion. Defeat/resignation cleanup still
removes all of the eliminated player's objects. See the wall-role table in
[`../../docs/ascendants-control-map.md`](../../docs/ascendants-control-map.md).

## Verification

```bash
.venv/bin/pytest -q tests/test_evolution_alpha.py
.venv/bin/pytest -q --ignore=tests/test_evolution_alpha.py
.venv/bin/python -m aoe2modes build evolution_alpha
.venv/bin/python -m aoe2modes audit \
  "dist/CBA Hero Ascendants v1.0.18.aoe2scenario" --strict
.venv/bin/python -m aoe2modes map evolution_alpha \
  --html dist/ascendants-map.html
```

v1.0.18 passes all 78 Ascendants-focused tests and all 60 remaining repository tests
in two complementary runs: 138/138 total. The strict structural audit reports
0 errors and 0 warnings, and repository Ruff checks pass.
Parser tests pin all eight colors, all 96 slider selectors, all 704 army/Hero movement mappings,
the complete ownership matrix, controller safety, isolated connected tracks, visible
HOLD/OFF boundaries, unique spawn pads,
mutually exclusive Hero bands, and the one-shot movement invariant.
Wall checks cover all 64 exact-reference breaches, the owner-resolved warning/wipe
pairs, protected-footprint exclusion, and closed-gate reachability after removal of
the side walls. Each owner's wipe uses 49 rectangles covering the 20,368 map cells
outside 368 protected barrier cells. All 956 placed objects, every terrain cell, and every roster restriction
are unchanged from the pulled v1.0.17 update. Controller confinement and names
are unchanged from v1.0.14. Two liveness tests walk the serialized victory subsystem as
a state machine across six lobby shapes, closed slots both cleaned and left in place,
and a split player identity, and prove a side that has lost its Castles always ends
the match. The new cleanup model additionally checks remaining objects before victory
and reproduces the defect on the old artifact.

AoE2ScenarioParser cannot execute DE pathfinding, lobby compaction, or multiplayer
scheduling. The remaining in-game acceptance cases are tracked in
[`../../docs/ascendants-issue-register.md`](../../docs/ascendants-issue-register.md).

## Release history

Older candidates are retained only as investigation history in `RELEASE_NOTES_v*.md`.
They are not alternative repair targets. See
[`RELEASE_NOTES_v1.0.18.md`](RELEASE_NOTES_v1.0.18.md) for the current change set.
