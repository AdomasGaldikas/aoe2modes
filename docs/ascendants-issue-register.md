# Ascendants v1.0.20 issue register

This is the working inventory recovered from the **Publish CBA Hero scenario** task.
Only **CBA Hero: Ascendants v1.0.3** is a comparison baseline. Older builds are not
repair targets. **v1.0.20** is the current code correction; live DE acceptance remains
separate. v1.0.18 and v1.0.19 both failed the reported closed-slot game.

The baseline file is 99,694 bytes with SHA-256
`4082a73c9e9323cda5678a758518c12a5e387c3beafa20ce3835f40466fb8d34`.
The failed v1.0.18 candidate was 161,074 bytes with SHA-256
`5262f6250889eb1dd6d0caeb9bdc080d8bf9c59c97725588d3f827274858a19d`.
The failed v1.0.19 candidate was 161,657 bytes with SHA-256
`ec4c03df92588582e5c5984e1befdd9d18b289b4553c9a4b86503a098c3991a0`;
142 tests and the warning-free strict audit passed, but did not catch the live failure.
See v1.0.20 release notes for the replacement detection path and validation.
“Guarded” means the serialized scenario and tests contain the intended correction; it
does not mean the Definitive Edition engine has been observed running it successfully.

## Reported issues

| ID | Report or requirement | Source status (historical claims qualified by ASC-049) | Parser/source evidence | Required game check |
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
| ASC-015 | Armies ordered back toward their Castles turned around at an invisible line. | Guarded and expanded in v1.0.13 | All 384 level 0–5 Castle-army route triggers require a color-specific new-wave variable set by XS only after unit creation. Each task captures only its exact cell-centred creation pad, and the selected owner route consumes the pulse once; no pulse means no task effect. | For all eight colors and every Sheep level, let a wave leave, order it back across all four spawn pads, and confirm the manual order remains. |
| ASC-016 | The marked milestone shoreline rejected building placement. | Guarded | The exact 20-cell Beach ribbon is transformed eight ways into 160 unique Grass 2 cells. Tests pin its terrain, elevation, layer, symmetry, and whole-map terrain hash. | Place representative buildings throughout every repaired shore strip, including the former corners. |
| ASC-017 | Marker ships added no value and could not be made reliable. | Resolved by removal | The serialized scenario contains zero Transport Ships. Their creation pass and all 56 marker protection effects are deleted; milestone hero creation and orders remain independently tested. | Confirm all eight shores are clear and milestone heroes still spawn normally. |
| ASC-018 | A resigned player's units and buildings remained on the map. | Guarded | Each of the 64 color/runtime resignation resolvers has one full-map `REMOVE_OBJECT` effect scoped to its resolved runtime player, alongside the elimination latch that XS reads. | Resign one player in full 4v4 and a compacted sparse lobby; all of that player's objects must disappear without touching anyone else. |
| ASC-019 | None of the five shared Sheep positions worked reliably; 200/400+ kill Heroes always took the default route. | Replaced in v1.0.13; containment revised in v1.0.14 | The five-point mechanism is gone. Per color, 6 Sheep selectors write Castle-army level 0–5 and 6 Penguin selectors write Hero level 0–5. Each family partitions its own water-isolated 9×2 track. Exactly 384 Castle and 320 Hero owner mappings consume separate one-shot pulses. | For every color in full and sparse lobbies, move the Sheep and Penguin through every level. New units must follow the selected controller only; existing units must retain manual orders. Confirm attempted cross-track orders cannot leave the controller's own track. |
| ASC-020 | Red/Green and Green/Yellow armies spawned from or routed through one another's Castle territories in shuffled lobbies. | Corrected and guarded in v1.0.11 | The v1.0.8–v1.0.10 implementation conflated trigger player selectors with XS world players. XS now uses the engine's `xsGetWorldPlayerId(scenarioPlayer)` conversion, while trigger effects keep the independent Castle-row resolver. Tests pin that boundary and the complete control chain; all 32 pads are dry, unique, empty, transformed as cells from one canonical row, created at their centres, and closest to their own Castles. | Start a full lobby with Red and Green reversed, then Yellow before Green, then another shuffled order. Confirm each territory's army color/civilization, Sheep route, heroes, HUD, rewards, resignation, and victory stay with that Castle row. |
| ASC-021 | Anti-Trebuchet protection did not cover the Castles of P4, P6, P7, or P8. | Guarded in v1.0.9 | Anti-Trebuchet zones derive from one canonical P3 rectangle through an independent eight-way transform. Every color's zone is one mirror orbit, covers all four of its Castles, and stays clear of its rear route. Effects remove packed Trebuchets for all owners inside the exclusion zones; the rule is not enemy-only. Separate wall-breach removal uses exact references, not rectangles, as recorded in ASC-029. | Place an enemy packed Trebuchet beside each Castle row, especially P4/P6/P7/P8; it must be removed without affecting friendly rear-route units. |
| ASC-022 | Milestone Heroes could be turned back by the invisible spawn line after the player ordered them toward the Castles. | Guarded and expanded in v1.0.13 | All 320 level 1–5 Hero movers require and consume one of eight Hero-creation pulses. The six 200–2000 bands and all three 3500/5000 Genghis loops arm that pulse only after creating a Hero. | For every color and active Penguin level, return milestone and late Genghis Heroes through the three Hero spawn cells; later player orders must remain intact. |
| ASC-023 | Raze-reward builders could have later orders overwritten when they returned across their creation pads. | Guarded in v1.0.10 | All 64 builder movers require and consume one of eight builder-creation pulses. Each reward arms the pulse after creating the pair, and only the resolved runtime owner can consume it once. | Earn a pair for every color orientation, let it auto-park, then move both villagers back across both spawn pads; they must obey the player. |
| ASC-024 | Obsolete wooden walls and Saboteurs were visible in the outer map corners. | Resolved statically in v1.0.11 | Exactly 56 submerged static Palisade Walls and eight static Saboteurs are removed after assertions pin their types, counts, water terrain, and corner locations. Their 64 object references are absent from all conditions/effects. | Reveal all four corners and confirm no Palisade Wall or Saboteur remains. |
| ASC-025 | The hidden Goth Palisade HP mechanic is unnecessary and must not remain. | Resolved statically in v1.0.12 | The mechanic required Elite Huskarl plus 12 Palisade Walls in a fixed row, then added 2,750 HP. All eight imported triggers and 64 color/player replacements are absent. Tests reject every serialized Palisade condition/effect while preserving the separate Goth Anarchy/Barracks family. | As Goths, research Elite Huskarl and build Palisades near the Castle lane; they must retain ordinary game HP and receive no scenario bonus. |
| ASC-026 | Spawn controls should be simple and independent: one Sheep for Castle armies and one Penguin for Hero OFF/ON plus distance. | Implemented in v1.0.13; clarified in v1.0.14 | Every color has exactly one Sheep and one War Penguin on separate water-isolated tracks, each with six detection bands. Snow is exactly L0 Castle HOLD / Hero OFF; L1–L5 progress toward battle. Controllers and four per-color Signs have short role-specific names. Both controllers are owner-resolved, undeletable, and untargetable, and Penguins cannot attack. The 251 hard cap plus custom-cap compensation preserves 250 gameplay slots. Mutually exclusive kill bands prevent stale Hero tiers after OFF. | Check visibility and movement on every orientation; leave Penguin at L0 across a milestone, then enable it and confirm only the current tier begins spawning. |
| ASC-027 | Decorative Castle Hay markers could block army creation or L0 holding cells. | Resolved statically in v1.0.13 | Footprint-aware validation found that the 32 two-by-two Hay Stack creates covered 16 of 32 launch pads and eight L0 destinations even though their anchors were distinct. All 32 Hay creation triggers are retired; tests reject any surviving Hay create and the path audit checks every pad/destination footprint. | Confirm all four Castle waves appear and clear L0 without displacement for every color, especially during sustained spawning. |
| ASC-028 | Sheep and Penguin could leave their own trigger line; HOLD/OFF endpoints and controller names were unclear. | Guarded in v1.0.14 | Each canonical track is 9×2, separated by three rows of Deep Water without beach bridges. Each controller's selectors partition only its own dry track. Snow covers exactly L0; the road begins at L1. Four per-color endpoint Signs leave a row clear, and controller names are `Army range - snow = HOLD` / `Hero range - snow = OFF`. Connectivity checks prove every level reachable without leaving the selector union; no recurring task/stop/freeze correction is added. | For every color, order both controllers beyond every track edge and across the water gap. They must remain on their own track and still reach all levels. Check that Snow means HOLD/OFF, the first road tile changes to L1, and all signs/names are readable. HOLD must keep producing Castle waves; OFF must pause new Heroes only. |
| ASC-029 | Side-wall deletion must not open a path around the front gates or remove the rear University boundary. | Corrected and guarded in v1.0.15 | v1.0.14 wrongly preserved the long side walls. The 64 `Wall Breach` mappings now remove the exact short shoulders plus 30 long side-wall references per color: 44 walls for P1/P2/P7/P8, 48 for P3/P4/P5/P6. The three front gates and complete front wall row remain, with two new end posts per color closing the bypass. The rear University wall/gate, joins, and teammate access gates remain protected. The switch at canonical `(23.0,43.5)` is separate from the University gate at `(14.5,54.0)`. | Delete the switch for every color: short and long side walls disappear; the front and University barriers remain. With other gates shut, test both front ends and the rear University route for bypasses. Repeat with sparse and shuffled owners; other players' fortifications must remain intact. |
| ASC-030 | The wall-limit wipe must remain active while sparing the permanent front and University barriers. | Restored and guarded in v1.0.15 | v1.0.14 wrongly removed the rule. There are now 64 owner-resolved warning/wipe pairs: one-shot warning at 200 owned WALL-class objects, then wipe at 220, including preplaced walls in the count. Each wipe selects only that owner's WALL class through 49 rectangles covering all 20,368 cells outside 368 protected barrier cells. Permanent references retain wildcard and owner-resolved manual-delete protection; the switch remains deletable. Some side walls retain legacy Delete protection, which scripted removal ignores. No ownership swap or remove/recreate workaround is used. | Reach 200 then 220 WALL-class objects for each color; confirm the warning, then removal of that owner's walls outside protected barrier cells. Front gates/posts, the University wall/gate, teammate access gates, and other owners' walls must survive. Test after side-wall deletion, in sparse/shuffled lobbies, and confirm the warning/wipe remains one-shot. |

