# CBA Hero Royal 4v4 (Big_Ytri baseline)

Big_Ytri's Royal 4v4, decompiled to Python. This is the reference point every Reforged
variant patches from — not original work, and not a mode to tune casually.

Original author: **Big_Ytri**. Kept here so the baseline builds through the same
pipeline as everything else, and so variants can be diffed against a known-good copy.

## Shape

| | |
| --- | --- |
| Map | 144×144 |
| Players | 8, two teams of four |
| Triggers | 2993 (3314 conditions, 7814 effects) |
| Units | 1123 |
| Terrain | 20736 tiles → 2132 run-length entries |

The trigger set is dominated by a handful of hand-copied families. The largest is a
**kill-counter ladder** — 1140 triggers, or 38% of the file: one
`accumulate_attribute(UNITS_KILLED, quantity=K)` per threshold per player, for 147
thresholds from 10 to 5000, each announcing the count and renaming the player's hero.
The scenario declares **zero trigger variables**, so all of that state is carried by
triggers alone.

## Source of truth

`build.py` calls `generated.apply(ctx)` — everything the original contained lives
under `generated/`. `base.aoe2scenario` is kept only as `scenario.reference`, so the
rebuild can be checked against it:

```
aoe2modes verify big_ytri
```

That compares 100,856 fields and must report `MATCH`. It also lists ~9400 field slots
that exist on only one side; those are the v1.55+ additions the v1.51 original never
had (`execute_on_load`, `caption_string`, `max_units_affected`, `disable_sound`), not
content differences.

## Version note

The original is scenario **v1.51**; this builds as **v1.58**. AoE2ScenarioParser only
ships blank templates for v1.57 and v1.58, so a from-scratch rebuild cannot target
v1.51. Content is unchanged, and the game upgrades a v1.51 file on first save anyway.

## Editing

Small changes go in `build.py`, after `apply_generated(ctx)` — that runs last and
overrides anything. Structural changes go in `generated/`, but note that
`aoe2modes decompile --mode big_ytri` overwrites those files.

Run `aoe2modes verify big_ytri` after any change that should be behaviour-preserving.
If you are deliberately changing behaviour, expect `verify` to fail and say so in the
commit — that is the check working.

## Build

```
aoe2modes build big_ytri --deploy
```
