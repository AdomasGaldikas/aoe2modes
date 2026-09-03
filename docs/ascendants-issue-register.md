# Ascendants v1.0.11 candidate issue register

This is the working inventory recovered from the **Publish CBA Hero scenario** task.
Only **CBA Hero: Ascendants v1.0.3** is a comparison baseline. Older builds are not
repair targets. **v1.0.11** is the active source-verified candidate; v1.0.10 remains the
immediately preceding candidate for focused comparison only.

The baseline file is 99,694 bytes with SHA-256
`4082a73c9e9323cda5678a758518c12a5e387c3beafa20ce3835f40466fb8d34`.
The v1.0.11 candidate is 125,040 bytes with SHA-256
`d516f9d9c472c8f650d590830788e5f62f21e28666c7c51bdc99f245413394c5`.
“Guarded” means the serialized scenario and tests contain the intended correction; it
does not mean the Definitive Edition engine has been observed running it successfully.

## Reported issues

| ID | Report or requirement | v1.0.11 source status | Parser/source evidence | Required game check |
| --- | --- | --- | --- | --- |
| ASC-001 | Leave two fewer rows behind every player's Castles. | Guarded | The canonical rear wall moved from source x=10.5 to x=14.5. Land is x=14..16: one wall row plus exactly two protected interior rows, transformed identically eight ways. | Visually inspect all eight rear Castle strips. |
| ASC-002 | Red, Teal, Purple, and Orange lost a side wall. | Guarded | All 16 `no wall` / `re no wall` shells and their 16 no-op incoming deactivations are removed. Complete rear-wall slots and their eight transforms are asserted. | Start 4v4, reveal the map, and inspect every side wall after trigger initialization. |
| ASC-003 | Sideways gates, wall gaps, unequal territory, wrong water, cliffs, and broken routes. | Guarded | Gate type and wall rotation are transformed by map axis; the terrain hash and all eight symmetry orbits are fixed; default cliffs are absent; allied routes and enemy-side water have explicit tests. | Walk units through every friendly gate/route and attempt every enemy bypass. |
| ASC-004 | Full or sparse games could declare defeat immediately on launch. | Guarded | Color owners are detected from their four-Castle rows. Defeat requires a settled two-sided match, an active mapped color, and absence of its Castles. All 6,560 occupied/alive color states are modeled; the audit finds no reachable unconditional defeat. | Launch full 4v4, P1 vs P5, and a non-adjacent sparse lobby; wait at least 15 seconds. |
| ASC-005 | P5 did not spawn in P1 vs P5; arbitrary closed slots and all civilizations must work. | Corrected and guarded in v1.0.11 | All 64 color/player candidates have trigger-side Castle-row detectors. Separately, XS obtains the actual lobby/world player with `xsGetWorldPlayerId(scenarioPlayer)` before reading civilization or creating an army. Civilization ids 1–59 have explicit unit, cap, and interval mappings. | Test P1 vs P5 and P2+P4 vs P5+P8 with representative civilizations. Add mappings before enabling any later DLC civilization id. |
| ASC-006 | Deleting rear vote markers did not kick a teammate safely. | Guarded | There are 24 two-voter detectors, 24 marker variables, 192 runtime-owner deletion detectors, and 64 target resolvers. Target plus both distinct voters must be active; a side with fewer than three live colors cannot resolve a kick. | With three and four teammates, cast two votes; with two teammates, prove no kick; repeat in a sparse lobby. |
| ASC-007 | Builder pairs were missing or awarded at the wrong razing threshold. | Guarded | All 59 civilization thresholds are explicit. Earned pairs are persistent and queue at `razings - threshold + 1`; the local start message reports the selected civilization's threshold. | Use Persians: first pair at 4 razings, then one pair per razing; verify another low-threshold and high-threshold civilization. |
| ASC-008 | Resources, research, buildings, upgrades, or repairs were not free; Bombard Tower was unavailable. | Guarded | Starting stockpiles and score resources are zeroed. XS sets technology and object costs to zero at runtime, repair modifiers are zero, and Bombard Tower availability is forced for every valid owner mapping. | Open several technology/build menus for multiple civilizations and confirm every available action costs zero. |
| ASC-009 | Starting scores differed; K/D/R was misaligned; razings/MVP were not represented. | Guarded | The right-side rows use ordered `P# | K | D | R` variables. Non-combat score attributes are neutralized and kill/death/razing values are republished from live engine attributes. | Compare all starting scores, live K/D/R updates, and post-game statistics in full and sparse games. |
| ASC-010 | Invisible spots behind Castles deleted units. | Resolved statically | All 32 legacy edge-deletion triggers are removed. No replacement trigger uses those hidden strips. | Patrol behind every Castle and leave units there for at least one minute. |
| ASC-011 | Rear gates needed a small dry path to the University and Blacksmith, with no water inside the walls. | Guarded | Each transformed gate path is three tiles wide and non-water. A bounded flood-fill reaches both technology buildings for all eight colors while treating water, walls, towers, Castles, and cliffs as blocked. | Path a builder from each base through its rear gate to both buildings. |
| ASC-012 | Allied paths must be walkable and protected without opening enemy shortcuts. | Guarded | Top/bottom team causeways are land; enemy-side corridors remain water; protected wall/gate references are included in anti-delete effects. | Test allied reinforcement and enemy pathfinding from every orientation. |
| ASC-013 | Objectives and public text must be clean and contain no development/AI references. | Resolved statically | Scenario messages are rewritten for Ascendants and serialized labels are sanitized; regression tests reject development references. | Review the lobby instructions, objectives panel, start messages, victory, and defeat text. |
| ASC-014 | Two score numbers appeared beside a player. | Not a scenario defect | The second number is Definitive Edition's team-average display, not another custom score field. | No change unless the game offers a supported UI option to hide it. |
| ASC-015 | Armies ordered back toward their Castles turned around at an invisible line. | Guarded | All 192 full/sparse Short, Medium, and Long route triggers require a color-specific new-wave variable set by XS only after unit creation. The selected owner route consumes the pulse once; no pulse means no task effect. | For all eight colors, let a wave leave, order it back across all four spawn pads, and confirm the manual order remains. |
| ASC-016 | The marked milestone shoreline rejected building placement. | Guarded | The exact 20-cell Beach ribbon is transformed eight ways into 160 unique Grass 2 cells. Tests pin its terrain, elevation, layer, symmetry, and whole-map terrain hash. | Place representative buildings throughout every repaired shore strip, including the former corners. |
| ASC-017 | Marker ships added no value and could not be made reliable. | Resolved by removal | The serialized scenario contains zero Transport Ships. Their creation pass and all 56 marker protection effects are deleted; milestone hero creation and orders remain independently tested. | Confirm all eight shores are clear and milestone heroes still spawn normally. |
| ASC-018 | A resigned player's units and buildings remained on the map. | Guarded | Each of the 64 color/runtime resignation resolvers has one full-map `REMOVE_OBJECT` effect scoped to its resolved runtime player, alongside the eliminated/active state changes. | Resign one player in full 4v4 and a compacted sparse lobby; all of that player's objects must disappear without touching anyone else. |
| ASC-019 | None of the five Sheep positions worked reliably; 200/400+ kill heroes always took the default Medium route. | Corrected and guarded in v1.0.11 | All 40 selectors use one exact Sheep reference per color, cover mutually exclusive reachable approach cells, and write that color's route variable. Normal-wave and hero movers read the same variable. The v1.0.10 cross-owned XS spawn could leave the correctly mapped mover with no selectable army; v1.0.11 repairs that identity boundary. An integrated regression follows Sheep → route variable → normal wave and hero route for all eight colors under identity, Red/Green swap, and full rotation mappings. | For every color in full and sparse lobbies, move the Sheep to Short, Medium, Long, Closed, and Open. Normal waves and 200/400/600/800/1000/2000 heroes must follow the selected route; Closed/Open must add/remove the shore blocker without resetting that route. |
| ASC-020 | Red/Green and Green/Yellow armies spawned from or routed through one another's Castle territories in shuffled lobbies. | Corrected and guarded in v1.0.11 | The v1.0.8–v1.0.10 implementation conflated trigger player selectors with XS world players. XS now uses the engine's `xsGetWorldPlayerId(scenarioPlayer)` conversion, while trigger effects keep the independent Castle-row resolver. Tests pin that boundary and the complete control chain; all 32 pads are dry, unique, empty, transformed from one canonical row, and closest to their own Castles. | Start a full lobby with Red and Green reversed, then Yellow before Green, then another shuffled order. Confirm each territory's army color/civilization, Sheep route, heroes, HUD, rewards, resignation, and victory stay with that Castle row. |
| ASC-021 | Anti-Trebuchet protection did not cover the Castles of P4, P6, P7, or P8. | Guarded in v1.0.9 | Both cleanup families now derive from one canonical P3 rectangle through an independent eight-way transform. Every color's anti-Trebuchet zone is one mirror orbit, covers all four of its Castles, and stays clear of its rear route. Effects remain restricted to an enemy player's packed Trebuchets. | Place an enemy packed Trebuchet beside each Castle row, especially P4/P6/P7/P8; it must be removed without affecting friendly rear-route units. |
| ASC-022 | Milestone heroes could be turned back by the invisible spawn line after the player ordered them toward the Castles. | Guarded in v1.0.10 | All 192 Short/Medium/Long hero movers now require and consume one of eight hero-creation pulses. The six 200–2000 milestones and all three 3500/5000 Genghis loops arm that pulse only after creating a hero. | For every color and each route, return milestone and late Genghis heroes through the three hero spawn cells; later player orders must remain intact. |
| ASC-023 | Raze-reward builders could have later orders overwritten when they returned across their creation pads. | Guarded in v1.0.10 | All 64 builder movers require and consume one of eight builder-creation pulses. Each reward arms the pulse after creating the pair, and only the resolved runtime owner can consume it once. | Earn a pair for every color orientation, let it auto-park, then move both villagers back across both spawn pads; they must obey the player. |
| ASC-024 | Obsolete wooden walls and Saboteurs were visible in the outer map corners. | Resolved statically in v1.0.11 | Exactly 56 submerged static Palisade Walls and eight static Saboteurs are removed after assertions pin their types, counts, water terrain, and corner locations. Their 64 object references are absent from all conditions/effects. The independent trigger-created Goth Palisade reward remains. | Reveal all four corners and confirm no Palisade Wall or Saboteur remains; verify a Goth player can still receive the intended Palisade reward. |

