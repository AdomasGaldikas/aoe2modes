"""CBA Hero: Ascendants — rebuilt from code rather than shipped as a binary.

Everything the original scenario contained now lives in ``generated/``: terrain,
units, players, lobby options and the original triggers. Ascendants then applies
substantial map and gameplay patches, so the public build intentionally differs from
``base.aoe2scenario``. Use ``make check-ascendants`` to validate both source layers.

Edit in one of two places:

- **Small, local changes** go here, after ``generated.apply(ctx)``. This code runs
  last and wins, so retuning a value or renaming a trigger needs no regeneration.
- **Reference reconstruction changes** go into ``generated/``. Those files are
  overwritten by ``aoe2modes decompile``; Ascendants-specific fixes belong here or
  in a focused helper module instead.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from copy import deepcopy

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import (
    ActionType,
    Attribute,
    Comparison,
    ObjectAttribute,
    ObjectClass,
    ObjectType,
    Operation,
    VictoryCondition,
)
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.unit_manager import create_id_generator

from aoe2modes.context import BuildContext
from aoe2modes.lib.decompile import (
    CONDITION_PARAMS,
    EFFECT_PARAMS,
    TRIGGER_PARAMS,
    condition_factory_name,
    effect_factory_name,
    safe_get,
)

from .generated import apply as apply_generated
from .v2_map import apply_v2_map, v2_cell_for_player, v2_position_for_player

PLAYERS = tuple(PlayerId.all(exclude_gaia=True))


def _possible_world_players(color: PlayerId):
    """Runtime slots a compacted scenario color can validly occupy."""
    return PLAYERS[: int(color)]


RESOURCE_STOCKPILES = (0, 1, 2, 3)  # food, wood, stone, gold
FREE_PLAYER_ATTRIBUTES = (
    Attribute.RESEARCH_COST_MODIFIER,
    Attribute.UNIT_REPAIR_COST,
    Attribute.BUILDING_REPAIR_COST,
)
SCORE_NEUTRAL_ATTRIBUTES = (
    Attribute.PERCENT_MAP_EXPLORED,
    Attribute.BUILDING_COST_SUM,
    Attribute.TECH_COST_SUM,
    Attribute.VALUE_CURRENT_UNITS,
    Attribute.VALUE_CURRENT_BUILDINGS,
    Attribute.TRIBUTE_SCORE,
    Attribute.VALUE_WONDERS_CASTLES,
    Attribute.FOOD_SCORE,
    Attribute.WOOD_SCORE,
    Attribute.STONE_SCORE,
    Attribute.GOLD_SCORE,
    Attribute.UNITS_VALUE_TOTAL,
    Attribute.BUILDINGS_VALUE_TOTAL,
)
VOTE_KICK_NAME = re.compile(r"VoteKickP([1-8])-P([1-8])-P([1-8])")
COLOR_ACTIVE_VARIABLE_BASE = 32
COLOR_WORLD_VARIABLE_BASE = 40
COLOR_ELIMINATED_VARIABLE_BASE = 48
MATCH_READY_VARIABLE_ID = 56
VOTE_MARKER_VARIABLE_BASE = 57
VOTE_FLAG_OFFSETS = {
    PlayerId.ONE: (2, 0),
    PlayerId.TWO: (-2, 0),
    PlayerId.THREE: (0, 2),
    PlayerId.FOUR: (0, 2),
    PlayerId.FIVE: (0, -2),
    PlayerId.SIX: (0, -2),
    PlayerId.SEVEN: (2, 0),
    PlayerId.EIGHT: (-2, 0),
}
PLAYER_COLOR_NAMES = {
    PlayerId.ONE: "BLUE",
    PlayerId.TWO: "RED",
    PlayerId.THREE: "GREEN",
    PlayerId.FOUR: "YELLOW",
    PlayerId.FIVE: "TEAL",
    PlayerId.SIX: "PURPLE",
    PlayerId.SEVEN: "GRAY",
    PlayerId.EIGHT: "ORANGE",
}
EDGE_KILL_ZONE_NAME = re.compile(r"uk[1-4] \(p[1-8]\)")
ANTI_TREB_NAME = re.compile(r"No trebs in p([1-8]) base(?: \(p[1-8]\))?")
LOBBY_SETTLE_SECONDS = 3
VICTORY_RESOLVE_SECONDS = 5
SPAWN_POINTS = {
    PlayerId.ONE: ((48, 22), (52, 22), (55, 22), (59, 22)),
    PlayerId.TWO: ((96, 22), (92, 22), (89, 22), (85, 22)),
    PlayerId.THREE: ((22, 48), (22, 52), (22, 55), (22, 59)),
    PlayerId.FOUR: ((122, 48), (122, 52), (122, 55), (122, 59)),
    PlayerId.FIVE: ((22, 96), (22, 92), (22, 89), (22, 85)),
    PlayerId.SIX: ((122, 96), (122, 92), (122, 89), (122, 85)),
    PlayerId.SEVEN: ((48, 122), (52, 122), (55, 122), (59, 122)),
    PlayerId.EIGHT: ((96, 122), (92, 122), (89, 122), (85, 122)),
}
SPAWN_MARKER_BOAT_POSITIONS = {
    player: v2_position_for_player(player, 16.5, 35.5)
    for player in PLAYERS
}
HAY_LOCATION_BY_CASTLE_REFERENCE = {
    9_761: (48, 21),
    22_013: (52, 21),
    22_014: (55, 21),
    22_015: (59, 21),
    78_945: (95, 21),
    78_946: (84, 21),
    78_947: (88, 21),
    78_948: (91, 21),
    35_044: (21, 59),
    35_045: (21, 55),
    35_046: (21, 52),
    35_043: (21, 48),
    22_019: (122, 48),
    22_020: (122, 52),
    22_021: (122, 55),
    22_022: (122, 59),
    35_050: (21, 95),
    35_049: (21, 84),
    35_048: (21, 88),
    35_047: (21, 91),
    22_023: (122, 95),
    22_024: (122, 84),
    22_025: (122, 88),
    22_026: (122, 91),
    79_333: (48, 122),
    79_334: (52, 122),
    79_335: (55, 122),
    79_336: (59, 122),
    35_057: (95, 122),
    35_055: (84, 122),
    35_056: (88, 122),
    35_058: (91, 122),
}
BASE_CASTLE_AREAS = {
    PlayerId.ONE: (48, 19, 60, 19),
    PlayerId.TWO: (84, 19, 96, 19),
    PlayerId.THREE: (19, 48, 19, 60),
    PlayerId.FOUR: (125, 48, 125, 60),
    PlayerId.FIVE: (19, 84, 19, 96),
    PlayerId.SIX: (125, 84, 125, 96),
    PlayerId.SEVEN: (48, 125, 60, 125),
    PlayerId.EIGHT: (84, 125, 96, 125),
}
BUILDER_SPAWN_POINTS = {
    player: {
        UnitInfo.VILLAGER_MALE.ID: v2_cell_for_player(player, 10, 54),
        UnitInfo.VILLAGER_FEMALE.ID: v2_cell_for_player(player, 11, 54),
    }
    for player in PLAYERS
}
BUILDER_DESTINATION_POINTS = {
    player: {
        UnitInfo.VILLAGER_MALE.ID: v2_cell_for_player(player, 17, 45),
        UnitInfo.VILLAGER_FEMALE.ID: v2_cell_for_player(player, 17, 63),
    }
    for player in PLAYERS
}
SOURCE_BUILDER_FLAG_POSITIONS = ((22.5, 40.5), (23.5, 40.5))
SOURCE_BUILDER_FLAG_TARGETS = ((10.5, 53.5), (10.5, 55.5))
BLACKSMITH_AREAS = {
    PlayerId.ONE: (50, 1, 58, 6),
    PlayerId.TWO: (85, 1, 93, 6),
    PlayerId.THREE: (1, 50, 6, 58),
    PlayerId.FOUR: (137, 50, 142, 58),
    PlayerId.FIVE: (1, 85, 6, 93),
    PlayerId.SIX: (137, 85, 142, 93),
    PlayerId.SEVEN: (50, 137, 58, 142),
    PlayerId.EIGHT: (85, 137, 93, 142),
}
# Civilization ID -> (spawned unit ID, military population cap, interval seconds).
# These reproduce the 59 legacy civilization loops without binding a color to a
# compacted runtime player number.
CIV_SPAWN_RULES = {
    1: (530, 72, 9),
    2: (531, 76, 8),
    3: (761, 92, 10),
    4: (554, 76, 8),
    5: (560, 80, 9),
    6: (559, 76, 8),
    7: (553, 56, 10),
    8: (239, 40, 13),
    9: (556, 68, 12),
    10: (46, 50, 9),
    11: (694, 86, 9),
    12: (561, 56, 9),
    13: (534, 80, 9),
    14: (771, 60, 10),
    15: (726, 92, 8),
    16: (765, 70, 8),
    17: (757, 80, 13),
    18: (829, 60, 12),
    19: (868, 72, 9),
    20: (1749, 60, 12),
    21: (881, 77, 8),
    22: (871, 80, 13),
    23: (878, 56, 10),
    24: (1001, 34, 12),
    25: (1018, 80, 8),
    26: (1015, 81, 10),
    27: (1009, 61, 10),
    28: (1122, 31, 14),
    29: (1125, 80, 6),
    30: (1128, 61, 10),
    31: (1131, 81, 10),
    32: (1227, 41, 12),
    33: (1230, 61, 12),
    34: (1233, 61, 12),
    35: (1236, 60, 10),
    36: (1657, 60, 8),
    37: (1659, 92, 8),
    38: (1703, 60, 8),
    39: (1706, 35, 15),
    40: (1737, 60, 8),
    41: (1761, 40, 8),
    42: (1743, 41, 11),
    43: (1792, 60, 8),
    44: (1802, 80, 8),
    45: (1805, 80, 8),
    46: (2175, 70, 10),
    47: (2105, 80, 10),
    48: (2108, 80, 8),
    49: (1961, 60, 10),
    50: (1970, 60, 10),
    51: (1951, 60, 10),
    52: (1910, 80, 10),
    53: (1922, 80, 10),
    54: (2383, 70, 10),
    55: (2387, 92, 8),
    56: (2389, 72, 9),
    57: (2587, 80, 8),
    58: (2571, 80, 10),
    59: (2584, 80, 8),
}
# Civilization ID -> (public name, razings needed for the first builder pair).
# After the first pair, the legacy CBA rule awards another pair for every razing.
CIV_BUILDER_RULES = {
    1: ("Britons", 1),
    2: ("Franks", 3),
    3: ("Goths", 2),
    4: ("Teutons", 3),
    5: ("Japanese", 3),
    6: ("Chinese", 2),
    7: ("Byzantines", 2),
    8: ("Persians", 4),
    9: ("Saracens", 2),
    10: ("Turks", 3),
    11: ("Vikings", 2),
    12: ("Mongols", 2),
    13: ("Celts", 2),
    14: ("Spanish", 3),
    15: ("Aztecs", 2),
    16: ("Mayans", 1),
    17: ("Huns", 4),
    18: ("Koreans", 3),
    19: ("Italians", 1),
    20: ("Hindustanis", 3),
    21: ("Incas", 2),
    22: ("Magyars", 1),
    23: ("Slavs", 2),
    24: ("Portuguese", 3),
    25: ("Ethiopians", 2),
    26: ("Malians", 3),
    27: ("Berbers", 1),
    28: ("Khmer", 4),
    29: ("Malay", 1),
    30: ("Burmese", 3),
    31: ("Vietnamese", 1),
    32: ("Bulgarians", 2),
    33: ("Tatars", 2),
    34: ("Cumans", 2),
    35: ("Lithuanians", 2),
    36: ("Burgundians", 2),
    37: ("Sicilians", 2),
    38: ("Poles", 2),
    39: ("Bohemians", 2),
    40: ("Dravidians", 2),
    41: ("Bengalis", 2),
    42: ("Gurjaras", 3),
    43: ("Romans", 2),
    44: ("Armenians", 2),
    45: ("Georgians", 1),
    46: ("Achaemenids", 1),
    47: ("Athenians", 1),
    48: ("Spartans", 1),
    49: ("Shu", 2),
    50: ("Wu", 2),
    51: ("Wei", 2),
    52: ("Jurchens", 2),
    53: ("Khitans", 2),
    54: ("Macedonians", 1),
    55: ("Thracians", 1),
    56: ("Puru", 1),
    57: ("Muisca", 1),
    58: ("Mapuche", 1),
    59: ("Tupi", 1),
}
REAR_ENCLOSURES = (
    (
        PlayerId.ONE,
        "horizontal",
        13.5,
        ((51.5, 51.5), (56.5, 56.5)),
        54.0,
        ((52.5, 15.5), (55.5, 15.5), (62.5, 16.5)),
    ),
    (
        PlayerId.TWO,
        "horizontal",
        13.5,
        ((84.5, 84.5), (89.5, 89.5)),
        87.0,
        ((85.5, 15.5), (88.5, 15.5), (78.5, 16.5)),
    ),
    (
        PlayerId.THREE,
        "vertical",
        10.5,
        ((51.5, 51.5), (56.5, 56.5)),
        54.0,
        ((12.5, 52.5), (12.5, 55.5), (15.5, 45.5)),
    ),
    (
        PlayerId.FOUR,
        "vertical",
        130.5,
        ((51.5, 51.5), (56.5, 56.5)),
        54.0,
        ((128.5, 52.5), (128.5, 55.5), (125.5, 45.5)),
    ),
    (
        PlayerId.FIVE,
        "vertical",
        10.5,
        ((84.5, 84.5), (89.5, 89.5)),
        87.0,
        ((12.5, 85.5), (12.5, 88.5), (15.5, 95.5)),
    ),
    (
        PlayerId.SIX,
        "vertical",
        130.5,
        ((84.5, 84.5), (89.5, 89.5)),
        87.0,
        ((128.5, 85.5), (128.5, 88.5), (125.5, 95.5)),
    ),
    (
        PlayerId.SEVEN,
        "horizontal",
        128.5,
        ((51.5, 51.5), (56.5, 56.5)),
        54.0,
        ((52.5, 126.5), (55.5, 126.5), (62.5, 125.5)),
    ),
    (
        PlayerId.EIGHT,
        "horizontal",
        128.5,
        ((84.5, 84.5), (89.5, 89.5)),
        87.0,
        ((85.5, 126.5), (88.5, 126.5), (78.5, 125.5)),
    ),
)
REAR_SIDE_GATES = (
    (PlayerId.ONE, 64.5, (20.5, 21.5, 22.5), 23.5, 22.0),
    (PlayerId.TWO, 76.5, (20.5, 21.5, 22.5), 23.5, 22.0),
    (PlayerId.SEVEN, 64.5, (121.5, 122.5, 123.5), 124.5, 123.0),
    (PlayerId.EIGHT, 76.5, (121.5, 122.5, 123.5), 124.5, 123.0),
)
# Short wall runs that close the walkable seam between each existing side wall
# and the first intact rear-cliff segment. These are deliberately perpendicular
# to the cliff barrier instead of duplicating it with another long wall.
REAR_END_CONNECTORS = (
    (PlayerId.ONE, "vertical", 43.5, 14.5, 15.5),
    (PlayerId.ONE, "vertical", 64.5, 14.5, 15.5),
    (PlayerId.TWO, "vertical", 76.5, 14.5, 15.5),
    (PlayerId.TWO, "vertical", 97.5, 14.5, 15.5),
    (PlayerId.THREE, "horizontal", 43.5, 11.5, 14.5),
    (PlayerId.THREE, "horizontal", 64.5, 11.5, 14.5),
    (PlayerId.FOUR, "horizontal", 43.5, 126.5, 129.5),
    (PlayerId.FOUR, "horizontal", 64.5, 126.5, 129.5),
    (PlayerId.FIVE, "horizontal", 76.5, 11.5, 14.5),
    (PlayerId.FIVE, "horizontal", 97.5, 11.5, 14.5),
    (PlayerId.SIX, "horizontal", 76.5, 126.5, 129.5),
    (PlayerId.SIX, "horizontal", 97.5, 126.5, 129.5),
    (PlayerId.SEVEN, "vertical", 43.5, 126.5, 127.5),
    (PlayerId.SEVEN, "vertical", 64.5, 126.5, 127.5),
    (PlayerId.EIGHT, "vertical", 76.5, 126.5, 127.5),
    (PlayerId.EIGHT, "vertical", 97.5, 126.5, 127.5),
)
# One extra wall tile beyond each end of the three-gate arena-facing wall
# removes the two diagonal squeeze points used to enter a base from the front.
FRONT_GATE_END_EXTENSIONS = (
    (PlayerId.ONE, "horizontal", 39.5, (46.5, 61.5)),
    (PlayerId.TWO, "horizontal", 39.5, (79.5, 94.5)),
    (PlayerId.THREE, "vertical", 39.5, (46.5, 61.5)),
    (PlayerId.FOUR, "vertical", 101.5, (46.5, 61.5)),
    (PlayerId.FIVE, "vertical", 39.5, (79.5, 94.5)),
    (PlayerId.SIX, "vertical", 101.5, (79.5, 94.5)),
    (PlayerId.SEVEN, "horizontal", 101.5, (46.5, 61.5)),
    (PlayerId.EIGHT, "horizontal", 101.5, (79.5, 94.5)),
)
REAR_TECH_PATHS = (
    (
        PlayerId.ONE,
        (53, 7, 54, 15),
        (
            (70385, OtherInfo.CLIFF_DEFAULT_3.ID, 52.5, 13.5),
            (70383, OtherInfo.CLIFF_DEFAULT_3.ID, 55.5, 13.5),
        ),
    ),
    (
        PlayerId.TWO,
        (86, 7, 87, 15),
        (
            (70319, OtherInfo.CLIFF_DEFAULT_3.ID, 85.5, 13.5),
            (70305, OtherInfo.CLIFF_DEFAULT_3.ID, 88.5, 13.5),
        ),
    ),
    (
        PlayerId.THREE,
        (7, 53, 14, 54),
        (
            (70476, OtherInfo.CLIFF_DEFAULT_1.ID, 13.5, 52.5),
            (70478, OtherInfo.CLIFF_DEFAULT_1.ID, 13.5, 55.5),
        ),
    ),
    (
        PlayerId.FOUR,
        (128, 53, 136, 54),
        (
            (70235, OtherInfo.CLIFF_DEFAULT_2.ID, 127.5, 52.5),
            (70233, OtherInfo.CLIFF_DEFAULT_2.ID, 127.5, 55.5),
        ),
    ),
    (
        PlayerId.FIVE,
        (7, 86, 14, 87),
        (
            (90121, OtherInfo.CLIFF_DEFAULT_1.ID, 10.5, 85.5),
            (90118, OtherInfo.CLIFF_DEFAULT_1.ID, 10.5, 88.5),
        ),
    ),
    (
        PlayerId.SIX,
        (128, 86, 136, 87),
        (
            (70167, OtherInfo.CLIFF_DEFAULT_2.ID, 127.5, 85.5),
            (70165, OtherInfo.CLIFF_DEFAULT_2.ID, 127.5, 88.5),
        ),
    ),
    (
        PlayerId.SEVEN,
        (53, 128, 54, 136),
        (
            (90179, OtherInfo.CLIFF_DEFAULT_1.ID, 52.5, 130.5),
            (90180, OtherInfo.CLIFF_DEFAULT_1.ID, 55.5, 130.5),
        ),
    ),
    (
        PlayerId.EIGHT,
        (86, 128, 87, 136),
        (
            (70095, OtherInfo.CLIFF_DEFAULT_1.ID, 85.5, 127.5),
            (70097, OtherInfo.CLIFF_DEFAULT_1.ID, 88.5, 127.5),
        ),
    ),
)
REAR_LAND_APRONS = (
    (PlayerId.ONE, (38, 13, 67, 15), (38, 12, 67, 12)),
    (PlayerId.TWO, (74, 13, 103, 15), (74, 12, 103, 12)),
    (PlayerId.THREE, (10, 38, 14, 67), (9, 38, 9, 67)),
    (PlayerId.FOUR, (126, 38, 130, 67), (131, 38, 131, 67)),
    (PlayerId.FIVE, (10, 74, 14, 103), (9, 74, 9, 103)),
    (PlayerId.SIX, (126, 74, 130, 103), (131, 74, 131, 103)),
    (PlayerId.SEVEN, (38, 126, 67, 128), (38, 129, 67, 129)),
    (PlayerId.EIGHT, (74, 126, 103, 128), (74, 129, 103, 129)),
)
# Water occupies only the short apron ends beyond the two side-wall endpoints.
# This blocks diagonal cliff-end bypasses without flooding the allied route.
REAR_WATER_END_CAPS = (
    (PlayerId.ONE, ((38, 13, 42, 15), (65, 13, 67, 15))),
    (PlayerId.TWO, ((74, 13, 75, 15), (98, 13, 103, 15))),
    (PlayerId.THREE, ((10, 38, 14, 42), (10, 65, 14, 67))),
    (PlayerId.FOUR, ((126, 38, 130, 42), (126, 65, 130, 67))),
    (PlayerId.FIVE, ((10, 74, 14, 75), (10, 98, 14, 103))),
    (PlayerId.SIX, ((126, 74, 130, 75), (126, 98, 130, 103))),
    (PlayerId.SEVEN, ((38, 126, 42, 128), (65, 126, 67, 128))),
    (PlayerId.EIGHT, ((74, 126, 75, 128), (98, 126, 103, 128))),
)
REAR_CLIFF_CLEANUP_AREAS = (
    (PlayerId.ONE, (37, 13, 68, 17)),
    (PlayerId.TWO, (73, 13, 104, 17)),
    (PlayerId.THREE, (13, 37, 17, 68)),
    (PlayerId.FOUR, (124, 37, 128, 68)),
    (PlayerId.FIVE, (10, 73, 17, 104)),
    (PlayerId.SIX, (124, 73, 128, 104)),
    (PlayerId.SEVEN, (37, 127, 68, 131)),
    (PlayerId.EIGHT, (73, 127, 104, 131)),
)
REAR_CLIFF_PERIMETERS = (
    (PlayerId.ONE, "horizontal", 13.5, 43.5, 64.5, 54.0, OtherInfo.CLIFF_DEFAULT_3.ID, (10, 11)),
    (PlayerId.TWO, "horizontal", 13.5, 76.5, 97.5, 87.0, OtherInfo.CLIFF_DEFAULT_3.ID, (10, 11)),
    (PlayerId.THREE, "vertical", 10.5, 43.5, 64.5, 54.0, OtherInfo.CLIFF_DEFAULT_1.ID, (1, 2)),
    (PlayerId.FOUR, "vertical", 130.5, 43.5, 64.5, 54.0, OtherInfo.CLIFF_DEFAULT_2.ID, (7, 8)),
    (PlayerId.FIVE, "vertical", 10.5, 76.5, 97.5, 87.0, OtherInfo.CLIFF_DEFAULT_1.ID, (1, 2)),
    (PlayerId.SIX, "vertical", 130.5, 76.5, 97.5, 87.0, OtherInfo.CLIFF_DEFAULT_2.ID, (7, 8)),
    (PlayerId.SEVEN, "horizontal", 128.5, 43.5, 64.5, 54.0, OtherInfo.CLIFF_DEFAULT_1.ID, (4, 5)),
    (PlayerId.EIGHT, "horizontal", 128.5, 76.5, 97.5, 87.0, OtherInfo.CLIFF_DEFAULT_1.ID, (4, 5)),
)

PUBLIC_INSTRUCTIONS = (
    "CBA HERO: ASCENDANTS\r\r"
    "HOW TO PLAY\r"
    "Units spawn automatically and march into the arena. Defeat enemy units to unlock "
    "stronger heroes. Protect your four Castles and destroy every enemy Castle to win.\r\r"
    "TEAMS\r"
    "Blue, Red, Green, and Yellow face Teal, Purple, Gray, and Orange. Close any unused "
    "slots, but keep at least one occupied color on each side.\r\r"
    "TEAM ROUTES\r"
    "The arena uses eight equal mirrored fortified territories. Guarded rear team routes and "
    "each player's protected gate let allies reinforce one another.\r\r"
    "VOTE KICK\r"
    "Delete the matching Vote Kick marker to vote against a teammate. Two occupied "
    "teammates must vote. Voting is disabled when fewer than three colors remain on that "
    "side, and closed slots never count as votes.\r\r"
    "COMBAT HUD\r"
    "The right-side Kills / Deaths / Razings list shows live combat totals for P1 through P8. "
    "Resources stay "
    "at zero; available units, buildings, upgrades, and repairs are free.\r\r"
    "HERO MILESTONES\r"
    "200 Robin Hood | 400 Theodoric | 600 Charles Martel | 800 Subotai\r"
    "1000 Genghis Khan | 2000 Super Genghis | 3500 and 5000 spawn boosts"
)

WHITE_KING_KILL_COUNTERS = {
    PlayerId.ONE: 48_301,
    PlayerId.TWO: 42_394,
    PlayerId.THREE: 42_395,
    PlayerId.FOUR: 42_396,
    PlayerId.FIVE: 42_397,
    PlayerId.SIX: 42_398,
    PlayerId.SEVEN: 42_399,
    PlayerId.EIGHT: 42_400,
}
MIDDLE_TREBUCHET_MARKERS = {
    PlayerId.ONE: 93_736,
    PlayerId.TWO: 93_737,
    PlayerId.THREE: 93_738,
    PlayerId.FOUR: 93_739,
    PlayerId.FIVE: 93_740,
    PlayerId.SIX: 93_741,
    PlayerId.SEVEN: 93_742,
    PlayerId.EIGHT: 93_743,
}
HERO_MILESTONES = (
    (200, HeroInfo.ROBIN_HOOD.ID),
    (400, HeroInfo.THEODORIC_THE_GOTH.ID),
    (600, HeroInfo.CHARLES_MARTEL.ID),
    (800, HeroInfo.SUBOTAI.ID),
    (1_000, HeroInfo.GENGHIS_KHAN.ID),
    (2_000, HeroInfo.GENGHIS_KHAN.ID),
)
HERO_MILESTONE_SPAWN_TILES = {
    player: v2_cell_for_player(player, 16, 38)
    for player in PLAYERS
}
HERO_ORDER_FAMILIES = {
    "Curto": "Short",
    "Médio": "Medium",
    "Longo": "Long",
}
LEGACY_AGE_UP_NAME = re.compile(r"\d+ kills")


def _unique_trigger(ctx: BuildContext, name: str):
    matches = [trigger for trigger in ctx.tm.triggers if trigger.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"expected one {name!r} trigger, found {len(matches)}")
    return matches[0]


def _reset_trigger(trigger) -> None:
    trigger.description = ""
    trigger.description_stid = 0
    trigger.display_as_objective = 0
    trigger.short_description = ""
    trigger.short_description_stid = 0
    trigger.display_on_screen = 0
    trigger.description_order = 0
    trigger.enabled = 0
    trigger.looping = 0
    trigger.execute_on_load = 0
    trigger.header = 0
    trigger.mute_objectives = 0
    trigger.conditions = []
    trigger.effects = []


def _component_signature(component, factory_name, parameters):
    """Return only the fields AoE2ScenarioParser serializes for a component."""
    factory = factory_name(component)
    return (
        factory,
        tuple(
            (name, safe_get(component, name, None))
            for name in parameters.get(factory, ())
        ),
    )


def _trigger_signature(trigger):
    """Build a stable, serialization-aware trigger signature for guarded deduping."""
    return (
        trigger.name,
        tuple((name, safe_get(trigger, name, None)) for name in TRIGGER_PARAMS),
        tuple(
            _component_signature(
                condition,
                condition_factory_name,
                CONDITION_PARAMS,
            )
            for condition in trigger.conditions
        ),
        tuple(
            _component_signature(effect, effect_factory_name, EFFECT_PARAMS)
            for effect in trigger.effects
        ),
    )


def _rewrite_trigger_references(ctx: BuildContext, replacements: dict[int, int]) -> int:
    """Repoint every trigger-reference field and return the number changed."""
    changed = 0
    for trigger in ctx.tm.triggers:
        for condition in trigger.conditions:
            if (
                condition.condition_type == ConditionId.TRIGGER_ACTIVE
                and condition.trigger_id in replacements
            ):
                condition.trigger_id = replacements[condition.trigger_id]
                changed += 1
        for effect in trigger.effects:
            if (
                effect.effect_type
                in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
                and effect.trigger_id in replacements
            ):
                effect.trigger_id = replacements[effect.trigger_id]
                changed += 1
    return changed


def _age_up_player(trigger) -> int:
    """Infer the one player controlled by a legacy kill-based age-up trigger."""
    players = set()
    for component in (*trigger.conditions, *trigger.effects):
        for field in (
            "source_player",
            "target_player",
            "player_source",
            "player_target",
        ):
            player = safe_get(component, field, -1)
            if isinstance(player, int) and 1 <= int(player) <= 8:
                players.add(int(player))
    if len(players) != 1:
        raise RuntimeError(
            f"could not infer one player for legacy age-up trigger {trigger.name!r}: "
            f"{sorted(players)}"
        )
    return players.pop()


def _compact_legacy_trigger_graph(ctx: BuildContext) -> None:
    """Remove proven no-op shells and merge byte-identical legacy age-up logic.

    The decompiled source intentionally preserves the imported scenario as evidence.
    This final pass runs after every name- and ID-based patch, rewires all references,
    then lets ``TriggerManager.remove_triggers`` remap IDs and display order safely.
    Exact baseline counts make a future upstream change fail closed instead of deleting
    a newly meaningful trigger by accident.
    """
    age_triggers = [
        trigger
        for trigger in ctx.tm.triggers
        if LEGACY_AGE_UP_NAME.fullmatch(trigger.name)
    ]
    if len(age_triggers) != 288:
        raise RuntimeError(
            f"expected 288 imported age-up triggers, found {len(age_triggers)}"
        )

    signature_groups = defaultdict(list)
    for trigger in age_triggers:
        signature_groups[_trigger_signature(trigger)].append(trigger)
    duplicate_groups = [
        group for group in signature_groups.values() if len(group) > 1
    ]
    duplicate_triggers = [
        duplicate for group in duplicate_groups for duplicate in group[1:]
    ]
    if len(duplicate_groups) != 70 or len(duplicate_triggers) != 189:
        raise RuntimeError(
            "legacy age-up graph changed: expected 70 duplicate groups and "
            f"189 redundant triggers, found {len(duplicate_groups)} and "
            f"{len(duplicate_triggers)}"
        )

    replacements = {
        duplicate.trigger_id: group[0].trigger_id
        for group in duplicate_groups
        for duplicate in group[1:]
    }
    rewired = _rewrite_trigger_references(ctx, replacements)
    if rewired != 346:
        raise RuntimeError(
            f"expected to rewire 346 legacy age-up activations, rewired {rewired}"
        )
    ctx.tm.remove_triggers([trigger.trigger_id for trigger in duplicate_triggers])

    remaining_age_ups = [
        trigger
        for trigger in ctx.tm.triggers
        if LEGACY_AGE_UP_NAME.fullmatch(trigger.name)
    ]
    if len(remaining_age_ups) != 99:
        raise RuntimeError(
            f"expected 99 canonical age-up triggers, found {len(remaining_age_ups)}"
        )

    semantic_groups = defaultdict(list)
    for trigger in remaining_age_ups:
        semantic_groups[(trigger.name, _age_up_player(trigger))].append(trigger)
    variant_groups = {
        key: group for key, group in semantic_groups.items() if len(group) > 1
    }
    expected_variants = {
        ("300 kills", 7),
        ("600 kills", 7),
        ("750 kills", 7),
    }
    if set(variant_groups) != expected_variants or any(
        len(group) != 2 for group in variant_groups.values()
    ):
        raise RuntimeError(
            "unexpected non-identical legacy age-up variants: "
            f"{sorted((key, len(group)) for key, group in variant_groups.items())}"
        )
    for (name, player), group in semantic_groups.items():
        if len(group) == 1:
            group[0].name = f"{name} (p{player})"
            continue
        for variant, trigger in enumerate(group, start=1):
            trigger.name = f"{name} (p{player}, legacy variant {variant})"

    empty_triggers = [
        trigger
        for trigger in ctx.tm.triggers
        if not trigger.conditions and not trigger.effects
    ]
    if len(empty_triggers) != 810:
        raise RuntimeError(
            f"expected 810 empty imported trigger shells, found {len(empty_triggers)}"
        )
    empty_ids = {trigger.trigger_id for trigger in empty_triggers}
    empty_by_id = {trigger.trigger_id: trigger for trigger in empty_triggers}
    incoming_conditions = [
        condition
        for trigger in ctx.tm.triggers
        for condition in trigger.conditions
        if condition.condition_type == ConditionId.TRIGGER_ACTIVE
        and condition.trigger_id in empty_ids
    ]
    incoming_effects = [
        effect
        for trigger in ctx.tm.triggers
        for effect in trigger.effects
        if effect.effect_type
        in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
        and effect.trigger_id in empty_ids
    ]
    if incoming_conditions or len(incoming_effects) != 16 or any(
        effect.effect_type != EffectId.DEACTIVATE_TRIGGER
        or re.fullmatch(
            r"(?:re )?no wall \(p[1-8]\)",
            empty_by_id[effect.trigger_id].name,
        )
        is None
        for effect in incoming_effects
    ):
        raise RuntimeError(
            "empty trigger shells gained meaningful references: "
            f"{len(incoming_conditions)} conditions and {len(incoming_effects)} effects"
        )

    for trigger in ctx.tm.triggers:
        trigger.effects = [
            effect
            for effect in trigger.effects
            if not (
                effect.effect_type == EffectId.DEACTIVATE_TRIGGER
                and effect.trigger_id in empty_ids
            )
        ]
    ctx.tm.remove_triggers([trigger.trigger_id for trigger in empty_triggers])

    # The builder appends the bundled ``XS SCRIPT`` trigger after ``build`` returns.
    if len(ctx.tm.triggers) != 2_326:
        raise RuntimeError(
            f"expected 2,326 compact pre-XS triggers, found {len(ctx.tm.triggers):,}"
        )
    if any(
        not trigger.conditions and not trigger.effects for trigger in ctx.tm.triggers
    ):
        raise RuntimeError("empty triggers remained after graph compaction")
    names = [trigger.name for trigger in ctx.tm.triggers]
    duplicate_names = sorted(
        name for name in set(names) if names.count(name) > 1
    )
    if duplicate_names:
        raise RuntimeError(
            f"duplicate trigger names remained after compaction: {duplicate_names}"
        )


def _configure_equalizer(trigger, player: PlayerId) -> None:
    """Keep stockpiles at zero after a real player is confirmed in the slot."""
    _reset_trigger(trigger)
    trigger.name = f"Resource Equalizer P{int(player)}"
    trigger.looping = 1
    trigger.new_condition.player_defeated(source_player=player, inverted=1)
    trigger.new_condition.timer(timer=1)
    for resource in RESOURCE_STOCKPILES:
        trigger.new_effect.modify_resource(
            quantity=0,
            tribute_list=resource,
            source_player=player,
            operation=Operation.SET,
        )
    for attribute in (Attribute.RESEARCH_COST_MODIFIER, *SCORE_NEUTRAL_ATTRIBUTES):
        trigger.new_effect.modify_resource(
            quantity=0,
            tribute_list=attribute,
            source_player=player,
            operation=Operation.SET,
        )


def _configure_free_costs(trigger, player: PlayerId) -> None:
    """Make repair costs free; XS handles every runtime object's purchase cost."""
    _reset_trigger(trigger)
    trigger.name = f"Free Costs P{int(player)}"

    for attribute in FREE_PLAYER_ATTRIBUTES:
        trigger.new_effect.modify_resource(
            quantity=0,
            tribute_list=attribute,
            source_player=player,
            operation=Operation.SET,
        )


