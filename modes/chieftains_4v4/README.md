# CBA Hero Chieftains 4v4 2026

Big_Ytri's Chieftains 2026, teams of four, decompiled to Python. This is the current
tested-and-working published 4v4 (workshop id `469500`) — not original work, and not a
mode to tune casually.

Original author: **Big_Ytri**. Kept here so the published mod builds through the same
pipeline as everything else, and so variants can be diffed against a known-good copy.

## Shape

| | |
| --- | --- |
| Map | 144×144 |
| Players | 8, two teams of four |
| Triggers | 3184 (3603 conditions, 8577 effects) |
| Trigger variables | 0 |
| Units | 1171 |
| Terrain | 20736 tiles → 2206 run-length entries |
| Scenario version | v1.58 |

Like `big_ytri`, the trigger set is dominated by the **kill-threshold ladder**: 1651
triggers, 51% of the file, each one an `accumulate_attribute(UNITS_KILLED)` check for a
single threshold and a single player, announcing the count and renaming that player's
hero. The scenario declares **zero trigger variables**, so all of that state is carried
by triggers alone. `evolution_alpha` is the variant that replaces this with 16
`kills_p*`/`deaths_p*` variables.

## What Chieftains adds over `big_ytri`

Against [`big_ytri`](../big_ytri/) (2993 triggers), a name-and-shape signature diff
reports 52 removed and 243 added signatures. The headline additions are the
**Chieftains DLC civ block** — 51 triggers under `...:: Chieftains DLC ::...`, split
into `--- Mapuche ---`, `-- Muiscas ---` and `--- Tupis ---` — alongside sections for
the Greece and Three Kingdoms DLCs and a 24-trigger `VoteKickP#-P#-P#` family.

## The FFA sibling

[`chieftains_ffa`](../chieftains_ffa/) (workshop id `469501`) is the free-for-all cut of
this file: same arena and roster, all-enemy diplomacy, and the team-based vote-kick
removed. A signature diff between the two reports 53 removed and 20 added — almost all
of it the vote-kick family. They are kept as two separate decompiles rather than one
shared base plus a patch, because the published mods are two separate files and
diverge across 73 signatures; making one a patch of the other would mean guessing at
which differences are intentional.

## Source of truth

`build.py` calls `generated.apply(ctx)` — everything the published mod contained lives
under `generated/`. `base.aoe2scenario` is kept only as `scenario.reference`, so the
rebuild can be checked against it:

```
aoe2modes verify chieftains_4v4
```

That compares 117,824 fields and must report `MATCH`, with **no version gap** — the
original is already v1.58, so both sides have the same field set.

## Editing

Small changes go in `build.py`, after `apply_generated(ctx)` — that runs last and
overrides anything. Structural changes go in `generated/`, but note that
`aoe2modes decompile --mode chieftains_4v4` overwrites those files.

Run `aoe2modes verify chieftains_4v4` after any change that should be
behaviour-preserving. If you are deliberately changing behaviour, expect `verify` to
fail and say so in the commit — that is the check working.

## Build

```
aoe2modes build chieftains_4v4 --deploy
```
