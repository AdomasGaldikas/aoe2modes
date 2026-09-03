# Ascendants v1.0.13 control and ownership map

This is the authoritative manifest for the two spawn controls in CBA Hero:
Ascendants. Coordinates are scenario cells unless they include `.5`, which denotes an
object position. P1–P8 mean fixed scenario colors: Blue, Red, Green, Yellow, Teal,
Purple, Gray, and Orange.

## Identity boundary

| Use | Authoritative identity |
| --- | --- |
| Territory, Castle row, controllers, and color-local variables | Scenario color P1–P8 |
| Trigger conditions and effects | Castle-row-resolved player in variables 40–47 |
| XS civilization, statistics, active state, and army creation | `xsGetWorldPlayerId(scenarioPlayer)` |

The last two rows are deliberately separate. Variables 40–47 retain the historical
name `p#worldplayer`, but XS never reads them. This prevents a shuffled Green Castle,
for example, from creating a Red-owned army.

## Relevant variables

| Ids | Meaning |
| --- | --- |
| 32–39 | Color is occupied/active |
| 40–47 | Trigger-side runtime owner resolved from that Castle row |
| 48–55 | Color is eliminated |
| 81–88 | One-shot new Castle-wave pulse |
| 89–96 | Sheep-selected Castle-army level, 0–5 |
| 97–104 | One-shot new Hero pulse |
| 105–112 | One-shot new builder-pair pulse |
| 113–120 | Penguin-selected Hero level, 0–5 |

Both range variables initialize to level 3 for every occupied color.

## Eight-way coordinate transform

All control geometry is declared once in P3 Green's left-edge source frame. Transform
a source point `(x,y)` as follows; cell transforms use `143`, while `.5` object
positions use `144`.

| Color | Cell transform |
| --- | --- |
| P1 Blue | `(y,x)` |
| P2 Red | `(143-y,x)` |
| P3 Green | `(x,y)` |
| P4 Yellow | `(143-x,y)` |
| P5 Teal | `(x,143-y)` |
| P6 Purple | `(143-x,143-y)` |
| P7 Gray | `(y,143-x)` |
| P8 Orange | `(143-y,143-x)` |

This single transform is used for controller lanes, Castle rows, spawn pads, Hero pads,
and every destination. Tests independently apply the same geometric operation and
assert all eight serialized results.

## Controller islands

The canonical P3 island occupies `(1,60)–(9,66)`:

| Feature | Canonical geometry |
| --- | --- |
| Outer visual borders | x=1 and x=9, Beach |
| Sheep lane | y=60–62, Road |
| Separator | y=63, Grass 2 |
| Penguin lane | y=64–66, Road Gravel |
| Rear sign | `(2.5,63.5)`: `LEVEL 0: CASTLE HOLD / HERO OFF` |
| Forward sign | `(9.5,63.5)`: `LEVEL 5: FAR BATTLE ROUTE` |

The two controllers share six reference-specific detection bands. Each band spans the
full island height so accidentally crossing the visual separator cannot strand a
controller; because Sheep and Penguin references are distinct, this overlap cannot
mix their variables. The wider end bands also catch the beach caps:

| Level | Sheep rectangle | Penguin rectangle |
| ---: | --- | --- |
| 0 | `(1,60)–(3,66)` | `(1,60)–(3,66)` |
| 1 | `(4,60)–(4,66)` | `(4,60)–(4,66)` |
| 2 | `(5,60)–(5,66)` | `(5,60)–(5,66)` |
| 3 | `(6,60)–(6,66)` | `(6,60)–(6,66)` |
| 4 | `(7,60)–(7,66)` | `(7,60)–(7,66)` |
| 5 | `(8,60)–(9,66)` | `(8,60)–(9,66)` |

Within each controller family the bands are contiguous, mutually exclusive, dry, and
cover all 63 island cells. The island has a complete water moat and contains only its
Sheep, Penguin, and two endpoint Signs. It does not depend on collision with props.

## Controller starts

| Color | Sheep start (Castle armies) | Penguin start (Heroes) |
| --- | --- | --- |
| P1 Blue | `(61.5,6.5)` | `(65.5,6.5)` |
| P2 Red | `(82.5,6.5)` | `(78.5,6.5)` |
| P3 Green | `(6.5,61.5)` | `(6.5,65.5)` |
| P4 Yellow | `(137.5,61.5)` | `(137.5,65.5)` |
| P5 Teal | `(6.5,82.5)` | `(6.5,78.5)` |
| P6 Purple | `(137.5,82.5)` | `(137.5,78.5)` |
| P7 Gray | `(61.5,137.5)` | `(65.5,137.5)` |
| P8 Orange | `(82.5,137.5)` | `(78.5,137.5)` |