def _configure_combat_hud_header(trigger) -> None:
    """Use DE's native right-side objective list without adding a full objective."""
    _reset_trigger(trigger)
    trigger.name = "Combat HUD Header"
    trigger.short_description = "P# | K | D | R"
    trigger.display_on_screen = 1
    trigger.description_order = 19
    trigger.enabled = 1
    trigger.header = 1
    trigger.mute_objectives = 1
    trigger.new_condition.player_defeated(source_player=PlayerId.GAIA)


def _reset_unsafe_vote_kick(ctx: BuildContext) -> None:
    """Clear the legacy vote-kick path before rebuilding it safely.

    During DE's first trigger pass, closed slots can briefly appear alive while
    their missing vote markers satisfy the inverted area checks. In a sparse
    lobby that can activate a ``Kick P#`` trigger and defeat a real player at
    tick zero. The rebuilt path is added after color/runtime mapping and the V2
    object transformation are complete.
    """
    vote_detectors = 0
    kick_actions = 0
    for trigger in ctx.tm.triggers:
        if VOTE_KICK_NAME.fullmatch(trigger.name):
            _reset_trigger(trigger)
            vote_detectors += 1
        elif re.fullmatch(r"Kick P[1-8]", trigger.name):
            _reset_trigger(trigger)
            kick_actions += 1
    if vote_detectors != 24 or kick_actions != 8:
        raise RuntimeError(
            f"expected 24 vote-kick detectors and 8 kick actions, found {vote_detectors} and {kick_actions}"
        )


def _remove_legacy_edge_deletion_strips(ctx: BuildContext) -> None:
    """Disable invisible strips that deleted every owned object at the map edges."""
    removed = 0
    for trigger in ctx.tm.triggers:
        if not EDGE_KILL_ZONE_NAME.fullmatch(trigger.name):
            continue
        original_name = trigger.name
        _reset_trigger(trigger)
        trigger.name = f"Legacy Edge Delete Disabled ({original_name})"
        removed += 1
    if removed != 32:
        raise RuntimeError(f"expected 32 legacy edge delete triggers, disabled {removed}")


def _disable_legacy_no_wall_cleanup(ctx: BuildContext) -> None:
    """Keep the complete symmetric side walls from being deleted at startup."""
    disabled = 0
    for trigger in ctx.tm.triggers:
        if re.fullmatch(r"(?:re )?no wall \(p[1-8]\)", trigger.name) is None:
            continue
        _reset_trigger(trigger)
        disabled += 1
    if disabled != 16:
        raise RuntimeError(
            f"expected 16 legacy no-wall triggers, disabled {disabled}"
        )