## v1.0.16 audit additions

| ID | Finding | Source status and verification | Required game check |
| --- | --- | --- | --- |
| ASC-031 | Training bans differ by color | Shared deduplicated union: 143 units, 14 buildings, one technology; all eight color lists checked. | Same civilization's menus across colors. |
| ASC-032 | Returning Genghis deleted/rebuffed by production | Replaced spawn-pad removal with an owned-Genghis absence condition at 2000/3500/5000 kills. Existing units survive; buffs share the exclusion area. | Park a Genghis on each pad, then clear it. |
| ASC-033 | Center Trebuchet reward removes parked units | Waits for absence of owned packed units instead of removing them. | Occupy and clear the reward pad. |
| ASC-034 | OFF retains a pending Hero move | OFF clears pending movement and production level. ON alone cannot restore the pulse. | OFF just after birth, then ON. |
| ASC-035 | Goth Imperial/Barracks race | Both Anarchy activation and removal require Imperial Age to be unresearched; all 128 triggers checked. | Research Imperial with Barracks present. |
| ASC-036 | Combat can delete vote Outposts | All 24 markers protected against attacks, initially and across owner mappings. Owner Delete remains available. | Attack markers, then intentionally delete to vote. |
| ASC-037 | New birth can retask an older unit on its capture pad | **Open.** One-shot pulses prevent retasking between births, not while another birth occurs. This qualifies ASC-015/019/022/023 and historical claims of complete manual-order safety. Experimental per-unit tracking is not shipped without engine validation. | Return/park old army, Hero, and builder units on pads while new units spawn. |
| ASC-038 | Closest Heroes must be directly in front of Castles | All 64 L1 mappings target canonical `(21,54)`, on the Army HOLD line. Actual Castle footprints and bounded tile connectivity checked for all eight orientations. OFF and L2–L5 unchanged. | First Penguin ON position at every tier, all eight colors; confirm units gather just in front of their own Castles. |

