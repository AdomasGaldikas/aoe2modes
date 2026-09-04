# Ascendants development

`modes/evolution_alpha` builds **CBA Hero: Ascendants v1.0.14**. Engine acceptance is
still a separate step from anything described here.

## Ascendants is code-defined

**The Python is the scenario.** There is no `scenario.base` and no
`scenario.reference`, and `dist/CBA Hero Ascendants v1.0.14.aoe2scenario` is a build
product, not an input. `aoe2modes verify` and `aoe2modes decompile` do not apply to
this mode — `decompile --mode evolution_alpha` refuses to run because the mode has no
binary base or reference.

Two source layers, both hand-maintained:

1. `scenario/` lays down the arena — terrain, units, players, lobby options, and the
   legacy CBA Hero trigger graph. It began as decompiler output; it is now ordinary
   source and is edited directly.
2. `build.py` and `v2_map.py` run after `scenario.apply(ctx)` and apply the Ascendants
   map and gameplay layer. They run last and win.

This replaces the "two verification layers" model used up to v1.0.8. That model claimed
`generated/` reconstructed `base.aoe2scenario` and that the round trip was proven on
every run. Neither held: the committed package differed from the declared reference in
8,811 fields, the reference was itself an output of an earlier Ascendants build rather
than an upstream source, and the test that appeared to check the round trip actually
decompiled the reference into a temporary directory and compared *that* against itself.
v1.0.9 removed the reference, the stale binary, and the claim.

### What is checked now

```bash
.venv/bin/python -m pytest tests/test_decompile.py tests/test_evolution_alpha.py
.venv/bin/python -m aoe2modes build evolution_alpha
.venv/bin/python -m aoe2modes audit "dist/CBA Hero Ascendants v1.0.14.aoe2scenario" --strict
.venv/bin/python -m aoe2modes map evolution_alpha --html dist/ascendants-map.html
```

`make check-ascendants` runs the same four steps where `make` is available. The build
itself fails closed on drift: exact trigger-family counts, eight-way symmetry of the
mirrored areas, and a contiguous-variable-id assertion all raise rather than emit a
quietly wrong scenario. `aoe2modes audit` then checks the serialized output for broken
references, invalid coordinates, unreachable or unpaced loops, and immediate
unconditional victory/defeat. v1.0.14 passes with **0 errors and 0 warnings**.

`aoe2modes map` covers the half of the scenario the trigger checks cannot see — the
geometry. It is not a pass/fail gate; read the report and confirm the arena still holds
its shape. v1.0.14 splits each transformed 9×7 control area into two 9×2 dry tracks
separated by three rows of Deep Water. Focused tests pin every lane cell,
Castle pad, Hero pad, destination, wall, gate, shore repair, and eight-way transform.
A map metric that moves without a matching geometry change is a signal to investigate.

The v1.0.14 map report contains 10,188 land cells and 10,548 water cells, with 103
walkable regions when gates are closed and 81 when open. The 216-cell land reduction
from v1.0.13 is entirely the three-row gap across all eight controller areas. Playable
base areas remain 285 cells per color; territory figures remain 911/879 by orientation,
and the `mirror_x` comparison retains its existing 72 mismatches.

The decompiler still has a round-trip test — `tests/test_decompile.py` — but it points
at `chieftains_4v4`, a mode that genuinely still is a decompile of its reference, plus a
synthetic scenario that pins trigger-variable ids and names across a decompile cycle.

The active issue inventory and manual acceptance cases are in
[`ascendants-issue-register.md`](ascendants-issue-register.md).
The exact Castle rows, Sheep/Penguin zones, army/hero creation pads, range
variables, and destinations for all eight colors are in
[`ascendants-control-map.md`](ascendants-control-map.md).

## v1.0.14 confined tracks and clear endpoints

The v1.0.13 sliders were visually separate but shared one walkable island. v1.0.14
keeps each controller on its own two-tile-wide land track using water boundaries,
including a three-tile Deep Water gap with no beach bridges. Every dry track cell
belongs to exactly one of that controller's six selector bands. Confinement does not
add a recurring movement override or freeze the controls.

The entire level-0 pad is Snow. Its boundary with the road is exactly where Army HOLD
or Hero OFF ends. Each track has its own HOLD/OFF and FAR Signs, placed on the outside
row so the other row remains clear. Short controller names match this visual rule:
`Army range - snow = HOLD` and `Hero range - snow = OFF`. HOLD continues Castle
production and keeps new waves near home; OFF pauses new Heroes. Both apply to future
spawns only. Levels, destinations, starting positions, ownership, and Hero tiers are
unchanged from v1.0.13.

