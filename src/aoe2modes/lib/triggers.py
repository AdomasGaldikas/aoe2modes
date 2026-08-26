"""Trigger patterns that recur across CBA-style modes.

Every helper returns the ``Trigger`` it created so callers can keep adding to it.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, AttackStance, PanelLocation
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.objects.support.tile import Tile

# The game evaluates triggers roughly once per second, so a looping trigger gated on
# a timer of N is the standard "every N seconds" primitive.
DEFAULT_WAVE_SECONDS = 20


def on_start(tm: TriggerManager, name: str, *, description: str = "") -> Trigger:
    """A one-shot trigger that fires as the scenario loads."""
    return tm.add_trigger(name, description=description, enabled=True, looping=False)


def every(
    tm: TriggerManager,
    name: str,
    seconds: int,
    *,
    enabled: bool = True,
    description: str = "",
) -> Trigger:
    """A looping trigger gated on a timer — fires every ``seconds``."""
    trigger = tm.add_trigger(name, description=description, enabled=enabled, looping=True)
    trigger.new_condition.timer(timer=seconds)
    return trigger


def objective(
    tm: TriggerManager,
    name: str,
    text: str,
    *,
    order: int = 0,
    enabled: bool = True,
) -> Trigger:
    """A never-firing trigger whose only job is to show a line in the objectives panel."""
    return tm.add_trigger(
        name,
        description=text,
        display_as_objective=True,
        description_order=order,
        short_description=text,
        display_on_screen=True,
        mute_objectives=True,
        enabled=enabled,
        looping=False,
    )


def announce(trigger: Trigger, message: str, *, player: PlayerId | None = None, seconds: int = 8) -> Trigger:
    """Put a message on screen — to one player, or to everyone when ``player`` is None."""
    trigger.new_effect.display_instructions(
        source_player=player if player is not None else PlayerId.GAIA,
        message=message,
        display_time=seconds,
        instruction_panel_position=PanelLocation.MIDDLE,
        string_id=-1,
    )
    return trigger


def spawn_units(
    trigger: Trigger,
    player: PlayerId,
    unit_ids: Iterable[int],
    tiles: Sequence[Tile],
) -> Trigger:
    """Create one unit per (unit, tile) pair.

    ``unit_ids`` is cycled over ``tiles``, so a 3-unit composition across 12 tiles
    gives 4 of each.
    """
    units = list(unit_ids)
    if not units:
        return trigger
    for index, tile in enumerate(tiles):
        trigger.new_effect.create_object(
            object_list_unit_id=units[index % len(units)],
            source_player=player,
            location_x=tile.x,
            location_y=tile.y,
        )
    return trigger


def attack_move_all(
    trigger: Trigger,
    player: PlayerId,
    target: Tile,
    *,
    area: tuple[int, int, int, int] | None = None,
) -> Trigger:
    """Send a player's units at a point.

    ``area`` restricts the order to units inside ``(x1, y1, x2, y2)``; without it the
    order goes to everything the player owns, which is what a wave spawner wants.
    """
    kwargs: dict[str, int] = {}
    if area is not None:
        kwargs = dict(area_x1=area[0], area_y1=area[1], area_x2=area[2], area_y2=area[3])
    trigger.new_effect.task_object(
        source_player=player,
        location_x=target.x,
        location_y=target.y,
        action_type=ActionType.ATTACK_MOVE,
        **kwargs,
    )
    return trigger


def set_stance(trigger: Trigger, player: PlayerId, stance: AttackStance) -> Trigger:
    trigger.new_effect.change_object_stance(source_player=player, attack_stance=stance)
    return trigger


def defeat_when_object_destroyed(
    tm: TriggerManager,
    player: PlayerId,
    unit_const: int,
    *,
    name: str | None = None,
    also_kill_units: bool = True,
) -> Trigger:
    """The CBA loss condition: lose your last castle, lose the game.

    ``also_kill_units`` reproduces the standard behaviour of wiping the eliminated
    player's army so the survivors are not left fighting a corpse.
    """
    trigger = tm.add_trigger(
        name or f"Defeat P{int(player)}",
        description="Player is eliminated once their last castle falls.",
        enabled=True,
        looping=False,
    )
    trigger.new_condition.own_fewer_objects(
        quantity=0,
        object_list=unit_const,
        source_player=player,
    )
    if also_kill_units:
        trigger.new_effect.kill_object(source_player=player)
    trigger.new_effect.declare_victory(source_player=player, enabled=False)
    return trigger


def link(source: Trigger, target: Trigger, *, activate: bool = True) -> Trigger:
    """Chain triggers: ``source`` (de)activates ``target`` when it fires."""
    if activate:
        source.new_effect.activate_trigger(trigger_id=target.trigger_id)
    else:
        source.new_effect.deactivate_trigger(trigger_id=target.trigger_id)
    return source
