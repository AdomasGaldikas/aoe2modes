# Ascendants control and ownership map

This is the exact v1.0.12 control manifest for CBA Hero: Ascendants. Coordinates are
scenario cells unless shown with `.5`, which is an object position. Rectangle notation
is `(x1,y1)–(x2,y2)`, inclusive. P1–P8 always mean the scenario player/color:
Blue, Red, Green, Yellow, Teal, Purple, Gray, Orange.

## Identity boundary

| Use | Authoritative identity |
| --- | --- |
| Fixed territory, Castle row, Sheep, trigger variables | Scenario player/color P1–P8 |
| Trigger conditions and effects | Castle-row-resolved trigger selector in variables 40–47 |
| XS civilization, population, statistics, active state, and unit creation | `xsGetWorldPlayerId(scenarioPlayer)` |

The two right-hand rows are deliberately not interchangeable. Variables 40–47 keep
their historical serialized names `p#worldplayer`, but XS must never read them. This
split is what prevents a Green Castle from creating a Red-owned army when lobby rows
are shuffled.

Route values are color-local: Medium `0`, Short `1`, Long `2` in variables 89–96.
New normal waves arm variables 81–88; new milestone/late heroes arm 97–104. A matching
movement trigger consumes its pulse once, so returning units retain later player orders.

## Territory and creation points

| Color | Territory | Castle row | Sheep ref / start | Four normal-wave pads | Hero/blocker pad |
| --- | --- | --- | --- | --- | --- |
| P1 Blue | top-left | y=19; x=48,52,56,60 | 88891 / (63.5,4.5) | (48,22), (52,22), (55,22), (59,22) | (38,16) |
| P2 Red | top-right | y=19; x=84,88,92,96 | 88892 / (80.5,4.5) | (96,22), (92,22), (89,22), (85,22) | (105,16) |
| P3 Green | left-top | x=19; y=48,52,56,60 | 88893 / (4.5,63.5) | (22,48), (22,52), (22,55), (22,59) | (16,38) |
| P4 Yellow | right-top | x=125; y=48,52,56,60 | 88894 / (139.5,63.5) | (122,48), (122,52), (122,55), (122,59) | (127,38) |
| P5 Teal | left-bottom | x=19; y=84,88,92,96 | 88895 / (4.5,80.5) | (22,96), (22,92), (22,89), (22,85) | (16,105) |
| P6 Purple | right-bottom | x=125; y=84,88,92,96 | 88896 / (139.5,80.5) | (122,96), (122,92), (122,89), (122,85) | (127,105) |
| P7 Gray | bottom-left | y=125; x=48,52,56,60 | 88897 / (63.5,139.5) | (48,122), (52,122), (55,122), (59,122) | (38,127) |
| P8 Orange | bottom-right | y=125; x=84,88,92,96 | 88898 / (80.5,139.5) | (96,122), (92,122), (89,122), (85,122) | (105,127) |

## Five Sheep controls

Each row lists the visible marker position followed by the trigger rectangle reached
by the Sheep. The same Sheep reference is used by all five controls for that color.

