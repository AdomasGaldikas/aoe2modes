# CBA Hero: Ascendants v1.0.14 candidate

v1.0.14 confines the Sheep and Penguin to their own slider tracks, makes the
HOLD/OFF endpoints visible, and keeps gate-triggered wall removal away from permanent
defenses. Castle and Hero spawning rules are unchanged.

## Player-facing changes

- Each color has two separate two-tile-wide land tracks, divided by three tiles of
  Deep Water. Controllers cannot walk onto each other's line or leave their own
  selector area by ordinary land movement.
- The whole snowy rear pad is the endpoint: Sheep on Snow means **HOLD**; Penguin on
  Snow means **OFF**. The first road tile is the first active distance level.
- Each track has its own HOLD/OFF and FAR Signs. Signs are on the outside row, leaving
  the other row clear for movement.
- Short controller names are `Army range - snow = HOLD` and
  `Hero range - snow = OFF`.
- Deleting the side/rear Castle-yard switch gate removes only the short yard walls.
  Long flanks, front-gate end caps, and the University enclosure stay intact and
  cannot be manually deleted. The University gate is not the removal switch.
- The old 220-wall penalty no longer removes a player's walls across the whole map.

HOLD still produces Castle armies and parks new waves near their Castles. OFF pauses
new Heroes. Moving forward sends future spawns progressively farther into battle.
Existing units keep their orders. Both controllers still begin at level 3.

## Implementation

The canonical P3 Sheep track is x=1–9, y=60–61; the Penguin track is x=1–9,
y=65–66. The gap at y=62–64 is entirely Deep Water, without beach bridges. Each
track's level-0 pad is exactly x=1–3. All eight colors use the same coordinate
transform, with each controller reference selecting only its own six contiguous bands.

There is no recurring task, stop, freeze, or teleport correction. The existing
undeletable/untargetable protections, owner resolution, spawn pulses, Hero bands,
population compensation, destinations, and 121-variable layout remain unchanged.

The 64 owner-mapped wall-breach triggers now remove exact static object references
instead of broad area filters. Only the canonical yard shoulder mask is eligible:
14 actual wall objects for P1/P2/P7/P8, 18 for P3/P4/P5/P6. Permanent wall/gate
references receive wildcard and owner-resolved manual-delete protection. The 16
legacy warning/removal triggers for the 220-wall penalty and their activation chain
are retired. Defeat, resignation, and vote-kick cleanup remain unchanged.

## Verification

Verified results:

- Ascendants-focused tests: 57 PASS;
- full repository tests: 117 PASS;
- 3,519 triggers, 14,049 conditions, 11,855 effects, 940 units, and 121 contiguous
  variables (ids 0–120);
- 616 embedded XS lines, validated by the full build;
- strict structural audit: PASS, 0 errors / 0 warnings;
- repository Ruff check: PASS;
- artifact size: 133,107 bytes;
- SHA-256:
  `cbb122c1b6bad41f5472b039f669ebfaea7d5e9b17a05556cf868ea4ba8095ea`.

Regression coverage verifies all eight track layouts, the exact Snow/road level-0
boundary, each controller's reachable selector union, separation from the other track,
readable names/Signs, and the unchanged army/Hero routing invariants.
Wall checks pin exact targets and permanent-defense protections, reject broad
wall-removal effects, and prove the permitted deletion does not open a front-arena or
University bypass with other gates closed in any color orientation.
The destructive-effect audit also checks kill, damage, HP modification, replacement,
and ownership changes, not only removal effects. Independent serialized readback
confirms 484 protected permanent wall/gate references, 64 exact wall breaches, and
16 isolated controllers.

An independent before/after comparison confirms terrain outside the eight control
areas and all 816 unrelated original objects are unchanged. Playable base areas
remain 285 cells per color; territory figures remain 911/879 by orientation.
The new scenario is installed in the local Steam game profile; its installed SHA-256
matches the artifact above.

DE engine acceptance remains required: try off-track and cross-track movement on all
eight orientations, move each controller through every level, and check the visible
HOLD/OFF transition. Parser checks do not execute engine pathfinding.
Delete each side/rear switch gate, verify the retained defenses and closed-gate
boundaries, and confirm no whole-map wall purge occurs after exceeding 220 walls.