def _configure_sparse_goth_palisade_bonus(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Apply the earned Goth Palisade bonus fairly in compacted lobbies."""
    bonuses = []
    for trigger in ctx.tm.triggers:
        if re.fullmatch(r"hp \(p[1-8]\)", trigger.name) is None:
            continue
        if not any(
            condition.condition_type == ConditionId.OBJECTS_IN_AREA
            and condition.object_list == BuildingInfo.PALISADE_WALL.ID
            for condition in trigger.conditions
        ):
            continue
        bonuses.append(trigger)
    if len(bonuses) != 8:
        raise RuntimeError(
            f"expected eight Goth Palisade bonus triggers, found {len(bonuses)}"
        )
    legacy_ids = {trigger.trigger_id for trigger in bonuses}
    for trigger in bonuses:
        _reset_trigger(trigger)
        trigger.name = f"Legacy Goth Palisade Bonus Disabled #{trigger.trigger_id}"
    for trigger in ctx.tm.triggers:
        trigger.effects = [
            effect
            for effect in trigger.effects
            if not (
                effect.effect_type == EffectId.ACTIVATE_TRIGGER
                and effect.trigger_id in legacy_ids
            )
        ]
    for player in PLAYERS:
        x1, y1 = v2_cell_for_player(player, 24, 48)
        x2, y2 = v2_cell_for_player(player, 24, 59)
        area = {
            "area_x1": min(x1, x2),
            "area_y1": min(y1, y2),
            "area_x2": max(x1, x2),
            "area_y2": max(y1, y2),
        }
        for world_player in _possible_world_players(player):
            trigger = ctx.tm.add_trigger(
                f"Goth Palisade Bonus S{int(player)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            trigger.new_condition.variable_value(
                quantity=1,
                variable=active_variables[player],
                comparison=Comparison.EQUAL,
            )
            trigger.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[player],
                comparison=Comparison.EQUAL,
            )
            trigger.new_condition.research_technology(
                source_player=world_player,
                technology=TechInfo.ELITE_HUSKARL.ID,
            )
            trigger.new_condition.objects_in_area(
                quantity=12,
                object_list=BuildingInfo.PALISADE_WALL.ID,
                source_player=world_player,
                **area,
            )
            trigger.new_effect.change_object_hp(
                quantity=2750,
                object_list_unit_id=BuildingInfo.PALISADE_WALL.ID,
                source_player=world_player,
                operation=Operation.ADD,
                **area,
            )


def _configure_sparse_goth_barracks_restriction(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Keep the Anarchy Barracks restriction correct in compacted lobbies."""
    legacy = {
        family: {
            color: _unique_trigger(ctx, f"goth {family} (p{int(color)})")
            for color in PLAYERS
        }
        for family in ("barracks", "anarchy", "imp")
    }
    legacy_ids = {
        trigger.trigger_id
        for family in legacy.values()
        for trigger in family.values()
    }
    for family, by_color in legacy.items():
        for trigger in by_color.values():
            old_id = trigger.trigger_id
            _reset_trigger(trigger)
            trigger.name = f"Legacy Goth {family.title()} Disabled #{old_id}"
    for trigger in ctx.tm.triggers:
        trigger.effects = [
            effect
            for effect in trigger.effects
            if not (
                effect.effect_type
                in {EffectId.ACTIVATE_TRIGGER, EffectId.DEACTIVATE_TRIGGER}
                and effect.trigger_id in legacy_ids
            )
        ]

    whole_map = {"area_x1": 0, "area_y1": 0, "area_x2": 143, "area_y2": 143}
    for color in PLAYERS:
        for world_player in _possible_world_players(color):
            restriction = ctx.tm.add_trigger(
                f"Goth Barracks Restriction S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
                enabled=0,
                looping=1,
            )
            restriction.new_condition.timer(timer=1)
            restriction.new_condition.objects_in_area(
                quantity=1,
                object_list=BuildingInfo.BARRACKS.ID,
                source_player=world_player,
                **whole_map,
            )
            restriction.new_effect.kill_object(
                object_list_unit_id=BuildingInfo.BARRACKS.ID,
                source_player=world_player,
                **whole_map,
            )
            restriction.new_effect.send_chat(
                source_player=world_player,
                message="Goths cannot build Barracks until Imperial Age.",
            )

            anarchy = ctx.tm.add_trigger(
                f"Goth Anarchy S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            anarchy.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            anarchy.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            anarchy.new_condition.research_technology(
                source_player=world_player,
                technology=TechInfo.ANARCHY.ID,
            )
            anarchy.new_effect.activate_trigger(
                trigger_id=restriction.trigger_id
            )
            anarchy.new_effect.send_chat(
                source_player=world_player,
                message=(
                    "Anarchy researched: Barracks remain unavailable until "
                    "Imperial Age."
                ),
            )

            imperial = ctx.tm.add_trigger(
                f"Goth Imperial S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            imperial.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            imperial.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            imperial.new_condition.research_technology(
                source_player=world_player,
                technology=TechInfo.IMPERIAL_AGE.ID,
            )
            imperial.new_effect.deactivate_trigger(
                trigger_id=restriction.trigger_id
            )
            imperial.new_effect.deactivate_trigger(trigger_id=anarchy.trigger_id)


def _disable_fixed_color_kill_announcements(ctx: BuildContext) -> None:
    """Remove duplicate announcements that report runtime colors as map colors."""
    disabled = 0
    for trigger in ctx.tm.triggers:
        has_legacy_kill_chat = any(
            effect.effect_type == EffectId.SEND_CHAT
            and re.match(r"<[^>]+> Kills:", effect.message or "")
            for effect in trigger.effects
        )
        thresholds = {
            condition.quantity
            for condition in trigger.conditions
            if condition.condition_type == ConditionId.ACCUMULATE_ATTRIBUTE
            and condition.attribute == Attribute.UNITS_KILLED
        }
        if has_legacy_kill_chat and thresholds & {10, 20, 30, 2_000}:
            original_id = trigger.trigger_id
            _reset_trigger(trigger)
            trigger.name = f"Legacy Fixed-Color Kill Notice Disabled #{original_id}"
            disabled += 1
    if disabled != 12:
        raise RuntimeError(
            f"expected 12 fixed-color kill notices, disabled {disabled}"
        )


def _optimize_legacy_polling(ctx: BuildContext) -> None:
    """Throttle persistent checks and make one-shot legacy events truly one-shot."""
    counts = {"hay": 0, "tc": 0, "goth imp": 0}
    for trigger in ctx.tm.triggers:
        family = next(
            (
                candidate
                for candidate in counts
                if re.fullmatch(
                    rf"{re.escape(candidate)}[1-4]? \(p[1-8]\)",
                    trigger.name,
                )
            ),
            None,
        )
        if family is None:
            continue
        if not any(
            condition.condition_type == ConditionId.TIMER
            for condition in trigger.conditions
        ):
            trigger.new_condition.timer(timer=1)
        if family in {"hay", "goth imp"}:
            trigger.looping = 0
        counts[family] += 1
    expected = {"hay": 32, "tc": 8, "goth imp": 8}
    if counts != expected:
        raise RuntimeError(
            f"unexpected legacy polling families: expected {expected}, found {counts}"
        )


def _protect_rear_routes_from_legacy_base_cleanup(ctx: BuildContext) -> None:
    """Keep legacy anti-treb/front-wall cleanup away from the new rear routes."""
    anti_treb_bounds = {
        1: (39, 19, 66, 25),
        2: (75, 19, 102, 26),
        3: (18, 38, 25, 64),
        4: (114, 38, 123, 65),
        5: (18, 74, 24, 101),
        6: (114, 74, 123, 101),
        7: (39, 116, 66, 123),
        8: (74, 116, 102, 123),
    }
    anti_treb_count = 0
    for trigger in ctx.tm.triggers:
        match = ANTI_TREB_NAME.fullmatch(trigger.name)
        if match is None:
            continue
        kill_effects = [effect for effect in trigger.effects if effect.effect_type == EffectId.KILL_OBJECT]
        if len(kill_effects) != 1:
            raise RuntimeError(f"expected one anti-treb effect in {trigger.name!r}")
        (
            kill_effects[0].area_x1,
            kill_effects[0].area_y1,
            kill_effects[0].area_x2,
            kill_effects[0].area_y2,
        ) = anti_treb_bounds[int(match.group(1))]
        if not any(
            condition.condition_type == ConditionId.TIMER
            for condition in trigger.conditions
        ):
            trigger.new_condition.timer(timer=1)
        anti_treb_count += 1
    if anti_treb_count != 64:
        raise RuntimeError(f"expected 64 anti-treb triggers, adjusted {anti_treb_count}")

    wall_cleanup_bounds = {
        1: (43, 17, 64, 38),
        2: (79, 17, 100, 38),
        3: (17, 43, 38, 64),
        4: (105, 43, 126, 64),
        5: (17, 79, 38, 100),
        6: (105, 79, 126, 100),
        7: (43, 105, 64, 126),
        8: (79, 105, 100, 126),
    }
    for player, bounds in wall_cleanup_bounds.items():
        trigger = _unique_trigger(ctx, f"Elimina Walls P{player}")
        remove_effects = [
            effect for effect in trigger.effects if effect.effect_type == EffectId.REMOVE_OBJECT
        ]
        if len(remove_effects) != 2:
            raise RuntimeError(f"expected two wall-cleanup effects for P{player}")
        for effect in remove_effects:
            effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2 = bounds


def _clear_legacy_resource_score_triggers(ctx: BuildContext) -> None:
    """Remove the remaining old 100k tribute loops that inflated score."""
    for player in range(1, 9):
        _reset_trigger(_unique_trigger(ctx, f"res (p{player})"))


def _zero_starting_resources(ctx: BuildContext) -> None:
    for player in PLAYERS:
        settings = ctx.pm.players[player]
        settings.food = 0
        settings.wood = 0
        settings.stone = 0
        settings.gold = 0


def _disable_castle_trebuchets(ctx: BuildContext) -> None:
    """Remove both Trebuchet forms from every player's trainable roster."""
    trebuchets = (UnitInfo.TREBUCHET.ID, UnitInfo.TREBUCHET_PACKED.ID)
    for player in PLAYERS:
        disabled_units = ctx.pm.players[player].disabled_units
        for unit_id in trebuchets:
            if unit_id not in disabled_units:
                disabled_units.append(unit_id)


def _add_color_runtime_variables(ctx: BuildContext):
    """Create the color-to-runtime state shared by sparse-safe systems."""
    active_variables = {
        player: ctx.tm.add_variable(
            f"p{int(player)}coloractive",
            variable_id=COLOR_ACTIVE_VARIABLE_BASE + int(player) - 1,
        ).variable_id
        for player in PLAYERS
    }
    world_variables = {
        player: ctx.tm.add_variable(
            f"p{int(player)}worldplayer",
            variable_id=COLOR_WORLD_VARIABLE_BASE + int(player) - 1,
        ).variable_id
        for player in PLAYERS
    }
    eliminated_variables = {
        player: ctx.tm.add_variable(
            f"p{int(player)}coloreliminated",
            variable_id=COLOR_ELIMINATED_VARIABLE_BASE + int(player) - 1,
        ).variable_id
        for player in PLAYERS
    }
    match_ready_variable = ctx.tm.add_variable(
        "colorsidesready",
        variable_id=MATCH_READY_VARIABLE_ID,
    ).variable_id
    return (
        active_variables,
        world_variables,
        eliminated_variables,
        match_ready_variable,
    )


def _add_color_owner_detection(ctx: BuildContext, active_variables, world_variables) -> None:
    """Latch each scenario color to the runtime owner of its Castle row.

    Sparse lobbies compact occupied colors into lower runtime player numbers.
    Detecting the actual owner of a color's fixed starting Castles avoids any
    ambiguity in the indexing convention of ``xsGetWorldPlayerId`` and gives
    triggers and XS one shared, map-verified mapping.
    """
    configured = 0
    for color in PLAYERS:
        area_x1, area_y1, area_x2, area_y2 = BASE_CASTLE_AREAS[color]
        for world_player in _possible_world_players(color):
            detector = ctx.tm.add_trigger(
                f"Color Owner Detect S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
                looping=1,
            )
            detector.new_condition.timer(timer=1)
            detector.new_condition.variable_value(
                quantity=0,
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            detector.new_condition.objects_in_area(
                quantity=1,
                object_list=BuildingInfo.CASTLE.ID,
                source_player=world_player,
                area_x1=area_x1,
                area_y1=area_y1,
                area_x2=area_x2,
                area_y2=area_y2,
            )
            detector.new_effect.change_variable(
                quantity=int(world_player),
                operation=Operation.SET,
                variable=world_variables[color],
            )
            detector.new_effect.change_variable(
                quantity=1,
                operation=Operation.SET,
                variable=active_variables[color],
            )
            detector.new_effect.deactivate_trigger(trigger_id=detector.trigger_id)
            configured += 1
    if configured != 36:
        raise RuntimeError(f"expected 36 color-owner detectors, configured {configured}")


def _configure_custom_team_victory(
    ctx: BuildContext,
    active_variables,
    world_variables,
    eliminated_variables,
    match_ready_variable,
) -> None:
    """Resolve defeat and victory through each occupied color's runtime player.

    DE compacts sparse colors into consecutive runtime player numbers.  A fixed
    ``P5`` defeat effect therefore targets runtime P5, not the person occupying
    teal when teal has been compacted to runtime P2.  Runtime variables written
    by XS keep every declaration attached to the selected color instead.
    """
    ctx.scenario.option_manager.victory_condition = VictoryCondition.CUSTOM
    ctx.scenario.option_manager.victory_custom_conditions_required = False
    ctx.scenario.sections["GlobalVictory"].retriever_map["conquest_required"].set_data(0)

    legacy_cleanup_by_color = {
        color: tuple(
            _unique_trigger(ctx, f"{family} (p{int(color)})")
            for family in ("units", "walls", "units2", "units3")
        )
        for color in PLAYERS
    }
    legacy_cleanup_ids = {
        trigger.trigger_id
        for triggers in legacy_cleanup_by_color.values()
        for trigger in triggers
    }
    for _color, triggers in legacy_cleanup_by_color.items():
        for trigger in triggers:
            original_name = trigger.name
            _reset_trigger(trigger)
            trigger.name = original_name
    for color in PLAYERS:
        trigger = _unique_trigger(ctx, f"remove (p{int(color)})")
        original_name = trigger.name
        _reset_trigger(trigger)
        trigger.name = original_name

    sides = (PLAYERS[:4], PLAYERS[4:])
    for color in PLAYERS:
        castle_loss = _unique_trigger(ctx, f"castle (p{int(color)})")
        area_x1, area_y1, area_x2, area_y2 = BASE_CASTLE_AREAS[color]
        castle_loss.effects = [
            effect
            for effect in castle_loss.effects
            if not (
                effect.effect_type == EffectId.ACTIVATE_TRIGGER
                and effect.trigger_id in legacy_cleanup_ids
            )
        ]
        for world_player in _possible_world_players(color):
            defeat = ctx.tm.add_trigger(
                f"Color Defeat Resolve S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
                enabled=0,
            )
            defeat.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            defeat.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            defeat.new_condition.variable_value(
                quantity=1,
                variable=match_ready_variable,
                comparison=Comparison.EQUAL,
            )
            # A resolver activated by a stale or remapped reference must not be
            # able to defeat a live player. Independently require that no Castle
            # remains in that color's four-Castle objective row.
            defeat.new_condition.objects_in_area(
                quantity=1,
                object_list=BuildingInfo.CASTLE.ID,
                source_player=world_player,
                area_x1=area_x1,
                area_y1=area_y1,
                area_x2=area_x2,
                area_y2=area_y2,
                inverted=1,
            )
            defeat.new_effect.change_variable(
                quantity=1,
                operation=Operation.SET,
                variable=eliminated_variables[color],
            )
            defeat.new_effect.change_variable(
                quantity=0,
                operation=Operation.SET,
                variable=active_variables[color],
            )
            defeat.new_effect.remove_object(
                source_player=world_player,
                area_x1=0,
                area_y1=0,
                area_x2=143,
                area_y2=143,
            )
            defeat.new_effect.declare_victory(
                source_player=world_player,
                enabled=0,
            )
            castle_loss.new_effect.activate_trigger(trigger_id=defeat.trigger_id)

            resigned = ctx.tm.add_trigger(
                f"Color Runtime Defeated S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            resigned.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            resigned.new_condition.variable_value(
                quantity=1,
                variable=match_ready_variable,
                comparison=Comparison.EQUAL,
            )
            resigned.new_condition.player_defeated(source_player=world_player)
            resigned.new_effect.change_variable(
                quantity=1,
                operation=Operation.SET,
                variable=eliminated_variables[color],
            )
            resigned.new_effect.change_variable(
                quantity=0,
                operation=Operation.SET,
                variable=active_variables[color],
            )

    # Latch only after at least one occupied color has been detected on each
    # side. This prevents the three-second victory pass from ending a solo map
    # inspection or racing ahead of sparse-lobby color discovery. Once latched,
    # it remains set so normal elimination can still resolve the match.
    for left_color in sides[0]:
        for right_color in sides[1]:
            ready = ctx.tm.add_trigger(
                f"Color Match Ready L{int(left_color)} R{int(right_color)}",
                description_stid=0,
                short_description_stid=0,
                looping=1,
            )
            ready.new_condition.timer(timer=LOBBY_SETTLE_SECONDS)
            # The world-player mapping persists after a resignation, while the
            # live-active bit correctly drops to zero.  Latch readiness from
            # occupied mappings so an early resignation cannot leave both the
            # defeat resolver and the opposing victory path blocked forever.
            ready.new_condition.variable_value(
                quantity=1,
                variable=world_variables[left_color],
                comparison=Comparison.LARGER_OR_EQUAL,
            )
            ready.new_condition.variable_value(
                quantity=1,
                variable=world_variables[right_color],
                comparison=Comparison.LARGER_OR_EQUAL,
            )
            ready.new_effect.change_variable(
                quantity=1,
                operation=Operation.SET,
                variable=match_ready_variable,
            )
            ready.new_effect.deactivate_trigger(trigger_id=ready.trigger_id)

    for side, opponents in ((sides[0], sides[1]), (sides[1], sides[0])):
        for color in side:
            for world_player in _possible_world_players(color):
                victory = ctx.tm.add_trigger(
                    f"Color Team Victory S{int(color)} W{int(world_player)}",
                    description_stid=0,
                    short_description_stid=0,
                )
                victory.new_condition.timer(timer=VICTORY_RESOLVE_SECONDS)
                victory.new_condition.variable_value(
                    quantity=1,
                    variable=active_variables[color],
                    comparison=Comparison.EQUAL,
                )
                victory.new_condition.variable_value(
                    quantity=int(world_player),
                    variable=world_variables[color],
                    comparison=Comparison.EQUAL,
                )
                victory.new_condition.variable_value(
                    quantity=1,
                    variable=match_ready_variable,
                    comparison=Comparison.EQUAL,
                )
                for opponent in opponents:
                    victory.new_condition.variable_value(
                        quantity=0,
                        variable=active_variables[opponent],
                        comparison=Comparison.EQUAL,
                    )
                victory.new_effect.declare_victory(
                    source_player=world_player,
                    enabled=1,
                )


def _render_color_spawn_xs() -> str:
    assignments = []
    for civilization, (unit_id, population_cap, interval) in CIV_SPAWN_RULES.items():
        assignments.extend(
            (
                f"    xsArraySetInt(gCbaUnitByCiv, {civilization}, {unit_id});",
                f"    xsArraySetInt(gCbaCapByCiv, {civilization}, {population_cap});",
                f"    xsArraySetInt(gCbaIntervalByCiv, {civilization}, {interval});",
            )
        )
    for civilization, (name, threshold) in CIV_BUILDER_RULES.items():
        assignments.extend(
            (
                f'    xsArraySetString(gCbaNameByCiv, {civilization}, "{name}");',
                f"    xsArraySetInt(gCbaBuilderThresholdByCiv, {civilization}, {threshold});",
            )
        )

    coordinate_branches = []
    for index, (scenario_player, points) in enumerate(SPAWN_POINTS.items()):
        prefix = "if" if index == 0 else "else if"
        coordinate_branches.append(f"    {prefix} (scenarioPlayer == {int(scenario_player)}) {{")
        coordinate_branches.extend(
            f"        xsCreateUnit(unitId, worldPlayer, vector({x}, {y}, -1), false, false, false);"
            for x, y in points
        )
        coordinate_branches.append("    }")

    spawn_calls = "\n".join(f"    cbaSpawnColor({int(player)});" for player in PLAYERS)
    builder_queue_calls = "\n".join(f"    cbaQueueColorBuilders({int(player)});" for player in PLAYERS)
    combat_hud_calls = "\n".join(f"    cbaUpdateCombatRow({int(player)});" for player in PLAYERS)
    color_runtime_calls = "\n".join(
        f"    cbaUpdateColorRuntime({int(player)});" for player in PLAYERS
    )
    score_neutral_lines = "\n".join(
        f"    xsSetPlayerAttribute(worldPlayer, {int(attribute)}, 0);"
        for attribute in SCORE_NEUTRAL_ATTRIBUTES
    )
    return f"""// Sparse-lobby color-aware army spawning.
// DE compacts occupied colors into consecutive runtime player numbers. The
// legacy trigger loops bind both concepts to one number; xsGetWorldPlayerId
// provides the required color -> runtime mapping.

int gCbaNextSpawnByColor = -1;
int gCbaUnitByCiv = -1;
int gCbaCapByCiv = -1;
int gCbaIntervalByCiv = -1;
int gCbaNameByCiv = -1;
int gCbaBuilderThresholdByCiv = -1;
int gCbaEarnedBuilderPairsByColor = -1;

int cbaWorldPlayerForColor(int scenarioPlayer = 0) {{
    return(xsTriggerVariable(
        {COLOR_WORLD_VARIABLE_BASE} + scenarioPlayer - 1
    ));
}}

void cbaCreateWave(int scenarioPlayer = 0, int worldPlayer = 0, int unitId = -1) {{
{chr(10).join(coordinate_branches)}
}}

void cbaSpawnColor(int scenarioPlayer = 0) {{
    int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);
    if (worldPlayer < 1 || xsGetPlayerInGame(worldPlayer) == false) {{
        return;
    }}

    int civilization = xsGetPlayerCivilization(worldPlayer);
    if (civilization < 1 || civilization >= xsArrayGetSize(gCbaUnitByCiv)) {{
        return;
    }}
    int unitId = xsArrayGetInt(gCbaUnitByCiv, civilization);
    int populationCap = xsArrayGetInt(gCbaCapByCiv, civilization);
    int interval = xsArrayGetInt(gCbaIntervalByCiv, civilization);
    if (unitId < 0 || populationCap < 1 || interval < 1) {{
        return;
    }}

    int now = xsGetGameTime();
    int nextSpawn = xsArrayGetInt(gCbaNextSpawnByColor, scenarioPlayer);
    if (nextSpawn == 0) {{
        xsArraySetInt(gCbaNextSpawnByColor, scenarioPlayer, now + interval);
        return;
    }}
    if (now < nextSpawn) {{
        return;
    }}
    if (xsPlayerAttribute(worldPlayer, cAttributeMilitaryPopulation) < populationCap) {{
        cbaCreateWave(scenarioPlayer, worldPlayer, unitId);
        xsArraySetInt(gCbaNextSpawnByColor, scenarioPlayer, now + interval);
    }}
}}

void cbaQueueColorBuilders(int scenarioPlayer = 0) {{
    int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);
    if (worldPlayer < 1 || xsGetPlayerInGame(worldPlayer) == false) {{
        return;
    }}

    int civilization = xsGetPlayerCivilization(worldPlayer);
    if (civilization < 1 || civilization >= xsArrayGetSize(gCbaBuilderThresholdByCiv)) {{
        return;
    }}
    int threshold = xsArrayGetInt(gCbaBuilderThresholdByCiv, civilization);
    if (threshold < 1) {{
        return;
    }}

    int currentRazings = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeRazings));
    int earnedPairs = currentRazings - threshold + 1;
    if (earnedPairs < 0) {{
        earnedPairs = 0;
    }}
    int previousEarnedPairs = xsArrayGetInt(gCbaEarnedBuilderPairsByColor, scenarioPlayer);
    if (earnedPairs > previousEarnedPairs) {{
        int pendingPairs = xsTriggerVariable(scenarioPlayer - 1);
        xsSetTriggerVariable(
            scenarioPlayer - 1,
            pendingPairs + earnedPairs - previousEarnedPairs
        );
        xsArraySetInt(gCbaEarnedBuilderPairsByColor, scenarioPlayer, earnedPairs);
    }}
}}

void cbaAnnounceLocalBuilderGoal() {{
    int localPlayer = xsGetLocalPlayerId();
    if (localPlayer < 1 || xsGetPlayerInGame(localPlayer) == false) {{
        return;
    }}

    int civilization = xsGetPlayerCivilization(localPlayer);
    if (civilization < 1 || civilization >= xsArrayGetSize(gCbaBuilderThresholdByCiv)) {{
        return;
    }}
    int threshold = xsArrayGetInt(gCbaBuilderThresholdByCiv, civilization);
    string civilizationName = xsArrayGetString(gCbaNameByCiv, civilization);
    if (threshold > 0) {{
        xsChatData(
            "[CBA] " + civilizationName + ": first builder pair after " + threshold +
            " building razings; each later razing earns another pair."
        );
    }}
}}

void cbaRefreshCombatValues(int worldPlayer = 0) {{
{score_neutral_lines}
    int kills = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeKills));
    int deaths = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeKilledByOthers));
    int razings = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeRazings));
    int razed = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeRazedByOthers));
    xsSetPlayerAttribute(worldPlayer, cAttributeTotalValueOfKills, kills * 100);
    xsSetPlayerAttribute(worldPlayer, cAttributeValueKilledByOthers, deaths * 100);
    xsSetPlayerAttribute(worldPlayer, cAttributeTotalValueOfRazings, razings * 500);
    xsSetPlayerAttribute(worldPlayer, cAttributeValueRazedByOthers, razed * 500);
}}

void cbaUpdateCombatRow(int scenarioPlayer = 0) {{
    int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);
    if (worldPlayer < 1 || xsGetPlayerInGame(worldPlayer) == false) {{
        return;
    }}
    int kills = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeKills));
    int deaths = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeKilledByOthers));
    int razings = xsCeilToInt(xsPlayerAttribute(worldPlayer, cAttributeRazings));
    int variableBase = 8 + ((scenarioPlayer - 1) * 3);
    xsSetTriggerVariable(variableBase, kills);
    xsSetTriggerVariable(variableBase + 1, deaths);
    xsSetTriggerVariable(variableBase + 2, razings);
    cbaRefreshCombatValues(worldPlayer);
}}

void cbaUpdateColorRuntime(int scenarioPlayer = 0) {{
    int worldPlayer = cbaWorldPlayerForColor(scenarioPlayer);
    int activeFlag = 0;
    int eliminatedFlag = xsTriggerVariable(
        {COLOR_ELIMINATED_VARIABLE_BASE} + scenarioPlayer - 1
    );
    if (worldPlayer >= 1) {{
        if (eliminatedFlag == 0 && xsGetPlayerInGame(worldPlayer)) {{
            activeFlag = 1;
        }}
    }}
    xsSetTriggerVariable(
        {COLOR_ACTIVE_VARIABLE_BASE} + scenarioPlayer - 1,
        activeFlag
    );
}}

void main() {{
    gCbaNextSpawnByColor = xsArrayCreateInt(9, 0, "cbaNextSpawnByColor");
    gCbaUnitByCiv = xsArrayCreateInt(60, -1, "cbaUnitByCiv");
    gCbaCapByCiv = xsArrayCreateInt(60, 0, "cbaCapByCiv");
    gCbaIntervalByCiv = xsArrayCreateInt(60, 0, "cbaIntervalByCiv");
    gCbaNameByCiv = xsArrayCreateString(60, "Unknown civilization", "cbaNameByCiv");
    gCbaBuilderThresholdByCiv = xsArrayCreateInt(60, 0, "cbaBuilderThresholdByCiv");
    gCbaEarnedBuilderPairsByColor = xsArrayCreateInt(
        9, 0, "cbaEarnedBuilderPairsByColor"
    );
{chr(10).join(assignments)}
    for (worldPlayer = 1; <= xsGetNumPlayers()) {{
        int technologyCount = xsGetPlayerNumberOfTechs(worldPlayer);
        for (technology = 0; < technologyCount) {{
            xsEffectAmount(cModifyTech, technology, cAttrSetFoodCost, 0, worldPlayer);
            xsEffectAmount(cModifyTech, technology, cAttrSetWoodCost, 0, worldPlayer);
            xsEffectAmount(cModifyTech, technology, cAttrSetStoneCost, 0, worldPlayer);
            xsEffectAmount(cModifyTech, technology, cAttrSetGoldCost, 0, worldPlayer);
        }}
        int objectCount = xsGetPlayerNumberOfObjects(worldPlayer);
        for (objectId = 0; < objectCount) {{
            xsEffectAmount(cSetAttribute, objectId, cFoodCost, 0, worldPlayer);
            xsEffectAmount(cSetAttribute, objectId, cWoodCost, 0, worldPlayer);
            xsEffectAmount(cSetAttribute, objectId, cStoneCost, 0, worldPlayer);
            xsEffectAmount(cSetAttribute, objectId, cGoldCost, 0, worldPlayer);
        }}
        cbaRefreshCombatValues(worldPlayer);
    }}
}}

rule cbaColorArmySpawns
    active
    minInterval 1
{{
{spawn_calls}
}}

rule cbaCombatHudValues
    active
    minInterval 2
{{
{combat_hud_calls}
}}

rule cbaColorRuntimeState
    active
    minInterval 1
{{
{color_runtime_calls}
}}

rule cbaBuilderRewardQueue
    active
    minInterval 1
{{
{builder_queue_calls}
}}

rule cbaBuilderRewardInfo
    active
    minInterval 1
{{
    if (xsGetGameTime() >= 4) {{
        cbaAnnounceLocalBuilderGoal();
        xsDisableSelf();
    }}
}}
"""


def _replace_legacy_army_spawns(ctx: BuildContext) -> None:
    """Spawn by selected color while addressing the compacted runtime owner."""
    disabled = 0
    legacy_ids = set()
    for trigger in ctx.tm.triggers:
        create_effects = [
            effect for effect in trigger.effects if effect.effect_type == EffectId.CREATE_OBJECT
        ]
        is_army_loop = (
            trigger.looping
            and len(create_effects) == 4
            and any(
                condition.condition_type == ConditionId.OWN_FEWER_OBJECTS for condition in trigger.conditions
            )
            and any(condition.condition_type == ConditionId.TIMER for condition in trigger.conditions)
        )
        if not is_army_loop:
            continue
        original_id = trigger.trigger_id
        legacy_ids.add(original_id)
        _reset_trigger(trigger)
        trigger.name = f"Legacy Army Spawn Disabled #{original_id}"
        disabled += 1
    if disabled != len(CIV_SPAWN_RULES) * len(PLAYERS):
        raise RuntimeError(f"expected {len(CIV_SPAWN_RULES) * len(PLAYERS)} army loops, disabled {disabled}")
    for trigger in ctx.tm.triggers:
        trigger.effects = [
            effect
            for effect in trigger.effects
            if not (
                effect.effect_type == EffectId.ACTIVATE_TRIGGER
                and effect.trigger_id in legacy_ids
            )
        ]

    canonical_move_tasks = {
        family: deepcopy(
            [
                effect
                for effect in _unique_trigger(ctx, f"{family} (p3)").effects
                if effect.effect_type == EffectId.TASK_OBJECT
            ]
        )
        for family in ("move", "move short", "move long")
    }
    if any(len(tasks) != 4 for tasks in canonical_move_tasks.values()):
        raise RuntimeError("expected four canonical P3 task effects per move family")

    for scenario_player in PLAYERS:
        movement_tasks = {}
        for family, canonical_tasks in canonical_move_tasks.items():
            target = _unique_trigger(ctx, f"{family} (p{int(scenario_player)})")
            target_tasks = [
                effect
                for effect in target.effects
                if effect.effect_type == EffectId.TASK_OBJECT
            ]
            if len(target_tasks) != 4:
                raise RuntimeError(
                    f"expected four task effects in {target.name!r}, "
                    f"found {len(target_tasks)}"
                )
            for effect, source, (spawn_x, spawn_y) in zip(
                target_tasks,
                canonical_tasks,
                SPAWN_POINTS[scenario_player],
                strict=True,
            ):
                effect.area_x1 = spawn_x - 1
                effect.area_y1 = spawn_y - 1
                effect.area_x2 = spawn_x + 1
                effect.area_y2 = spawn_y + 1
                effect.action_type = ActionType.MOVE
                effect.location_x, effect.location_y = v2_cell_for_player(
                    scenario_player,
                    source.location_x,
                    source.location_y,
                )
            if not any(
                condition.condition_type == ConditionId.TIMER
                for condition in target.conditions
            ):
                target.new_condition.timer(timer=1)
            movement_tasks[family] = target_tasks

        area_x1, area_y1, area_x2, area_y2 = BASE_CASTLE_AREAS[scenario_player]
        sparse_movements = {}
        for world_player in _possible_world_players(scenario_player):
            if world_player == scenario_player:
                continue
            for family, task_effects in movement_tasks.items():
                public_family = {
                    "move": "",
                    "move short": " Short",
                    "move long": " Long",
                }[family]
                movement = ctx.tm.add_trigger(
                    f"Sparse Move{public_family} S{int(scenario_player)} "
                    f"W{int(world_player)}",
                    description_stid=0,
                    short_description_stid=0,
                    enabled=1 if family == "move" else 0,
                    looping=1,
                )
                movement.new_condition.objects_in_area(
                    quantity=1,
                    object_list=BuildingInfo.CASTLE.ID,
                    source_player=world_player,
                    area_x1=area_x1,
                    area_y1=area_y1,
                    area_x2=area_x2,
                    area_y2=area_y2,
                )
                movement.new_condition.timer(timer=1)
                for effect, (spawn_x, spawn_y) in zip(
                    task_effects,
                    SPAWN_POINTS[scenario_player],
                    strict=True,
                ):
                    movement.new_effect.task_object(
                        object_list_unit_id=effect.object_list_unit_id,
                        source_player=world_player,
                        location_x=effect.location_x,
                        location_y=effect.location_y,
                        location_object_reference=effect.location_object_reference,
                        area_x1=spawn_x - 1,
                        area_y1=spawn_y - 1,
                        area_x2=spawn_x + 1,
                        area_y2=spawn_y + 1,
                        object_group=effect.object_group,
                        object_type=effect.object_type,
                        action_type=ActionType.MOVE,
                        max_units_affected=effect.max_units_affected,
                        issue_group_command=effect.issue_group_command,
                        queue_action=effect.queue_action,
                    )
                sparse_movements[family, world_player] = movement

        selected_family = {
            "short": "move short",
            "med": "move",
            "long": "move long",
        }
        for selector_name, chosen_family in selected_family.items():
            selector = _unique_trigger(
                ctx,
                f"{selector_name} (p{int(scenario_player)})",
            )
            if not any(
                condition.condition_type == ConditionId.TIMER
                for condition in selector.conditions
            ):
                selector.new_condition.timer(timer=1)
            for world_player in _possible_world_players(scenario_player):
                if world_player == scenario_player:
                    continue
                for family in canonical_move_tasks:
                    movement = sparse_movements[family, world_player]
                    if family == chosen_family:
                        selector.new_effect.activate_trigger(
                            trigger_id=movement.trigger_id
                        )
                    else:
                        selector.new_effect.deactivate_trigger(
                            trigger_id=movement.trigger_id
                        )

    ctx.add_xs(_render_color_spawn_xs(), label="color-aware army spawning")


def _transformed_v2_area(
    player: PlayerId,
    source_component,
) -> tuple[int, int, int, int] | None:
    coordinates = (
        source_component.area_x1,
        source_component.area_y1,
        source_component.area_x2,
        source_component.area_y2,
    )
    if any(coordinate < 0 for coordinate in coordinates):
        return None
    x1, y1, x2, y2 = coordinates
    corners = (
        v2_cell_for_player(player, x1, y1),
        v2_cell_for_player(player, x1, y2),
        v2_cell_for_player(player, x2, y1),
        v2_cell_for_player(player, x2, y2),
    )
    return (
        min(x for x, _y in corners),
        min(y for _x, y in corners),
        max(x for x, _y in corners),
        max(y for _x, y in corners),
    )


def _copy_v2_component_geometry(
    player: PlayerId,
    source_component,
    target_component,
) -> None:
    area = _transformed_v2_area(player, source_component)
    if area is not None:
        (
            target_component.area_x1,
            target_component.area_y1,
            target_component.area_x2,
            target_component.area_y2,
        ) = area
    if (
        hasattr(source_component, "location_x")
        and hasattr(source_component, "location_y")
        and source_component.location_x >= 0
        and source_component.location_y >= 0
    ):
        # Trigger locations address integer map cells.  Unit positions use a
        # 144-wide continuous coordinate space, but cell reflections use 143.
        # Mixing the two moves reflected effects one tile outward, which put
        # hero blockers, selector tasks, and King cannons on water or walls.
        target_component.location_x, target_component.location_y = v2_cell_for_player(
            player,
            source_component.location_x,
            source_component.location_y,
        )


def _copy_v2_trigger_geometry(
    player: PlayerId,
    source_trigger,
    target_trigger,
) -> None:
    if len(source_trigger.conditions) != len(target_trigger.conditions):
        raise RuntimeError(
            f"V2 condition mismatch between {source_trigger.name!r} and "
            f"{target_trigger.name!r}"
        )
    if len(source_trigger.effects) != len(target_trigger.effects):
        raise RuntimeError(
            f"V2 effect mismatch between {source_trigger.name!r} and "
            f"{target_trigger.name!r}"
        )
    for source, target in zip(
        source_trigger.conditions,
        target_trigger.conditions,
        strict=True,
    ):
        if source.condition_type != target.condition_type:
            raise RuntimeError(
                f"V2 condition type mismatch in {target_trigger.name!r}"
            )
        _copy_v2_component_geometry(player, source, target)
    for source, target in zip(
        source_trigger.effects,
        target_trigger.effects,
        strict=True,
    ):
        if source.effect_type != target.effect_type:
            raise RuntimeError(f"V2 effect type mismatch in {target_trigger.name!r}")
        _copy_v2_component_geometry(player, source, target)


def _remap_v2_trigger_geometry(ctx: BuildContext) -> None:
    """Move legacy selector, hero-spawn, and marker effects with V2."""
    family_names = {
        family: {
            player: f"{family} (p{int(player)})"
            for player in PLAYERS
        }
        for family in ("short", "med", "long")
    }
    family_names.update(
        {
            family: {
                player: family if player == PlayerId.ONE else f"{family} (p{int(player)})"
                for player in PLAYERS
            }
            for family in ("herospawnclose", "herospawnopen")
        }
    )

    for family, names in family_names.items():
        source = deepcopy(_unique_trigger(ctx, names[PlayerId.THREE]))
        for player, name in names.items():
            target = _unique_trigger(ctx, name)
            if family in {"short", "med", "long"}:
                # Sparse movement adds a different number of trigger-switch
                # effects for each color (only valid W<=S mappings). Those
                # effects have no geometry; only the selector conditions do.
                if len(source.conditions) != len(target.conditions):
                    raise RuntimeError(
                        f"V2 selector condition mismatch in {target.name!r}"
                    )
                for source_condition, target_condition in zip(
                    source.conditions,
                    target.conditions,
                    strict=True,
                ):
                    _copy_v2_component_geometry(
                        player,
                        source_condition,
                        target_condition,
                    )
            else:
                _copy_v2_trigger_geometry(player, source, target)

    # Selector loops should react quickly without running on every trigger
    # pass.  Close also needs an absence guard; otherwise it creates another
    # Old Stone Head every pass while the selector remains on the rug.
    for player in PLAYERS:
        suffix = "" if player == PlayerId.ONE else f" (p{int(player)})"
        close = _unique_trigger(ctx, f"herospawnclose{suffix}")
        close.new_condition.timer(timer=1)
        close_creates = [
            effect
            for effect in close.effects
            if effect.effect_type == EffectId.CREATE_OBJECT
            and effect.object_list_unit_id == OtherInfo.OLD_STONE_HEAD.ID
        ]
        if len(close_creates) != 1:
            raise RuntimeError(
                f"expected one hero-spawn blocker create for P{int(player)}"
            )
        blocker_x = close_creates[0].location_x
        blocker_y = close_creates[0].location_y
        close.new_condition.objects_in_area(
            quantity=1,
            object_list=OtherInfo.OLD_STONE_HEAD.ID,
            source_player=PlayerId.GAIA,
            area_x1=blocker_x,
            area_y1=blocker_y,
            area_x2=blocker_x,
            area_y2=blocker_y,
            inverted=1,
        )

        open_trigger = _unique_trigger(ctx, f"herospawnopen{suffix}")
        open_trigger.new_condition.timer(timer=1)
        remove_effects = [
            effect
            for effect in open_trigger.effects
            if effect.effect_type == EffectId.REMOVE_OBJECT
        ]
        if len(remove_effects) != 1:
            raise RuntimeError(
                f"expected one hero-spawn blocker removal for P{int(player)}"
            )
        remove = remove_effects[0]
        remove.object_list_unit_id = OtherInfo.OLD_STONE_HEAD.ID
        open_trigger.new_condition.objects_in_area(
            quantity=1,
            object_list=OtherInfo.OLD_STONE_HEAD.ID,
            source_player=PlayerId.GAIA,
            area_x1=remove.area_x1,
            area_y1=remove.area_y1,
            area_x2=remove.area_x2,
            area_y2=remove.area_y2,
        )

        # Open is a persistent selector like Close/Short/Medium/Long. The
        # legacy order immediately sent the mover back to its center tile;
        # current DE can keep that order ahead of the player's next command,
        # making the five-position control appear immobile.
        return_orders = [
            effect
            for effect in open_trigger.effects
            if effect.effect_type == EffectId.TASK_OBJECT
            and effect.selected_object_ids
        ]
        if len(return_orders) != 1:
            raise RuntimeError(
                f"expected one legacy selector return order for P{int(player)}"
            )
        open_trigger.effects.remove(return_orders[0])

    # King objects move with V2, but the legacy triggers retained eight
    # different hand-authored island corners, cannon spawns, and buff areas.
    # Blue watched one obsolete cell; several colors also spawned a cannon in
    # water or against a wall. Copy all geometry from P3's complete grounded
    # King layout while retaining each color's selected King ref and effects.
    source_king = deepcopy(_unique_trigger(ctx, "P3 King"))
    for player in PLAYERS:
        target = _unique_trigger(ctx, f"P{int(player)} King")
        _copy_v2_trigger_geometry(player, source_king, target)

    seen_hay_references = set()
    for player in PLAYERS:
        for hay_index in range(1, 5):
            target = _unique_trigger(ctx, f"hay{hay_index} (p{int(player)})")
            reference_ids = {
                condition.unit_object
                for condition in target.conditions
                if condition.unit_object >= 0
            }
            creates = [
                effect
                for effect in target.effects
                if effect.effect_type == EffectId.CREATE_OBJECT
            ]
            if len(reference_ids) != 1 or len(creates) != 1:
                raise RuntimeError(
                    f"expected one castle reference and create effect in {target.name!r}"
                )
            reference_id = reference_ids.pop()
            location = HAY_LOCATION_BY_CASTLE_REFERENCE.get(reference_id)
            if location is None:
                raise RuntimeError(
                    f"unknown V2 hay castle reference {reference_id} in {target.name!r}"
                )
            creates[0].location_x, creates[0].location_y = location
            seen_hay_references.add(reference_id)
    if seen_hay_references != set(HAY_LOCATION_BY_CASTLE_REFERENCE):
        raise RuntimeError("not every V2 hay castle reference was assigned")


def _restore_mobile_distance_movers(ctx: BuildContext) -> None:
    """Use a supported controllable unit for every five-position selector."""
    unit_by_reference = {
        unit.reference_id: unit
        for units in ctx.um.units
        for unit in units
    }
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    forbidden_effects = {
        EffectId.DISABLE_OBJECT_SELECTION,
        EffectId.FREEZE_OBJECT,
        EffectId.STOP_OBJECT,
    }

    for player in PLAYERS:
        suffix = "" if player == PlayerId.ONE else f" (p{int(player)})"
        selector_names = (
            f"short (p{int(player)})",
            f"med (p{int(player)})",
            f"long (p{int(player)})",
            f"herospawnclose{suffix}",
            f"herospawnopen{suffix}",
        )
        references = {
            condition.unit_object
            for name in selector_names
            for condition in _unique_trigger(ctx, name).conditions
            if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
            and condition.unit_object >= 0
        }
        if len(references) != 1:
            raise RuntimeError(
                f"expected one five-position mover for P{int(player)}, "
                f"found {sorted(references)}"
            )
        reference_id = references.pop()
        mover = unit_by_reference.get(reference_id)
        if mover is None or mover.player != player:
            raise RuntimeError(
                f"missing owner-correct distance mover {reference_id} "
                f"for P{int(player)}"
            )
        if mover.unit_const != 159:
            raise RuntimeError(
                f"unexpected legacy mover unit {mover.unit_const} "
                f"for P{int(player)}"
            )
        if ctx.mm.get_tile(x=int(mover.x), y=int(mover.y)).terrain_id in water:
            raise RuntimeError(
                f"P{int(player)} distance mover {reference_id} is on water"
            )

        # ID 159 is an obsolete hidden Relic Cart variant and is not reliably
        # commandable in current DE. A player-owned Sheep is a normal movable
        # selector without trade/build/attack commands or population cost.
        mover.unit_const = UnitInfo.SHEEP.ID

        selected = [reference_id]
        protection = _unique_trigger(ctx, f"Antidelete P{int(player)}")
        protection.new_effect.disable_object_deletion(
            source_player=player,
            selected_object_ids=selected,
        )

        conflicts = [
            (trigger.name, effect.effect_type)
            for trigger in ctx.tm.triggers
            for effect in trigger.effects
            if reference_id in (effect.selected_object_ids or ())
            and effect.effect_type in forbidden_effects
        ]
        if conflicts:
            raise RuntimeError(
                f"P{int(player)} distance mover {reference_id} has "
                f"conflicting effects: {conflicts}"
            )


def _configure_sparse_center_rewards(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Award center control to the runtime player occupying each color."""
    centered_area = {
        "area_x1": 65,
        "area_y1": 65,
        "area_x2": 78,
        "area_y2": 78,
    }
    unit_by_reference = {
        unit.reference_id: unit
        for units in ctx.um.units
        for unit in units
    }
    originals = {}
    for color in PLAYERS:
        suffix = "" if color == PlayerId.ONE else f" (p{int(color)})"
        originals[color, "Kills"] = _unique_trigger(ctx, f"Middle kills{suffix}")
        originals[color, "Trebuchet"] = _unique_trigger(
            ctx, f"Middle Trebuchet{suffix}"
        )

    for color in PLAYERS:
        marker = unit_by_reference.get(MIDDLE_TREBUCHET_MARKERS[color])
        if marker is None or marker.unit_const != OtherInfo.FLAG_A.ID:
            raise RuntimeError(f"missing center reward marker for P{int(color)}")
        marker_x, marker_y = int(marker.x), int(marker.y)
        for world_player in _possible_world_players(color):
            for family in ("Kills", "Trebuchet"):
                if world_player == color:
                    trigger = originals[color, family]
                    _reset_trigger(trigger)
                    trigger.name = (
                        f"Center {family} S{int(color)} W{int(world_player)}"
                    )
                    trigger.enabled = 1
                else:
                    trigger = ctx.tm.add_trigger(
                        f"Center {family} S{int(color)} W{int(world_player)}",
                        description_stid=0,
                        short_description_stid=0,
                    )
                trigger.looping = 1
                trigger.new_condition.timer(
                    timer=180 if family == "Kills" else 1800
                )
                trigger.new_condition.variable_value(
                    quantity=1,
                    variable=active_variables[color],
                    comparison=Comparison.EQUAL,
                )
                trigger.new_condition.variable_value(
                    quantity=int(world_player),
                    variable=world_variables[color],
                    comparison=Comparison.EQUAL,
                )
                trigger.new_condition.objects_in_area(
                    quantity=1,
                    source_player=world_player,
                    object_type=ObjectType.MILITARY,
                    **centered_area,
                )
                if family == "Kills":
                    trigger.new_effect.send_chat(
                        source_player=world_player,
                        message="Center control reward: +10 kills (3 minutes).",
                    )
                    trigger.new_effect.tribute(
                        quantity=10,
                        tribute_list=20,
                        source_player=PlayerId.GAIA,
                        target_player=world_player,
                    )
                    continue
                trigger.new_effect.send_chat(
                    source_player=world_player,
                    message=(
                        "Center control reward: a Trebuchet has arrived "
                        "(30 minutes)."
                    ),
                )
                trigger.new_effect.remove_object(
                    source_player=world_player,
                    object_group=ObjectClass.PACKED_UNIT,
                    area_x1=marker_x,
                    area_y1=marker_y,
                    area_x2=marker_x,
                    area_y2=marker_y,
                )
                trigger.new_effect.create_object(
                    object_list_unit_id=UnitInfo.TREBUCHET_PACKED.ID,
                    source_player=world_player,
                    location_x=marker_x,
                    location_y=marker_y,
                    disable_sound=1,
                )
                trigger.new_effect.change_object_hp(
                    quantity=200,
                    object_list_unit_id=UnitInfo.TREBUCHET_PACKED.ID,
                    source_player=world_player,
                    object_group=ObjectClass.PACKED_UNIT,
                    object_type=ObjectType.MILITARY,
                    operation=Operation.ADD,
                    area_x1=marker_x,
                    area_y1=marker_y,
                    area_x2=marker_x,
                    area_y2=marker_y,
                )


def _align_selector_labels(ctx: BuildContext) -> None:
    """Name every selector by the behavior of the rug it actually occupies.

    Several reflected sectors kept the old left-to-right labels even though
    their selector areas were mirrored.  Resolve names from final object and
    trigger geometry so future map transforms cannot silently reverse them.
    """
    unit_by_reference = {
        unit.reference_id: unit
        for units in ctx.um.units
        for unit in units
    }

    def align(
        rename_messages: set[str],
        behavior_names: dict[PlayerId, dict[str, str]],
        public_names: dict[str, str],
    ) -> None:
        effects = [
            effect
            for trigger in ctx.tm.triggers
            for effect in trigger.effects
            if effect.effect_type == EffectId.CHANGE_OBJECT_NAME
            and (effect.message or "") in rename_messages
            and len(effect.selected_object_ids or ()) == 1
        ]
        expected_count = len(PLAYERS) * len(public_names)
        if len(effects) != expected_count:
            raise RuntimeError(
                f"expected {expected_count} selector labels, found {len(effects)}"
            )

        unused_effects = set(range(len(effects)))
        for player in PLAYERS:
            slots = {}
            selector_reference = None
            for role, trigger_name in behavior_names[player].items():
                trigger = _unique_trigger(ctx, trigger_name)
                conditions = [
                    condition
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
                    and condition.unit_object >= 0
                ]
                if len(conditions) != 1:
                    raise RuntimeError(
                        f"expected one selector area in {trigger_name!r}"
                    )
                condition = conditions[0]
                if selector_reference is None:
                    selector_reference = condition.unit_object
                elif selector_reference != condition.unit_object:
                    raise RuntimeError(
                        f"selector reference mismatch for P{int(player)}"
                    )
                slots[role] = (
                    (condition.area_x1 + condition.area_x2) / 2,
                    (condition.area_y1 + condition.area_y2) / 2,
                )

            player_effects = []
            for index in unused_effects:
                reference_id = effects[index].selected_object_ids[0]
                unit = unit_by_reference.get(reference_id)
                if unit is None:
                    raise RuntimeError(
                        f"selector label references missing object {reference_id}"
                    )
                distances = {
                    role: (unit.x - center_x) ** 2 + (unit.y - center_y) ** 2
                    for role, (center_x, center_y) in slots.items()
                }
                nearest_role, nearest_distance = min(
                    distances.items(), key=lambda item: item[1]
                )
                if nearest_distance <= 9:
                    player_effects.append((index, nearest_role, nearest_distance))

            if len(player_effects) != len(public_names):
                raise RuntimeError(
                    f"expected {len(public_names)} nearby selector labels for "
                    f"P{int(player)}, found {len(player_effects)}"
                )
            assigned_roles = [role for _index, role, _distance in player_effects]
            if set(assigned_roles) != set(public_names):
                raise RuntimeError(
                    f"ambiguous selector labels for P{int(player)}: {assigned_roles}"
                )
            for index, role, _distance in player_effects:
                effects[index].message = public_names[role]
                unused_effects.remove(index)

        if unused_effects:
            raise RuntimeError("not every selector label was aligned")

    align(
        {"Spawn - Close", "Spawn - Normal", "Spawn - Long"},
        {
            player: {
                family: f"{family} (p{int(player)})"
                for family in ("short", "med", "long")
            }
            for player in PLAYERS
        },
        {
            "short": "Army Route - Short",
            "med": "Army Route - Medium",
            "long": "Army Route - Long",
        },
    )
    align(
        {"Hero Spawn Close", "Hero Spawn Open"},
        {
            player: {
                family: (
                    family
                    if player == PlayerId.ONE
                    else f"{family} (p{int(player)})"
                )
                for family in ("herospawnclose", "herospawnopen")
            }
            for player in PLAYERS
        },
        {
            "herospawnclose": "Hero Spawn - Closed",
            "herospawnopen": "Hero Spawn - Open",
        },
    )


def _retire_obsolete_public_loops(ctx: BuildContext) -> None:
    """Remove obsolete every-pass effects and keep their useful labels once."""
    for name in ("Hawk", "==Move Vils=====", "Nome Razing ----- "):
        trigger = _unique_trigger(ctx, name)
        _reset_trigger(trigger)
        trigger.name = f"Legacy {name.strip()} Disabled"

    looping_renames = [
        trigger
        for trigger in ctx.tm.triggers
        if trigger.name == "==Rename======" and trigger.looping
    ]
    if len(looping_renames) != 1:
        raise RuntimeError(
            f"expected one looping legacy rename trigger, found {len(looping_renames)}"
        )
    raze_rename = looping_renames[0]
    original_effects = deepcopy(raze_rename.effects)
    _reset_trigger(raze_rename)
    raze_rename.name = "Razing Counter Labels"
    raze_rename.enabled = 1
    raze_rename.new_condition.timer(timer=1)
    for effect in original_effects:
        effect.message = "Razings - health shows the current total"
        raze_rename.effects.append(effect)

    selector_names = _unique_trigger(ctx, "Nome ---------------- ")
    for effect in selector_names.effects:
        if effect.effect_type == EffectId.CHANGE_OBJECT_NAME:
            effect.message = "Move me to select an army route"


def _neutralize_fixed_color_tags(ctx: BuildContext) -> None:
    """Let runtime-player chat coloring work after sparse color compaction."""
    color_tag = re.compile(
        r"<(?:BLUE|RED|GREEN|YELLOW|AQUA|PURPLE|GREY|ORANGE)>\s*",
        re.IGNORECASE,
    )
    for trigger in ctx.tm.triggers:
        for effect in trigger.effects:
            if effect.message:
                effect.message = color_tag.sub("", effect.message)

def _copy_for_world_player(component, scenario_player: PlayerId, world_player: PlayerId):
    copied = deepcopy(component)
    if copied.source_player == scenario_player:
        copied.source_player = world_player
    if copied.target_player == scenario_player:
        copied.target_player = world_player
    return copied


def _configure_sparse_center_views(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Center each runtime player's camera on the color they selected."""
    templates = {
        color: deepcopy(_unique_trigger(ctx, f"Center View P{int(color)}"))
        for color in PLAYERS
    }
    originals = {
        color: _unique_trigger(ctx, f"Center View P{int(color)}")
        for color in PLAYERS
    }
    for color in PLAYERS:
        template_effects = [
            effect
            for effect in templates[color].effects
            if effect.effect_type == EffectId.CHANGE_VIEW
        ]
        if len(template_effects) != 1:
            raise RuntimeError(
                f"expected one center-view effect for P{int(color)}"
            )
        for world_player in _possible_world_players(color):
            if world_player == color:
                trigger = originals[color]
                _reset_trigger(trigger)
                trigger.name = (
                    f"Center View S{int(color)} W{int(world_player)}"
                )
                trigger.enabled = 1
            else:
                trigger = ctx.tm.add_trigger(
                    f"Center View S{int(color)} W{int(world_player)}",
                    description_stid=0,
                    short_description_stid=0,
                )
            trigger.new_condition.timer(timer=1)
            trigger.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            trigger.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            trigger.effects.append(
                _copy_for_world_player(
                    template_effects[0], color, world_player
                )
            )


def _configure_sparse_wall_breaches(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Remove a color's front wall with its compacted runtime owner."""
    templates = {
        color: deepcopy(_unique_trigger(ctx, f"Elimina Walls P{int(color)}"))
        for color in PLAYERS
    }
    originals = {
        color: _unique_trigger(ctx, f"Elimina Walls P{int(color)}")
        for color in PLAYERS
    }
    for color in PLAYERS:
        destroy_conditions = [
            condition
            for condition in templates[color].conditions
            if condition.condition_type == ConditionId.DESTROY_OBJECT
            and condition.unit_object >= 0
        ]
        removal_effects = [
            effect
            for effect in templates[color].effects
            if effect.effect_type == EffectId.REMOVE_OBJECT
            and effect.object_list_unit_id
            in {BuildingInfo.STONE_WALL.ID, BuildingInfo.FORTIFIED_WALL.ID}
        ]
        if len(destroy_conditions) != 1 or len(removal_effects) != 2:
            raise RuntimeError(
                f"invalid wall-breach template for P{int(color)}"
            )
        for world_player in _possible_world_players(color):
            if world_player == color:
                trigger = originals[color]
                _reset_trigger(trigger)
                trigger.name = (
                    f"Wall Breach S{int(color)} W{int(world_player)}"
                )
                trigger.enabled = 1
            else:
                trigger = ctx.tm.add_trigger(
                    f"Wall Breach S{int(color)} W{int(world_player)}",
                    description_stid=0,
                    short_description_stid=0,
                )
            trigger.conditions.append(deepcopy(destroy_conditions[0]))
            trigger.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            trigger.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            trigger.effects.extend(
                _copy_for_world_player(effect, color, world_player)
                for effect in removal_effects
            )


def _configure_sparse_king_islands(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Award every color's island cannons to its compacted runtime player."""
    legacy_cleanup = _unique_trigger(ctx, "sem cr")
    _reset_trigger(legacy_cleanup)
    legacy_cleanup.name = "Legacy Shared King Cleanup Disabled"

    cleanups = {}
    for world_player in PLAYERS:
        cleanup = ctx.tm.add_trigger(
            f"King Island Cleanup W{int(world_player)}",
            description_stid=0,
            short_description_stid=0,
            enabled=0,
        )
        cleanup.new_condition.timer(timer=50)
        cleanup.new_effect.remove_object(
            object_list_unit_id=UnitInfo.SCORPION.ID,
            source_player=world_player,
            area_x1=0,
            area_y1=0,
            area_x2=143,
            area_y2=143,
        )
        cleanups[world_player] = cleanup

    templates = {
        color: deepcopy(_unique_trigger(ctx, f"P{int(color)} King"))
        for color in PLAYERS
    }
    originals = {
        color: _unique_trigger(ctx, f"P{int(color)} King")
        for color in PLAYERS
    }
    for color in PLAYERS:
        bring_conditions = [
            condition
            for condition in templates[color].conditions
            if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
            and condition.unit_object >= 0
        ]
        cannon_creates = [
            effect
            for effect in templates[color].effects
            if effect.effect_type == EffectId.CREATE_OBJECT
            and effect.object_list_unit_id == UnitInfo.SCORPION.ID
        ]
        if len(bring_conditions) != 1 or len(cannon_creates) != 6:
            raise RuntimeError(
                f"invalid King-island template for P{int(color)}"
            )
        for world_player in _possible_world_players(color):
            if world_player == color:
                trigger = originals[color]
                _reset_trigger(trigger)
                trigger.name = (
                    f"King Island S{int(color)} W{int(world_player)}"
                )
                trigger.enabled = 1
            else:
                trigger = ctx.tm.add_trigger(
                    f"King Island S{int(color)} W{int(world_player)}",
                    description_stid=0,
                    short_description_stid=0,
                )
            trigger.conditions.append(deepcopy(bring_conditions[0]))
            trigger.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            trigger.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            trigger.new_effect.activate_trigger(
                trigger_id=cleanups[world_player].trigger_id
            )
            for source_effect in templates[color].effects:
                if source_effect.effect_type == EffectId.ACTIVATE_TRIGGER:
                    continue
                effect = _copy_for_world_player(
                    source_effect, color, world_player
                )
                if effect.effect_type == EffectId.DISPLAY_INSTRUCTIONS:
                    effect.message = (
                        f"P{int(color)} claimed the side island."
                    )
                if (
                    effect.effect_type == EffectId.CHANGE_OBJECT_HP
                    and effect.operation == -1
                ):
                    effect.operation = Operation.ADD
                trigger.effects.append(effect)


def _configure_sparse_late_hero_boosts(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Continue the established Super Genghis phase at 3500/5000 kills."""
    legacy = [
        trigger
        for trigger in ctx.tm.triggers
        if trigger.name.strip().startswith(("3500 ", "5000 "))
    ]
    if len(legacy) != 40:
        raise RuntimeError(
            f"expected 40 legacy late-hero triggers, found {len(legacy)}"
        )
    for trigger in legacy:
        original_id = trigger.trigger_id
        _reset_trigger(trigger)
        trigger.name = f"Legacy Late Hero Boost Disabled #{original_id}"

    def add_loop(
        color: PlayerId,
        world_player: PlayerId,
        label: str,
        timer: int,
        location: tuple[int, int],
    ):
        trigger = ctx.tm.add_trigger(
            f"Hero Boost {label} S{int(color)} W{int(world_player)}",
            description_stid=0,
            short_description_stid=0,
            enabled=0,
            looping=1,
        )
        trigger.new_condition.timer(timer=timer)
        trigger.new_condition.own_fewer_objects(
            quantity=300,
            source_player=world_player,
            object_type=ObjectType.MILITARY,
        )
        trigger.new_condition.variable_value(
            quantity=1,
            variable=active_variables[color],
            comparison=Comparison.EQUAL,
        )
        trigger.new_condition.variable_value(
            quantity=int(world_player),
            variable=world_variables[color],
            comparison=Comparison.EQUAL,
        )
        x, y = location
        trigger.new_effect.remove_object(
            object_list_unit_id=HeroInfo.GENGHIS_KHAN.ID,
            source_player=world_player,
            area_x1=x,
            area_y1=y,
            area_x2=x,
            area_y2=y,
        )
        trigger.new_effect.create_object(
            object_list_unit_id=HeroInfo.GENGHIS_KHAN.ID,
            source_player=world_player,
            location_x=x,
            location_y=y,
        )
        trigger.new_effect.change_object_attack(
            armour_attack_quantity=25,
            object_list_unit_id=HeroInfo.GENGHIS_KHAN.ID,
            source_player=world_player,
            area_x1=x,
            area_y1=y,
            area_x2=x,
            area_y2=y,
            operation=Operation.ADD,
        )
        trigger.new_effect.change_object_hp(
            quantity=300,
            object_list_unit_id=HeroInfo.GENGHIS_KHAN.ID,
            source_player=world_player,
            area_x1=x,
            area_y1=y,
            area_x2=x,
            area_y2=y,
            operation=Operation.ADD,
        )
        return trigger

    for color in PLAYERS:
        locations = {
            "K3500": v2_cell_for_player(color, 16, 38),
            "K5000A": v2_cell_for_player(color, 15, 38),
            "K5000B": v2_cell_for_player(color, 17, 38),
        }
        for label, (x, y) in locations.items():
            tile = ctx.mm.get_tile(x=x, y=y)
            if tile.terrain_id in set(TerrainId.water_terrains()):
                raise RuntimeError(
                    f"P{int(color)} {label} hero spawn ({x}, {y}) is water"
                )
        for world_player in _possible_world_players(color):
            milestone_2000 = _unique_trigger(
                ctx,
                f"Hero Milestone S{int(color)} W{int(world_player)} K2000",
            )
            loop_3500 = add_loop(
                color, world_player, "K3500", 3, locations["K3500"]
            )
            loop_5000_a = add_loop(
                color, world_player, "K5000A", 3, locations["K5000A"]
            )
            loop_5000_b = add_loop(
                color, world_player, "K5000B", 4, locations["K5000B"]
            )

            threshold_3500 = ctx.tm.add_trigger(
                f"Hero Boost Unlock K3500 S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            threshold_3500.new_condition.accumulate_attribute(
                quantity=3_500,
                attribute=Attribute.UNITS_KILLED,
                source_player=world_player,
            )
            threshold_3500.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            threshold_3500.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            threshold_3500.new_effect.deactivate_trigger(
                trigger_id=milestone_2000.trigger_id
            )
            threshold_3500.new_effect.activate_trigger(
                trigger_id=loop_3500.trigger_id
            )

            threshold_5000 = ctx.tm.add_trigger(
                f"Hero Boost Unlock K5000 S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            threshold_5000.new_condition.accumulate_attribute(
                quantity=5_000,
                attribute=Attribute.UNITS_KILLED,
                source_player=world_player,
            )
            threshold_5000.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            threshold_5000.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            threshold_5000.new_effect.deactivate_trigger(
                trigger_id=milestone_2000.trigger_id
            )
            threshold_5000.new_effect.deactivate_trigger(
                trigger_id=loop_3500.trigger_id
            )
            threshold_5000.new_effect.activate_trigger(
                trigger_id=loop_5000_a.trigger_id
            )
            threshold_5000.new_effect.activate_trigger(
                trigger_id=loop_5000_b.trigger_id
            )


def _configure_sparse_hero_milestones(
    ctx: BuildContext,
    active_variables,
    world_variables,
    match_ready_variable,
) -> None:
    """Make every kill hero and its orders follow the occupied color.

    The legacy P5/P6 milestones created their heroes on rear Stone Walls after
    the V2 perimeter was compacted.  They also read a fixed player number, so a
    sparse Teal slot mapped to runtime P2 never saw Teal's kills.  Use P3's
    complete milestone/order families as the semantic template, then bind each
    color to every possible runtime player behind the shared color resolver.
    """
    milestone_targets = {}
    for scenario_player in PLAYERS:
        for threshold, unit_id in HERO_MILESTONES:
            matches = []
            for trigger in ctx.tm.triggers:
                creates = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.CREATE_OBJECT
                    and effect.source_player == scenario_player
                    and effect.object_list_unit_id == unit_id
                ]
                kill_conditions = [
                    condition
                    for condition in trigger.conditions
                    if condition.condition_type == ConditionId.ACCUMULATE_ATTRIBUTE
                    and condition.source_player == scenario_player
                    and condition.attribute == Attribute.UNITS_KILLED
                    and condition.quantity == threshold
                ]
                if trigger.enabled and trigger.looping and len(creates) == 1 and len(kill_conditions) == 1:
                    matches.append(trigger)
            if len(matches) != 1:
                raise RuntimeError(
                    f"expected one live P{int(scenario_player)} {threshold}-kill "
                    f"hero milestone, found {len(matches)}"
                )
            milestone_targets[scenario_player, threshold] = matches[0]

    milestone_templates = {
        threshold: deepcopy(milestone_targets[PlayerId.THREE, threshold])
        for threshold, _unit_id in HERO_MILESTONES
    }

    order_targets = {}
    for scenario_player in PLAYERS:
        for source_name in HERO_ORDER_FAMILIES:
            matches = []
            for trigger in ctx.tm.triggers:
                task_effects = [
                    effect
                    for effect in trigger.effects
                    if effect.effect_type == EffectId.TASK_OBJECT
                    and effect.source_player == scenario_player
                ]
                if (
                    trigger.enabled
                    and trigger.looping
                    and trigger.name.strip().startswith(source_name)
                    and len(task_effects) == 1
                ):
                    matches.append(trigger)
            if len(matches) != 1:
                raise RuntimeError(
                    f"expected one live P{int(scenario_player)} {source_name} "
                    f"hero order, found {len(matches)}"
                )
            order_targets[scenario_player, source_name] = matches[0]

    order_templates = {
        source_name: deepcopy(order_targets[PlayerId.THREE, source_name])
        for source_name in HERO_ORDER_FAMILIES
    }
    medium_task_effects = [
        effect
        for effect in order_templates["Médio"].effects
        if effect.effect_type == EffectId.TASK_OBJECT
    ]
    if len(medium_task_effects) != 1:
        raise RuntimeError("expected one canonical Medium hero task effect")
    medium_task_template = medium_task_effects[0]
    order_selector_references = {}
    for scenario_player in PLAYERS:
        for source_name in HERO_ORDER_FAMILIES:
            selector_conditions = [
                condition
                for condition in order_targets[
                    scenario_player,
                    source_name,
                ].conditions
                if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA
                and condition.unit_object >= 0
            ]
            if len(selector_conditions) != 1:
                raise RuntimeError(
                    f"expected one P{int(scenario_player)} {source_name} "
                    "selector relic reference"
                )
            order_selector_references[scenario_player, source_name] = (
                selector_conditions[0].unit_object
            )

    for scenario_player, (spawn_x, spawn_y) in HERO_MILESTONE_SPAWN_TILES.items():
        tile = ctx.mm.get_tile(x=spawn_x, y=spawn_y)
        if tile.terrain_id in {
            TerrainId.WATER_SHALLOW,
            TerrainId.WATER_DEEP,
            TerrainId.WATER_MEDIUM,
        }:
            raise RuntimeError(
                f"P{int(scenario_player)} hero milestone tile "
                f"({spawn_x}, {spawn_y}) is water"
            )
        occupied = [
            unit
            for units in ctx.um.units
            for unit in units
            if int(unit.x) == spawn_x and int(unit.y) == spawn_y
        ]
        if occupied:
            references = ", ".join(str(unit.reference_id) for unit in occupied)
            raise RuntimeError(
                f"P{int(scenario_player)} hero milestone tile "
                f"({spawn_x}, {spawn_y}) is occupied by refs {references}"
            )

        for world_player in _possible_world_players(scenario_player):
            previous = None
            for threshold, expected_unit_id in HERO_MILESTONES:
                template = milestone_templates[threshold]
                if world_player == scenario_player:
                    trigger = milestone_targets[scenario_player, threshold]
                    _reset_trigger(trigger)
                    trigger.name = (
                        f"Hero Milestone S{int(scenario_player)} "
                        f"W{int(world_player)} K{threshold}"
                    )
                    trigger.enabled = 1
                    trigger.looping = 1
                else:
                    trigger = ctx.tm.add_trigger(
                        f"Hero Milestone S{int(scenario_player)} "
                        f"W{int(world_player)} K{threshold}",
                        description_stid=0,
                        short_description_stid=0,
                        enabled=1,
                        looping=1,
                    )

                trigger.conditions.extend(
                    _copy_for_world_player(condition, PlayerId.THREE, world_player)
                    for condition in template.conditions
                )
                trigger.new_condition.variable_value(
                    quantity=1,
                    variable=active_variables[scenario_player],
                    comparison=Comparison.EQUAL,
                )
                trigger.new_condition.variable_value(
                    quantity=int(world_player),
                    variable=world_variables[scenario_player],
                    comparison=Comparison.EQUAL,
                )
                deactivations = 0
                creates = 0
                for source_effect in template.effects:
                    if source_effect.effect_type == EffectId.DEACTIVATE_TRIGGER:
                        if previous is None:
                            raise RuntimeError(
                                f"unexpected leading deactivation at {threshold} kills"
                            )
                        trigger.new_effect.deactivate_trigger(
                            trigger_id=previous.trigger_id
                        )
                        deactivations += 1
                        continue
                    effect = _copy_for_world_player(
                        source_effect,
                        PlayerId.THREE,
                        world_player,
                    )
                    if effect.effect_type == EffectId.CREATE_OBJECT:
                        if effect.object_list_unit_id != expected_unit_id:
                            raise RuntimeError(
                                f"unexpected hero {effect.object_list_unit_id} at "
                                f"{threshold} kills"
                            )
                        effect.location_x = spawn_x
                        effect.location_y = spawn_y
                        creates += 1
                    if (
                        effect.effect_type
                        in {EffectId.CHANGE_OBJECT_ATTACK, EffectId.CHANGE_OBJECT_HP}
                        and effect.operation == -1
                    ):
                        effect.operation = Operation.ADD
                    if min(
                        effect.area_x1,
                        effect.area_y1,
                        effect.area_x2,
                        effect.area_y2,
                    ) >= 0:
                        effect.area_x1 = effect.area_x2 = spawn_x
                        effect.area_y1 = effect.area_y2 = spawn_y
                    trigger.effects.append(effect)
                expected_deactivations = int(previous is not None)
                if deactivations != expected_deactivations or creates != 1:
                    raise RuntimeError(
                        f"invalid {threshold}-kill hero chain for "
                        f"S{int(scenario_player)} W{int(world_player)}"
                    )
                previous = trigger

            for source_name, public_name in HERO_ORDER_FAMILIES.items():
                template = order_templates[source_name]
                if world_player == scenario_player:
                    trigger = order_targets[scenario_player, source_name]
                    _reset_trigger(trigger)
                    trigger.name = (
                        f"Hero Orders {public_name} S{int(scenario_player)} "
                        f"W{int(world_player)}"
                    )
                    trigger.enabled = 1
                    trigger.looping = 1
                else:
                    trigger = ctx.tm.add_trigger(
                        f"Hero Orders {public_name} S{int(scenario_player)} "
                        f"W{int(world_player)}",
                        description_stid=0,
                        short_description_stid=0,
                        enabled=1,
                        looping=1,
                    )

                for source_condition in template.conditions:
                    condition = _copy_for_world_player(
                        source_condition,
                        PlayerId.THREE,
                        world_player,
                    )
                    _copy_v2_component_geometry(
                        scenario_player,
                        source_condition,
                        condition,
                    )
                    if condition.condition_type == ConditionId.BRING_OBJECT_TO_AREA:
                        condition.unit_object = order_selector_references[
                            scenario_player,
                            source_name,
                        ]
                    trigger.conditions.append(condition)
                trigger.new_condition.variable_value(
                    quantity=1,
                    variable=active_variables[scenario_player],
                    comparison=Comparison.EQUAL,
                )
                trigger.new_condition.variable_value(
                    quantity=int(world_player),
                    variable=world_variables[scenario_player],
                    comparison=Comparison.EQUAL,
                )
                trigger.new_condition.timer(timer=1)

                task_effects = [
                    effect
                    for effect in template.effects
                    if effect.effect_type == EffectId.TASK_OBJECT
                ]
                if len(task_effects) != 1:
                    raise RuntimeError(
                        f"expected one task effect in canonical {source_name} order"
                    )
                task = _copy_for_world_player(
                    task_effects[0],
                    PlayerId.THREE,
                    world_player,
                )
                task.area_x1 = spawn_x - 1
                task.area_y1 = spawn_y - 1
                task.area_x2 = spawn_x + 1
                task.area_y2 = spawn_y + 1
                task.location_x, task.location_y = v2_cell_for_player(
                    scenario_player,
                    task_effects[0].location_x,
                    task_effects[0].location_y,
                )
                task.action_type = ActionType.MOVE
                trigger.effects.append(task)

            open_route = ctx.tm.add_trigger(
                f"Hero Orders Open S{int(scenario_player)} "
                f"W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
                enabled=1,
                looping=1,
            )
            open_route.new_condition.objects_in_area(
                quantity=1,
                object_list=OtherInfo.OLD_STONE_HEAD.ID,
                source_player=PlayerId.GAIA,
                area_x1=spawn_x,
                area_y1=spawn_y,
                area_x2=spawn_x,
                area_y2=spawn_y,
                inverted=1,
            )
            open_route.new_condition.variable_value(
                quantity=1,
                variable=active_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            open_route.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            open_route.new_condition.timer(timer=1)
            destination_x, destination_y = v2_cell_for_player(
                scenario_player,
                medium_task_template.location_x,
                medium_task_template.location_y,
            )
            for unit_id in dict.fromkeys(
                unit_id for _threshold, unit_id in HERO_MILESTONES
            ):
                open_route.new_effect.task_object(
                    object_list_unit_id=unit_id,
                    source_player=world_player,
                    location_x=destination_x,
                    location_y=destination_y,
                    area_x1=spawn_x - 1,
                    area_y1=spawn_y - 1,
                    area_x2=spawn_x + 1,
                    area_y2=spawn_y + 1,
                    action_type=ActionType.MOVE,
                )


def _add_sparse_feudal_upgrades(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Apply the original timed upgrade package at the occupied color's Blacksmith."""
    for scenario_player in PLAYERS:
        original = _unique_trigger(ctx, f"feudal ups (p{int(scenario_player)})")
        blacksmith_conditions = [
            condition
            for condition in original.conditions
            if condition.condition_type == ConditionId.OBJECTS_IN_AREA
            and condition.object_list == BuildingInfo.BLACKSMITH.ID
        ]
        if len(blacksmith_conditions) != 1:
            raise RuntimeError(
                f"expected one Blacksmith condition for P{int(scenario_player)}, "
                f"found {len(blacksmith_conditions)}"
            )
        (
            blacksmith_conditions[0].area_x1,
            blacksmith_conditions[0].area_y1,
            blacksmith_conditions[0].area_x2,
            blacksmith_conditions[0].area_y2,
        ) = BLACKSMITH_AREAS[scenario_player]
        original.new_condition.variable_value(
            quantity=1,
            variable=active_variables[scenario_player],
            comparison=Comparison.EQUAL,
        )
        original.new_condition.variable_value(
            quantity=int(scenario_player),
            variable=world_variables[scenario_player],
            comparison=Comparison.EQUAL,
        )
        for world_player in _possible_world_players(scenario_player):
            if world_player == scenario_player:
                continue
            remapped = ctx.tm.add_trigger(
                f"Sparse Feudal S{int(scenario_player)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            remapped.conditions.extend(
                _copy_for_world_player(condition, scenario_player, world_player)
                for condition in original.conditions
                if not (
                    condition.condition_type == ConditionId.VARIABLE_VALUE
                    and condition.variable
                    in {
                        active_variables[scenario_player],
                        world_variables[scenario_player],
                    }
                )
            )
            remapped.new_condition.variable_value(
                quantity=1,
                variable=active_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            remapped.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            remapped.effects.extend(
                _copy_for_world_player(effect, scenario_player, world_player) for effect in original.effects
            )


def _remap_raze_villagers(
    ctx: BuildContext,
    active_variables,
    world_variables,
    match_ready_variable,
) -> None:
    """Create and reliably park builder pairs beside each color's Castles."""
    pending_variables = {
        scenario_player: ctx.tm.add_variable(
            f"pending_builders_p{int(scenario_player)}",
            variable_id=int(scenario_player) - 1,
        ).variable_id
        for scenario_player in PLAYERS
    }

    originals = {
        scenario_player: _unique_trigger(ctx, f"1 raze (p{int(scenario_player)})")
        for scenario_player in PLAYERS
    }
    template_effects = [
        deepcopy(effect)
        for effect in originals[PlayerId.THREE].effects
        if (
            effect.effect_type == EffectId.SEND_CHAT
            or (
                effect.effect_type == EffectId.CREATE_OBJECT
                and effect.object_list_unit_id
                in {UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID}
            )
        )
    ]
    if len(template_effects) != 3:
        raise RuntimeError(
            f"expected one chat and two canonical builder creates, found {len(template_effects)}"
        )

    legacy_stage_ids = set()
    for scenario_player in PLAYERS:
        for remaining in range(1, 6):
            noun = "raze" if remaining == 1 else "razes"
            trigger = _unique_trigger(ctx, f"{remaining} {noun} (p{int(scenario_player)})")
            legacy_stage_ids.add(trigger.trigger_id)
            original_id = trigger.trigger_id
            _reset_trigger(trigger)
            trigger.name = f"Legacy Raze Reward Disabled #{original_id}"

    # Civilization selectors no longer need to activate a color-number-bound
    # legacy chain; XS calculates the exact cumulative entitlement instead.
    for trigger in ctx.tm.triggers:
        trigger.effects = [
            effect
            for effect in trigger.effects
            if not (effect.effect_type == EffectId.ACTIVATE_TRIGGER and effect.trigger_id in legacy_stage_ids)
        ]

    for scenario_player in PLAYERS:
        for unit_id in (UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID):
            for label, points in (
                ("spawn", BUILDER_SPAWN_POINTS),
                ("destination", BUILDER_DESTINATION_POINTS),
            ):
                x, y = points[scenario_player][unit_id]
                tile = ctx.mm.get_tile(x=x, y=y)
                if tile.terrain_id in {
                    TerrainId.WATER_SHALLOW,
                    TerrainId.WATER_DEEP,
                    TerrainId.WATER_MEDIUM,
                }:
                    raise RuntimeError(
                        f"P{int(scenario_player)} builder {label} ({x}, {y}) is water"
                    )
                occupied = [
                    unit
                    for units in ctx.um.units
                    for unit in units
                    if int(unit.x) == x and int(unit.y) == y
                ]
                if occupied:
                    references = ", ".join(str(unit.reference_id) for unit in occupied)
                    raise RuntimeError(
                        f"P{int(scenario_player)} builder {label} ({x}, {y}) "
                        f"is occupied by refs {references}"
                    )

        area_x1, area_y1, area_x2, area_y2 = BASE_CASTLE_AREAS[scenario_player]
        for world_player in _possible_world_players(scenario_player):
            reward = ctx.tm.add_trigger(
                f"Builder Reward S{int(scenario_player)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
                enabled=1,
                looping=1,
            )
            reward.new_condition.timer(timer=1)
            reward.new_condition.variable_value(
                quantity=1,
                inverted=-1,
                variable=pending_variables[scenario_player],
                comparison=Comparison.LARGER_OR_EQUAL,
            )
            reward.new_condition.variable_value(
                quantity=1,
                variable=active_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            reward.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            reward.new_condition.objects_in_area(
                quantity=1,
                object_list=BuildingInfo.CASTLE.ID,
                source_player=world_player,
                area_x1=area_x1,
                area_y1=area_y1,
                area_x2=area_x2,
                area_y2=area_y2,
            )
            for source_effect in template_effects:
                effect = _copy_for_world_player(
                    source_effect,
                    PlayerId.THREE,
                    world_player,
                )
                if effect.effect_type == EffectId.CREATE_OBJECT:
                    effect.location_x, effect.location_y = BUILDER_SPAWN_POINTS[
                        scenario_player
                    ][effect.object_list_unit_id]
                reward.effects.append(effect)
            reward.new_effect.change_variable(
                quantity=1,
                operation=Operation.SUBTRACT,
                variable=pending_variables[scenario_player],
            )

            mover = ctx.tm.add_trigger(
                f"Builder Move S{int(scenario_player)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
                enabled=1,
                looping=1,
            )
            mover.new_condition.timer(timer=1)
            mover.new_condition.variable_value(
                quantity=1,
                variable=active_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            mover.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[scenario_player],
                comparison=Comparison.EQUAL,
            )
            for unit_id in (
                UnitInfo.VILLAGER_MALE.ID,
                UnitInfo.VILLAGER_FEMALE.ID,
            ):
                spawn_x, spawn_y = BUILDER_SPAWN_POINTS[scenario_player][unit_id]
                destination_x, destination_y = BUILDER_DESTINATION_POINTS[
                    scenario_player
                ][unit_id]
                mover.new_effect.task_object(
                    object_list_unit_id=unit_id,
                    source_player=world_player,
                    location_x=destination_x,
                    location_y=destination_y,
                    area_x1=spawn_x - 1,
                    area_y1=spawn_y - 1,
                    area_x2=spawn_x + 1,
                    area_y2=spawn_y + 1,
                    action_type=ActionType.MOVE,
                )


def _relocate_builder_spawn_flags(ctx: BuildContext) -> None:
    """Move only the two old builder flags onto the widened rear causeway."""
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    for player in PLAYERS:
        for source_position, target_position in zip(
            SOURCE_BUILDER_FLAG_POSITIONS,
            SOURCE_BUILDER_FLAG_TARGETS,
            strict=True,
        ):
            old_x, old_y = v2_position_for_player(player, *source_position)
            new_x, new_y = v2_position_for_player(player, *target_position)
            flags = [
                unit
                for unit in ctx.um.units[player]
                if unit.unit_const == OtherInfo.FLAG_A.ID
                and (unit.x, unit.y) == (old_x, old_y)
            ]
            if len(flags) != 1:
                raise RuntimeError(
                    f"expected one P{int(player)} builder flag at "
                    f"({old_x}, {old_y}), found {len(flags)}"
                )
            if any(
                (unit.x, unit.y) == (new_x, new_y)
                for units in ctx.um.units
                for unit in units
                if unit is not flags[0]
            ):
                raise RuntimeError(
                    f"occupied P{int(player)} builder-flag target at "
                    f"({new_x}, {new_y})"
                )
            if ctx.mm.get_tile(x=int(new_x), y=int(new_y)).terrain_id in water:
                raise RuntimeError(
                    f"P{int(player)} builder-flag target ({new_x}, {new_y}) is water"
                )
            flags[0].x = new_x
            flags[0].y = new_y


def _remove_remaining_ice_decorations(ctx: BuildContext) -> None:
    """Remove the legacy ice objects that obstruct otherwise buildable shore."""
    ice_objects = [
        unit
        for units in ctx.um.units
        for unit in units
        if unit.unit_const == OtherInfo.ICE_NAVIGABLE.ID
    ]
    if len(ice_objects) != 20:
        raise RuntimeError(
            f"expected 20 remaining legacy ice decorations, found {len(ice_objects)}"
        )
    for unit in ice_objects:
        ctx.um.remove_unit(unit=unit)


def _add_spawn_marker_boats(ctx: BuildContext) -> None:
    """Mark every color's milestone-hero spawn with an immobile Transport Ship."""
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    ctx.um.reference_id_generator = create_id_generator(
        ctx.um.find_highest_reference_id() + 1
    )
    for player, (x, y) in SPAWN_MARKER_BOAT_POSITIONS.items():
        tile = ctx.mm.get_tile(x=int(x), y=int(y))
        if tile.terrain_id not in water:
            raise RuntimeError(
                f"P{int(player)} spawn-marker boat ({x}, {y}) is not on water"
            )
        occupied = [
            unit
            for units in ctx.um.units
            for unit in units
            if (unit.x, unit.y) == (x, y)
        ]
        if occupied:
            references = ", ".join(str(unit.reference_id) for unit in occupied)
            raise RuntimeError(
                f"P{int(player)} spawn-marker boat position ({x}, {y}) "
                f"is occupied by refs {references}"
            )

        castle_x1, castle_y1, castle_x2, castle_y2 = BASE_CASTLE_AREAS[player]
        target_x = (castle_x1 + castle_x2) / 2
        target_y = (castle_y1 + castle_y2) / 2
        boat = ctx.um.add_unit(
            player=player,
            unit_const=UnitInfo.TRANSPORT_SHIP.ID,
            x=x,
            y=y,
            rotation=math.atan2(target_y - y, target_x - x) % (2 * math.pi),
        )
        protection = _unique_trigger(ctx, f"Antidelete P{int(player)}")
        selected = [boat.reference_id]
        protection.new_effect.disable_object_deletion(
            source_player=player,
            selected_object_ids=selected,
        )
        protection.new_effect.disable_object_selection(
            source_player=player,
            selected_object_ids=selected,
        )
        protection.new_effect.disable_unit_attackable(
            source_player=player,
            selected_object_ids=selected,
        )
        protection.new_effect.disable_unit_targeting(
            source_player=player,
            selected_object_ids=selected,
        )
        protection.new_effect.freeze_object(
            source_player=player,
            selected_object_ids=selected,
        )
        protection.new_effect.change_object_speed(
            quantity=0,
            source_player=player,
            selected_object_ids=selected,
        )


def _force_bombard_tower_unlock(ctx: BuildContext) -> None:
    """Grant Bombard Towers through the confirmed color-to-runtime mapping."""
    legacy = _unique_trigger(ctx, "BT -------------------- By: System")
    _reset_trigger(legacy)
    legacy.name = "Legacy Bombard Tower Unlock Disabled"

    configured = 0
    for color in PLAYERS:
        for world_player in _possible_world_players(color):
            occupied = _unique_trigger(
                ctx,
                f"Occupied Slot S{int(color)} W{int(world_player)}",
            )
            occupied.new_effect.research_technology(
                source_player=world_player,
                technology=TechInfo.BOMBARD_TOWER.ID,
                force_research_technology=1,
            )
            occupied.new_effect.enable_disable_object(
                object_list_unit_id=BuildingInfo.BOMBARD_TOWER.ID,
                source_player=world_player,
                enabled=1,
            )
            configured += 1
    if configured != 36:
        raise RuntimeError(
            f"expected 36 mapped Bombard Tower grants, configured {configured}"
        )


def _finalize_occupied_slot_gates(ctx: BuildContext) -> None:
    """Retry occupied-color setup until its owner is known, then stop it."""
    configured = 0
    for color in PLAYERS:
        for world_player in _possible_world_players(color):
            gate = _unique_trigger(
                ctx,
                f"Occupied Slot S{int(color)} W{int(world_player)}",
            )
            gate.looping = 1
            gate.new_effect.deactivate_trigger(trigger_id=gate.trigger_id)
            configured += 1
    if configured != 36:
        raise RuntimeError(
            f"expected 36 retrying occupied-slot gates, configured {configured}"
        )


def _add_rear_enclosures(ctx: BuildContext) -> None:
    """Close every base's rear edge while leaving the allied route open."""
    # The decompiled source places explicit legacy IDs and therefore leaves the
    # blank scenario's generator at zero. Resume after the real maximum so new
    # buildings and trigger selections cannot collide with existing units.
    ctx.um.reference_id_generator = create_id_generator(ctx.um.find_highest_reference_id() + 1)

    protected_by_player = {player: [] for player in PLAYERS}
    for player, gate_x, placeholder_ys, adjacent_wall_y, gate_y in REAR_SIDE_GATES:
        for placeholder_y in placeholder_ys:
            matches = [
                unit
                for unit in ctx.um.units[player]
                if unit.unit_const == OtherInfo.ICE_NAVIGABLE.ID
                and (unit.x, unit.y) == (gate_x, placeholder_y)
            ]
            if len(matches) != 1:
                raise RuntimeError(
                    f"expected one rear side-gate placeholder for P{int(player)} "
                    f"at ({gate_x}, {placeholder_y}), found {len(matches)}"
                )
            ctx.um.remove_unit(unit=matches[0])

        adjacent_walls = [
            unit
            for unit in ctx.um.units[player]
            if unit.unit_const == BuildingInfo.STONE_WALL.ID and (unit.x, unit.y) == (gate_x, adjacent_wall_y)
        ]
        if len(adjacent_walls) != 1:
            raise RuntimeError(
                f"expected one wall beside rear side gate for P{int(player)} "
                f"at ({gate_x}, {adjacent_wall_y}), found {len(adjacent_walls)}"
            )
        ctx.um.remove_unit(unit=adjacent_walls[0])

        side_gate = ctx.um.add_unit(
            player=player,
            unit_const=BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID,
            x=gate_x,
            y=gate_y,
        )
        protected_by_player[player].append(side_gate.reference_id)

    for player, axis, line, start, end in REAR_END_CONNECTORS:
        rotation = 0 if axis == "horizontal" else 1
        for position in (start + offset for offset in range(int(end - start) + 1)):
            x, y = (position, line) if axis == "horizontal" else (line, position)
            existing = [
                unit
                for unit in ctx.um.units[player]
                if unit.unit_const == BuildingInfo.STONE_WALL.ID and (unit.x, unit.y) == (x, y)
            ]
            if existing:
                raise RuntimeError(
                    f"unexpected existing rear connector wall for P{int(player)} at ({x}, {y})"
                )
            connector = ctx.um.add_unit(
                player=player,
                unit_const=BuildingInfo.STONE_WALL.ID,
                x=x,
                y=y,
                rotation=rotation,
            )
            protected_by_player[player].append(connector.reference_id)

    for player, axis, line, positions in FRONT_GATE_END_EXTENSIONS:
        rotation = 0 if axis == "horizontal" else 1
        for position in positions:
            x, y = (position, line) if axis == "horizontal" else (line, position)
            tile = ctx.mm.get_tile(x=int(x), y=int(y))
            if tile.terrain_id in {
                TerrainId.WATER_SHALLOW,
                TerrainId.WATER_DEEP,
                TerrainId.WATER_MEDIUM,
            }:
                tile.terrain_id = TerrainId.BEACH
            existing = [
                unit
                for unit in ctx.um.units[player]
                if unit.unit_const == BuildingInfo.STONE_WALL.ID
                and (unit.x, unit.y) == (x, y)
            ]
            if existing:
                raise RuntimeError(
                    f"unexpected existing front-gate extension for P{int(player)} "
                    f"at ({x}, {y})"
                )
            extension = ctx.um.add_unit(
                player=player,
                unit_const=BuildingInfo.STONE_WALL.ID,
                x=x,
                y=y,
                rotation=rotation,
            )
            protected_by_player[player].append(extension.reference_id)

    for player, axis, line, wall_segments, gate_axis, tower_positions in REAR_ENCLOSURES:
        protected_ids = protected_by_player[player]
        wall_rotation = 0 if axis == "horizontal" else 1
        for start, end in wall_segments:
            for position in (start + offset for offset in range(int(end - start) + 1)):
                x, y = (position, line) if axis == "horizontal" else (line, position)
                wall = ctx.um.add_unit(
                    player=player,
                    unit_const=BuildingInfo.STONE_WALL.ID,
                    x=x,
                    y=y,
                    rotation=wall_rotation,
                )
                protected_ids.append(wall.reference_id)

        gate_x, gate_y = (gate_axis, line) if axis == "horizontal" else (line, gate_axis)
        gate_const = (
            BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID
            if axis == "horizontal"
            else BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID
        )
        gate = ctx.um.add_unit(
            player=player,
            unit_const=gate_const,
            x=gate_x,
            y=gate_y,
        )
        protected_ids.append(gate.reference_id)

        for tower_x, tower_y in tower_positions:
            tower = ctx.um.add_unit(
                player=player,
                unit_const=BuildingInfo.BOMBARD_TOWER.ID,
                x=tower_x,
                y=tower_y,
                rotation=2,
            )
            protected_ids.append(tower.reference_id)

        _unique_trigger(ctx, f"Antidelete P{int(player)}").new_effect.disable_object_deletion(
            source_player=player,
            selected_object_ids=protected_ids,
        )


def _open_rear_technology_paths(ctx: BuildContext) -> None:
    """Open two-tile causeways from each rear gate to its technology island."""
    for player, (x1, y1, x2, y2), cliff_specs in REAR_TECH_PATHS:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                tile = ctx.mm.get_tile(x=x, y=y)
                actual = (tile.terrain_id, tile.elevation, tile.layer)
                expected_terrains = {TerrainId.WATER_MEDIUM, TerrainId.BEACH_ICE}
                if tile.terrain_id not in expected_terrains or tile.elevation != 1 or tile.layer != -1:
                    raise RuntimeError(
                        f"unexpected rear path tile for P{int(player)} at ({x}, {y}): "
                        f"expected water/beach at elevation 1, found {actual}"
                    )
                tile.terrain_id = TerrainId.SNOW

        for reference_id, unit_const, x, y in cliff_specs:
            matches = [
                unit
                for unit in ctx.um.units[PlayerId.GAIA]
                if unit.reference_id == reference_id
                and unit.unit_const == unit_const
                and (unit.x, unit.y) == (x, y)
            ]
            if len(matches) != 1:
                raise RuntimeError(
                    f"expected one rear-path cliff for P{int(player)} at ({x}, {y}), found {len(matches)}"
                )
            ctx.um.remove_unit(unit=matches[0])


def _finish_rear_perimeters(ctx: BuildContext) -> None:
    """Join each cliff gate cleanly, with dry land inside and water outside."""
    allowed_terrain = {
        TerrainId.WATER_DEEP,
        TerrainId.WATER_MEDIUM,
        TerrainId.BEACH_ICE,
        TerrainId.SNOW,
        TerrainId.ICE,
    }
    causeway_tiles = {
        (x, y)
        for _player, (x1, y1, x2, y2), _cliff_specs in REAR_TECH_PATHS
        for y in range(y1, y2 + 1)
        for x in range(x1, x2 + 1)
    }
    for player, apron, outside_water in REAR_LAND_APRONS:
        for rectangle, terrain_id in (
            (apron, TerrainId.SNOW),
            (outside_water, TerrainId.WATER_MEDIUM),
        ):
            x1, y1, x2, y2 = rectangle
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if terrain_id == TerrainId.WATER_MEDIUM and (x, y) in causeway_tiles:
                        continue
                    tile = ctx.mm.get_tile(x=x, y=y)
                    if tile.terrain_id not in allowed_terrain or tile.elevation != 1 or tile.layer != -1:
                        raise RuntimeError(
                            f"unexpected rear perimeter tile for P{int(player)} at ({x}, {y}): "
                            f"found {(tile.terrain_id, tile.elevation, tile.layer)}"
                        )
                    tile.terrain_id = terrain_id

        x1, y1, x2, y2 = apron
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                tile = ctx.mm.get_tile(x=x, y=y)
                if tile.terrain_id != TerrainId.SNOW:
                    raise RuntimeError(
                        f"non-land tile remains inside P{int(player)} rear perimeter at ({x}, {y})"
                    )

    for player, cap_rectangles in REAR_WATER_END_CAPS:
        for x1, y1, x2, y2 in cap_rectangles:
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    tile = ctx.mm.get_tile(x=x, y=y)
                    if (
                        tile.terrain_id not in allowed_terrain
                        or tile.elevation != 1
                        or tile.layer != -1
                    ):
                        raise RuntimeError(
                            f"unexpected rear water-cap tile for P{int(player)} at "
                            f"({x}, {y}): found "
                            f"{(tile.terrain_id, tile.elevation, tile.layer)}"
                        )
                    tile.terrain_id = TerrainId.WATER_MEDIUM

    default_cliffs = {getattr(OtherInfo, f"CLIFF_DEFAULT_{index}").ID for index in range(1, 10)}
    expected_cleanup_counts = {
        PlayerId.ONE: 11,
        PlayerId.TWO: 11,
        PlayerId.THREE: 11,
        PlayerId.FOUR: 10,
        PlayerId.FIVE: 13,
        PlayerId.SIX: 10,
        PlayerId.SEVEN: 11,
        PlayerId.EIGHT: 9,
    }
    for player, (x1, y1, x2, y2) in REAR_CLIFF_CLEANUP_AREAS:
        obsolete = [
            unit
            for unit in ctx.um.units[PlayerId.GAIA]
            if unit.unit_const in default_cliffs and x1 <= unit.x <= x2 and y1 <= unit.y <= y2
        ]
        if len(obsolete) != expected_cleanup_counts[player]:
            raise RuntimeError(
                f"unexpected old rear cliff count for P{int(player)}: "
                f"expected {expected_cleanup_counts[player]}, found {len(obsolete)}"
            )
        for unit in obsolete:
            ctx.um.remove_unit(unit=unit)

    for player, axis, line, start, end, gate_axis, unit_const, rotations in REAR_CLIFF_PERIMETERS:
        expected_positions = set()
        positions = (start + 3 * offset for offset in range(int((end - start) / 3) + 1))
        for index, position in enumerate(positions):
            if abs(position - gate_axis) < 2:
                continue
            x, y = (position, line) if axis == "horizontal" else (line, position)
            ctx.um.add_unit(
                player=PlayerId.GAIA,
                unit_const=unit_const,
                x=x,
                y=y,
                rotation=rotations[index % len(rotations)],
            )
            expected_positions.add((x, y))

        actual_positions = {
            (unit.x, unit.y)
            for unit in ctx.um.units[PlayerId.GAIA]
            if unit.unit_const == unit_const and (unit.x, unit.y) in expected_positions
        }
        if actual_positions != expected_positions:
            raise RuntimeError(
                f"unexpected rebuilt rear cliff perimeter for P{int(player)}: "
                f"expected {sorted(expected_positions)}, found {sorted(actual_positions)}"
            )


def _rewrite_public_messages(ctx: BuildContext) -> None:
    messages = ctx.message_manager
    messages.instructions = PUBLIC_INSTRUCTIONS
    messages.history = (
        "CBA Hero: Ascendants.\r"
        "Automatic armies earn stronger heroes through combat. Guard four Castles, support "
        "your allies through the protected team routes, and destroy every enemy Castle."
    )
    messages.hints = (
        "Defeat enemy units to ascend through six hero tiers. Protect all four Castles, "
        "choose an army route with the relic selectors, and use the rear gates to reinforce "
        "your allies."
    )
    messages.scouts = (
        "Blue/Red/Green/Yellow face Teal/Purple/Gray/Orange. Close unused slots while keeping "
        "both color teams represented. Every territory has equal mirrored terrain and "
        "defenses."
    )
    messages.victory = (
        "\rASCENDANT VICTORY\rYour team destroyed every enemy Castle."
    )
    messages.loss = (
        "\rDEFEAT\rYour Castles have fallen. Return to the map to watch the battle."
    )


def _sanitize_serialized_labels(ctx: BuildContext) -> None:
    """Remove obsolete identity and attribution text after all name-based passes."""
    for trigger in ctx.tm.triggers:
        for attribute in ("name", "description", "short_description"):
            value = getattr(trigger, attribute, "") or ""
            value = re.sub(r"Reforged", "Ascendants", value, flags=re.IGNORECASE)
            value = re.sub(
                r"Evolution Alpha",
                "Ascendants",
                value,
                flags=re.IGNORECASE,
            )
            value = re.sub(
                r"\s*By:\s*System\s*",
                " ",
                value,
                flags=re.IGNORECASE,
            ).strip()
            setattr(trigger, attribute, value)


def _add_sparse_lobby_scoreboard(
    ctx: BuildContext,
    active_variables,
    world_variables,
) -> None:
    """Build a compact right-side combat HUD and guard the zero-resource economy."""
    tm = ctx.tm

    equalizers = {PlayerId.ONE: _unique_trigger(ctx, "Resource Equalizer")}
    _configure_equalizer(equalizers[PlayerId.ONE], PlayerId.ONE)
    for player in PLAYERS[1:]:
        equalizer = tm.add_trigger(f"Resource Equalizer P{int(player)}")
        _configure_equalizer(equalizer, player)
        equalizers[player] = equalizer

    header = _unique_trigger(ctx, "Kills and Deaths")
    _configure_combat_hud_header(header)

    divider = tm.add_trigger(
        "Combat HUD Team Divider",
        description_stid=0,
        short_description="----------------",
        short_description_stid=0,
        display_on_screen=1,
        description_order=14,
        enabled=1,
        mute_objectives=1,
    )
    divider.new_condition.player_defeated(source_player=PlayerId.GAIA)

    placeholder_rows = {}
    live_rows = {}
    for player in PLAYERS:
        player_number = int(player)
        variable_base = 8 + ((player_number - 1) * 3)
        variable_names = (
            f"p{player_number}k",
            f"p{player_number}d",
            f"p{player_number}r",
        )
        for offset, name in enumerate(variable_names):
            tm.add_variable(name, variable_id=variable_base + offset)

        display_order = (
            19 - player_number
            if player_number <= 4
            else 18 - player_number
        )
        placeholder = tm.add_trigger(
            f"Combat HUD Empty P{player_number}",
            description_stid=0,
            short_description=f"P{player_number} | - | - | -",
            short_description_stid=0,
            display_on_screen=1,
            description_order=display_order,
            enabled=1,
            mute_objectives=1,
        )
        placeholder.new_condition.player_defeated(source_player=PlayerId.GAIA)
        placeholder_rows[player] = placeholder

        kills_name, deaths_name, razings_name = variable_names
        live = tm.add_trigger(
            f"Combat HUD Live P{player_number}",
            description_stid=0,
            short_description=(
                f"P{player_number} | <{kills_name}> | "
                f"<{deaths_name}> | <{razings_name}>"
            ),
            short_description_stid=0,
            display_on_screen=1,
            description_order=display_order,
            enabled=0,
            mute_objectives=1,
        )
        live.new_condition.player_defeated(source_player=PlayerId.GAIA)
        live_rows[player] = live

    free_costs = {}
    for player in PLAYERS:
        trigger = _unique_trigger(ctx, f"resources (p{int(player)})")
        _configure_free_costs(trigger, player)
        free_costs[player] = trigger

    for color in PLAYERS:
        for world_player in _possible_world_players(color):
            gate = tm.add_trigger(
                f"Occupied Slot S{int(color)} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
            )
            gate.new_condition.timer(timer=LOBBY_SETTLE_SECONDS)
            gate.new_condition.variable_value(
                quantity=1,
                variable=active_variables[color],
                comparison=Comparison.EQUAL,
            )
            gate.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[color],
                comparison=Comparison.EQUAL,
            )
            gate.new_effect.activate_trigger(
                trigger_id=equalizers[world_player].trigger_id
            )
            gate.new_effect.activate_trigger(
                trigger_id=free_costs[world_player].trigger_id
            )
            gate.new_effect.deactivate_trigger(
                trigger_id=placeholder_rows[color].trigger_id
            )
            gate.new_effect.activate_trigger(trigger_id=live_rows[color].trigger_id)


def _add_live_white_king_kill_counters(ctx: BuildContext) -> None:
    """Show every color's live kill total on its white selector King.

    Trigger-variable tokens are expanded in objective text but are printed
    literally by Change Object Name. Keep the name static and publish the
    exact live value through the King's displayed sword/attack statistic.
    """
    counter_references = set(WHITE_KING_KILL_COUNTERS.values())
    removed_legacy_effects = 0
    for trigger in ctx.tm.triggers:
        retained_effects = []
        for effect in trigger.effects:
            selected_references = set(effect.selected_object_ids or ())
            if (
                effect.effect_type == EffectId.CHANGE_OBJECT_NAME
                and selected_references & counter_references
            ):
                removed_legacy_effects += 1
                continue
            retained_effects.append(effect)
        trigger.effects = retained_effects
    if removed_legacy_effects != 12:
        raise RuntimeError(
            "expected 12 legacy white-King kill labels, removed "
            f"{removed_legacy_effects}"
        )

    configured = 0
    for color, reference_id in WHITE_KING_KILL_COUNTERS.items():
        color_number = int(color)
        kills_variable = 8 + ((color_number - 1) * 3)
        for world_player in _possible_world_players(color):
            live_counter = ctx.tm.add_trigger(
                f"White King Kills S{color_number} W{int(world_player)}",
                description_stid=0,
                short_description_stid=0,
                enabled=0,
                looping=1,
            )
            live_counter.new_condition.timer(timer=1)
            live_counter.new_effect.change_object_name(
                source_player=world_player,
                message=f"P{color_number} Kills",
                selected_object_ids=[reference_id],
            )
            live_counter.new_effect.modify_object_attribute_by_variable(
                source_player=world_player,
                object_attributes=ObjectAttribute.SHOWN_ATTACK,
                selected_object_ids=[reference_id],
                operation=Operation.SET,
                variable=kills_variable,
            )
            occupied = _unique_trigger(
                ctx,
                f"Occupied Slot S{color_number} W{int(world_player)}",
            )
            occupied.new_effect.activate_trigger(trigger_id=live_counter.trigger_id)
            configured += 1
    if configured != 36:
        raise RuntimeError(
            f"expected 36 mapped White King counters, configured {configured}"
        )


def _configure_sparse_vote_kick(
    ctx: BuildContext,
    active_variables,
    world_variables,
    eliminated_variables,
    match_ready_variable,
) -> None:
    """Require two occupied teammates to delete their target vote markers.

    The color activity variables are maintained by XS through
    ``xsGetWorldPlayerId``. Requiring the target and both distinct voters to be
    active means a side needs at least three live colors before a vote can
    resolve. Closed slots therefore cannot create startup votes, and a side
    reduced to two colors cannot kick again.
    """
    unit_by_reference = {
        unit.reference_id: (PlayerId(player), unit)
        for player, units in enumerate(ctx.um.units)
        for unit in units
    }
    color_by_name = {name: player for player, name in PLAYER_COLOR_NAMES.items()}
    rename_triggers = [
        trigger for trigger in ctx.tm.triggers if trigger.name == "==Rename======"
    ]
    if len(rename_triggers) != 2:
        raise RuntimeError(
            f"expected two legacy rename triggers, found {len(rename_triggers)}"
        )
    vote_markers = {}
    for effect in (
        effect for trigger in rename_triggers for effect in trigger.effects
    ):
        if (
            effect.effect_type != EffectId.CHANGE_OBJECT_NAME
            or not (effect.message or "").startswith("Delete Vote Kick ")
        ):
            continue
        target_name = effect.message.removeprefix("Delete Vote Kick ")
        target = color_by_name.get(target_name)
        if target is None or len(effect.selected_object_ids) != 1:
            raise RuntimeError(f"invalid vote marker rename effect: {effect.message!r}")
        reference_id = effect.selected_object_ids[0]
        voter, marker = unit_by_reference[reference_id]
        if marker.unit_const != BuildingInfo.OUTPOST.ID:
            raise RuntimeError(
                f"vote marker {reference_id} is unit {marker.unit_const}, not an Outpost"
            )
        key = (target, voter)
        if key in vote_markers:
            raise RuntimeError(
                f"duplicate P{int(voter)} vote marker for P{int(target)}"
            )
        vote_markers[key] = marker

    expected_marker_keys = {
        (target, voter)
        for team in (PLAYERS[:4], PLAYERS[4:])
        for target in team
        for voter in team
        if voter != target
    }
    if vote_markers.keys() != expected_marker_keys:
        missing = expected_marker_keys - vote_markers.keys()
        extra = vote_markers.keys() - expected_marker_keys
        raise RuntimeError(
            f"unexpected vote-marker mapping; missing={sorted(missing)}, extra={sorted(extra)}"
        )

    # Each target-colored flag labels the matching Outpost on a teammate's
    # vote island. The old layout scattered flags horizontally regardless of
    # the island's orientation, putting several in water or even on top of a
    # marker. Align every flag parallel to its three Outposts on existing land.
    flag_unit_const = OtherInfo.CIV_FLAG_ACHAEMENIDS_2.ID
    flags_by_target = {
        target: [
            unit
            for unit in ctx.um.units[target]
            if unit.unit_const == flag_unit_const
        ]
        for target in PLAYERS
    }
    if any(len(flags) != 3 for flags in flags_by_target.values()):
        counts = {
            int(target): len(flags)
            for target, flags in flags_by_target.items()
        }
        raise RuntimeError(f"expected three vote flags per color, found {counts}")
    original_flag_positions = {
        flag.reference_id: (flag.x, flag.y)
        for flags in flags_by_target.values()
        for flag in flags
    }
    assigned_flags = set()
    water = {int(terrain) for terrain in TerrainId.water_terrains()}
    for target, voter in sorted(
        expected_marker_keys,
        key=lambda key: (int(key[0]), int(key[1])),
    ):
        marker = vote_markers[target, voter]
        candidates = [
            flag
            for flag in flags_by_target[target]
            if flag.reference_id not in assigned_flags
        ]
        flag = min(
            candidates,
            key=lambda candidate: (
                (original_flag_positions[candidate.reference_id][0] - marker.x) ** 2
                + (original_flag_positions[candidate.reference_id][1] - marker.y) ** 2,
                candidate.reference_id,
            ),
        )
        offset_x, offset_y = VOTE_FLAG_OFFSETS[voter]
        flag.x = marker.x + offset_x
        flag.y = marker.y + offset_y
        assigned_flags.add(flag.reference_id)
        if ctx.mm.get_tile(x=int(flag.x), y=int(flag.y)).terrain_id in water:
            raise RuntimeError(
                f"vote flag {flag.reference_id} for P{int(target)} remains on water"
            )
    if len(assigned_flags) != 24:
        raise RuntimeError(f"expected 24 aligned vote flags, found {len(assigned_flags)}")

    ordered_marker_keys = sorted(
        expected_marker_keys,
        key=lambda key: (int(key[0]), int(key[1])),
    )
    vote_variables = {
        key: ctx.tm.add_variable(
            f"votekickp{int(key[0])}byp{int(key[1])}",
            variable_id=VOTE_MARKER_VARIABLE_BASE + index,
        ).variable_id
        for index, key in enumerate(ordered_marker_keys)
    }
    for target, voter in ordered_marker_keys:
        marker = vote_markers[target, voter]
        marker_x = math.floor(marker.x)
        marker_y = math.floor(marker.y)
        # A compacted color can only move downward in runtime numbering, so
        # scenario color Pn has possible world owners W1..Wn.
        for world_player in range(1, int(voter) + 1):
            deleted = ctx.tm.add_trigger(
                f"Vote Marker Deleted P{int(target)} V{int(voter)} W{world_player}",
                description_stid=0,
                short_description_stid=0,
            )
            deleted.new_condition.timer(timer=LOBBY_SETTLE_SECONDS + 1)
            deleted.new_condition.variable_value(
                quantity=1,
                variable=match_ready_variable,
                comparison=Comparison.EQUAL,
            )
            deleted.new_condition.variable_value(
                quantity=1,
                variable=active_variables[voter],
                comparison=Comparison.EQUAL,
            )
            deleted.new_condition.variable_value(
                quantity=world_player,
                variable=world_variables[voter],
                comparison=Comparison.EQUAL,
            )
            deleted.new_condition.objects_in_area(
                quantity=1,
                object_list=BuildingInfo.OUTPOST.ID,
                source_player=world_player,
                area_x1=marker_x,
                area_y1=marker_y,
                area_x2=marker_x,
                area_y2=marker_y,
                inverted=1,
            )
            deleted.new_effect.change_variable(
                quantity=1,
                operation=Operation.SET,
                variable=vote_variables[target, voter],
            )

    resolvers = {}
    for target in PLAYERS:
        area_x1, area_y1, area_x2, area_y2 = BASE_CASTLE_AREAS[target]
        target_resolvers = []
        for world_player in _possible_world_players(target):
            if world_player == target:
                resolver = _unique_trigger(ctx, f"Kick P{int(target)}")
            else:
                resolver = ctx.tm.add_trigger(
                    f"Vote Kick Resolve P{int(target)} W{int(world_player)}",
                    description_stid=0,
                    short_description_stid=0,
                    enabled=0,
                )
            _reset_trigger(resolver)
            resolver.name = (
                f"Vote Kick Resolve P{int(target)} W{int(world_player)}"
            )
            resolver.new_condition.variable_value(
                quantity=1,
                variable=match_ready_variable,
                comparison=Comparison.EQUAL,
            )
            resolver.new_condition.variable_value(
                quantity=1,
                variable=active_variables[target],
                comparison=Comparison.EQUAL,
            )
            resolver.new_condition.variable_value(
                quantity=int(world_player),
                variable=world_variables[target],
                comparison=Comparison.EQUAL,
            )
            resolver.new_condition.objects_in_area(
                quantity=1,
                object_list=BuildingInfo.CASTLE.ID,
                source_player=world_player,
                area_x1=area_x1,
                area_y1=area_y1,
                area_x2=area_x2,
                area_y2=area_y2,
            )
            resolver.new_effect.send_chat(
                source_player=-1,
                message=f"{PLAYER_COLOR_NAMES[target]} has been vote-kicked.",
            )
            resolver.new_effect.change_variable(
                quantity=0,
                operation=Operation.SET,
                variable=active_variables[target],
            )
            resolver.new_effect.change_variable(
                quantity=1,
                operation=Operation.SET,
                variable=eliminated_variables[target],
            )
            resolver.new_effect.remove_object(
                source_player=world_player,
                area_x1=0,
                area_y1=0,
                area_x2=143,
                area_y2=143,
            )
            resolver.new_effect.declare_victory(
                source_player=world_player,
                enabled=0,
            )
            target_resolvers.append(resolver)
        resolvers[target] = tuple(target_resolvers)

    configured = 0
    for trigger in ctx.tm.triggers:
        match = VOTE_KICK_NAME.fullmatch(trigger.name)
        if not match:
            continue
        target, first_voter, second_voter = (
            PlayerId(int(value)) for value in match.groups()
        )
        original_name = trigger.name
        _reset_trigger(trigger)
        trigger.name = original_name
        trigger.enabled = 1
        trigger.new_condition.timer(timer=LOBBY_SETTLE_SECONDS + 1)
        trigger.new_condition.variable_value(
            quantity=1,
            variable=match_ready_variable,
            comparison=Comparison.EQUAL,
        )
        for participant in (target, first_voter, second_voter):
            trigger.new_condition.variable_value(
                quantity=1,
                variable=active_variables[participant],
                comparison=Comparison.EQUAL,
            )
        for voter in (first_voter, second_voter):
            trigger.new_condition.variable_value(
                quantity=1,
                variable=vote_variables[target, voter],
                comparison=Comparison.EQUAL,
            )
        for resolver in resolvers[target]:
            trigger.new_effect.activate_trigger(trigger_id=resolver.trigger_id)
        configured += 1

    if configured != 24:
        raise RuntimeError(f"expected 24 safe vote-kick detectors, configured {configured}")


def build(ctx: BuildContext) -> None:
    apply_generated(ctx)

    _reset_unsafe_vote_kick(ctx)
    _remove_legacy_edge_deletion_strips(ctx)
    _disable_legacy_no_wall_cleanup(ctx)
    _optimize_legacy_polling(ctx)
    _protect_rear_routes_from_legacy_base_cleanup(ctx)
    _clear_legacy_resource_score_triggers(ctx)
    _zero_starting_resources(ctx)
    _disable_castle_trebuchets(ctx)
    (
        active_variables,
        world_variables,
        eliminated_variables,
        match_ready_variable,
    ) = _add_color_runtime_variables(ctx)
    _add_color_owner_detection(ctx, active_variables, world_variables)
    _configure_sparse_goth_palisade_bonus(
        ctx,
        active_variables,
        world_variables,
    )
    _configure_sparse_goth_barracks_restriction(
        ctx,
        active_variables,
        world_variables,
    )
    _configure_custom_team_victory(
        ctx,
        active_variables,
        world_variables,
        eliminated_variables,
        match_ready_variable,
    )
    _replace_legacy_army_spawns(ctx)
    _add_sparse_feudal_upgrades(ctx, active_variables, world_variables)
    _add_rear_enclosures(ctx)
    _open_rear_technology_paths(ctx)
    _finish_rear_perimeters(ctx)
    _rewrite_public_messages(ctx)
    _add_sparse_lobby_scoreboard(ctx, active_variables, world_variables)
    _force_bombard_tower_unlock(ctx)
    _add_live_white_king_kill_counters(ctx)
    _disable_fixed_color_kill_announcements(ctx)
    _configure_sparse_center_views(ctx, active_variables, world_variables)

    v2_report = apply_v2_map(ctx)
    _remap_v2_trigger_geometry(ctx)
    _restore_mobile_distance_movers(ctx)
    _configure_sparse_center_rewards(ctx, active_variables, world_variables)
    _align_selector_labels(ctx)
    _configure_sparse_wall_breaches(ctx, active_variables, world_variables)
    _configure_sparse_king_islands(ctx, active_variables, world_variables)
    _relocate_builder_spawn_flags(ctx)
    _remove_remaining_ice_decorations(ctx)
    _add_spawn_marker_boats(ctx)
    _remap_raze_villagers(
        ctx,
        active_variables,
        world_variables,
        match_ready_variable,
    )
    _configure_sparse_hero_milestones(
        ctx,
        active_variables,
        world_variables,
        match_ready_variable,
    )
    _configure_sparse_late_hero_boosts(
        ctx,
        active_variables,
        world_variables,
    )
    _configure_sparse_vote_kick(
        ctx,
        active_variables,
        world_variables,
        eliminated_variables,
        match_ready_variable,
    )
    _finalize_occupied_slot_gates(ctx)
    _retire_obsolete_public_loops(ctx)
    _neutralize_fixed_color_tags(ctx)
    _sanitize_serialized_labels(ctx)
    for player, reference_ids in v2_report.new_wall_ids.items():
        protections = [
            effect
            for effect in _unique_trigger(ctx, f"Antidelete P{int(player)}").effects
            if effect.effect_type == EffectId.DISABLE_OBJECT_DELETION
            and effect.selected_object_ids
        ]
        if not protections:
            raise RuntimeError(f"missing Antidelete protection for P{int(player)}")
        protections[-1].selected_object_ids.extend(reference_ids)

    _compact_legacy_trigger_graph(ctx)

    ctx.log(
        f"rebuilt from source — {len(ctx.tm.triggers)} triggers, "
        f"{sum(len(units) for units in ctx.um.units)} units; "
        f"Excel V2 moved {v2_report.moved_units} objects and changed "
        f"{v2_report.terrain_changes} terrain squares"
    )
