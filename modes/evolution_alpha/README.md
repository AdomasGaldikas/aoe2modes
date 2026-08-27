# CBA Hero Reforged — Evolution Alpha

The AI-improved variant of [`big_ytri`](../big_ytri/), decompiled to Python. Same
144×144 arena, a third fewer triggers, and the kill/death bookkeeping moved off the
trigger ladder and onto real trigger variables.

Original authors: **Big_Ytri** (baseline), Reforged (improvement passes).

Tracking source: `CBA Hero Reforged Evolution Alpha v0.12.0.aoe2scenario`. When a newer
alpha lands, replace `base.aoe2scenario`, re-run `aoe2modes decompile --mode
evolution_alpha`, and bump `mode.version`.

## Shape

| | big_ytri | evolution_alpha v0.12.0 |
| --- | --- | --- |
| Triggers | 2993 | 2029 |
| Conditions | 3314 | 2481 |
| Effects | 7814 | 7203 |
| Trigger variables | 0 | 16 |
| Kill-threshold triggers | 1651 (55%) | 404 (19%) |
| Units | 1123 | 1311 |
| Terrain runs | 2132 | 2576 |
| Scenario version | v1.51 | v1.58 |

## What changed from the baseline

The interesting half is the **variable-backed K/D overlay**, which is what buys the
trigger reduction. 16 variables — `kills_p1`/`deaths_p1` … `kills_p8`/`deaths_p8`, ids
1–16 — are fed by a looping `K/D Update P#` trigger per player using
`modify_variable_by_resource` on the kills and losses tallies, and rendered by a
`K/D Row P#` trigger whose objective text is `P#  K: <Variable n>   D: <Variable n+1>`.
`Occupied Slot P#` gates each pair on the slot actually being taken, so an 8-player
overlay collapses cleanly in a smaller lobby. That is 404 kill-threshold triggers where
the baseline needed 1651.

The other structural change is economic: the baseline's `resources (p#)` / `res (p#)`
grants are gone, replaced by **`Free Costs P#`** — one 115-effect trigger per player
that zeroes the resource pools and rewrites unit costs directly with
`change_object_cost`. This is why `[players.resources]` is absent from `mode.toml`: the
players genuinely start on nothing.

### Since the previous alpha in this repo

Against the alpha that was here before (1988 triggers), a name-and-shape signature diff
reports 1923 unchanged, 65 removed and 106 added signatures — the `Free Costs P#`
family and the K/D variable machinery arriving, the old `resources`/`res` grants
leaving, and `castle (p#)` picking up a fifth effect.

A plain `aoe2modes diff` against `big_ytri`'s base file is much noisier than the counts
above suggest, because the author tag in the trigger names changed from `By: Milhao` to
`By: System` across hundreds of triggers and a name-based signature counts every one of
those as a remove plus an add.

## Variable ids collide with `lib/variables`

`lib/variables.SHARED` hands out ids 0–2 for the XS bridge (`wave`, `wave_size`,
`match_seconds`), and this mode occupies 1–16. They do not clash today because
`build.py` never calls `variables.declare`. If you add XS to this mode, allocate its
ids above 16 rather than reusing the shared block — `add_variable` raises on a
duplicate id, so the build will tell you, but only after you have written the XS side.

## Source of truth

`build.py` calls `generated.apply(ctx)`; everything lives under `generated/`.
`base.aoe2scenario` is kept only as `scenario.reference`:

```
aoe2modes verify evolution_alpha
```

That compares 89,977 fields and must report `MATCH`, with no version gap — the original
is already v1.58, so both sides have the same field set. This mode is therefore also the
fidelity test for the decompiler itself (`tests/test_decompile.py`), since it needs no
cross-version handling.

## Editing

Small changes go in `build.py`, after `apply_generated(ctx)` — that runs last and
overrides anything. Structural changes go in `generated/`, but
`aoe2modes decompile --mode evolution_alpha` overwrites those files.

## Build

```
aoe2modes build evolution_alpha --deploy
```
