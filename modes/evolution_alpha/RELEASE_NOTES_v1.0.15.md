# CBA Hero: Ascendants v1.0.15 candidate

v1.0.15 corrects the wall rules from v1.0.14: **side walls are removable, and the
wall-limit wipe is active; front and University barriers remain**. Sheep/Penguin
confinement, snowy HOLD/OFF endpoints, controller names, and all spawn logic are
unchanged.

## Player-facing changes

- Deleting the side/rear Castle-yard switch gate removes the short shoulders and
  long side walls for that color, not merely the short shoulders.
- The three front gates and their wall row remain. Two small end posts per color
  close the ends so the new side opening cannot bypass the front gates.
- The rear University wall, its access gate, joins, and teammate access gates remain.
  The University gate is not the wall-removal switch.
- The wall-limit rule warns once at **200 owned WALL-class objects** and wipes at
  **220**. The count includes owned preplaced walls, as the original rule did.
- The wipe removes that player's walls across the map except the protected permanent
  barrier footprints. It keeps front and University defenses, teammate access gates,
  and other players' walls intact. Player-built walls in protected footprint cells
  are also spared.

Permanent barriers reject manual deletion, while the side switch remains deletable.
Some side walls retain legacy manual-delete protection; this does not stop their
scripted removal by the switch or wall-limit wipe. These protections do not prevent
normal combat damage or full cleanup when an owner is defeated, resigns, or is
vote-kicked.

## Implementation

The canonical P3 removable mask combines the 22 short shoulder slots with the 30 long
side-wall positions `(x+0.5,47.5)` and `(x+0.5,60.5)` for integer x=24–38. Only
existing Stone/Fortified Wall references are selected. This gives 44 actual removals
for P1/P2/P7/P8 and 48 for P3/P4/P5/P6; teammate gates replacing shoulder slots
are untouched. All 64 `Wall Breach` color/owner mappings consume those exact lists.

The retained front row is x=39.5: gates at y=50,54,58; existing wall posts at
y=46.5,47.5,60.5,61.5; and new end posts at y=45.5,62.5. The rear University
boundary remains at x=14.5 with its gate at y=54 and its existing joins. All positions
use the same eight-way object-coordinate transform. No terrain changes are made.

The 16 imported warning/wipe shells are reset and reused for same-numbered owners;
112 additional triggers complete 64 `Wall Cap Warn S# W#` / `Wall Cap Wipe S# W#`
pairs. The old activation chain is removed. The rebuilt family retains the original
one-shot warning-then-wipe sequence and thresholds but resolves the owner from the
Castle row. Wipe effects select the resolved owner's WALL class through rectangles that
cover the map outside permanent barrier footprints. No protected cell occurs in a
wipe rectangle, and no ownership/recreation workaround is used.

The exact roles and coordinates are documented in
[`../../docs/ascendants-control-map.md`](../../docs/ascendants-control-map.md).

## Verification

Verified results:

- Ascendants-focused tests: 59 PASS;
- remaining repository tests: 60 PASS; 119/119 total across complementary runs;
- 3,647 triggers, 14,561 conditions, 15,183 effects, 956 units, and 121 contiguous
  variables (ids 0–120);
- 616 embedded XS lines, validated by the full build;
- strict structural audit: PASS, 0 errors / 0 warnings;
- repository Ruff and diff checks: PASS;
- artifact size: 152,537 bytes;
- SHA-256:
  `320c52ce11ad304645cea706a81362f1ed48198c623ef037dd255fda2c96b209`.

The test commands were:

```bash
.venv/bin/pytest -q tests/test_evolution_alpha.py
.venv/bin/pytest -q --ignore=tests/test_evolution_alpha.py
```

Regression coverage verifies exact side-wall targets for all eight colors,
permanent-defense identity and manual-delete protection, the full warning/wipe
ownership matrix and thresholds, and closed-gate reachability after side-wall
removal, including all eight breaches together. Each wipe's 49 disjoint rectangles
cover all 20,368 unprotected cells while excluding all 368 protected barrier cells.

Readback comparison confirms all terrain and 940 existing objects are unchanged;
exactly 16 front end posts are added. The map remains 10,188 land / 10,548 water
cells, with 103 closed-gate and 81 open-gate regions. Base areas remain 285 per color;
territories are 893/861 by orientation, 18 fewer after closing the front seams. The
existing 72 `mirror_x` mismatches are unchanged. The local Steam-profile scenario is
installed and its SHA-256 matches the artifact above.

DE engine acceptance remains required. In full, sparse, and shuffled lobbies, delete
each switch, verify both long side walls disappear, and try to path around both ends
of the retained front row and around the University gate with gates shut. Reach 200
then 220 owned WALL-class objects and verify the warning/wipe without damage to
permanent defenses or another player's walls. Repeat after opening the side walls.
Static parser checks do not execute engine pathfinding or multiplayer identity rules.
