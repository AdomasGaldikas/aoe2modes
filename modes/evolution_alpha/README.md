# CBA Hero: Ascendants v1.0.8

An expanded 144×144 CBA Hero arena rebuilt for reliable full and compact lobbies,
equal territory geometry, predictable automatic movement, and complete
runtime-player ownership. Ascendants keeps the familiar automatic-army foundation
while making every color, route, reward, and late-game system work as one coherent game.

## Shape

| | Baseline | Ascendants v1.0.8 |
| --- | --- | --- |
| Triggers | 2,993 | 3,383 |
| Conditions | 3,314 | 11,384 |
| Effects | 7,814 | 9,975 |
| Units | 1,123 | 1,076 |
| Runtime variables | 0 | 97 |
| Scenario version | v1.51 | v1.58 |

## What changed from the baseline

The original unit waves, civilization pacing, hero milestones, builder thresholds,
center rewards, and two-team structure remain intact. The release replaces brittle
fixed-slot behavior with guarded color-to-runtime mappings, corrects map and trigger
geometry, removes obsolete destructive strips, and throttles every active or
activatable loop.

## Flexible lobbies

The map exposes all eight colors and permits arbitrary closed slots. Blue, Red, Green,
and Yellow are locked to one side; Teal, Purple, Gray, and Orange are locked to the
other. At least one occupied color is required on each side.

Fixed-number closed-slot cleanup is disabled in favor of the runtime-player resolver.
Vote-kick requires two occupied teammates to delete their matching vote markers.
Each marker is checked against its color's resolved runtime owner; no ownerless
wildcard checks remain. A target and both voters must be active, which disables further kicking once a
side has fewer than three remaining colors. Runtime-player resolver triggers defeat
the intended color even when DE compacts a sparse lobby. The scenario's locked color diplomacy keeps
P1-P4 opposed to P5-P8 without overwriting compacted runtime players. Custom
color-side victory also replaces Conquest: losing all four Castles activates only the
resolver mapped to that color's real runtime player, and a side wins only when every
opposing occupied color has been eliminated. Closed colors cannot satisfy either a
defeat or victory resolver. Resolution remains locked until both sides are confirmed
present through the color-to-runtime mapping. Defeat also
independently requires zero Castles in the color's objective row, preventing stale
references from ending a live match. A resignation is resolved through the same
color/runtime mapping and removes every remaining unit and building owned by that
runtime player across the full map. The scoreboard and resource systems do not touch a slot
until an occupied-player gate confirms it is present.

## Color-aware army spawning

DE assigns occupied colors to consecutive runtime player numbers, but lobby row
order can differ from numeric color order. For example, Teal/P5 can become runtime
P2 in a sparse lobby, while a full lobby can put Yellow at runtime P3 and Green at
runtime P4. The legacy army loops used the color slot as the runtime player, leaving
some colors without waves or routing them through the wrong owner. Ascendants detects
the runtime owner directly from each color's fixed Castle row and covers all 64
color/runtime combinations. It then spawns that civilization's original unit at the
correct color territory with the original population cap and interval. Runtime-owner move
triggers send each newly created wave out of the matching base, consume a one-shot
launch pulse, and then remain inert until the next wave. A returning army can cross
the spawn line without the scenario overwriting the player's order. Each color's Sheep
writes a persistent Short, Medium, or Long route value directly. All full and compacted
owner movement triggers read that value, so route choice no longer depends on fragile
trigger activation state. The 472 retired static army shells are removed from the final
trigger graph.

The same territory/runtime mapping now covers the automatic Feudal upgrade package.
Builder rewards use a separate color-indexed queue: XS resolves the selected color's
runtime civilization and razing total, then the matching color trigger creates the
villagers in its own base. A persistent color/runtime-aware movement pass catches
each new pair on the next tick and parks one builder at each protected side of the
Castle row, away from the automatic army lane. Each civilization keeps its original one-to-four-raze
threshold; the first pair arrives at that threshold and every later razing earns
another pair. A short local chat line at match start states the player's civilization
and first-builder threshold. The two-second Bombard Tower grant is forced for every
runtime player so the free tower is reliably available once a builder is earned.

Kill heroes are color-aware as well. Every 200/400/600/800/1000/2000 milestone reads
the occupied color's resolved runtime player, creates the correct hero on an empty
mirrored grass tile, and applies the same latched Short/Medium/Long route used by that
color's normal waves. Moving the Sheep to Hero Spawn Closed or Open changes only the
shoreline blocker and preserves the selected route. This keeps Teal and Purple clear
of the compact rear walls and makes the complete ladder
work identically for all eight colors in both full and sparse lobbies.

The 3500- and 5000-kill Genghis reinforcements use the same mapping and corrected
spawn lane, including the Hero Spawn Open fallback. Center-control kills and
Trebuchet rewards now belong to the actual runtime player for each selected color.
The Goth Elite Huskarl Palisade bonus uses one clear transformed twelve-wall row in
every territory, and the Anarchy Barracks restriction remains active until Imperial
Age for both full and compact lobbies.

