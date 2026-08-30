# Ascendants development

`modes/evolution_alpha` builds **CBA Hero: Ascendants v1.0.3**. That release is the
reproducible starting point for ongoing fixes, not a claim that every gameplay issue
has been resolved.

The canonical v1.0.3 checkpoint is 99,694 bytes with SHA-256
`4082a73c9e9323cda5678a758518c12a5e387c3beafa20ce3835f40466fb8d34`. An intentional
gameplay fix is expected to change that hash; an unexplained change while reconstructing
the baseline is not.

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
review because those patterns can be intentional in legacy CBA trigger systems.

The target is entirely local. It does not use GitHub Actions or any paid CI service.

The active issue inventory and manual acceptance cases are in
[`ascendants-issue-register.md`](ascendants-issue-register.md). Older pre-1.0 builds are
historical input only; v1.0.3 is the sole comparison baseline.

## What the automated checks cannot prove

The parser and regression suite can prove scenario structure, but they do not run the
Age of Empires II engine. Keep these as explicit in-game checks for every candidate:

- full 4v4 and at least one sparse lobby with closed colors on both teams;
- automatic armies, builders, six hero milestones, and all five distance positions;
- vote-kick resolution, resignation/defeat, and team victory for both sides;
- local HUD values, player names, zero costs/resources, and post-game combat score;
- unit pathing through every allied route and around all eight rear walls.

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
7. Advance the public version and release notes only after gameplay validation.

The `evolution_alpha` id is retained for repository compatibility. User-facing names
and output filenames use **CBA Hero Ascendants**.