The same release narrows gate-triggered wall removal to exact static Castle-yard
shoulder references. The old broad rectangles also selected 30 permanent long flank
pieces and could include mirrored rear joins; the source path audit found an arena
bypass in all eight colors. The replacement preserves all long flanks, front-gate end caps,
and the University enclosure. Permanent walls and gates receive manual-delete
protection through both initial and owner-resolved setup. The side/rear switch gate
remains deletable; it is distinct from the protected University gate. The exact
positions and closed-gate path contract are in `ascendants-control-map.md`.

The imported 220-wall penalty was a second deletion path: its eight warning and
eight removal triggers could remove every wall owned by a player across the map.
Those 16 triggers and their activation chain are retired. Neither correction changes
the intended full-owner cleanup on defeat, resignation, or vote-kick.

## v1.0.13 independent proportional spawn controls

The shared five-position Sheep mixed Castle-army routing with Hero Open/Closed state,
depended on collision-heavy Relic/Rug targets, and was difficult to reason about after
eight map transforms. v1.0.13 replaces it with exactly one Sheep for Castle armies and
one War Penguin for Heroes per color.

Each controller moves across a continuous six-level lane. Sheep level 0 parks new
Castle waves one tile Castle-ward; levels 1–5 send them progressively farther into the
arena. Penguin level 0 disables automatic Hero production; levels 1–5 enable it and
route new Heroes progressively farther. Both start at level 3. Endpoint Signs and the
controller names explain the controls in-game.

At that release point, each controller's six detection bands covered the complete
9×7 island, including both beach caps. Road and Road Gravel marked visual lanes, but
controllers could cross the separator. v1.0.14 replaces that crossable layout with
physically separated tracks and track-specific detection bands.

The 96 selector triggers write separate variables. The 384 Castle-army and 320 Hero
movement mappings retain the one-shot spawn-pulse rule, so slider changes affect only
future spawns and manual return orders remain safe. All Hero loops now occupy exclusive
kill bands; turning Heroes off cannot leave old tiers waiting to burst when the Penguin
moves forward again. Controllers are undeletable and untargetable, and the Penguin has
No Attack stance plus zero scenario attack. Its one real population slot is excluded
from custom army and Hero ceilings, while a hard cap of 251 preserves 250 gameplay
slots. Old selector Relics, Rugs, Torches, blocking Castle Hay markers, and the
shoreline blocker toggle are removed.

## v1.0.12 Goth Palisade mechanic removal

The imported scenario contained an undocumented civilization-specific exception. Once
a Goth player researched Elite Huskarl and built exactly 12 Palisade Walls in a fixed
row near the Castle lane, a trigger added 2,750 HP to those walls. It was neither a
raze reward nor part of the permanent arena wall geometry.

The eight imported `hp (p#)` triggers remain visible only in the code-defined source
layer as provenance, then are reset and removed during the build. Their incoming
activations are stripped, and v1.0.12 does not generate the 64 color/player replacement
triggers introduced by v1.0.8. A regression rejects every serialized Palisade condition
or effect. Goth unit spawning, kill heroes, civilization values, and the separate
Anarchy/Barracks restriction are unchanged.

## v1.0.11 player-identity boundary and corner cleanup

Engine testing of v1.0.10 exposed a defect that parser-only permutation tests had
missed: trigger player selectors and XS world-player ids are separate identity
domains. The Castle-row detector resolves the player value used by trigger conditions
and effects. XS player APIs instead require the engine conversion
`xsGetWorldPlayerId(scenarioPlayer)`. v1.0.8 through v1.0.10 incorrectly shared the
trigger-derived value with XS, allowing Red, Green, or another shuffled color to spawn
an army owned by a different lobby player. The Sheep changed the correct color route
variable, but the correctly mapped route trigger could not select that cross-owned
army, so its failure appeared to be a second route-selector defect.

XS now performs the official conversion at one explicit boundary, while the trigger
graph retains the Castle resolver only for trigger-side player fields. An integrated
regression follows each of the eight Sheep selectors through normal-wave and hero
movement under identity order, an explicit Red/Green swap, and a full eight-color
rotation. The old 8! loop was removed: it only proved that dictionary keys existed and
never modeled the engine identity boundary that had failed.

