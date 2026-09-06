# Ascendants development

`modes/evolution_alpha` builds **CBA Hero: Ascendants v1.0.1.0**. Engine acceptance is
still a separate step from anything described here.

## Ascendants is code-defined

**The Python is the scenario.** There is no `scenario.base` and no
`scenario.reference`, and `dist/CBA Hero Ascendants v1.0.1.0.aoe2scenario` is a build
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
.venv/bin/pytest -q tests/test_evolution_alpha.py
.venv/bin/pytest -q --ignore=tests/test_evolution_alpha.py
.venv/bin/python -m aoe2modes build evolution_alpha
.venv/bin/python -m aoe2modes audit "dist/CBA Hero Ascendants v1.0.1.0.aoe2scenario" --strict
.venv/bin/python -m aoe2modes map evolution_alpha --html dist/ascendants-map.html
```

`make check-ascendants` runs the focused scenario/decompiler tests, build, audit, and
map steps where `make` is available; the two pytest commands above additionally cover
the complete repository suite. The build itself fails closed on drift: exact
trigger-family counts, eight-way symmetry of the
mirrored areas, and a contiguous-variable-id assertion all raise rather than emit a
quietly wrong scenario. `aoe2modes audit` then checks the serialized output for broken
references, invalid coordinates, unreachable or unpaced loops, and immediate
unconditional victory/defeat. See the current release notes for validation results;
mocked engine reads and structural checks do not establish native lobby behavior.
Repository Ruff checks and the 624-line embedded XS build also pass.

The structural audit cannot see whether a match can be *won*: a permanent deadlock is
made of individually well-formed triggers. Two liveness tests cover that separately —
they select the victory subsystem from the serialized data and run it as a state
machine across lobby shapes and a split player identity. See
[`RELEASE_NOTES_v1.0.17.md`](../modes/evolution_alpha/RELEASE_NOTES_v1.0.17.md).

`aoe2modes map` covers the half of the scenario the trigger checks cannot see — the
geometry. It is not a pass/fail gate; read the report and confirm the arena still holds
its shape. v1.0.14 splits each transformed 9×7 control area into two 9×2 dry tracks
separated by three rows of Deep Water. Focused tests pin every lane cell,
Castle pad, Hero pad, destination, wall, gate, shore repair, and eight-way transform.
A map metric that moves without a matching geometry change is a signal to investigate.

The v1.0.15 map report contains 10,188 land cells and 10,548 water cells, with 103
walkable regions when gates are closed and 81 when open, unchanged from v1.0.14.
Every terrain cell and all 940 pre-existing objects are unchanged; this release adds
only two front-row end posts per color. Playable base areas remain 285 cells per color.
Territory figures are 893/861 by orientation, 18 fewer than before because the front
seams are now closed. The `mirror_x` comparison retains its existing 72 mismatches.

The decompiler still has a round-trip test — `tests/test_decompile.py` — but it points
at `chieftains_4v4`, a mode that genuinely still is a decompile of its reference, plus a
synthetic scenario that pins trigger-variable ids and names across a decompile cycle.

The active issue inventory and manual acceptance cases are in
[`ascendants-issue-register.md`](ascendants-issue-register.md).
The exact Castle rows, Sheep/Penguin zones, army/hero creation pads, range
variables, and destinations for all eight colors are in
[`ascendants-control-map.md`](ascendants-control-map.md).

## v1.0.1.0 live sparse-lobby correction

Native Castle and resource conditions failed for P5/P8 in the live P1/P3/P5/P8
match even though v1.0.20 passed automated tests. `runtime_conditions.py` now
emits XS guards for those conditions and player defeat. Each candidate trigger
selector is converted into an XS index before checking the actual starting Castle
references, owner and positive hitpoints. Native effects remain responsible for
latches, HUD copies, cleanup and victory. The resource-token spawning bridge remains.

Only occupied colors activate an Objectives row. Closed slots have no placeholder;
players who later resign or lose retain their final stats. The live production
build showed precisely P1/P3/P5/P8, with no gaps, and initialized all four players.
Tests execute serialized guard bodies with mocked APIs, including missing, dead
and wrong-owner Castles; they are not an engine emulator.

The sweep covers three condition classes and no more; the build now refuses to emit an
artifact where one of them returned to the native domain. The remaining 3,499
player-scoped conditions — hero tiers, age gates, center rewards, vote markers, wall
caps and the `Color Cleanup Complete` victory gate — still resolve owners natively.
Whether that matters depends on a root cause nobody has isolated yet, so it is tracked
as an open item (ASC-053) rather than patched on inference. The next person to reproduce
the sparse lobby should carry a probe that reports one inverted and one non-inverted
native check for a high color; that single observation decides whether the sweep should
grow or the diagnosis should shrink.

See [v1.0.1.0 notes](../modes/evolution_alpha/RELEASE_NOTES_v1.0.1.0.md).

## v1.0.18 cleanup after elimination

Pulled Adomas's `eb9a077` update before applying this focused fix. An eliminated
color could become inactive before the active-gated purge ran, while the row-empty
fallback allowed victory without object cleanup. Persistent occupancy now keeps
cleanup eligible; unrestricted owner-only purges cover protected buildings and
foundations, 64 timed retries handle residue, and 64 empty-owner confirmations gate
victory. Trigger and XS producers also check elimination directly. There are 137
variables (0–136); map objects, terrain, roster, ranges, and Scorpion lifetime are
unchanged. See
[`RELEASE_NOTES_v1.0.18.md`](../modes/evolution_alpha/RELEASE_NOTES_v1.0.18.md).

## v1.0.17 match resolution and roster derivation

A live 1 v 4 ended with every enemy Castle destroyed and no victory. Victory is gated
on `p#coloractive`, which XS clears only from `p#coloreliminated`, and elimination had a
single reachable path: the one-shot `castle (p#)` chain of four `Destroy Object`
conditions. A Castle that leaves the map by `Remove Object`, a purge, or engine slot
cleanup satisfies none of them, so the colour stayed alive with nothing left to kill.

