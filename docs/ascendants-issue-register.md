# Ascendants v1.0.7 candidate issue register

This is the working inventory recovered from the **Publish CBA Hero scenario** task.
Only **CBA Hero: Ascendants v1.0.3** is a comparison baseline. Older builds are not
repair targets. **v1.0.7** is the active source-verified candidate.

The baseline file is 99,694 bytes with SHA-256
`4082a73c9e9323cda5678a758518c12a5e387c3beafa20ce3835f40466fb8d34`.
The v1.0.7 candidate is 89,119 bytes with SHA-256
`28dfec1fdf2d17e6b9bf00500d1167ad4dc780f2a350f8037b1c006722c20378`.
“Guarded” means the serialized scenario and tests contain the intended correction; it
does not mean the Definitive Edition engine has been observed running it successfully.

## Reported issues

| ID | Report or requirement | v1.0.7 source status | Parser/source evidence | Required game check |
| --- | --- | --- | --- | --- |
| ASC-001 | Leave two fewer rows behind every player's Castles. | Guarded | The canonical rear wall moved from source x=10.5 to x=14.5. Land is x=14..16: one wall row plus exactly two protected interior rows, transformed identically eight ways. | Visually inspect all eight rear Castle strips. |
| ASC-002 | Red, Teal, Purple, and Orange lost a side wall. | Guarded | All 16 `no wall` / `re no wall` shells and their 16 no-op incoming deactivations are removed. Complete rear-wall slots and their eight transforms are asserted. | Start 4v4, reveal the map, and inspect every side wall after trigger initialization. |
| ASC-003 | Sideways gates, wall gaps, unequal territory, wrong water, cliffs, and broken routes. | Guarded | Gate type and wall rotation are transformed by map axis; the terrain hash and all eight symmetry orbits are fixed; default cliffs are absent; allied routes and enemy-side water have explicit tests. | Walk units through every friendly gate/route and attempt every enemy bypass. |
| ASC-004 | Full or sparse games could declare defeat immediately on launch. | Guarded | Color owners are detected from their four-Castle rows. Defeat requires a settled two-sided match, an active mapped color, and absence of its Castles. All 6,560 occupied/alive color states are modeled; the audit finds no reachable unconditional defeat. | Launch full 4v4, P1 vs P5, and a non-adjacent sparse lobby; wait at least 15 seconds. |
| ASC-005 | P5 did not spawn in P1 vs P5; arbitrary closed slots and all civilizations must work. | Guarded | Every valid compacted color-to-world pair has a detector. XS spawns by detected world owner, and civilization ids 1–59 have explicit unit, cap, and interval mappings. | Test P1 vs P5 and P2+P4 vs P5+P8 with representative civilizations. Add mappings before enabling any later DLC civilization id. |
| ASC-006 | Deleting rear vote markers did not kick a teammate safely. | Guarded | There are 24 two-voter detectors, 24 marker variables, 108 compact-owner deletion detectors, and 36 target resolvers. Target plus both distinct voters must be active; a side with fewer than three live colors cannot resolve a kick. | With three and four teammates, cast two votes; with two teammates, prove no kick; repeat in a sparse lobby. |
| ASC-007 | Builder pairs were missing or awarded at the wrong razing threshold. | Guarded | All 59 civilization thresholds are explicit. Earned pairs are persistent and queue at `razings - threshold + 1`; the local start message reports the selected civilization's threshold. | Use Persians: first pair at 4 razings, then one pair per razing; verify another low-threshold and high-threshold civilization. |
| ASC-008 | Resources, research, buildings, upgrades, or repairs were not free; Bombard Tower was unavailable. | Guarded | Starting stockpiles and score resources are zeroed. XS sets technology and object costs to zero at runtime, repair modifiers are zero, and Bombard Tower availability is forced for every valid owner mapping. | Open several technology/build menus for multiple civilizations and confirm every available action costs zero. |
| ASC-009 | Starting scores differed; K/D/R was misaligned; razings/MVP were not represented. | Guarded | The right-side rows use ordered `P# | K | D | R` variables. Non-combat score attributes are neutralized and kill/death/razing values are republished from live engine attributes. | Compare all starting scores, live K/D/R updates, and post-game statistics in full and sparse games. |
| ASC-010 | Invisible spots behind Castles deleted units. | Resolved statically | All 32 legacy edge-deletion triggers are removed. No replacement trigger uses those hidden strips. | Patrol behind every Castle and leave units there for at least one minute. |
| ASC-011 | Rear gates needed a small dry path to the University and Blacksmith, with no water inside the walls. | Guarded | Each transformed gate path is three tiles wide and non-water. A bounded flood-fill reaches both technology buildings for all eight colors while treating water, walls, towers, Castles, and cliffs as blocked. | Path a builder from each base through its rear gate to both buildings. |
| ASC-012 | Allied paths must be walkable and protected without opening enemy shortcuts. | Guarded | Top/bottom team causeways are land; enemy-side corridors remain water; protected wall/gate references are included in anti-delete effects. | Test allied reinforcement and enemy pathfinding from every orientation. |
| ASC-013 | Objectives and public text must be clean and contain no development/AI references. | Resolved statically | Scenario messages are rewritten for Ascendants and serialized labels are sanitized; regression tests reject development references. | Review the lobby instructions, objectives panel, start messages, victory, and defeat text. |
| ASC-014 | Two score numbers appeared beside a player. | Not a scenario defect | The second number is Definitive Edition's team-average display, not another custom score field. | No change unless the game offers a supported UI option to hide it. |
| ASC-015 | Armies ordered back toward their Castles turned around at an invisible line. | Guarded | All 108 full/sparse Short, Medium, and Long route triggers require a color-specific new-wave variable set by XS only after unit creation. The selected owner route consumes the pulse once; no pulse means no task effect. | For all eight colors, let a wave leave, order it back across all four spawn pads, and confirm the manual order remains. |
| ASC-016 | The marked milestone shoreline rejected building placement. | Guarded | The exact 20-cell Beach ribbon is transformed eight ways into 160 unique Grass 2 cells. Tests pin its terrain, elevation, layer, symmetry, and whole-map terrain hash. | Place representative buildings throughout every repaired shore strip, including the former corners. |
| ASC-017 | Marker ships added no value and could not be made reliable. | Resolved by removal | The serialized scenario contains zero Transport Ships. Their creation pass and all 56 marker protection effects are deleted; milestone hero creation and orders remain independently tested. | Confirm all eight shores are clear and milestone heroes still spawn normally. |
| ASC-018 | A resigned player's units and buildings remained on the map. | Guarded | Each of the 36 valid color/runtime resignation resolvers has one full-map `REMOVE_OBJECT` effect scoped to its resolved runtime player, alongside the eliminated/active state changes. | Resign one player in full 4v4 and a compacted sparse lobby; all of that player's objects must disappear without touching anyone else. |
| ASC-019 | None of the five Sheep positions worked reliably; 200/400+ kill heroes always took the default Medium route. | Guarded in v1.0.7 | Engine evidence disproved the narrow v1.0.6 zones. All 40 selectors now cover collision-limited approach cells, and all five regions are mutually exclusive. All 108 normal-wave and 108 milestone-hero route triggers read the same eight latched route variables. The 36 fixed-Medium Open fallbacks are absent. | For every color in full and sparse lobbies, move the Sheep to Short, Medium, Long, Closed, and Open. Normal waves and 200/400/600/800/1000/2000 heroes must follow the selected route; Closed/Open must add/remove the shore blocker without resetting that route. |