The 50-second Scorpion reward cleanup is intentional and unchanged. Both ordinary
Scorpion training types were already disabled. The detailed audit record is in
[`RELEASE_NOTES_v1.0.16.md`](../modes/evolution_alpha/RELEASE_NOTES_v1.0.16.md).

## v1.0.17 source review additions

Reported from a live 1 v 4 game: one player destroyed every enemy Castle and every
reachable building, and the match never ended. The review that followed found the
victory path had three independent ways to become unreachable, plus roster and
maintenance defects around it. All are fixed in v1.0.17; the detailed record is in
[`RELEASE_NOTES_v1.0.17.md`](../modes/evolution_alpha/RELEASE_NOTES_v1.0.17.md).

| ID | Finding | Source status and verification | Required game check |
| --- | --- | --- | --- |
| ASC-039 | A match can deadlock with one side visibly wiped out | Fixed. Victory is gated on `p#coloractive`, which XS clears only from `p#coloreliminated`, and elimination had a single reachable path: the one-shot `castle (p#)` chain of four `Destroy Object` conditions. A Castle that leaves the map by `Remove Object`, a purge, or engine slot cleanup can never satisfy that condition, so the colour stayed alive and un-eliminable forever. `Color Defeat Resolve` now ships enabled and fires from its own Castle-row condition, and eight `Color Castle Row Empty S#` triggers clear the gate from map state alone. Two liveness tests walk the serialized subsystem as a state machine over six lobby shapes × closed slots cleaned/left × both sides, plus a split player identity; both fail on the pre-fix build. | Replay the reported 1 v 4. After the last enemy Castle falls the match must end within about five seconds. Repeat with a resignation and with a closed slot on the losing side. |
| ASC-040 | Elimination and aliveness came from two different identity domains | Fixed. `p#worldplayer` is latched in the trigger-player domain; `p#coloractive` is written by `xsGetWorldPlayerId` in the lobby-slot domain. When those disagree, none of a colour's eight owner-resolved resolvers can match while it reads alive. The row-empty fallback needs neither latch. XS additionally latches elimination once a colour that was seen in game leaves it. | Shuffled and sparse lobbies: eliminate a colour whose lobby slot number differs from its scenario colour and confirm the match still resolves. |
| ASC-041 | `p#coloractive` had two writers with different semantics | Fixed. XS is now the sole writer; every trigger path writes only `p#coloreliminated`. It previously worked by convention — a trigger clearing the active bit without also setting elimination was reverted within one second — and a regression now rejects any trigger effect targeting that block. | None; structural. |
| ASC-042 | Seven civilizations could hand-train their own auto-spawned unique unit | Fixed. The Immortal, Companion Cavalry, Rhomphaia Warrior, Pattiyodha Longbowman, Temple Guard, Bolas Rider and Ibirapema Warrior were absent from the imported per-colour bans, so those civilizations could queue their unique unit for free on top of the automatic army. The ban is now derived from `CIV_SPAWN_RULES` and covers Elite/non-Elite and ranged/melee siblings; the roster grew from 143 to 159 units. | As each of the seven, open every military building and confirm the unique unit cannot be trained. |
| ASC-043 | Krepost and Donjon escaped the Castle ban | Fixed. `CASTLE` was banned, but the two civilization-specific castle-class fortifications were not, so Bulgarians and Sicilians could raise unlimited free fortresses — and the Donjon trains Serjeants. All three are banned together; the building roster grew from 14 to 16. Inherited id 621, which resolves to no building in the pinned dataset, is deliberately left in place: removing a ban is a live gameplay change and a ban on an absent id is inert. | As Bulgarians and Sicilians, confirm neither Krepost nor Donjon is buildable and no other fortification changed. |
| ASC-044 | XS wrote a trigger-variable block through a bare literal base | Fixed. `cbaQueueColorBuilders` read the pending-builder variable through the interpolated base and wrote it through `scenarioPlayer - 1`; the two agreed only because that base is zero. A regression now requires every XS trigger-variable access to address a named base. | None; structural. |
| ASC-045 | 64-way victory fan-out stayed live for the whole match | Improved. `Color Team Victory` ships disabled and is armed by the single owner detector whose latch it can match, so 56 of the 64 leave the tick loop at start-up. Initially enabled triggers are unchanged at 3,195 because the 64 defeat resolvers became enabled in the same change. | None; structural. |
| ASC-046 | Imported Portuguese trigger names and a stale README | Fixed. The three hero-order template triggers are named in English in the `scenario/` source, so the build no longer keys on the imported scenario's display language. The mode README tracked v1.0.15 while `mode.toml` and the docs were on v1.0.16; a regression now asserts the README title matches `mode.toml`. | None; structural. |

