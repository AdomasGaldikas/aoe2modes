# Ascendants v1.0.3 issue register

This is the working inventory recovered from the **Publish CBA Hero scenario** task.
Only **CBA Hero: Ascendants v1.0.3** is an active baseline. Older builds are useful for
provenance but are not candidates to repair or publish.

The baseline file is 99,694 bytes with SHA-256
`4082a73c9e9323cda5678a758518c12a5e387c3beafa20ce3835f40466fb8d34`.
“Guarded” means the serialized scenario and tests contain the intended correction; it
does not mean the Definitive Edition engine has been observed running it successfully.

## Reported issues

| ID | Report or requirement | v1.0.3 status | Parser/source evidence | Required game check |
| --- | --- | --- | --- | --- |
| ASC-001 | Leave two fewer rows behind every player's Castles. | Guarded | The canonical rear wall moved from source x=10.5 to x=14.5. Land is x=14..16: one wall row plus exactly two protected interior rows, transformed identically eight ways. | Visually inspect all eight rear Castle strips. |
| ASC-002 | Red, Teal, Purple, and Orange lost a side wall. | Guarded | All 16 `no wall` / `re no wall` legacy cleanup triggers are empty and disabled. Complete rear-wall slots and their eight transforms are asserted. | Start 4v4, reveal the map, and inspect every side wall after trigger initialization. |
| ASC-003 | Sideways gates, wall gaps, unequal territory, wrong water, cliffs, and broken routes. | Guarded | Gate type and wall rotation are transformed by map axis; the terrain hash and all eight symmetry orbits are fixed; default cliffs are absent; allied routes and enemy-side water have explicit tests. | Walk units through every friendly gate/route and attempt every enemy bypass. |
| ASC-004 | Full or sparse games could declare defeat immediately on launch. | Guarded | Color owners are detected from their four-Castle rows. Defeat requires a settled two-sided match, an active mapped color, and absence of its Castles. The parser audit finds no reachable unconditional defeat. | Launch full 4v4, P1 vs P5, and a non-adjacent sparse lobby; wait at least 15 seconds. |
| ASC-005 | P5 did not spawn in P1 vs P5; arbitrary closed slots and all civilizations must work. | Guarded | Every valid compacted color-to-world pair has a detector. XS spawns by detected world owner, and civilization ids 1–59 have explicit unit, cap, and interval mappings. | Test P1 vs P5 and P2+P4 vs P5+P8 with representative civilizations. Add mappings before enabling any later DLC civilization id. |
| ASC-006 | Deleting rear vote markers did not kick a teammate safely. | Guarded | There are 24 two-voter detectors, 24 marker variables, 108 compact-owner deletion detectors, and 36 target resolvers. Target plus both distinct voters must be active; a side with fewer than three live colors cannot resolve a kick. | With three and four teammates, cast two votes; with two teammates, prove no kick; repeat in a sparse lobby. |
| ASC-007 | Builder pairs were missing or awarded at the wrong razing threshold. | Guarded | All 59 civilization thresholds are explicit. Earned pairs are persistent and queue at `razings - threshold + 1`; the local start message reports the selected civilization's threshold. | Use Persians: first pair at 4 razings, then one pair per razing; verify another low-threshold and high-threshold civilization. |
| ASC-008 | Resources, research, buildings, upgrades, or repairs were not free; Bombard Tower was unavailable. | Guarded | Starting stockpiles and score resources are zeroed. XS sets technology and object costs to zero at runtime, repair modifiers are zero, and Bombard Tower availability is forced for every valid owner mapping. | Open several technology/build menus for multiple civilizations and confirm every available action costs zero. |
| ASC-009 | Starting scores differed; K/D/R was misaligned; razings/MVP were not represented. | Guarded | The right-side rows use ordered `P# | K | D | R` variables. Non-combat score attributes are neutralized and kill/death/razing values are republished from live engine attributes. | Compare all starting scores, live K/D/R updates, and post-game statistics in full and sparse games. |
| ASC-010 | Invisible spots behind Castles deleted units. | Resolved statically | All 32 legacy edge-deletion strips are empty and disabled. No replacement trigger uses those hidden strips. | Patrol behind every Castle and leave units there for at least one minute. |
| ASC-011 | Rear gates needed a small dry path to the University and Blacksmith, with no water inside the walls. | Guarded | Each transformed gate path is three tiles wide, connects the protected interior to the technology island, and is asserted as non-water. | Path a builder from each base through its rear gate to both buildings. |
| ASC-012 | Allied paths must be walkable and protected without opening enemy shortcuts. | Guarded | Top/bottom team causeways are land; enemy-side corridors remain water; protected wall/gate references are included in anti-delete effects. | Test allied reinforcement and enemy pathfinding from every orientation. |
| ASC-013 | Objectives and public text must be clean and contain no development/AI references. | Resolved statically | Scenario messages are rewritten for Ascendants and serialized labels are sanitized; regression tests reject development references. | Review the lobby instructions, objectives panel, start messages, victory, and defeat text. |
| ASC-014 | Two score numbers appeared beside a player. | Not a scenario defect | The second number is Definitive Edition's team-average display, not another custom score field. | No change unless the game offers a supported UI option to hide it. |

## Additional parser findings

The v1.0.3 binary currently passes the structural audit with **0 errors**:

- 3,326 unique trigger ids and a complete display order;
- 1,084 unique object references, all on-map, with no dangling garrisons;
- 81 unique variable ids and no dangling variable use;
- no dangling trigger or selected-object references;
- no partial, inverted, or out-of-bounds trigger geometry;
- no reachable looping trigger without a Timer condition;
- no reachable unconditional remove, kill, victory, or defeat trigger.

Two warnings are intentional technical debt rather than confirmed gameplay failures:

- **22 duplicate trigger-name groups.** The largest are legacy civilization age-up
  chains such as `300 kills`. Their ids, not their names, are activation targets. Do
  not merge or bulk-rename them without rewriting and retesting the activation graph.
- **810 empty legacy trigger shells, 112 initially enabled.** Most preserve ids from
  the decompiled source, including 472 retired army-spawn slots. They are harmless to
  serialized references, but should be compacted only as a dedicated migration after
  an editor round-trip and game test.

Run the same audit after every build:

```bash
aoe2modes audit "dist/CBA Hero Ascendants v1.0.3.aoe2scenario"
```

`--strict` also fails on the two legacy warnings. The normal command fails only on
structural errors.

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

For a failure, record the exact selected colors, runtime player numbers, civilizations,
game time, action, observed result, and expected result. That is enough to turn most
engine reports into a focused parser-backed regression test.