## Additional parser findings

The v1.0.7 candidate passes the structural audit with **0 errors and 0 warnings**:

- 2,291 uniquely named, non-empty triggers and a complete display order;
- 1,076 unique object references, all on-map, with no dangling garrisons;
- 97 unique variable ids and no dangling variable use;
- no dangling trigger or selected-object references;
- no partial, inverted, or out-of-bounds trigger geometry;
- no reachable looping trigger without a Timer condition;
- no reachable unconditional remove, kill, victory, or defeat trigger.

The dedicated migration removed all prior audit debt. It deleted 810 proven empty
shells, merged 189 byte-identical age-up copies, rewired 346 incoming activations, and
retained/name-disambiguated the three non-identical P7 variants. Exact baseline counts
and reference-shape assertions make the migration fail closed if the imported graph
ever changes.

Run the same audit after every build:

```bash
aoe2modes audit "dist/CBA Hero Ascendants v1.0.7.aoe2scenario"
```

`--strict` passes too. The normal command fails only on structural errors; strict also
fails if future warning-level hazards return.

## Engine acceptance matrix

AoE2ScenarioParser does not execute XS, multiplayer slot compaction, pathfinding,
score UI, or the victory scheduler. A release candidate is not finished until these
cases are recorded in-game.

| Case | Lobby | Must be observed |
| --- | --- | --- |
| Full initialization | P1–P4 vs P5–P8 | No early defeat; equal starts; all eight armies; complete walls and dry paths. |
| Minimum sparse | P1 vs P5 | Correct P5 ownership/spawns, no startup cleanup, normal final victory. |
| Non-adjacent sparse | P2+P4 vs P5+P8 | Correct color bases, HUD rows, upgrades, builders, heroes, and victory owner. |
| Vote success | Any side with at least three live colors | Two distinct teammate marker deletions defeat only the target. |
| Vote safety | Any side with two live colors | One or two deleted markers never kick either player. |
| Builder threshold | Persian plus one other civilization | First pair at the documented threshold, then exactly one pair per later razing. |
| Route/pathing | All eight colors | Friendly rear and team routes work; walls have no diagonal gap; enemies cannot bypass. |
| Score/UI | Full and sparse | K/D/R updates, starting scores are neutral, and post-game combat/razing totals are credible. |
| Manual army return | All eight colors, full and sparse | Returning units cross the four launch pads without being sent back toward the arena. |
| Five Sheep controls | All eight colors, full and sparse | Short/Medium/Long route the next normal wave and every kill hero identically; Closed/Open add/remove the shore blocker without resetting the route; existing armies keep manual orders. |
| Milestone shore | All eight colors | Buildings can be placed on the repaired strip; hero spawns and nearby water remain clear. |
| Marker removal | All eight colors | No Transport Ship is present; milestone heroes still spawn and route normally. |
| Resignation cleanup | Full and sparse | Every unit and building owned by the resigned runtime player disappears; other colors remain intact. |

For a failure, record the exact selected colors, runtime player numbers, civilizations,
game time, action, observed result, and expected result. That is enough to turn most
engine reports into a focused parser-backed regression test.