## v1.0.18 — remaining objects after defeat

GitHub had one new commit after our last change: Adomas's `eb9a077` (September 5),
which was pulled by fast-forward before this patch. Its other fixes are preserved.

| ID | Finding | Source status and verification | Required game check |
| --- | --- | --- | --- |
| ASC-047 | Some defeated players keep buildings/items after losing their Castles | Corrected. Fallback/XS elimination could clear active before the active-gated purge. Persistent occupancy now keeps the resolver eligible. All defeat/resignation/vote paths share an owner-only purge with no area/type/class/state/count filter, preceded by enabling deletion. There are 64 timed cleanup retries and 64 owner-empty confirmations; victory also requires every opposing color clean. The new object-state regression fails on the pulled v1.0.17 artifact and verifies residue is gone before a winner is declared. | Leave University, walls/gates, towers, foundations, controllers and garrisoned units; lose all Castles, resign, or vote-kick. Repeat all colors, shuffled/sparse lobbies and final-opponent elimination. Every defeated-owned object must disappear; surviving players and Gaia remain. |
| ASC-048 | A creation pass can run after elimination but before XS clears active | Corrected. Color-gated trigger producers additionally require eliminated=0. XS Castle spawning and builder queuing also return immediately on elimination. Existing routes, spawn positions and rewards are unchanged. | Lose the last Castle as a Hero, builder pair or normal wave is due. No late reward should leave new defeated-owned units. |

