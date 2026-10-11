"""Owner-resolved enemy exclusion for the six allied reinforcement routes."""

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison

from aoe2modes.context import BuildContext

from .v2_map import MAP_SIZE, TEAM_ROUTE_RECTANGLES

# P1/P3's corner, including the existing narrow approaches to the gates.
# Reflect into the other corners; never extend into the Castle yards or arena.
_LEFT_CORNER = ((16, 16, 43, 23), (16, 24, 23, 43))
_TOP_ROUTES = (
    *_LEFT_CORNER,
    *((MAP_SIZE - 1 - x2, y1, MAP_SIZE - 1 - x1, y2) for x1, y1, x2, y2 in _LEFT_CORNER),
    *(area for area in TEAM_ROUTE_RECTANGLES if area[1] < MAP_SIZE // 2),
)
_BOTTOM_ROUTES = tuple(
    (x1, MAP_SIZE - 1 - y2, x2, MAP_SIZE - 1 - y1)
    for x1, y1, x2, y2 in _TOP_ROUTES
)
_ACCESS_GATES = (109743, 109744, 109745, 109746, 65500, 23621, 23076, 23205,
                 23618, 23624, 23615, 23627)


def protect_team_routes(
    ctx: BuildContext, active_variables, world_variables, match_ready_variable,
) -> None:
    """Remove intruders once a second, including when a route owner is eliminated.

    Guards depend on the intruder's active color and resolved native selector,
    never the protected endpoint's occupancy. Variable conditions avoid adding
    native player-condition exposure in sparse/shuffled lobbies (ASC-053).
    Remove Object gives no combat kill credit and also clears hostile foundations.
    """
    labels = ctx.tm.add_trigger(
        "Allied Route Gate Labels", description_stid=0, short_description_stid=0,
    )
    labels.new_condition.timer(timer=1)
    labels.new_effect.change_object_name(
        source_player=-1,
        selected_object_ids=list(_ACCESS_GATES[:4]),
        message="Allied route - enemy units removed",
    )
    # The eight corner entrances are also the intentionally deletable wall
    # switches. A generic route label concealed that gameplay action in v1.1.
    labels.new_effect.change_object_name(
        source_player=-1,
        selected_object_ids=list(_ACCESS_GATES[4:]),
        message="Side-wall switch - DELETE opens walls",
    )
    for color in PlayerId.all(exclude_gaia=True):
        enemy_routes = _BOTTOM_ROUTES if int(color) <= 4 else _TOP_ROUTES
        for selector in PlayerId.all(exclude_gaia=True):
            guard = ctx.tm.add_trigger(
                f"Allied Route Guard P{int(color)} W{int(selector)}",
                description_stid=0, short_description_stid=0, looping=1,
            )
            guard.new_condition.timer(timer=1)
            for variable, value in (
                (match_ready_variable, 1),
                (active_variables[color], 1),
                (world_variables[color], int(selector)),
            ):
                guard.new_condition.variable_value(
                    variable=variable, quantity=value, comparison=Comparison.EQUAL,
                )
            for x1, y1, x2, y2 in enemy_routes:
                guard.new_effect.remove_object(
                    source_player=selector,
                    area_x1=x1, area_y1=y1, area_x2=x2, area_y2=y2,
                )