Three changes close it. `Color Defeat Resolve` ships enabled and fires from the
Castle-row condition it already carried, so defeat is map state rather than a one-shot
event. Eight new `Color Castle Row Empty S#` triggers clear the gate using only "does
anybody still hold a Castle in this row", which needs neither the trigger-side
`p#worldplayer` latch nor the XS lobby-slot mapping — the two identity domains can now
disagree without hanging a match. XS became the sole writer of `p#coloractive` and
latches elimination when a colour that was seen in game leaves it.

The same release derives the shared training ban from `CIV_SPAWN_RULES` instead of the
imported per-colour lists (143 → 159 units, closing seven DLC civilizations that could
hand-train their own auto-spawned unit), bans Krepost and Donjon alongside the Castle,
and fixes a bare literal variable base in XS. Two balance findings are deliberately left
open. Every terrain cell and placed object is unchanged. See
[`RELEASE_NOTES_v1.0.17.md`](../modes/evolution_alpha/RELEASE_NOTES_v1.0.17.md).

## v1.0.16 audit corrections and Castle-front Heroes

The first active Penguin setting now sends Heroes to canonical `(21,54)`, on the
Army HOLD line one cell outside the Castle footprint, for all 64 owner mappings.
OFF remains production-off; higher levels and every map object/terrain cell are
unchanged from v1.0.15. Six additional corrections cover training-list parity,
returning Genghis/center rewards, stale Hero OFF orders, Goth Imperial transition,
and combat-proof vote markers. See
[`RELEASE_NOTES_v1.0.16.md`](../modes/evolution_alpha/RELEASE_NOTES_v1.0.16.md).

A remaining spatial-order limitation is tracked as ASC-037: an old unit on a capture
pad during a new birth may still receive that birth's order. A new per-unit XS
tracking approach was not shipped without engine validation. The 50-second
Scorpion reward lifetime remains intentional and unchanged.

## v1.0.15 side-wall removal and protected wall-limit wipe

The user clarified that side walls must disappear, while the front gate/wall row and
rear University barrier remain. The wall-limit wipe must also remain active.
v1.0.14 had misinterpreted that requirement by preserving the long side walls and
retiring the wipe; this release corrects that behavior rather than changing the
controller work.

The 64 `Wall Breach` mappings select exact existing static wall references from the
short shoulder mask plus all 30 long side-wall pieces per color. That produces 44
targets for P1/P2/P7/P8 and 48 for P3/P4/P5/P6; teammate access gates replacing
shoulder slots are not selected. The three front gates, four existing front posts,
and University wall/gate boundary remain. Two additional front end posts per color
close the otherwise exposed ends after the side walls disappear. No terrain or
spawn-control geometry changes. The exact coordinates and all eight transforms are
recorded in `ascendants-control-map.md`.

The warning at 200 and wipe at 220 use the original WALL-class count basis, including
owned preplaced walls, and the original one-shot warning-then-wipe sequence. The
eight imported pairs are reset and expanded into 64 `Wall Cap Warn S# W#` /
`Wall Cap Wipe S# W#` pairs, covering every scenario-color/trigger-owner mapping.
Their old activation chain is removed. The active-color and
resolved-owner conditions keep sparse and shuffled lobbies attached to the right
territory.

Wipe rectangles cover the map except protected permanent wall/gate footprint cells.
Each effect selects only the resolved owner's WALL class. Thus the rule removes
player-built walls and remaining side walls without deleting the front gates/posts,
rear University wall/gate, or teammate access gates. Walls built within a protected
footprint cell are also spared. Protection is geometric, not an ownership swap or a
remove/recreate cycle. The permanent references retain manual-delete protection and
the side switch remains deletable. Some side walls retain legacy manual-delete
protection, which does not prevent their scripted removal by the switch or wipe.

The serialized wipe for each owner has 49 non-overlapping rectangles covering all
20,368 unprotected map cells, excluding all 368 permanent barrier footprint cells.

Tests must check the exact target lists, the full warning/wipe ownership matrix,
rectangle coverage and protected-cell exclusion, and closed-gate reachability after
the permitted deletion in every color orientation. Defeat, resignation, and vote-kick
still deliberately remove all objects belonging to the eliminated owner.

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

The same release narrowed gate-triggered removal to the short shoulder references
and retired the 220-wall penalty. Those wall decisions were incorrect for the user's
intended rules and are superseded by v1.0.15 above. The confined tracks, Snow
boundaries, and controller names remain unchanged.

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

v1.0.11 performed the official conversion at one explicit boundary, while the trigger
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

The final build removes 810 conditionless/effectless imported shells and the 32 Hay
marker triggers retired in v1.0.13. v1.0.14 additionally removed the 16 imported
wall-penalty shells; v1.0.15 resets and reuses them within the new owner-resolved
warning/wipe family instead of retaining the imported logic. Before removal it proves
that the empty imported shells'
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
- deleting each Castle-yard switch gate and confirming the short shoulders and long
  side walls disappear, while the front gate/wall row, University walls/gate, and
  teammate access gates remain, with no front-arena or University bypass while shut;
- reaching 200 owned WALL-class objects to warn, then 220 to wipe that owner's walls
  outside the protected barrier footprints; confirm the permanent defenses and other
  players' walls survive, including in sparse and shuffled lobbies;
- trying manual deletion on permanent walls/gates, confirming the switch remains
  deletable, and confirming legacy side-wall Delete protection does not stop the
  scripted switch/wipe removal;
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
