# CBA Hero: Ascendants v1.0.8 candidate

> Superseded by v1.0.11. The 64 trigger-side candidates introduced here are valid for
> trigger player fields, but the candidate incorrectly reused that value in XS. Its 8!
> Python enumeration did not model the engine boundary and must not be treated as
> shuffled-lobby acceptance.

This candidate fixes Castle-territory ownership for arbitrary lobby color order.

- Removes the invalid assumption that a color can only map to an equal-or-lower
  runtime player number. Every mapped gameplay family now covers all 64
  color/runtime candidates.
- Explicitly covers the reported Green at runtime P4 and Yellow at runtime P3
  reversal. Castle-row detection still activates only the real owner for each color.
- Derives all 32 army wave pads from one canonical P3 row through the continuous
  V2 position transforms instead of maintaining eight independent coordinate rows.
- Adds build and regression guards proving that every pad is unique, dry, empty,
  closest to its own four Castles, watched by its movement effects, and serialized
  into the matching XS color branch.
- Moves all 32 Hay Stack markers one cell toward their referenced Castle. The old
  geometry put P4's and P7's four markers directly on their wave pads.
- Exercises all 8! full-lobby color orders and reversed victory ownership, plus
  verifies every army, hero, builder, upgrade, HUD, vote, defeat, resignation, and
  reward family has all 64 runtime-owner candidates.
- Produces 3,383 uniquely named non-empty triggers, 1,076 objects, 11,384
  conditions, 9,975 effects, and 97 variables.
- Passes the parser structural audit in strict mode with 0 errors and 0 warnings.

File size: 120,284 bytes

SHA-256:
`e9c8760f9078903045deb82c2f5f8f70d26f5598a7ae38dc0cef187e74eef3af`

Definitive Edition multiplayer, pathfinding, and UI acceptance still require an
in-game check. The first priority is a full lobby with Yellow listed before Green.
