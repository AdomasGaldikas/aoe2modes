"""Owner-resolved enemy exclusion for the six allied reinforcement routes."""

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, VisibilityState

from aoe2modes.context import BuildContext

from .v2_map import MAP_SIZE, TEAM_ROUTE_RECTANGLES

# P1/P3's corner, including the existing narrow approaches to the gates.
# Reflect into the other corners; never extend into the Castle yards or arena.
_LEFT_CORNER = ((8, 8, 43, 23), (8, 24, 23, 43))
_TOP_ROUTES = (
    *_LEFT_CORNER,
    *((MAP_SIZE - 1 - x2, y1, MAP_SIZE - 1 - x1, y2) for x1, y1, x2, y2 in _LEFT_CORNER),
    *(area for area in TEAM_ROUTE_RECTANGLES if area[1] < MAP_SIZE // 2),
)
_BOTTOM_ROUTES = tuple((x1, MAP_SIZE - 1 - y2, x2, MAP_SIZE - 1 - y1) for x1, y1, x2, y2 in _TOP_ROUTES)
_ACCESS_GATES = (109743, 109744, 109745, 109746, 65500, 23621, 23076, 23205, 23618, 23624, 23615, 23627)


def _route_warning_markers(ctx, active_variables, world_variables):
    """Native per-player visibility; no unsynchronized game-state mutation."""
    left = [(x, 9) for x in (12, 20, 28, 36)] + [(42, 20), (9, 28), (9, 36), (20, 42)]
    north = left + [(143 - x, y) for x, y in left] + [(x, 14) for x in (67, 71, 75)]
    refs = []
    labels = ctx.tm.add_trigger("Enemy Route Hazard Labels")
    labels.new_condition.timer(timer=1)
    for points in (north, [(x, 143 - y) for x, y in north]):
        group = []
        for x, y in points:
            unit = ctx.um.add_unit(
                player=PlayerId.GAIA, unit_const=OtherInfo.BONFIRE.ID, x=x + 0.5, y=y + 0.5
            )
            group.append(unit.reference_id)
        refs.append(group)
    labels.new_effect.change_object_name(
        source_player=PlayerId.GAIA,
        selected_object_ids=refs[0] + refs[1],
        message="DANGER - enemy rear route: units killed",
    )
    for color in PlayerId.all(exclude_gaia=True):
        for selector in PlayerId.all(exclude_gaia=True):
            trigger = ctx.tm.add_trigger(f"Route Hazard Visibility P{int(color)} W{int(selector)}", looping=1)
            trigger.new_condition.timer(timer=5)
            for variable, value in ((active_variables[color], 1), (world_variables[color], int(selector))):
                trigger.new_condition.variable_value(
                    variable=variable, quantity=value, comparison=Comparison.EQUAL
                )
            for north_side, group in enumerate(refs):
                enemy_side = (int(color) <= 4) == bool(north_side)
                trigger.new_effect.change_object_visibility(
                    source_player=PlayerId.GAIA,
                    target_player=selector,
                    selected_object_ids=group,
                    visibility_state=VisibilityState.VISIBLE if enemy_side else VisibilityState.INVISIBLE,
                )


def protect_team_routes(
    ctx: BuildContext,
    active_variables,
    world_variables,
    match_ready_variable,
) -> None:
    """Kill intruders once a second, including when a route owner is eliminated.

    Guards depend on the intruder's active color and resolved native selector,
    never the protected endpoint's occupancy. Variable conditions avoid adding
    native player-condition exposure in sparse/shuffled lobbies (ASC-053).
    Kill Object uses native owner-scoped areas and also clears hostile foundations.
    """
    labels = ctx.tm.add_trigger(
        "Allied Route Gate Labels",
        description_stid=0,
        short_description_stid=0,
    )
    labels.new_condition.timer(timer=1)
    labels.new_effect.change_object_name(
        source_player=-1,
        selected_object_ids=list(_ACCESS_GATES[:4]),
        message="Allied route - enemy units killed",
    )
    # The eight corner entrances are also the intentionally deletable wall
    # switches. A generic route label concealed that gameplay action in v1.1.
    labels.new_effect.change_object_name(
        source_player=-1,
        selected_object_ids=list(_ACCESS_GATES[4:]),
        message="Side-wall switch - DELETE opens walls",
    )
    _route_warning_markers(ctx, active_variables, world_variables)
    for color in PlayerId.all(exclude_gaia=True):
        enemy_routes = _BOTTOM_ROUTES if int(color) <= 4 else _TOP_ROUTES
        for selector in PlayerId.all(exclude_gaia=True):
            guard = ctx.tm.add_trigger(
                f"Allied Route Guard P{int(color)} W{int(selector)}",
                description_stid=0,
                short_description_stid=0,
                looping=1,
            )
            guard.new_condition.timer(timer=1)
            for variable, value in (
                (match_ready_variable, 1),
                (active_variables[color], 1),
                (world_variables[color], int(selector)),
            ):
                guard.new_condition.variable_value(
                    variable=variable,
                    quantity=value,
                    comparison=Comparison.EQUAL,
                )
            for x1, y1, x2, y2 in enemy_routes:
                guard.new_effect.kill_object(
                    source_player=selector,
                    area_x1=x1,
                    area_y1=y1,
                    area_x2=x2,
                    area_y2=y2,
                )
