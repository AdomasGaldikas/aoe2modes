"""CBA Hero Chieftains FFA 2026 — rebuilt from code rather than shipped as a binary.

Everything the published mod contained now lives in ``generated/``: terrain, units,
players, lobby options and all 3151 triggers. ``aoe2modes verify chieftains_ffa``
rebuilds it and diffs against ``base.aoe2scenario`` to prove the two still match.

Unlike ``big_ytri``, the source is already scenario v1.58, so the rebuild targets the
same version the original used — there is no version gap for ``verify`` to bucket.

This is the free-for-all cut of ``chieftains_4v4``: the same arena and hero roster
with an all-enemy diplomacy table and the team-based vote-kick triggers dropped. The
two are kept as separate decompiles rather than a shared base, because the published
mods are separate files and diverge across 73 trigger signatures.

Edit in one of two places:

- **Small, local changes** go here, after ``generated.apply(ctx)``. This code runs
  last and wins, so retuning a value or renaming a trigger needs no regeneration.
- **Structural changes** go into ``generated/``. Those files are overwritten by
  ``aoe2modes decompile``, so once you start editing them, stop regenerating —
  or move the change up here.
"""

from __future__ import annotations

from aoe2modes.context import BuildContext

from .generated import apply as apply_generated


def build(ctx: BuildContext) -> None:
    apply_generated(ctx)

    ctx.log(
        f"rebuilt from source — {len(ctx.tm.triggers)} triggers, "
        f"{sum(len(units) for units in ctx.um.units)} units"
    )

    # --- mode changes go below this line -------------------------------------------
