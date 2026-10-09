# CBA Hero King Zalabatta Adrenaline Rush

Decompiled from `base.aoe2scenario` (v1.58, 8 players, 4v4, 11619 triggers) — a CBA
Hero variant with per-civilization, per-player "rush" trigger blocks granting bonus
techs/units for every civilization in the game.

Rebuild and verify it still matches the source:

```
aoe2modes build adrenaline_rush
aoe2modes verify adrenaline_rush
```

Structural changes go into `generated/` (overwritten by `aoe2modes decompile`);
small local tweaks go into `build.py` after `generated.apply(ctx)`.
