# Ascendants development

`modes/evolution_alpha` builds **CBA Hero: Ascendants v1.0.5** as the current
source-verified release candidate. It is derived only from v1.0.3; older versions are
not repair or comparison targets. Engine acceptance is still a separate step.

The canonical v1.0.3 checkpoint is 99,694 bytes with SHA-256
`4082a73c9e9323cda5678a758518c12a5e387c3beafa20ce3835f40466fb8d34`. The v1.0.5
candidate is 93,590 bytes with SHA-256
`b5182d2b123a389ca50a584ab341a5ea957246867b0528d44865b2079a3e3903`.
Its intentional trigger-graph migration and engine-reported fixes explain the changed hash.

## Two verification layers

Ascendants has two source layers:

1. `generated/` reconstructs the old v1.58 reference in `base.aoe2scenario`.
2. `build.py`, `v2_map.py`, and `free_costs.py` apply the Ascendants map and gameplay
   changes after the generated layer.

Because the public build intentionally differs from the reference, do not use a raw
`aoe2modes verify evolution_alpha` result as the release verdict. Verify both layers:

```bash
make check-ascendants
```

The target first proves that the parser can still round-trip the reference, including
trigger-variable ids. It then runs the final-build gameplay contract and produces the
scenario that should be tested in-game. Finally, `aoe2modes audit` checks the serialized
output for broken references, invalid coordinates, and immediate unconditional
victory/defeat. Potential scheduling or cleanup risks are reported as warnings for
review. The v1.0.5 candidate currently passes with **0 errors and 0 warnings**.

The target is entirely local. It does not use GitHub Actions or any paid CI service.

The active issue inventory and manual acceptance cases are in
[`ascendants-issue-register.md`](ascendants-issue-register.md). v1.0.3 is the sole
comparison baseline and v1.0.5 is the only active candidate.

## v1.0.5 engine-report fixes

Automatic army movement is now edge-triggered instead of area-polled. XS sets one
color-specific pulse only after creating a wave; exactly one active full- or
compact-owner route consumes it. The three-by-three launch capture area still handles
spawn collision, but it cannot take over units that later return toward their Castles.

The milestone shoreline has an exact twenty-cell source mask transformed into all
eight territories. Its 160 legacy Beach cells are now buildable Grass 2 without moving
water or the hero landing tile. Each Transport Ship marker is two tiles nearer the
matching shore and is a Gaia-owned, stopped, frozen, speed-zero, unselectable,
undeletable, untargetable, and unattackable prop, outside player and AI control.

## v1.0.4 graph migration

The final build now removes 810 conditionless/effectless imported shells. Before
removal it proves that their only 16 external references are no-op deactivations of
the retired `no wall` family, then strips those references. It also groups the legacy
kill-based age-up chains by every serialized field, merges 189 byte-identical copies,
and rewires all 346 incoming activations to 99 canonical triggers. Three non-identical
P7 parser variants are preserved and named explicitly.

The resulting file has 2,327 uniquely named non-empty triggers. The audit is clean,
the victory model exhausts all 6,560 occupied/alive color states, and a bounded map
flood-fill proves that every rear interior can reach its University and Blacksmith
without crossing water, walls, towers, Castles, or cliffs.

## What the automated checks cannot prove

The parser and regression suite can prove scenario structure, but they do not run the
Age of Empires II engine. Keep these as explicit in-game checks for every candidate:

- full 4v4 and at least one sparse lobby with closed colors on both teams;
- automatic armies, builders, six hero milestones, and all five distance positions;
- vote-kick resolution, resignation/defeat, and team victory for both sides;
- local HUD values, player names, zero costs/resources, and post-game combat score;
- unit pathing through every allied route and around all eight rear walls;
- manually returning an army across each Castle launch line without its order changing;
- placing buildings across every milestone-shore repair strip;
- leaving all eight marker ships under AI play and confirming they neither move nor take damage.

When one fails, record the exact lobby colors, civilization, trigger-visible symptom,
and expected result before changing code. That turns an engine-only report into a
focused regression test wherever the scenario format exposes enough evidence.

Ascendants already carries explicit army and builder mappings for civilization ids
1–59, including the later DLC blocks recovered from this repository's newer
Chieftains scenarios. New civilization support must add both mappings and a regression
test; never guess a spawn unit, population cap, interval, or builder threshold.

## Fixing an issue

1. Reproduce the issue in a focused test in `tests/test_evolution_alpha.py`.
2. Locate the responsible final-build code in `build.py` or `v2_map.py`; avoid editing
   `generated/` for an Ascendants-specific behavior.
3. Make one small correction and run the focused test.
4. Run both verification layers and build the scenario.
5. Use `aoe2modes inspect` or `aoe2modes diff` when the change affects trigger shape,
   object placement, terrain, or variables.
6. Run `aoe2modes audit` on the built scenario. Treat an error as a blocker; review
   warnings in context because decompiled legacy triggers may intentionally reuse names.
7. Version source-changing candidates independently; mark one publishable only after
   the engine acceptance matrix passes.

The `evolution_alpha` id is retained for repository compatibility. User-facing names
and output filenames use **CBA Hero Ascendants**.