The eight occupancy variables (121–128) persist after defeat. The eight cleaned
variables (129–136) start true for unused slots, reset on first participation, and
become true only on owner-empty confirmation. No trigger-owner number is passed to
an XS player API. See
[`RELEASE_NOTES_v1.0.18.md`](../modes/evolution_alpha/RELEASE_NOTES_v1.0.18.md).

## ASC-049 — two explicitly closed slots hide P7/P8 from runtime systems

**Live failure confirmed in v1.0.18 and v1.0.19. Code correction in v1.0.20;
native acceptance not yet observed.** The user played P1/P3 against P5/P6/P7/P8,
explicitly closing lobby slots before starting. P7/P8 had blank custom score rows,
retained buildings after Castle loss, and prevented victory. Read-only replay
inspection confirms the current v1.0.19 match and compacted Gray/Orange world
players 5/6; it does not establish native XS return values.

v1.0.20 moves participation and HUD reads to native owner-resolved triggers.
The active bit is derived from persistent occupancy and elimination, without XS
identity lookup. A reserved-resource token separately translates owners into XS
indices for spawning and builder rewards. Cleanup and victory no longer require
this token. The former converter and Castle-reference paths, including debug chat,
are removed. Tests begin with zero participation instead of supplying the answer.
See [v1.0.20 release notes](../modes/evolution_alpha/RELEASE_NOTES_v1.0.20.md) and
[recording evidence](ascendants-closed-slot-investigation.md).

## Additional parser findings (v1.0.18 historical snapshot)

The v1.0.18 serialized candidate passes the strict structural audit with **0 errors and
0 warnings**, with:

- 3,783 uniquely named, non-empty triggers and a complete display order;
- 3,323 initially enabled triggers and 3,774 conservatively reachable triggers;
- 16,873 conditions and 15,136 effects;
- 956 unique object references, all on-map, with no dangling garrisons;
- 137 unique variable ids and no dangling variable use;
- no dangling trigger or selected-object references;
- no partial, inverted, or out-of-bounds trigger geometry;
- no reachable looping trigger without a Timer condition;
- no reachable unconditional remove, kill, victory, or defeat trigger.

All 138 repository tests pass (78 Ascendants, 60 others). Repository Ruff checks and
the full 646-line embedded XS build pass. Readback comparison confirms every terrain
cell and all 956 placed objects, plus every roster restriction, are unchanged from v1.0.17. The installed
game scenario matches the SHA-256 above. None of these checks substitutes for the
engine acceptance matrix below.

The dedicated migration removed all prior audit debt. It deleted 810 proven imported
empty shells plus 32 retired Hay triggers,
merged 189 byte-identical age-up copies,
rewired 346 incoming activations, and retained/name-disambiguated the three non-identical P7 variants. Exact baseline counts
and reference-shape assertions make the migration fail closed if the imported graph
ever changes. v1.0.15 restores the wall-limit rule by resetting/reusing the 16 imported
warning/wipe shells and adding 112 owner-resolved mappings; the old activation chain
does not return.

