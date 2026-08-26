"""CBA Hero Duel — the 1v1 cut of CBA Hero.

Deliberately built from the same library as ``cba_hero`` to show what sharing looks
like: the arena geometry, hero pool, wave spawner and loss condition are all reused,
and only the pacing and the win condition differ.

Differences from the 4v4:

* One hero each, top tier from the start — no upgrade ladder to climb.
* Waves are smaller and faster, and stop entirely at the sudden-death wave.
* Both players pick from a two-line pool so the matchup stays legible.
"""

from __future__ import annotations

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import (
    AttackStance,
    Comparison,
    DamageClass,
    ObjectAttribute,
    Operation,
)
from AoE2ScenarioParser.datasets.units import UnitInfo

from aoe2modes.context import BuildContext
from aoe2modes.lib import heroes, players, spawns, terrain, triggers, variables

WAVE_INTERVAL = 12
WAVE_SIZE_BASE = 3
WAVE_SIZE_CAP = 10
SUDDEN_DEATH_WAVE = 20

WAVE_COMPOSITION = (UnitInfo.MILITIA.ID, UnitInfo.SKIRMISHER.ID)

#: A duel reads better with a clear matchup, so the pool is narrowed to two archetypes.
DUEL_POOL = heroes.HeroPool((
    heroes.CLASSIC_LINES["paladin"],
    heroes.CLASSIC_LINES["huskarl"],
))


def build(ctx: BuildContext) -> None:
    size = ctx.map_size
    bases = spawns.lane_bases(ctx.players, size, margin=14, castle_offset=5, spawn_offset=8)

    centre = size // 2
    terrain.disc(ctx.mm, centre, centre, int(size * 0.40), TerrainId.GRASS_2, elevation=1)
    terrain.border(ctx.mm, 4, TerrainId.WATER_DEEP)

    variables.declare(ctx.tm)
    ctx.set_xs_vars(
        WAVE_INTERVAL=WAVE_INTERVAL,
        WAVE_SIZE_BASE=WAVE_SIZE_BASE,
        WAVE_SIZE_CAP=WAVE_SIZE_CAP,
        SUDDEN_DEATH_WAVE=SUDDEN_DEATH_WAVE,
    )

    triggers.objective(ctx.tm, "Goal", "Raze your opponent's castle.", order=0)
    triggers.objective(
        ctx.tm, "Sudden death", f"Reinforcements stop at wave {SUDDEN_DEATH_WAVE}.", order=1
    )

    start = triggers.on_start(ctx.tm, "Duel setup")
    triggers.announce(start, "CBA Hero Duel — one hero, one castle.", seconds=8)

    for base in bases.values():
        line = DUEL_POOL.for_player(base.player)
        _place(ctx, base, line)
        heroes.make_heroic(start, base.player, line.top)
        triggers.set_stance(start, base.player, AttackStance.AGGRESSIVE_STANCE)

        _waves(ctx, base)
        _scaling(ctx, base, line)
        triggers.defeat_when_object_destroyed(
            ctx.tm,
            base.player,
            BuildingInfo.CASTLE.ID,
            name=f"Defeat — P{int(base.player)}",
        )


def _place(ctx: BuildContext, base: spawns.Base, line: heroes.HeroLine) -> None:
    ctx.um.add_unit(
        player=base.player,
        unit_const=BuildingInfo.CASTLE.ID,
        x=base.castle.x + 0.5,
        y=base.castle.y + 0.5,
    )
    ctx.um.add_unit(
        player=base.player,
        unit_const=line.top.ID,
        x=base.center.x + 0.5,
        y=base.center.y + 0.5,
    )
    players.set_camera(ctx.pm, base.player, base.center.x, base.center.y)


def _waves(ctx: BuildContext, base: spawns.Base) -> None:
    trigger = triggers.every(ctx.tm, f"Wave — P{int(base.player)}", WAVE_INTERVAL)
    # Stop feeding chaff once sudden death starts; the XS rule announces the switch.
    trigger.new_condition.variable_value(
        variable=variables.WAVE,
        quantity=SUDDEN_DEATH_WAVE,
        comparison=Comparison.LESS,
    )
    tiles = spawns.block(base.spawn, columns=3, rows=4, map_size=ctx.map_size)
    triggers.spawn_units(trigger, base.player, WAVE_COMPOSITION, tiles[:WAVE_SIZE_BASE])
    triggers.attack_move_all(trigger, base.player, base.target)


def _scaling(ctx: BuildContext, base: spawns.Base, line: heroes.HeroLine) -> None:
    """No tier ladder here — the single hero just gets steadily tougher."""
    buff = triggers.every(ctx.tm, f"Hero scaling — P{int(base.player)}", WAVE_INTERVAL * 2)
    heroes.buff(buff, base.player, line.top, ObjectAttribute.HIT_POINTS, 40, operation=Operation.ADD)
    heroes.buff_attack(buff, base.player, line.top, 1, damage_class=DamageClass.BASE_MELEE)