## Compact combat HUD

The full Objectives overlay is disabled. A native compact HUD list on the right shows
P1 through P8 vertically under fixed `P# | K | D | R` headings (kills, deaths, and
buildings razed), with one small divider between the two teams, so it no longer covers
the battle in the middle of the screen. XS maps each selected color to its
compacted runtime player and publishes the live counters through short named trigger
variables. Empty colors show dashes, occupied colors show values, and player nicknames
remain unchanged. The list uses plain text without color markup or printed newline
markers.

All players start with zero food, wood, gold, and stone; occupied-slot loops keep all
four stockpiles at zero. Research, repairs, and every unit or building are free. At
startup, XS walks every runtime player's complete data-object and technology tables
and sets all four purchase costs to zero. This changes cost only, preserving existing
availability, prerequisites, and unlock timing—including buildings introduced by new
game updates. This also keeps the villager reward unlocked after the first razing
useful. The K/D HUD remains the canonical
combat result because zero-cost units no longer contribute their normal resource
value to DE's built-in score. The runtime-player loop also clears exploration,
technology, tribute, stockpile, and standing unit/building value from native score;
this is important in sparse lobbies, where selected colors are renumbered and fixed
slot equalizers cannot safely address P5-P8. Combat value is therefore republished
from kills, deaths, razings, and buildings lost, allowing the result screen to
calculate a useful combat score and MVP without reintroducing economy score. The villager-reward chain
uses hidden trigger variables instead of spending the real razings counter, so the
post-game `Buildings Razed` statistic remains accurate. The old 100,000-resource
tribute shells are removed, eliminating their economy and tribute-score inflation.

## Corrected V2 symmetric map

Terrain and player-owned objects derive from the Structure-Aware Symmetry V2
workbook, with later gameplay corrections versioned in code. P3's complete territory
is the canonical template; the build
rotates or reflects that sector into all eight color positions. The result has equal
mirrored base geometry, including Castles, gates, spawn lanes, builders, technology
buildings, defensive structures, land, and water.

The workbook's original object table placed 20 gates sideways and filled or detached
the four allied side-gate openings. The corrected build transforms gates and straight
wall artwork by their physical map axis and keeps four guarded teammate openings clear.
Each route-facing corner replaces exactly four wall cells with its allied gate opening;
that deliberate passage is the only wall-count difference between sectors and does not
reduce the enclosed Castle footprint.
The confusing legacy cliff artwork is removed. Each territory instead receives the
same transformed continuous rear wall, exactly two buildable rear rows, outer water strip,
and three-tile technology path. Winter terrain is replaced globally: territories and
paths use buildable grass, while former icy shore transitions generally use sand.
The exact twenty-cell milestone shoreline ribbon in every color is buildable grass,
so its sand-looking legacy terrain cannot reject construction. Legacy
wall cleanup stops before them so last-ditch defenses remain available. The obsolete
`no wall` cleanup family is removed so it
cannot erase the side walls of Red, Teal, Purple, or Orange at match start. The map has
1,076 total objects; every added wall is attached to its owner's anti-delete protection.
The broad outer aprons at all four allied team corners are cut back to matching
five-tile L routes. The straight allied causeways at the top and bottom are four tiles
wide, matching their gate openings. The corresponding left and right corridors remain
water because those colors are enemies, so the team routes do not create a side bypass.

Army movement areas and destinations, hay markers, hero selectors, wall-cleanup
regions, Castle checks, builder rewards, and Blacksmith upgrade areas are transformed
with the map. King and relic-selector references are pinned explicitly so triggers
cannot exchange two visually similar objects. Every King destination uses the same
transformed island-corner area, so Blue's King Sancho and all seven mirrored Kings
activate their reward reliably. Every white counter King is named for its color and
shows that color's exact live kills as its sword/attack value, using the same runtime
value as the combat HUD. Regression
tests also require the team
routes to be land, the enemy sides to remain water, every technology path to remain
dry, and every gate and straight wall to follow its physical wall axis. Vote flags
now stand in parallel rows beside their matching Outposts, and the edge-island Relics,
Rugs, and King ornaments are aligned to their existing symmetric ground tiles.
Kinging also uses one mirrored six-cannon layout: every cannon appears on ground,
clear of the perimeter walls, and inside its matching health and attack buff area.
Rear Bombard Towers sit against the wall and gate rather than the Castle footprint.
Builder rewards appear on the center of the technology causeway between two dedicated
flags, then move automatically into the two side pockets beside the Castles.
Each front gate also has the same compact mirrored ground marker, with a different
grass, sand, dirt, or road tint for each player color.
Automatic armies spawn one tile nearer the arena wall. Movement triggers watch a
three-by-three area around every spawn point, and the Short, Medium, and Long relic
selectors now control compacted-color players as well as their original slots. Their
three mutually exclusive route regions cover the Sheep's diagonal stopping cells, and
the separate Closed/Open regions cover both approaches to the lower markers. All five
are mutually exclusive, derived from one canonical geometry, and transformed
identically for every color.
Every army, hero, and builder task uses an explicit move action so newly created units
leave
their spawn pads reliably. Legacy ice decorations are removed as objects as well as
terrain, leaving the surrounding shore buildable. The separate milestone-hero spawn
(Robin Hood, Theodoric, and later kill rewards) uses its shoreline pad directly;
decorative Transport Ships and all marker-specific trigger effects are absent.
Hero Spawn Closed creates the shoreline blocker; Open removes it. Once clear, the
selected Short/Medium/Long hero trigger moves milestone heroes from the pad without a
competing fixed-Medium fallback. Packed and unpacked Trebuchets are disabled for every
player, so Castles
cannot train them while scripted rewards can still create their intended units.