Run the same audit after every build:

```bash
.venv/bin/pytest -q tests/test_evolution_alpha.py
.venv/bin/pytest -q --ignore=tests/test_evolution_alpha.py
aoe2modes audit "dist/CBA Hero Ascendants v1.0.20.aoe2scenario" --strict
```

The normal command fails only on structural errors; `--strict` also
fails if future warning-level hazards return.

## Engine acceptance matrix

AoE2ScenarioParser does not execute XS, multiplayer slot compaction, pathfinding,
score UI, or the victory scheduler. A release candidate is not finished until these
cases are recorded in-game.

| Case | Lobby | Must be observed |
| --- | --- | --- |
| Full initialization | P1–P4 vs P5–P8 | No early defeat; equal starts; all eight armies; complete walls and dry paths. |
| Shuffled full lobby | Red/Green reversed, Yellow before Green, then another nonnumeric order | Every Castle row creates its own color/civilization; its Sheep/Penguin controls, Heroes, HUD, rewards, resignation, and victory stay attached to that territory. |
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
| Sheep Castle slider | All eight colors, full and sparse | L0 parks each new wave Castle-ward; L1–L5 move progressively farther; existing armies keep manual orders. |
| Penguin Hero slider | All eight colors, full and sparse | L0 produces no Heroes; L1 gathers immediately in front of the Castles on the Army HOLD line; L2–L5 route progressively farther. Only the current kill tier produces; no stale-tier burst occurs after OFF. |
| Controller confinement | All eight colors | Orders across the Deep Water gap or beyond every track edge cannot leave the controller's own track; every level remains reachable without getting stuck at a Sign. |
| HOLD/OFF clarity | All eight colors | Every snowy track cell selects L0; the first road cell selects L1. The four endpoint Signs and two short controller names are readable and distinguish Castle HOLD from Hero production OFF. |
| Yard gate switch | All eight colors, full/sparse/shuffled | Deleting the side/rear switch removes the short shoulders and long side walls, but not the front gates/posts, University walls/gate, or teammate access gates. With other gates shut, no front-arena or University bypass opens. |
| Wall-limit warning/wipe | All eight colors, full/sparse/shuffled | At 200 owned WALL-class objects, warn once; at 220, wipe that owner's walls outside protected permanent barrier footprints. Include preplaced walls in the count. Front and University barriers, teammate access gates, and other owners' walls survive. Repeat after side-wall deletion. |
| Permanent wall safety | All eight colors, full/sparse/shuffled | Permanent walls/gates reject manual deletion; the switch remains deletable. Any legacy manual-delete protection on side walls must not prevent scripted side-wall removal. Defeat/resignation cleanup still removes all of the eliminated player's objects, including protected barriers. |
| Controller population | Any color near the hard cap | The Penguin occupies the reserved 251st slot; normal gameplay still reaches 250 slots and custom army/Hero ceilings behave as before. |
| Castle launch pads | All eight colors | All four waves appear at their exact pads and clear L0; no Hay Stack is created or displaces a unit. |
| Milestone shore | All eight colors | Buildings can be placed on the repaired strip; hero spawns and nearby water remain clear. |
| Marker removal | All eight colors | No Transport Ship is present; milestone heroes still spawn and route normally. |
| Corner cleanup | All four outer corners | No static Palisade Wall or Saboteur remains. |
| Goth Palisade removal | Goths after Elite Huskarl | Player-built Palisades receive no hidden scenario HP bonus; Anarchy/Barracks progression still works. |
| Defeat/resignation cleanup | All colors, full/sparse/shuffled | Leave buildings, foundations and garrisoned units. Lose all Castles, resign or vote-kick, including the last opponent. All defeated-owned objects disappear before victory; other owners and Gaia remain intact. |
| Anti-Trebuchet parity | All eight colors | An enemy packed Trebuchet beside any Castle row is removed, including P4/P6/P7/P8; no friendly rear-route unit is touched. |

For a failure, record the exact selected colors, runtime player numbers, civilizations,
game time, action, observed result, and expected result. That is enough to turn most
engine reports into a focused parser-backed regression test.
