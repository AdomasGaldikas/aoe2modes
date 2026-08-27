# CBA Hero Chieftains FFA 2026

Big_Ytri's Chieftains 2026, free-for-all, decompiled to Python. This is the current
tested-and-working published FFA (workshop id `469501`) — not original work, and not a
mode to tune casually.

Original author: **Big_Ytri**. Kept here so the published mod builds through the same
pipeline as everything else, and so variants can be diffed against a known-good copy.

## Shape

| | |
| --- | --- |
| Map | 144×144 |
| Players | 8, every player their own team |
| Triggers | 3151 (3555 conditions, 8529 effects) |
| Trigger variables | 0 |
| Units | 1059 |
| Terrain | 20736 tiles → 2132 run-length entries |
| Scenario version | v1.58 |

Every slot's diplomacy row is all-enemy, which is the only structural difference in the
player table — ages (Feudal), pop cap (250) and the 99999-of-everything starting
resources match the 4v4.

As in `big_ytri`, the trigger set is dominated by the **kill-threshold ladder**: 1651
triggers, 52% of the file, one `accumulate_attribute(UNITS_KILLED)` check per threshold
per player. The scenario declares **zero trigger variables**.

## Relationship to the 4v4

[`chieftains_4v4`](../chieftains_4v4/) (workshop id `469500`) is the team cut of the same
2026 release. A name-and-shape signature diff from the 4v4 to this file reports 53
removed and 20 added signatures:

- **Removed**: the `-- Vote Kick` section and its 24 `VoteKickP#-P#-P#` triggers, which
  only mean anything with teams, plus the team-scoped variants around them.
- **Added**: a slightly larger `..:: Chieftains ::..` block (52 triggers here vs 51) with
  the sections spelled `--- Mapuches ---`, `--- Muiscas ---`, `--- Tupi ---`, and
  per-player unit triggers such as `Tupi P#` and `Ibirapema P#`.

The two are kept as separate decompiles rather than one shared base plus a patch,
because the published mods are two separate files and diverge across 73 signatures;
making one a patch of the other would mean guessing at which differences are
intentional. If a future release makes the FFA a genuine derivative, converting it to
base+patch is the cheaper shape — see the flavours section in `CLAUDE.md`.

## Source of truth

`build.py` calls `generated.apply(ctx)` — everything the published mod contained lives
under `generated/`. `base.aoe2scenario` is kept only as `scenario.reference`, so the
rebuild can be checked against it:

```
aoe2modes verify chieftains_ffa
```

That compares 115,299 fields and must report `MATCH`, with **no version gap** — the
original is already v1.58, so both sides have the same field set.

## Editing

Small changes go in `build.py`, after `apply_generated(ctx)` — that runs last and
overrides anything. Structural changes go in `generated/`, but note that
`aoe2modes decompile --mode chieftains_ffa` overwrites those files.

Run `aoe2modes verify chieftains_ffa` after any change that should be
behaviour-preserving. If you are deliberately changing behaviour, expect `verify` to
fail and say so in the commit — that is the check working.

## Build

```
aoe2modes build chieftains_ffa --deploy
```
