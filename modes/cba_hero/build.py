"""CBA Hero — 8-player hero arena.

Shape of the mode:

* Two lines of four players face each other across an open arena.
* Every player owns exactly one castle. Lose it and you are out; the last team
  standing wins.
* Every player is assigned a hero *line* (an archetype with three tiers). The hero
  upgrades to the next tier as the match progresses.
* Waves of support units spawn automatically and attack-move into the middle, so
  there is no economy and nothing to build.

The wave clock lives in ``xs/main.xs``; this file owns everything that needs to know
where things are on the map.
"""

from __future__ import annotations

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import (
    AttackStance,
    Comparison,
    ObjectAttribute,
    Operation,
)
from AoE2ScenarioParser.datasets.units import UnitInfo

from aoe2modes.context import BuildContext
from aoe2modes.lib import heroes, players, spawns, terrain, triggers, variables

# --- tuning ------------------------------------------------------------------------

WAVE_INTERVAL = 20          # seconds between waves
WAVE_SIZE_BASE = 4          # units per wave at wave 0
WAVE_SIZE_STEP = 1          # extra units per wave
WAVE_SIZE_CAP = 16          # plateau, keeps late-game unit counts bounded

#: Support units cycled through each wave. The hero is the star; these are chaff.
WAVE_COMPOSITION = (
    UnitInfo.MILITIA.ID,
    UnitInfo.SPEARMAN.ID,
    UnitInfo.ARCHER.ID,
    UnitInfo.SKIRMISHER.ID,
)

#: Wave number at which each hero tier unlocks. Index 0 is the starting tier.
TIER_UNLOCK_WAVES = (0, 6, 14)

HERO_POOL = heroes.CLASSIC_LINES


# --- build -------------------------------------------------------------------------

def build(ctx: BuildContext) -> None:
    size = ctx.map_size
    bases = spawns.lane_bases(ctx.players, size, margin=16, castle_offset=7, spawn_offset=11)

    _shape_arena(ctx, size)
    _place_bases(ctx, bases)

    variables.declare(ctx.tm)
    ctx.set_xs_vars(
        WAVE_INTERVAL=WAVE_INTERVAL,
        WAVE_SIZE_BASE=WAVE_SIZE_BASE,
        WAVE_SIZE_STEP=WAVE_SIZE_STEP,
        WAVE_SIZE_CAP=WAVE_SIZE_CAP,
    )

    _objectives(ctx)
    _opening(ctx, bases)

    for base in bases.values():
        _wave_spawner(ctx, base)
        _hero_progression(ctx, base)
        triggers.defeat_when_object_destroyed(
            ctx.tm,
            base.player,
            BuildingInfo.CASTLE.ID,
            name=f"Defeat — P{int(base.player)} loses last castle",
        )


def _shape_arena(ctx: BuildContext, size: int) -> None:
    """An open grass arena ringed by water, so nothing wanders off the playable area."""
    centre = size // 2
    terrain.disc(ctx.mm, centre, centre, int(size * 0.42), TerrainId.GRASS_1, elevation=1)
    terrain.border(ctx.mm, 6, TerrainId.WATER_DEEP)
    ctx.log(f"arena shaped on {size}x{size}")


def _place_bases(ctx: BuildContext, bases: dict[PlayerId, spawns.Base]) -> None:
    """One castle and one starting hero per player, with the camera looking at them."""
    for base in bases.values():
        line = HERO_POOL.for_player(base.player)
        ctx.um.add_unit(
            player=base.player,
            unit_const=BuildingInfo.CASTLE.ID,
            x=base.castle.x + 0.5,
            y=base.castle.y + 0.5,
        )
        ctx.um.add_unit(
            player=base.player,
            unit_const=line.base.ID,
            x=base.center.x + 0.5,
            y=base.center.y + 0.5,
        )
        players.set_camera(ctx.pm, base.player, base.center.x, base.center.y)
        ctx.log(f"P{int(base.player)} -> {line.label} at {base.center}")


def _objectives(ctx: BuildContext) -> None:
    triggers.objective(ctx.tm, "Goal", "Destroy every enemy castle.", order=0)
    triggers.objective(ctx.tm, "Lives", "Lose your castle and you are eliminated.", order=1)
    triggers.objective(
        ctx.tm, "Waves", f"Reinforcements arrive every {WAVE_INTERVAL} seconds.", order=2
    )


def _opening(ctx: BuildContext, bases: dict[PlayerId, spawns.Base]) -> None:
    """One-shot setup: hero status, stances, and the welcome banner."""
    start = triggers.on_start(ctx.tm, "Match setup", description="Runs once on load.")
    triggers.announce(start, f"{ctx.spec.name} — destroy every enemy castle!", seconds=10)

    for base in bases.values():
        line = HERO_POOL.for_player(base.player)
        for hero in line.tiers:
            heroes.make_heroic(start, base.player, hero)
        triggers.set_stance(start, base.player, AttackStance.AGGRESSIVE_STANCE)


def _wave_spawner(ctx: BuildContext, base: spawns.Base) -> None:
    """Spawn a wave at this player's spawn pad, then send it at the enemy line."""
    trigger = triggers.every(
        ctx.tm,
        f"Wave — P{int(base.player)}",
        WAVE_INTERVAL,
        description=f"Reinforcements for player {int(base.player)}.",
    )
    tiles = spawns.block(base.spawn, columns=4, rows=WAVE_SIZE_CAP // 4, map_size=ctx.map_size)
    triggers.spawn_units(trigger, base.player, WAVE_COMPOSITION, tiles[:WAVE_SIZE_BASE * 2])
    triggers.attack_move_all(trigger, base.player, base.target)


def _hero_progression(ctx: BuildContext, base: spawns.Base) -> None:
    """Upgrade the hero one tier at a time, gated on the wave counter XS publishes."""
    line = HERO_POOL.for_player(base.player)

    for tier_index, (old, new) in enumerate(line.upgrades(), start=1):
        unlock_wave = TIER_UNLOCK_WAVES[min(tier_index, len(TIER_UNLOCK_WAVES) - 1)]
        trigger = ctx.tm.add_trigger(
            f"Hero tier {tier_index + 1} — P{int(base.player)}",
            description=f"{line.label}: {old.name} -> {new.name} at wave {unlock_wave}.",
            enabled=True,
            looping=False,
        )
        trigger.new_condition.variable_value(
            variable=variables.WAVE,
            quantity=unlock_wave,
            comparison=Comparison.LARGER_OR_EQUAL,
        )
        heroes.upgrade_hero(trigger, base.player, old, new)
        heroes.make_heroic(trigger, base.player, new)
        triggers.announce(
            trigger,
            f"{line.label} advanced to {new.name.replace('_', ' ').title()}.",
            player=base.player,
            seconds=6,
        )

    # A small permanent buff per tier keeps the hero relevant as waves grow.
    buff = triggers.every(
        ctx.tm,
        f"Hero regen buff — P{int(base.player)}",
        WAVE_INTERVAL * 3,
        description="Slow, compounding hero scaling.",
    )
    heroes.buff(buff, base.player, line.top, ObjectAttribute.HIT_POINTS, 25, operation=Operation.ADD)