The same release removes 56 submerged static Palisade Walls and eight static
Saboteurs from the outer corners. None had a trigger, garrison, or object reference.
At that release point the independent Goth Palisade HP trigger was not affected;
v1.0.12 removes it explicitly.

## v1.0.10 one-shot order completion

A full scan of every reachable looping `Task Object` effect found two families that
still polled their spawn pads continuously: 192 milestone-hero route triggers and 64
builder movers. Like the normal-wave defect fixed in v1.0.5, either family could take
control back after a player manually returned a unit across its creation area.

Each color now has a dedicated hero pulse and builder pulse. Creation arms the pulse;
only the active color/runtime-owner trigger with the selected route can consume it;
the move effect then resets it to zero. The 3500/5000-kill Genghis loops arm the same
hero pulse. This preserves automatic departure for newly created units while leaving
all later player orders alone. A scenario-wide regression checks all 448 reachable
looping move triggers and fails if any lacks a one-shot pulse, one-second pacing, or an
explicit Move action.

## v1.0.8 trigger-side lobby candidate expansion (superseded for XS)

Runtime player order follows lobby rows, not numeric colors. A full lobby can therefore
map Yellow to runtime P3 and Green to runtime P4. The earlier compact-lobby model only
generated mappings where the runtime number was no greater than the color number, so
valid reversed and shuffled rows were absent from army movement, rewards, defeat,
resignation, HUD, vote, upgrade, and hero systems.

Every trigger-mapped family contains all 64 color/player candidates. Castle-row owner
detection activates exactly one trigger-side candidate per occupied color, so closed
or unrelated rows remain inert. This expansion was correct for trigger conditions and
effects, including Green/P4 and Yellow/P3. Reusing its value inside XS was not correct;
v1.0.11 replaces that XS path with the engine's `xsGetWorldPlayerId` conversion.

At the v1.0.8 stage, Army pads stopped being eight hand-maintained tables. v1.0.13
finishes that repair by transforming map cells, creating XS waves at their `.5` cell
centres, and selecting only the exact creation cell. All 32 pads are dry, unique,
unoccupied, and closest to their own four Castles. The 32 two-by-two Hay Stack creates
are now removed because footprint checks proved that anchor-only validation had missed
their overlap with 16 pads and eight level-0 destinations.

## v1.0.7 five-position Sheep repair

Engine testing showed that the v1.0.6 route variable alone was insufficient. The
Sheep stopped diagonally beside the Relic/Rug collision boxes, outside the narrow
trigger cells. Milestone heroes also retained a separate Open fallback that issued a
Medium order after a Short or Long order.

All 40 selector areas now use symmetric approach regions between the Sheep's island
center and the five visible markers. All five regions are mutually exclusive, so
crossing the island center cannot silently change the latched route. The 108
milestone-hero route triggers no
longer poll separate Sheep areas: they read the same latched route variable as the 108
normal army routes. The 36 competing fixed-Medium Open fallback triggers are removed.
Close/Open continue to create or remove the shoreline blocker without changing the
last selected army/hero route.

## v1.0.6 route, removal, and resignation fixes

This release introduced a persistent Short/Medium/Long army-route variable instead of
activating and deactivating normal-wave route triggers. Its first narrow selector-area
repair did not cover the Sheep's actual collision-limited approach positions, and the
milestone-hero family still had independent behavior; v1.0.7 supersedes both parts.

The milestone hero spawn already works without a visual object, so all eight
decorative Transport Ships and their 56 protection effects are removed. The final
scenario contains no Transport Ship and no marker-specific trigger logic.

Every compact-safe resignation detector now performs the same full-map, resolved
runtime-owner purge already used by Castle defeat. Once the engine reports that the
mapped player is defeated, all of that player's remaining units and buildings are
removed before team victory continues resolving.

## v1.0.5 engine-report fixes

Automatic army movement is now edge-triggered instead of area-polled. XS sets one
color-specific pulse only after creating a wave; exactly one active full- or
compact-owner route consumes it. The three-by-three launch capture area still handles
spawn collision, but it cannot take over units that later return toward their Castles.

The milestone shoreline has an exact twenty-cell source mask transformed into all
eight territories. Its 160 legacy Beach cells are now buildable Grass 2 without moving
water or the hero landing tile. Each Transport Ship marker is two tiles nearer the
matching shore and is a Gaia-owned, stopped, frozen, speed-zero, unselectable,
undeletable, untargetable, and unattackable prop, outside player and AI control.

