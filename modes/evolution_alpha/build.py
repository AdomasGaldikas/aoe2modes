"""Evolution Alpha — rebuilt from code rather than shipped as a binary.

Everything the original scenario contained now lives in ``generated/``: terrain,
units, players, lobby options and all 1988 triggers. ``aoe2modes verify
evolution_alpha`` rebuilds it and diffs against ``base.aoe2scenario`` to prove the
two still match.

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
