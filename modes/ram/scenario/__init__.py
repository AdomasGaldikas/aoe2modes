"""Ascendants scenario source — hand-maintained Python, not a decompile.

``apply(ctx)`` lays down the whole scenario. The mode's build.py calls it and then
patches on top — build.py runs after this and wins.

This package began as `aoe2modes decompile` output, but Ascendants no longer
round-trips any binary. There is no `scenario.reference` and no reference layer to
verify against: **this code is the only source of truth**, and the .aoe2scenario in
`dist/` is its build product. Do not run `aoe2modes decompile --mode
evolution_alpha`; it would overwrite this source with a dump of a build output.

Stage order matters: the map is sized before terrain is painted, units are placed
before triggers reference them, and triggers are created in a fixed order because
``activate_trigger`` addresses them positionally.
"""

from __future__ import annotations

from . import setup, terrain, triggers, units

STAGES = (setup, terrain, units, triggers)


def apply(ctx) -> None:
    """Run every generated stage in order."""
    for stage in STAGES:
        ctx.log(f"generated: {stage.__name__.rsplit('.', 1)[-1]}")
        stage.apply(ctx)