## v1.0.4 graph migration

The final build removes 810 conditionless/effectless imported shells, the 32 Hay
marker triggers retired in v1.0.13, and the 16 wall-penalty triggers retired in
v1.0.14. Before removal it proves that the imported shells'
only 16 external references are no-op deactivations of the retired `no wall` family,
then strips those references. It also groups the legacy
kill-based age-up chains by every serialized field, merges 189 byte-identical copies,
and rewires all 346 incoming activations to 99 canonical triggers. Three non-identical
P7 parser variants are preserved and named explicitly.

The resulting file has 2,327 uniquely named non-empty triggers. The audit is clean,
the victory model exhausts all 6,560 occupied/alive color states, and a bounded map
flood-fill proves that every rear interior can reach its University and Blacksmith
without crossing water, walls, towers, Castles, or cliffs.

## What the automated checks cannot prove

The parser and regression suite can prove scenario structure, but they do not run the
Age of Empires II engine. Keep these as explicit in-game checks for every candidate:

- full 4v4 and at least one sparse lobby with closed colors on both teams;
- shuffled full lobbies with Red/Green reversed and Yellow before Green, checking that
  Castle territory, army ownership, civilization, Sheep route, heroes, HUD, rewards,
  resignation, and victory remain attached to the same color;
- automatic armies, builders, six Hero milestones, all six Sheep levels, and all six
  Penguin levels including Hero OFF;
- vote-kick resolution, resignation/defeat, and team victory for both sides;
- local HUD values, player names, zero costs/resources, and post-game combat score;
- unit pathing through every allied route and around all eight rear walls;
- manually returning an army across each Castle launch line without its order changing;
- moving every Sheep through levels 0–5 and confirming only the next Castle wave uses
  the selected distance;
- moving every Penguin through levels 0–5, confirming level 0 pauses Heroes and levels
  1–5 route only the current Hero tier without catch-up spawning;
- ordering each controller across the water gap and beyond every track edge, confirming
  it remains on its own track while all six levels remain reachable;
- checking each HOLD/OFF sign and the Snow-to-road boundary in all orientations: every
  snowy cell selects level 0, and the first road tile selects level 1;
- deleting each Castle-yard switch gate and confirming only the short yard shoulders
  disappear: long flanks, front-gate end caps, University walls/gate, and allied routes
  remain intact, with no new front-arena or rear-University bypass while gates are shut;
- trying manual deletion on permanent walls/gates and exceeding 220 walls without a
  whole-map wall purge, including in sparse and shuffled lobbies;
- placing buildings across every milestone-shore repair strip;
- confirming all eight shores have no Transport Ship while milestone heroes still spawn;
- revealing all four outer corners and confirming no static Palisade Wall or Saboteur
  remains there;
- resigning in full and sparse lobbies and confirming all owned units/buildings disappear.

When one fails, record the exact lobby colors, civilization, trigger-visible symptom,
and expected result before changing code. That turns an engine-only report into a
focused regression test wherever the scenario format exposes enough evidence.

Ascendants already carries explicit army and builder mappings for civilization ids
1–59, including the later DLC blocks recovered from this repository's newer
Chieftains scenarios. New civilization support must add both mappings and a regression
test; never guess a spawn unit, population cap, interval, or builder threshold.

## Fixing an issue

1. Reproduce the issue in a focused test in `tests/test_evolution_alpha.py`.
2. Locate the responsible code. Ascendants behavior belongs in `build.py` or
   `v2_map.py`; edit `scenario/` only for structural arena changes (terrain, unit
   placement, the legacy trigger graph).
3. Make one small correction and run the focused test.
4. Run the full test files and build the scenario.
5. Use `aoe2modes inspect` or `aoe2modes diff` when the change affects trigger shape,
   object placement, terrain, or variables. Use `aoe2modes map` when it affects the
   arena itself — walls, gates, shorelines, spawn geometry — and compare the region,
   symmetry, and territory figures against the ones above before and after.
6. Run `aoe2modes audit` on the built scenario. Treat an error as a blocker; review
   warnings in context because decompiled legacy triggers may intentionally reuse names.
7. Version source-changing candidates independently; mark one publishable only after
   the engine acceptance matrix passes.

The `evolution_alpha` id is retained for repository compatibility. User-facing names
and output filenames use **CBA Hero Ascendants**.
