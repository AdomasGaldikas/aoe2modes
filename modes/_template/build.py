"""Template mode — the smallest thing that builds.

``build(ctx)`` runs after mode.toml has already been applied, so the map is sized and
terraformed and the players are configured. Everything here is additive.
"""

from __future__ import annotations

from AoE2ScenarioParser.datasets.players import PlayerId

from aoe2modes.context import BuildContext
from aoe2modes.lib import triggers


def build(ctx: BuildContext) -> None:
    centre = ctx.map_size // 2

    triggers.objective(ctx.tm, "Objective", "Replace this with your mode's goal.", order=0)

    start = triggers.on_start(ctx.tm, "Welcome")
    triggers.announce(start, f"{ctx.spec.name} v{ctx.spec.version}", seconds=6)

    for player in ctx.players.ids:
        ctx.um.add_unit(player=PlayerId(player), unit_const=4, x=centre + int(player), y=centre)
