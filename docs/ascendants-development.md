# Ascendants development

`modes/evolution_alpha` builds **CBA Hero: Ascendants v1.0.8** as the current
source-verified release candidate. It is derived only from v1.0.3; older versions are
not repair or comparison targets. Engine acceptance is still a separate step.

The canonical v1.0.3 checkpoint is 99,694 bytes with SHA-256
`4082a73c9e9323cda5678a758518c12a5e387c3beafa20ce3835f40466fb8d34`. The v1.0.8
candidate is 120,284 bytes with SHA-256
`e9c8760f9078903045deb82c2f5f8f70d26f5598a7ae38dc0cef187e74eef3af`.
Its intentional trigger-graph migration and engine-reported fixes explain the changed hash.

## Two verification layers

Ascendants has two source layers:

1. `generated/` reconstructs the old v1.58 reference in `base.aoe2scenario`.
2. `build.py`, `v2_map.py`, and `free_costs.py` apply the Ascendants map and gameplay
   changes after the generated layer.

Because the public build intentionally differs from the reference, do not use a raw
`aoe2modes verify evolution_alpha` result as the release verdict. Verify both layers:

```bash
make check-ascendants
```

The target first proves that the parser can still round-trip the reference, including
trigger-variable ids. It then runs the final-build gameplay contract and produces the
scenario that should be tested in-game. Finally, `aoe2modes audit` checks the serialized
output for broken references, invalid coordinates, and immediate unconditional
victory/defeat. Potential scheduling or cleanup risks are reported as warnings for
review. The v1.0.8 candidate currently passes with **0 errors and 0 warnings**.

The target is entirely local. It does not use GitHub Actions or any paid CI service.

The active issue inventory and manual acceptance cases are in
[`ascendants-issue-register.md`](ascendants-issue-register.md). v1.0.3 is the sole
comparison baseline and v1.0.8 is the only active candidate.

## v1.0.8 arbitrary lobby-order repair

Runtime player order follows lobby rows, not numeric colors. A full lobby can therefore
map Yellow to runtime P3 and Green to runtime P4. The earlier compact-lobby model only
generated mappings where the runtime number was no greater than the color number, so
valid reversed and shuffled rows were absent from army movement, rewards, defeat,
resignation, HUD, vote, upgrade, and hero systems.

Every mapped family now contains all 64 color/runtime candidates. Castle-row owner
detection activates exactly one candidate per occupied color, so closed or unrelated
rows remain inert. Regression tests require the Green/P4 and Yellow/P3 pair explicitly,
exercise all 8! full-lobby color orders, and model reversed victory ownership.

Army pads are no longer eight hand-maintained tables. All 32 positions come from one P3
row through the continuous-coordinate V2 transform, and a build-time geometry audit
requires dry, unique, unoccupied pads that are closest to their own four Castles. Hay
markers are assigned to the nearest Castle/pad pair and moved one cell Castle-ward;
none can share a runtime wave-creation cell.

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

The final build now removes 810 conditionless/effectless imported shells. Before
removal it proves that their only 16 external references are no-op deactivations of
the retired `no wall` family, then strips those references. It also groups the legacy
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
- automatic armies, builders, six hero milestones, and all five distance positions;
- vote-kick resolution, resignation/defeat, and team victory for both sides;
- local HUD values, player names, zero costs/resources, and post-game combat score;
- unit pathing through every allied route and around all eight rear walls;
- manually returning an army across each Castle launch line without its order changing;
- moving every Sheep to Short, Medium, and Long and confirming the next wave follows it;
- placing buildings across every milestone-shore repair strip;
- confirming all eight shores have no Transport Ship while milestone heroes still spawn;
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
2. Locate the responsible final-build code in `build.py` or `v2_map.py`; avoid editing
   `generated/` for an Ascendants-specific behavior.
3. Make one small correction and run the focused test.
4. Run both verification layers and build the scenario.
5. Use `aoe2modes inspect` or `aoe2modes diff` when the change affects trigger shape,
   object placement, terrain, or variables.
6. Run `aoe2modes audit` on the built scenario. Treat an error as a blocker; review
   warnings in context because decompiled legacy triggers may intentionally reuse names.
7. Version source-changing candidates independently; mark one publishable only after
   the engine acceptance matrix passes.

The `evolution_alpha` id is retained for repository compatibility. User-facing names
and output filenames use **CBA Hero Ascendants**.
