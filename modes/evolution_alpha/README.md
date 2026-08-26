# CBA Hero Reforged — Evolution Alpha

The first improved variant of [`big_ytri`](../big_ytri/), decompiled to Python. Same
144×144 arena, roughly a third fewer triggers.

Original authors: **Big_Ytri** (baseline), Reforged (compaction pass).

## Shape

| | big_ytri | evolution_alpha |
| --- | --- | --- |
| Triggers | 2993 | 1988 |
| Conditions | 3314 | 2434 |
| Effects | 7814 | 6311 |
| Units | 1123 | 1171 |
| Terrain runs | 2132 | 2576 |
| Scenario version | v1.51 | v1.58 |

## What changed from the baseline

Compared at template level — trigger name and effect shape with the player number and
the threshold factored out — the two share 220 templates. 47 exist only in the
baseline (1293 triggers, mostly the trimmed kill ladder) and 53 only here (288
triggers).

The additions are the interesting half: `VoteKickP#-P#-P#`, `feudal ups (p#)`, and
per-player hero triggers (`Espartano`, `Hippeus`, `Kitans`).

A plain `aoe2modes diff` between the two base files is much noisier — it reports 1377
removed and 372 added signatures, because the author tag in the trigger names changed
from `By: Milhao` to `By: System` across hundreds of triggers and a name-based
signature counts every one of those as a remove plus an add.

## Source of truth

`build.py` calls `generated.apply(ctx)`; everything lives under `generated/`.
`base.aoe2scenario` is kept only as `scenario.reference`:

```
aoe2modes verify evolution_alpha
```

That compares 81,053 fields and must report `MATCH`, with no version gap — the
original is already v1.58, so both sides have the same field set. This mode is
therefore also the fidelity test for the decompiler itself
(`tests/test_decompile.py`), since it needs no cross-version handling.

## Editing

Small changes go in `build.py`, after `apply_generated(ctx)` — that runs last and
overrides anything. Structural changes go in `generated/`, but
`aoe2modes decompile --mode evolution_alpha` overwrites those files.

## Build

```
aoe2modes build evolution_alpha --deploy
```