## Additional parser findings

The v1.0.11 candidate passes the strict structural audit with **0 errors and 0 warnings**:

- 3,383 uniquely named, non-empty triggers and a complete display order;
- 1,012 unique object references, all on-map, with no dangling garrisons;
- 113 unique variable ids and no dangling variable use;
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
aoe2modes audit "dist/CBA Hero Ascendants v1.0.11.aoe2scenario" --strict
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
| Shuffled full lobby | Red/Green reversed, Yellow before Green, then another nonnumeric order | Every Castle row creates its own color/civilization; its Sheep route, heroes, HUD, rewards, resignation, and victory stay attached to that territory. |
| Minimum sparse | P1 vs P5 | Correct P5 ownership/spawns, no startup cleanup, normal final victory. |
| Non-adjacent sparse | P2+P4 vs P5+P8 | Correct color bases, HUD rows, upgrades, builders, heroes, and victory owner. |
| Vote success | Any side with at least three live colors | Two distinct teammate marker deletions defeat only the target. |
| Vote safety | Any side with two live colors | One or two deleted markers never kick either player. |
| Builder threshold | Persian plus one other civilization | First pair at the documented threshold, then exactly one pair per later razing. |
| Route/pathing | All eight colors | Friendly rear and team routes work; walls have no diagonal gap; enemies cannot bypass. |
| Score/UI | Full and sparse | K/D/R updates, starting scores are neutral, and post-game combat/razing totals are credible. |
| Manual army return | All eight colors, full and sparse | Returning units cross the four launch pads without being sent back toward the arena. |
| Manual hero return | All eight colors, full and sparse | Returning 200–2000 and 3500/5000 heroes cross all three hero pads without being sent back toward the arena. |
| Manual builder return | All eight colors, full and sparse | After auto-parking, both raze-reward villagers can cross their two creation pads without being retasked. |
| Five Sheep controls | All eight colors, full and sparse | Short/Medium/Long route the next normal wave and every kill hero identically; Closed/Open add/remove the shore blocker without resetting the route; existing armies keep manual orders. |
| Milestone shore | All eight colors | Buildings can be placed on the repaired strip; hero spawns and nearby water remain clear. |
| Marker removal | All eight colors | No Transport Ship is present; milestone heroes still spawn and route normally. |
| Corner cleanup | All four outer corners; include Goth once | No static Palisade Wall or Saboteur remains; the separate Goth Palisade reward still works. |
| Resignation cleanup | Full and sparse | Every unit and building owned by the resigned runtime player disappears; other colors remain intact. |
| Anti-Trebuchet parity | All eight colors | An enemy packed Trebuchet beside any Castle row is removed, including P4/P6/P7/P8; no friendly rear-route unit is touched. |

For a failure, record the exact selected colors, runtime player numbers, civilizations,
game time, action, observed result, and expected result. That is enough to turn most
engine reports into a focused parser-backed regression test.
