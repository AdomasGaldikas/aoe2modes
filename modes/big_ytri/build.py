"""Big_Ytri Royal 4v4 — rebuilt from code rather than shipped as a binary.

Everything the original scenario contained now lives in ``generated/``: terrain,
units, players, lobby options and all 2993 triggers. ``aoe2modes verify big_ytri``
rebuilds it and diffs against ``base.aoe2scenario`` to prove the two still match.

One deliberate difference from the original: this builds as scenario **v1.58**, not
the v1.51 the source file used. The parser only ships blank templates for v1.57 and
v1.58, so a from-scratch rebuild cannot target v1.51. Content is unchanged; the game
upgrades a v1.51 file on first save anyway.

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
