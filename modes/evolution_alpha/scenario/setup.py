"""Ascendants scenario source — hand-maintained Python, not a decompile.

This file began life as `aoe2modes decompile` output, but Ascendants no longer
round-trips any binary: this code IS the scenario. Edit it directly. Do not run
`aoe2modes decompile --mode evolution_alpha` — there is nothing to decompile
from, and it would overwrite this source.
"""

from __future__ import annotations


from AoE2ScenarioParser.datasets.buildings import BuildingInfo  # noqa: F401
from AoE2ScenarioParser.datasets.heroes import HeroInfo  # noqa: F401
from AoE2ScenarioParser.datasets.object_support import Civilization, StartingAge  # noqa: F401
from AoE2ScenarioParser.datasets.other import OtherInfo  # noqa: F401
from AoE2ScenarioParser.datasets.players import ColorId, PlayerId  # noqa: F401
from AoE2ScenarioParser.datasets.techs import TechInfo  # noqa: F401
from AoE2ScenarioParser.datasets.terrains import TerrainId  # noqa: F401
from AoE2ScenarioParser.datasets.trigger_lists import *  # noqa: F401,F403
from AoE2ScenarioParser.datasets.units import UnitInfo  # noqa: F401


def apply(ctx) -> None:
    """Map, player and lobby settings for the Ascendants arena."""
    mm, pm, om, msg = ctx.mm, ctx.pm, ctx.scenario.option_manager, ctx.message_manager

    # Map size first: resizing rebuilds the terrain array.
    mm.map_size = 144
    mm.map_color_mood = ColorMood.DEFAULT

    pm.active_players = 8
    # --- GAIA
    p = pm.players[0]
    p.starting_age = StartingAge.DARK_AGE
    p.lock_civ = False
    p.lock_personality = False
    p.food = 0
    p.wood = 0
    p.gold = 0
    p.stone = 0
    p.color = ColorId.GRAY
    p.human = False
    p.civilization = Civilization.SARACENS
    p.architecture_set = Civilization.SARACENS
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    # --- P1
    p = pm.players[1]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.BLUE
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Blue'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 109, 621, 72, 50, 276, 68, 104, 45, 598, 199]
    p.disabled_units = [83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 765, 763, 1007, 1009, 692, 694, 876, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 773, 1655, 1657, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 866, 868, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 725, 726, 2107, 2108, 41, 759, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 331, 1234, 1236, 1920, 1922, 282, 556, 280, 11, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 440, 1759, 1761, 1811, 291, 560, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 757, 887, 1105, 1942, 1923]
    p.diplomacy = [DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]
    # --- P2
    p = pm.players[2]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.RED
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Red'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 621, 109, 72, 50, 68, 104, 45, 598, 199, 276]
    p.disabled_units = [83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 763, 765, 1007, 1009, 692, 694, 876, 878, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 773, 1655, 1657, 250, 533, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 866, 868, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 753, 752, 725, 726, 2107, 2108, 41, 759, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 1234, 1236, 1920, 1922, 282, 556, 280, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 440, 1759, 1761, 1811, 291, 560, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 757, 887, 1105, 1942, 1923]
    p.diplomacy = [DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]
    # --- P3
    p = pm.players[3]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.GREEN
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Green'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 621, 109, 72, 50, 68, 104, 45, 598, 199, 276]
    p.disabled_units = [83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 763, 765, 1007, 692, 694, 876, 878, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 773, 1655, 1657, 250, 533, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 725, 726, 2107, 2108, 41, 759, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 331, 1234, 1236, 1920, 1922, 282, 556, 280, 11, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 440, 1759, 1761, 1123, 1125, 1811, 291, 560, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 757, 887, 1105, 1942, 1923]
    p.diplomacy = [DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]
    # --- P4
    p = pm.players[4]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.YELLOW
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Yellow'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 109, 72, 50, 68, 104, 45, 276]
    p.disabled_units = [83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 765, 763, 1007, 1009, 692, 694, 876, 878, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 1655, 1657, 250, 533, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 866, 868, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 753, 752, 725, 726, 2107, 2108, 41, 759, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 331, 1234, 1236, 1920, 1922, 282, 556, 280, 11, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 440, 1759, 1761, 1811, 291, 560, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 757, 887, 1105, 1942, 1923]
    p.diplomacy = [DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]
    # --- P5
    p = pm.players[5]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.AQUA
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Teal'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 621, 109, 72, 50, 68, 104, 45, 598, 199, 276]
    p.disabled_units = [83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 765, 763, 1007, 1009, 692, 694, 876, 878, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 773, 1655, 1657, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 866, 868, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 725, 726, 2107, 2108, 41, 759, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 1234, 1236, 1920, 1922, 282, 556, 280, 11, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 440, 1759, 1761, 1123, 1125, 1811, 291, 560, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 757, 887, 1105, 1942, 1923]
    p.diplomacy = [DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]
    # --- P6
    p = pm.players[6]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.PURPLE
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Purple'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 621, 109, 72, 50, 68, 104, 45, 598, 199, 276]
    p.disabled_units = [83, 1810, 83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 763, 765, 1007, 1009, 692, 694, 876, 878, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 773, 1655, 1657, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 866, 868, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 725, 726, 2107, 2108, 41, 759, 41, 759, 555, 761, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 331, 1234, 1236, 1920, 1922, 282, 556, 280, 11, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 1759, 1761, 1123, 1125, 1811, 291, 560, 1658, 1660, 1658, 1660, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 755, 886, 757, 887, 757, 887, 1105, 1942, 1923, 440]
    p.diplomacy = [DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]
    # --- P7
    p = pm.players[7]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.GRAY
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Gray'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 621, 109, 72, 50, 68, 104, 45, 598, 199, 276]
    p.disabled_units = [83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 765, 763, 1007, 1009, 692, 694, 876, 878, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 773, 1655, 1657, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 866, 868, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 725, 726, 2107, 2108, 41, 759, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 331, 1234, 1236, 1920, 1922, 282, 556, 280, 11, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 440, 1759, 1761, 1123, 1125, 1811, 291, 560, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 757, 887, 1105, 1942, 1923]
    p.diplomacy = [DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]
    # --- P8
    p = pm.players[8]
    p.starting_age = StartingAge.FEUDAL_AGE
    p.lock_civ = False
    p.lock_personality = False
    # Reserve one hard-pop slot for the permanent War Penguin controller.
    p.population_cap = 251
    p.food = 1000
    p.wood = 1000
    p.gold = 1000
    p.stone = 1000
    p.color = ColorId.ORANGE
    p.human = True
    p.civilization = Civilization.RANDOM
    p.architecture_set = Civilization.RANDOM
    p.allied_victory = True
    p.base_priority = 0
    p.tribe_name = 'Orange'
    p.string_table_name_id = -2
    p.initial_player_view_x = 117
    p.initial_player_view_y = 46
    p.disabled_techs = [51]
    p.disabled_buildings = [562, 584, 70, 82, 109, 621, 72, 50, 68, 104, 45, 598, 199, 276]
    p.disabled_units = [83, 1810, 83, 1810, 1126, 1128, 530, 1800, 1802, 8, 1968, 1970, 1129, 1131, 765, 763, 1007, 1009, 692, 694, 876, 878, 554, 25, 1949, 1951, 1263, 36, 1001, 1003, 827, 829, 128, 1904, 1907, 2150, 1980, 1962, 2151, 1704, 1706, 40, 553, 1790, 1792, 73, 559, 771, 773, 1655, 1657, 1120, 1122, 239, 558, 279, 542, 1735, 1737, 866, 868, 1747, 1749, 1911, 1959, 1961, 1013, 1015, 725, 726, 2107, 2108, 41, 759, 41, 759, 555, 761, 555, 761, 869, 871, 232, 534, 2101, 2102, 46, 557, 879, 881, 1228, 1230, 1231, 1233, 1225, 1254, 1225, 1254, 1225, 1254, 1225, 1254, 1227, 1255, 1227, 1255, 1227, 1255, 1227, 1255, 1741, 1743, 281, 531, 1234, 1236, 1920, 1922, 282, 556, 280, 11, 561, 1701, 1703, 1803, 1805, 1709, 550, 588, 1908, 1910, 1759, 1761, 1123, 1125, 1811, 291, 560, 1658, 1660, 1658, 1660, 1658, 1660, 1658, 1660, 1659, 1661, 1659, 1661, 1659, 1661, 1659, 1661, 1016, 1018, 2104, 2105, 755, 886, 755, 886, 757, 887, 757, 887, 1105, 1942, 1923, 440]
    p.diplomacy = [DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ALLY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY, DiplomacyState.ENEMY]

    # --- lobby options
    om.victory_condition = VictoryCondition.CONQUEST
    om.victory_score = 14000
    om.victory_years = 900
    om.victory_custom_conditions_required = False
    om.secondary_game_modes = SecondaryGameMode.NONE
    om.lock_teams = True
    om.lock_coop_alliances = True
    om.allow_players_choose_teams = False
    om.random_start_points = False
    om.collide_and_correct = False
    om.villager_force_drop = True
    om.legacy_execution_order = True

    # --- Messages tab
    msg.instructions = 'CBA HERO REFORGED EVOLUTION ALPHA\r\rOBJECTIVE\rDestroy all four castles of every enemy player.\rDefend your castles and support your team.\r\rLOBBY TEAMS\rP1-P4 versus P5-P8. Close any unused slots.\rKeep at least one occupied player slot on each side.\rClosed slots are cleaned automatically when the match starts.\r\rCOMBAT SCOREBOARD\rPlayer nicknames remain unchanged in the normal score panel.\rA compact Kills / Deaths table appears in the Objectives display.\rResource stockpiles are kept equal, so score differences come from\rcombat and survival.\r\rHERO MILESTONES\r200 Robin Hood | 400 Theodoric | 600 Charles Martel | 800 Subotai\r1000 Genghis Khan | 2000 Super Genghis | 3500 and 5000 spawn boosts'
    msg.hints = '[KILLS NEEDED FOR HEROES]\r\r200 Kills: Robin Hood\r400 Kills: Teodoric the Godo\r600 Kills: Charles Martel\r800 Kills: Subotai\r1000 Kills: Genghis Khan\r2000 Kills: Super Genghis Khan\r3500 Kills: Respawn 60% + Faster\r5000 Kills: Respawn 190% + Faster\r__________________________________________\r\rCivilization Table:\r--------------------------\r\rCivilization (Ing) | Civilization (Esp) | Kills CA | Kills IA | Razings | Units | Time\r--------------------------------------------------------------------------------------------------------\rACHAEMENIDS | AQUEMÉNIDAS | 300 | 600 | 1 | 70 | 10\rARMENIANS | ARMENIOS | 300 | 600 | 2 | 80 | 8\rATHENIANS | ATENIENSES | 250 | 500 | 1 | 80 | 10\rAZTECS | AZTECAS | 250 | 500 | 2 | 92 | 8\rBENGALIS | BENGALIES | 300 | 600 | 2 | 40 | 8\rBERBERS | BEREBERES | 250 | 500 | 1 | 61 | 10\rBOHEMIANS | BOHEMIOS | 300 | 600 | 2 | 35 | 15\rBRITONS | BRITANOS | 300 | 600 | 1 | 72 | 9\rBULGARIANS | BULGAROS | 250 | 500 | 2 | 41 | 12\rBURGUNDIANS | BORGOÑESES | 300 | 600 | 2 | 60 | 8\rBURMESE | BIRMANOS | 300 | 600 | 3 | 61 | 10\rBYZANTINES | BIZANTINOS | 300 | 600 | 2 | 56 | 10\rCELTS | CELTAS | 200 | 450 | 2 | 80 | 9\rCHINESE | CHINOS | 200 | 500 | 2 | 76 | 8\rCUMANS | CUMANOS | 300 | 500 | 2 | 61 | 12\rDRAVIDIANS | DRAVÍDICOS | 300 | 600 | 2 | 60 | 8\rETHIOPIANS | ETÍOPES | 200 | 500 | 2 | 80 | 8\rFRANKS | FRANCOS | 300 | 450 | 3 | 76 | 8\rGEORGIANS | GEORGIANOS | 250 | 600 | 1 | 80 | 8\rGOTHS | GODOS | 250 | 350 | 2 | 76 | 8\rGURJARAS | GURJARAS | 300 | 750 | 3 | 41 | 11\rHINDUSTIANIS | INDOSTANOS | 300 | 600 | 3 | 60 | 12\rHUNS | HUNOS | 200 | 400 | 4 | 80 | 13\rINCA | INCAS | 250 | 350 | 2 | 77 | 8\rITALIANS | ITALIANOS | 300 | 500 | 1 | 72 | 9\rJAPANESE | JAPONESES | 300 | 600 | 3 | 80 | 9\rJURCHENS | YURCHEN | 300 | 600 | 2 | 80 | 10\rKHITANS | KITÁN | 250 | 500 | 2 | 80 | 10\rKHMER | JEMERES | 300 | 700 | 4 | 31 | 14\rKOREANS | COREANOS | 300 | 600 | 3 | 60 | 12\rLITHUANIANS | LITUANOS | 300 | 600 | 2 | 60 | 10\rMAGYARS | MAGIARES | 250 | 600 | 1 | 80 | 13\rMALAY | MALAYOS | 200 | 400 | 1 | 80 | 6\rMALIANS | MALÍ | 300 | 600 | 3 | 81 | 10\rMAYA | MAYA | 250 | 450 | 1 | 70 | 8\rMONGOLS | MONGOL | 300 | 650 | 2 | 56 | 9\rPERSIANS | PERSA | 300 | 750 | 4 | 56 | 13\rPOLES | POLACOS | 300 | 600 | 2 | 60 | 8\rPORTUGUESE | PORTUGUESES | 300 | 600 | 3 | 34 | 12\rROMANS | ROMANOS | 300 | 600 | 2 | 60 | 8\rSARACENS | SARRACENOS | 300 | 650 | 2 | 68 | 12\rSHU | SHU | 300 | 600 | 2 | 60 | 10\rSICILIANS | SICILIANO | 200 | 350 | 2 | 92 | 8\rSLAVS | ESLAVO | 300 | 600 | 2 | 56 | 10\rSPANISH | ESPAÑOL | 300 | 750 | 3 | 60 | 10\rSPARTANS | ESPARTANO | 250 | 600 | 1 | 80 | 8\rTATARS | TARTAROS | 250 | 500 | 2 | 61 | 12\rTEUTONS | TEUTON | 300 | 450 | 3 | 76 | 8\rTURKS | TURCO | 300 | 700 | 3 | 61 | 9\rVIETNAMESE | VIETNAMITA | 300 | 500 | 1 | 81 | 10\rVIKINGS | VIKINGO | 200 | 500 | 2 | 86 | 9\rWEI | WEI | 300 | 600 | 2 | 60 | 10\rWU | WU | 300 | 600 | 2 | 60 | 10\r'
    msg.history = 'CBA Hero Reforged Evolution Alpha.\rFixed P1-P4 versus P5-P8 teams support closed player slots.\rThe Objectives panel shows live Kills and Deaths only for occupied slots.'
    msg.loss = '\rKeep practicing...\r\rBy Reforged'
    msg.scouts = 'Teams are fixed as P1-P4 versus P5-P8; close unused slots.\rThe compact Objectives display shows live Kills and Deaths for occupied slots.\rResources are automatically equalized only after a slot is confirmed occupied.'
    msg.victory = '\rCongratulations! Now you are part of the CBA Hero Elite\r\rby Reforged'
