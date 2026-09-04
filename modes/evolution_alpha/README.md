# CBA Hero: Ascendants v1.0.14

Ascendants is a 144×144, eight-color CBA Hero scenario with automatic Castle armies,
kill-based Hero tiers, free development, four Castles per color, protected team routes,
center rewards, vote-kicks, and a compact K/D/R display. The maintained Python source is
authoritative; v1.0.3 is the sole historical comparison baseline.

## Current build

| Metric | v1.0.14 |
| --- | ---: |
| Triggers | 3,519 |
| Conditions | 14,049 |
| Effects | 11,855 |
| Units | 940 |
| Runtime variables | 121 (ids 0–120) |
| Scenario format | DE v1.58 |

The serialized artifact is `dist/CBA Hero Ascendants v1.0.14.aoe2scenario`.

## Two independent spawn controls

Every color has two movable, protected controllers on separate rear tracks:

- **Sheep — Castle armies.** Its snowy HOLD pad (level 0) sends each new
  four-unit Castle wave one tile back toward its own Castle row. Levels 1–5 send each
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
created. Exactly one owner-correct movement trigger consumes that pulse. Units that
later cross a spawn pad therefore keep the player's manual order.

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
Trigger-side systems resolve the owner standing in each Castle row. XS calls
`xsGetWorldPlayerId(scenarioPlayer)` before civilization lookup, statistics access, or
unit creation. This boundary keeps every army, Hero, route, reward, HUD row,
resignation, and victory result attached to the correct color territory in full,
sparse, and shuffled lobbies.

Blue, Red, Green, and Yellow form one side; Teal, Purple, Gray, and Orange form the
other. At least one occupied color is required on each side. A resigned or defeated
runtime player's remaining units and buildings are removed from the entire map.

## Arena and cleanup

All eight territories derive from one canonical sector and an eight-way transform.
The scenario retains the corrected walls, oriented gates, buildable milestone shores,
dry technology routes, Castle-relative spawn pads, protected allied routes, and
mirrored anti-Trebuchet areas. It contains no Transport Ships, submerged corner
Palisades, corner Saboteurs, decorative selector Relics/Rugs/Torches, or hidden Goth
Palisade HP bonus.

Deleting the side/rear Castle-yard switch gate opens only the short wall shoulders
beside that yard. Long flank walls, front-gate end caps, and the University enclosure
stay in place. Permanent walls and gates cannot be manually deleted, and the hidden
220-wall whole-map removal penalty is gone. The University access gate is not the
wall-removal switch. Exact-reference removal and owner resolution keep this behavior
scoped to the correct color in full, sparse, and shuffled lobbies.

## Verification

```bash
.venv/bin/pytest -q tests/test_evolution_alpha.py
.venv/bin/python -m aoe2modes build evolution_alpha
.venv/bin/python -m aoe2modes audit \
  "dist/CBA Hero Ascendants v1.0.14.aoe2scenario" --strict
.venv/bin/python -m aoe2modes map evolution_alpha \
  --html dist/ascendants-map.html
```

v1.0.14 passes all 57 Ascendants-focused tests and all 117 repository tests. The strict
structural audit reports 0 errors and 0 warnings, and repository Ruff checks pass.
Parser tests pin all eight colors, all 96 slider selectors, all 704 army/Hero movement mappings,
the complete ownership matrix, controller safety, isolated connected tracks, visible
HOLD/OFF boundaries, unique spawn pads,
mutually exclusive Hero bands, and the one-shot movement invariant.
Wall checks pin all 64 exact-reference breaches, permanent-defense protection, and
closed-gate reachability after the permitted yard opening. Independent artifact
readback confirms 484 protected permanent wall/gate references and 16 contained
controllers.

AoE2ScenarioParser cannot execute DE pathfinding, lobby compaction, or multiplayer
scheduling. The remaining in-game acceptance cases are tracked in
[`../../docs/ascendants-issue-register.md`](../../docs/ascendants-issue-register.md).

## Release history

Older candidates are retained only as investigation history in `RELEASE_NOTES_v*.md`.
They are not alternative repair targets. See
[`RELEASE_NOTES_v1.0.14.md`](RELEASE_NOTES_v1.0.14.md) for the current change set.