Each player owns exactly one Sheep and one War Penguin. Both are undeletable and
untargetable. Penguins additionally receive No Attack stance and an attack multiplier
of zero. Wildcard setup is backed by the exact Castle-row-resolved runtime owner, so
these protections and controller names survive sparse or shuffled lobby compaction.
No task, stop, freeze, kill, damage, replacement, ownership-change, or ordinary remove
effect selects either controller; full-map defeat, resignation, and vote-kick cleanup
remain intentionally able to remove an eliminated player's objects.

War Penguin is a military-class one-population object. The scenario hard cap is 251
so the controller does not take one of the intended 250 gameplay slots. XS subtracts
the one permanent Penguin from civilization army-cap checks, and Hero object-count
ceilings are raised by one for the same reason.

## Castle-wave creation and destinations

The canonical P3 Castle row is x=19 at y=48,52,56,60. Its four wave pads are
`(22,48)`, `(22,52)`, `(22,55)`, and `(22,59)`. All other colors use the transform
above. XS creates units at the centres of those cells—canonical
`(22.5,48.5)`, `(22.5,52.5)`, `(22.5,55.5)`, and `(22.5,59.5)`—and each route
captures only its exact creation cell. Level 0 therefore moves each new wave one tile
Castle-ward without allowing a later pulse to reclaim the held wave; levels 1–5 form
a monotonic route toward the central battle. The 32 old two-by-two Hay Stack creation
markers are removed because their footprints overlapped pads and L0 destinations.

| Level | Four canonical destinations, in pad order |
| ---: | --- |
| 0 | `(21,48)`, `(21,52)`, `(21,55)`, `(21,59)` |
| 1 | `(25,49)`, `(25,50)`, `(25,54)`, `(25,55)` |
| 2 | `(30,50)`, `(30,51)`, `(30,54)`, `(30,55)` |
| 3 | `(34,51)`, `(34,52)`, `(34,54)`, `(34,54)` |
| 4 | `(38,52)`, `(38,52)`, `(38,54)`, `(38,54)` |
| 5 | `(43,53)`, `(43,53)`, `(43,54)`, `(43,54)` |

There are 384 mappings: six levels × eight colors × eight possible runtime owners.
Each requires the exact active color, owner, Sheep level, and one-shot wave pulse. It
issues four Move effects and resets the pulse last.

## Hero creation and destinations

The canonical milestone Hero pad is `(16,38)`; the two additional late-Genghis pads
are `(15,38)` and `(17,38)`. The Hero mover watches the three-by-three area around the
middle pad, so one pulse routes whichever current tier has just spawned.

| Penguin level | Production | Canonical destination |
| ---: | --- | --- |
| 0 | OFF | none |
| 1 | ON | `(25,54)` |
| 2 | ON | `(30,52)` |
| 3 | ON | `(34,52)` |
| 4 | ON | `(38,53)` |
| 5 | ON | `(43,53)` |

There are 320 Hero movement mappings: five active levels × eight colors × eight
possible runtime owners. Each consumes one Hero pulse after issuing its Move order.

Hero spawning itself requires Penguin level 1 or greater and exactly one current kill
band: 200–399, 400–599, 600–799, 800–999, 1,000–1,999, 2,000–3,499,
3,500–4,999, or 5,000+. Thus level 0 pauses production, and re-enabling it cannot
activate stale lower tiers.

## Removed legacy controls

The built artifact contains none of the old five-point control furniture: 40 Relics,
40 Rugs, and 32 central selector Torches are removed. The old Short/Medium/Long and
Hero Open/Closed selector triggers are repurposed or retired. Hero OFF no longer uses
an Old Stone Head shoreline blocker; it gates Hero production directly.

## Release gate

Regression tests assert every rectangle, controller reference, variable, destination,
owner mapping, terrain cell, endpoint label, safety effect, Hero band, and pulse reset.
The strict scenario audit must remain at 0 errors and 0 warnings. Final acceptance must
still be performed in DE for all eight orientations and shuffled/sparse lobbies because
the parser cannot execute pathfinding or lobby-player mapping.