Version 1.0.3 replaces the obsolete hidden distance-selector object with a movable
Sheep for every color. It has no trade, build, attack, or population side effects and
cannot be deleted. All five selector rugs are persistent: choosing Hero Spawn Open
removes the blocker without ordering the selector back to the center. The same release
also restores P2/P3 HUD and spawn updates through Castle-verified runtime ownership
and removes every object owned by a successfully vote-kicked player.

Version 1.0.4 compacts the imported trigger graph without changing intended gameplay.
It removes 810 empty shells and 16 no-op cleanup references, merges 189
byte-identical civilization age-up copies, and rewires all 346 incoming activations.
The 99 canonical age-up triggers keep explicit player names; three non-identical P7
legacy variants remain separate. The serialized candidate has no empty triggers,
duplicate names, dangling references, audit errors, or audit warnings. Regression
coverage now exhausts every occupied/alive color state and flood-fills every rear
technology route with collision-relevant blockers.

Version 1.0.5 resolves three engine-reported map interactions without expanding the
trigger graph. All 108 full- and compact-lobby army route triggers require and consume
one of eight XS wave pulses. The 160 mirrored non-buildable milestone-shore Beach
cells become Grass 2. All eight marker ships move two tiles shoreward and become
fully protected Gaia props. The serialized candidate remains 2,327 triggers and
1,084 objects, with 6,940 conditions, 6,975 effects, and 89 variables.

Version 1.0.6 removes the eight decorative Transport Ship spawn markers after engine
testing showed that they added no value to the already-working milestone spawn. Their
56 stop, freeze, speed, selection, deletion, targeting, and attack-protection effects
are removed with them. Hero creation and ordering remain unchanged and fully covered
for every color/runtime owner. The same release adds a full-map ownership purge to all
36 compact-safe resignation resolvers, so a resigned player's units and buildings do
not remain in play. It also replaces route-trigger switching with eight persistent
Short/Medium/Long variables. Its first narrow selector-zone repair and separate
milestone-hero behavior were not sufficient in the game and are superseded by v1.0.7.
The serialized candidate has 2,327 triggers, 1,076 objects, 7,048
conditions, 6,655 effects, and 97 variables.

Version 1.0.7 repairs all five Sheep positions from observed engine behavior. The
selector stopped diagonally beside the Relic/Rug collision boxes, so all 40 conditions
now cover the reachable approach cells while keeping each state unambiguous. The 108
milestone-hero order triggers now use the same latched route variables as the 108
normal-wave routes. The 36 later fixed-Medium Open fallbacks are removed, eliminating
the order that overrode Short or Long. The candidate has 2,291 triggers, 1,076 objects,
6,904 conditions, 6,475 effects, and 97 variables.

Version 1.0.8 removes the remaining assumption that runtime rows follow numeric color
order. Every mapped system now covers all 64 color/runtime combinations, including
Green at runtime P4 and Yellow at runtime P3. The four wave pads for every color are
derived from one canonical P3 row with the continuous-coordinate V2 transforms, and
the build rejects overlaps, water, static occupants, trigger-created occupants, or a
pad closer to another color's Castles. All 32 decorative Hay Stacks are moved one cell
toward their own Castle; none occupies a wave pad. The candidate has 3,383 triggers,
1,076 objects, 11,384 conditions, 9,975 effects, and 97 variables.

## Source of truth

`build.py` starts with `generated.apply(ctx)`, applies the gameplay compatibility
passes, then runs `v2_map.py` and its trigger-geometry remap. `base.aoe2scenario` is
kept as the decompiled legacy reference. Since this mode deliberately changes that
reference, release validation uses the test suite, deterministic rebuilds, and the
focused V2 structural checks:

```
make check-ascendants
```

## Editing

Small changes go in `build.py`, after `apply_generated(ctx)` — that runs last and
overrides anything. Structural changes go in `generated/`, but
`aoe2modes decompile --mode evolution_alpha` overwrites those files.

## Build

```
.venv/bin/aoe2modes build evolution_alpha --deploy
```