| Color | Short | Medium | Long | Hero Open | Hero Closed |
| --- | --- | --- | --- | --- | --- |
| P1 | (61.5,1.5) / (60,1)–(62,3) | (63.5,1.5) / (63,1)–(63,3) | (65.5,1.5) / (64,1)–(66,3) | (61.5,7.5) / (60,4)–(62,8) | (65.5,7.5) / (64,4)–(66,8) |
| P2 | (82.5,1.5) / (81,1)–(83,3) | (80.5,1.5) / (80,1)–(80,3) | (78.5,1.5) / (77,1)–(79,3) | (82.5,7.5) / (81,4)–(83,8) | (78.5,7.5) / (77,4)–(79,8) |
| P3 | (1.5,61.5) / (1,60)–(3,62) | (1.5,63.5) / (1,63)–(3,63) | (1.5,65.5) / (1,64)–(3,66) | (7.5,61.5) / (4,60)–(8,62) | (7.5,65.5) / (4,64)–(8,66) |
| P4 | (142.5,61.5) / (140,60)–(142,62) | (142.5,63.5) / (140,63)–(142,63) | (142.5,65.5) / (140,64)–(142,66) | (136.5,61.5) / (135,60)–(139,62) | (136.5,65.5) / (135,64)–(139,66) |
| P5 | (1.5,82.5) / (1,81)–(3,83) | (1.5,80.5) / (1,80)–(3,80) | (1.5,78.5) / (1,77)–(3,79) | (7.5,82.5) / (4,81)–(8,83) | (7.5,78.5) / (4,77)–(8,79) |
| P6 | (142.5,82.5) / (140,81)–(142,83) | (142.5,80.5) / (140,80)–(142,80) | (142.5,78.5) / (140,77)–(142,79) | (136.5,82.5) / (135,81)–(139,83) | (136.5,78.5) / (135,77)–(139,79) |
| P7 | (61.5,142.5) / (60,140)–(62,142) | (63.5,142.5) / (63,140)–(63,142) | (65.5,142.5) / (64,140)–(66,142) | (61.5,136.5) / (60,135)–(62,139) | (65.5,136.5) / (64,135)–(66,139) |
| P8 | (82.5,142.5) / (81,140)–(83,142) | (80.5,142.5) / (80,140)–(80,142) | (78.5,142.5) / (77,140)–(79,142) | (82.5,136.5) / (81,135)–(83,139) | (78.5,136.5) / (77,135)–(79,139) |

Open removes the Gaia Old Stone Head at that color's hero pad. Closed creates exactly
one there, guarded by an absence condition. Open and Closed do not change the saved
Short/Medium/Long route.

## Route destinations

Normal destinations correspond in order to the four pads in the territory table.
Hero destinations are the single target used for every 200/400/600/800/1000/2000 and
3500/5000 hero created on that color's hero pad.

| Color | Normal Short | Normal Medium | Normal Long | Hero S / M / L |
| --- | --- | --- | --- | --- |
| P1 | (49,25),(50,25),(54,25),(55,25) | (53,31),(53,30),(53,30),(53,30) | (53,43),(53,43),(54,43),(54,43) | (54,25) / (52,31) / (53,43) |
| P2 | (94,25),(93,25),(89,25),(88,25) | (90,31),(90,30),(90,30),(90,30) | (90,43),(90,43),(89,43),(89,43) | (89,25) / (91,31) / (90,43) |
| P3 | (25,49),(25,50),(25,54),(25,55) | (31,53),(30,53),(30,53),(30,53) | (43,53),(43,53),(43,54),(43,54) | (25,54) / (31,52) / (43,53) |
| P4 | (118,49),(118,50),(118,54),(118,55) | (112,53),(113,53),(113,53),(113,53) | (100,53),(100,53),(100,54),(100,54) | (118,54) / (112,52) / (100,53) |
| P5 | (25,94),(25,93),(25,89),(25,88) | (31,90),(30,90),(30,90),(30,90) | (43,90),(43,90),(43,89),(43,89) | (25,89) / (31,91) / (43,90) |
| P6 | (118,94),(118,93),(118,89),(118,88) | (112,90),(113,90),(113,90),(113,90) | (100,90),(100,90),(100,89),(100,89) | (118,89) / (112,91) / (100,90) |
| P7 | (49,118),(50,118),(54,118),(55,118) | (53,112),(53,113),(53,113),(53,113) | (53,100),(53,100),(54,100),(54,100) | (54,118) / (52,112) / (53,100) |
| P8 | (94,118),(93,118),(89,118),(88,118) | (90,112),(90,113),(90,113),(90,113) | (90,100),(90,100),(89,100),(89,100) | (89,118) / (91,112) / (90,100) |

## Release gate for this graph

The regression suite checks all eight rows above, every trigger-owner candidate, an
explicit Red↔Green lobby swap, and a permutation in which all eight colors move to a
different lobby row. It also proves that Short/Medium/Long write the same route variable
read by normal waves and all hero tiers, and that every creation pad and destination is
in its own transformed territory. This is structural proof; the final acceptance step
is still an in-game shuffled-lobby run because AoE2ScenarioParser cannot execute DE.
