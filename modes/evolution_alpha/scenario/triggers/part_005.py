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


def emit(tm) -> None:
    """Triggers 1250..1499. Mostly: 1x 'kamayukp1', 1x 'kamayukp2', 1x 'kamayukp3'."""
    # --- #1250  kamayukp1   [display 1451]
    t = tm.add_trigger('kamayukp1', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=77, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1251  kamayukp2   [display 1452]
    t = tm.add_trigger('kamayukp2', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=77,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1252  kamayukp3   [display 1453]
    t = tm.add_trigger('kamayukp3', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=77, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1253  kamayukp4   [display 1454]
    t = tm.add_trigger('kamayukp4', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=77,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1254  kamayukp5   [display 1455]
    t = tm.add_trigger('kamayukp5', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=77,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1255  kamayukp6   [display 1456]
    t = tm.add_trigger('kamayukp6', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=77,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1256  kamayukp7   [display 1457]
    t = tm.add_trigger('kamayukp7', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=77,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1257  kamayukp8   [display 1458]
    t = tm.add_trigger('kamayukp8', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=77,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KAMAYUK.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1258  incap1   [display 1443]
    t = tm.add_trigger('incap1', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1250)
    t.new_effect.activate_trigger(trigger_id=302)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=457)
    t.new_effect.activate_trigger(trigger_id=879)

    # --- #1259  incap2   [display 1444]
    t = tm.add_trigger('incap2', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1251)
    t.new_effect.activate_trigger(trigger_id=363)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=518)
    t.new_effect.activate_trigger(trigger_id=880)

    # --- #1260  incap3   [display 1445]
    t = tm.add_trigger('incap3', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1252)
    t.new_effect.activate_trigger(trigger_id=364)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=519)
    t.new_effect.activate_trigger(trigger_id=881)

    # --- #1261  incap4   [display 1446]
    t = tm.add_trigger('incap4', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1253)
    t.new_effect.activate_trigger(trigger_id=365)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=520)
    t.new_effect.activate_trigger(trigger_id=882)

    # --- #1262  incap5   [display 1447]
    t = tm.add_trigger('incap5', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1254)
    t.new_effect.activate_trigger(trigger_id=366)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=521)
    t.new_effect.activate_trigger(trigger_id=883)

    # --- #1263  incap6   [display 1448]
    t = tm.add_trigger('incap6', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1255)
    t.new_effect.activate_trigger(trigger_id=367)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=522)
    t.new_effect.activate_trigger(trigger_id=884)

    # --- #1264  incap7   [display 1449]
    t = tm.add_trigger('incap7', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1256)
    t.new_effect.activate_trigger(trigger_id=368)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=523)
    t.new_effect.activate_trigger(trigger_id=885)

    # --- #1265  incap8   [display 1450]
    t = tm.add_trigger('incap8', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.INCA.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1257)
    t.new_effect.activate_trigger(trigger_id=369)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=524)
    t.new_effect.activate_trigger(trigger_id=886)

    # --- #1266  huszarp1   [display 1467]
    t = tm.add_trigger('huszarp1', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1267  huszarp2   [display 1468]
    t = tm.add_trigger('huszarp2', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=80,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1268  huszarp3   [display 1469]
    t = tm.add_trigger('huszarp3', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1269  huszarp4   [display 1470]
    t = tm.add_trigger('huszarp4', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=80,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1270  huszarp5   [display 1471]
    t = tm.add_trigger('huszarp5', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=80,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1271  huszarp6   [display 1472]
    t = tm.add_trigger('huszarp6', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=80,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1272  huszarp7   [display 1473]
    t = tm.add_trigger('huszarp7', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=80,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1273  huszarp8   [display 1474]
    t = tm.add_trigger('huszarp8', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=80,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=13, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MAGYAR_HUSZAR.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1274  magyarp1   [display 1459]
    t = tm.add_trigger('magyarp1', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.MAGYARS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1266)
    t.new_effect.activate_trigger(trigger_id=302)
    t.new_effect.activate_trigger(trigger_id=737)
    t.new_effect.activate_trigger(trigger_id=460)

    # --- #1275  magyarp2   [display 1460]
    t = tm.add_trigger('magyarp2', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.MAGYARS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1267)
    t.new_effect.activate_trigger(trigger_id=363)
    t.new_effect.activate_trigger(trigger_id=738)
    t.new_effect.activate_trigger(trigger_id=539)

    # --- #1276  magyarp3   [display 1461]
    t = tm.add_trigger('magyarp3', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.MAGYARS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1268)
    t.new_effect.activate_trigger(trigger_id=364)
    t.new_effect.activate_trigger(trigger_id=739)
    t.new_effect.activate_trigger(trigger_id=491)

    # --- #1277  magyarp4   [display 1462]
    t = tm.add_trigger('magyarp4', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.MAGYARS.ID)
    t.new_effect.activate_trigger(trigger_id=1269)
    t.new_effect.activate_trigger(trigger_id=365)
    t.new_effect.activate_trigger(trigger_id=740)
    t.new_effect.activate_trigger(trigger_id=492)

    # --- #1278  magyarp5   [display 1463]
    t = tm.add_trigger('magyarp5', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.MAGYARS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1270)
    t.new_effect.activate_trigger(trigger_id=366)
    t.new_effect.activate_trigger(trigger_id=741)
    t.new_effect.activate_trigger(trigger_id=493)

    # --- #1279  magyarp6   [display 1464]
    t = tm.add_trigger('magyarp6', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.MAGYARS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1271)
    t.new_effect.activate_trigger(trigger_id=367)
    t.new_effect.activate_trigger(trigger_id=742)
    t.new_effect.activate_trigger(trigger_id=494)

    # --- #1280  magyarp7   [display 1465]
    t = tm.add_trigger('magyarp7', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.MAGYARS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1272)
    t.new_effect.activate_trigger(trigger_id=368)
    t.new_effect.activate_trigger(trigger_id=743)
    t.new_effect.activate_trigger(trigger_id=495)

    # --- #1281  magyarp8   [display 1466]
    t = tm.add_trigger('magyarp8', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.MAGYARS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1273)
    t.new_effect.activate_trigger(trigger_id=369)
    t.new_effect.activate_trigger(trigger_id=744)
    t.new_effect.activate_trigger(trigger_id=496)

    # --- #1282  elearcherp1   [display 1483]
    t = tm.add_trigger('elearcherp1', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        location_x=48,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        location_x=52,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        location_x=55,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        location_x=59,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1283  elearcherp2   [display 1484]
    t = tm.add_trigger('elearcherp2', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1284  elearcherp3   [display 1485]
    t = tm.add_trigger('elearcherp3', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )

    # --- #1285  elearcherp4   [display 1486]
    t = tm.add_trigger('elearcherp4', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )

    # --- #1286  elearcherp5   [display 1487]
    t = tm.add_trigger('elearcherp5', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )

    # --- #1287  elearcherp6   [display 1488]
    t = tm.add_trigger('elearcherp6', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )

    # --- #1288  elearcherp7   [display 1489]
    t = tm.add_trigger('elearcherp7', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )

    # --- #1289  elearcherp8   [display 1490]
    t = tm.add_trigger('elearcherp8', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GHULAM.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )

    # --- #1290  hindusp1   [display 1475]
    t = tm.add_trigger('hindusp1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1282)
    t.new_effect.activate_trigger(trigger_id=305)
    t.new_effect.activate_trigger(trigger_id=721)
    t.new_effect.activate_trigger(trigger_id=460)

    # --- #1291  hindusp2   [display 1476]
    t = tm.add_trigger('hindusp2', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1283)
    t.new_effect.activate_trigger(trigger_id=384)
    t.new_effect.activate_trigger(trigger_id=722)
    t.new_effect.activate_trigger(trigger_id=539)

    # --- #1292  hindusp3   [display 1477]
    t = tm.add_trigger('hindusp3', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1284)
    t.new_effect.activate_trigger(trigger_id=385)
    t.new_effect.activate_trigger(trigger_id=723)
    t.new_effect.activate_trigger(trigger_id=540)

    # --- #1293  hindusp4   [display 1478]
    t = tm.add_trigger('hindusp4', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1285)
    t.new_effect.activate_trigger(trigger_id=386)
    t.new_effect.activate_trigger(trigger_id=724)
    t.new_effect.activate_trigger(trigger_id=541)

    # --- #1294  hindusp5   [display 1479]
    t = tm.add_trigger('hindusp5', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1286)
    t.new_effect.activate_trigger(trigger_id=387)
    t.new_effect.activate_trigger(trigger_id=725)
    t.new_effect.activate_trigger(trigger_id=542)

    # --- #1295  hindusp6   [display 1480]
    t = tm.add_trigger('hindusp6', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1287)
    t.new_effect.activate_trigger(trigger_id=388)
    t.new_effect.activate_trigger(trigger_id=726)
    t.new_effect.activate_trigger(trigger_id=543)

    # --- #1296  hindusp7   [display 1481]
    t = tm.add_trigger('hindusp7', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1288)
    t.new_effect.activate_trigger(trigger_id=389)
    t.new_effect.activate_trigger(trigger_id=727)
    t.new_effect.activate_trigger(trigger_id=544)

    # --- #1297  hindusp8   [display 1482]
    t = tm.add_trigger('hindusp8', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.HINDUSTANIS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1289)
    t.new_effect.activate_trigger(trigger_id=390)
    t.new_effect.activate_trigger(trigger_id=728)
    t.new_effect.activate_trigger(trigger_id=545)

    # --- #1298  herospawnrelic   [display 1491]
    t = tm.add_trigger('herospawnrelic', description_stid=0)
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94898])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94896])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94911])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94901])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94909])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94903])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94907])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Close', selected_object_ids=[94905])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94899])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94897])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94910])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94900])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94908])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94902])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94906])
    t.new_effect.change_object_name(source_player=PlayerId.GAIA, message='Hero Spawn Open', selected_object_ids=[94904])

    # --- #1299  herospawnclose   [display 1492]
    t = tm.add_trigger('herospawnclose', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88891, area_x1=59, area_y1=6, area_x2=60, area_y2=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=39,
        location_y=16,
        disable_sound=-1,
    )

    # --- #1300  herospawnopen   [display 1500]
    t = tm.add_trigger('herospawnopen', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88891, area_x1=64, area_y1=6, area_x2=65, area_y2=6, inverted=-1)
    t.new_effect.remove_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        area_x1=39,
        area_y1=16,
        area_x2=39,
        area_y2=16,
        object_state=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=63,
        location_y=4,
        area_x1=64,
        area_y1=6,
        area_x2=65,
        area_y2=6,
        action_type=-1,
        selected_object_ids=[88891],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1301  herospawnclose (p2)   [display 1493]
    t = tm.add_trigger('herospawnclose (p2)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88892, area_x1=76, area_y1=6, area_x2=77, area_y2=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=101,
        location_y=16,
        disable_sound=-1,
    )

    # --- #1302  herospawnclose (p3)   [display 1494]
    t = tm.add_trigger('herospawnclose (p3)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88893, area_x1=6, area_y1=65, area_x2=6, area_y2=66, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=16,
        location_y=38,
        disable_sound=-1,
    )

    # --- #1303  herospawnclose (p4)   [display 1495]
    t = tm.add_trigger('herospawnclose (p4)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88894, area_x1=137, area_y1=59, area_x2=137, area_y2=60, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=126,
        location_y=40,
        disable_sound=-1,
    )

    # --- #1304  herospawnclose (p5)   [display 1496]
    t = tm.add_trigger('herospawnclose (p5)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88895, area_x1=6, area_y1=80, area_x2=6, area_y2=81, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=14,
        location_y=100,
        disable_sound=-1,
    )

    # --- #1305  herospawnclose (p6)   [display 1497]
    t = tm.add_trigger('herospawnclose (p6)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88896, area_x1=137, area_y1=74, area_x2=137, area_y2=75, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=126,
        location_y=100,
        disable_sound=-1,
    )

    # --- #1306  herospawnclose (p7)   [display 1498]
    t = tm.add_trigger('herospawnclose (p7)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88897, area_x1=62, area_y1=137, area_x2=63, area_y2=137, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=40,
        location_y=126,
        disable_sound=-1,
    )

    # --- #1307  herospawnclose (p8)   [display 1499]
    t = tm.add_trigger('herospawnclose (p8)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88898, area_x1=77, area_y1=137, area_x2=78, area_y2=137, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.OLD_STONE_HEAD.ID,
        source_player=PlayerId.GAIA,
        location_x=102,
        location_y=124,
        disable_sound=-1,
    )

    # --- #1308  herospawnopen (p2)   [display 1501]
    t = tm.add_trigger('herospawnopen (p2)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88892, area_x1=81, area_y1=6, area_x2=82, area_y2=6, inverted=-1)
    t.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        area_x1=101,
        area_y1=16,
        area_x2=101,
        area_y2=16,
        object_state=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=80,
        location_y=4,
        area_x1=81,
        area_y1=6,
        area_x2=82,
        area_y2=6,
        action_type=-1,
        selected_object_ids=[88892],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1309  herospawnopen (p3)   [display 1502]
    t = tm.add_trigger('herospawnopen (p3)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88893, area_x1=6, area_y1=60, area_x2=6, area_y2=61, inverted=-1)
    t.new_effect.remove_object(source_player=PlayerId.GAIA, area_x1=16, area_y1=38, area_x2=16, area_y2=38, object_state=-1)
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=62,
        area_x1=6,
        area_y1=60,
        area_x2=6,
        area_y2=61,
        action_type=-1,
        selected_object_ids=[88893],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1310  herospawnopen (p4)   [display 1503]
    t = tm.add_trigger('herospawnopen (p4)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88894, area_x1=137, area_y1=64, area_x2=137, area_y2=65, inverted=-1)
    t.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        area_x1=126,
        area_y1=40,
        area_x2=126,
        area_y2=40,
        object_state=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=139,
        location_y=63,
        area_x1=137,
        area_y1=64,
        area_x2=137,
        area_y2=65,
        action_type=-1,
        selected_object_ids=[88894],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1311  herospawnopen (p5)   [display 1504]
    t = tm.add_trigger('herospawnopen (p5)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88895, area_x1=6, area_y1=75, area_x2=6, area_y2=76, inverted=-1)
    t.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        area_x1=14,
        area_y1=100,
        area_x2=14,
        area_y2=100,
        object_state=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=77,
        area_x1=6,
        area_y1=75,
        area_x2=6,
        area_y2=76,
        action_type=-1,
        selected_object_ids=[88895],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1312  herospawnopen (p6)   [display 1505]
    t = tm.add_trigger('herospawnopen (p6)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88896, area_x1=137, area_y1=79, area_x2=137, area_y2=80, inverted=-1)
    t.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        area_x1=126,
        area_y1=100,
        area_x2=126,
        area_y2=100,
        object_state=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=139,
        location_y=78,
        area_x1=137,
        area_y1=79,
        area_x2=137,
        area_y2=80,
        action_type=-1,
        selected_object_ids=[88896],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1313  herospawnopen (p7)   [display 1506]
    t = tm.add_trigger('herospawnopen (p7)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88897, area_x1=57, area_y1=137, area_x2=58, area_y2=137, inverted=-1)
    t.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        area_x1=40,
        area_y1=126,
        area_x2=40,
        area_y2=126,
        object_state=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=59,
        location_y=139,
        area_x1=57,
        area_y1=137,
        area_x2=58,
        area_y2=137,
        action_type=-1,
        selected_object_ids=[88897],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1314  herospawnopen (p8)   [display 1507]
    t = tm.add_trigger('herospawnopen (p8)', description_stid=0, looping=1)
    t.new_condition.bring_object_to_area(unit_object=88898, area_x1=72, area_y1=137, area_x2=73, area_y2=137, inverted=-1)
    t.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        area_x1=102,
        area_y1=124,
        area_x2=102,
        area_y2=124,
        object_state=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.GAIA,
        location_x=74,
        location_y=139,
        area_x1=72,
        area_y1=137,
        area_x2=73,
        area_y2=137,
        action_type=-1,
        selected_object_ids=[88898],
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1315  sem cr   [display 1508]
    t = tm.add_trigger('sem cr', description_stid=0)
    t.new_condition.timer(timer=50, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=UnitInfo.SCORPION.ID, area_x1=0, area_y1=0, area_x2=143, area_y2=143)
    t.new_effect.remove_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.remove_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.remove_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.remove_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.remove_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.remove_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.remove_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )

    # --- #1316  P1 King   [display 1509]
    t = tm.add_trigger('P1 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95792, area_x1=38, area_y1=2, area_x2=38, area_y2=2, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.SCORPION.ID, location_x=46, location_y=26, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.SCORPION.ID, location_x=46, location_y=32, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.SCORPION.ID, location_x=46, location_y=38, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.SCORPION.ID, location_x=62, location_y=38, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.SCORPION.ID, location_x=62, location_y=32, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.SCORPION.ID, location_x=62, location_y=26, disable_sound=-1)
    t.new_effect.remove_object(object_state=-1, selected_object_ids=[95792])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p1 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        area_x1=45,
        area_y1=25,
        area_x2=64,
        area_y2=39,
        operation=-1,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        area_x1=45,
        area_y1=25,
        area_x2=64,
        area_y2=39,
        operation=Operation.MULTIPLY,
    )

    # --- #1317  P2 King   [display 1510]
    t = tm.add_trigger('P2 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95959, area_x1=102, area_y1=2, area_x2=104, area_y2=3, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        location_x=79,
        location_y=27,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        location_x=79,
        location_y=32,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        location_x=79,
        location_y=38,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        location_x=95,
        location_y=38,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        location_x=95,
        location_y=32,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        location_x=95,
        location_y=26,
        disable_sound=-1,
    )
    t.new_effect.remove_object(source_player=PlayerId.TWO, object_state=-1, selected_object_ids=[95959])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p2 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        area_x1=78,
        area_y1=26,
        area_x2=96,
        area_y2=39,
        operation=-1,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.TWO,
        area_x1=78,
        area_y1=26,
        area_x2=96,
        area_y2=39,
        operation=Operation.MULTIPLY,
    )

    # --- #1318  P3 King   [display 1511]
    t = tm.add_trigger('P3 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95961, area_x1=2, area_y1=38, area_x2=3, area_y2=40, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        location_x=25,
        location_y=61,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        location_x=32,
        location_y=61,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        location_x=38,
        location_y=61,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        location_x=38,
        location_y=45,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        location_x=34,
        location_y=45,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        location_x=27,
        location_y=45,
        disable_sound=-1,
    )
    t.new_effect.remove_object(source_player=PlayerId.THREE, object_state=-1, selected_object_ids=[95961])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p3 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        area_x1=24,
        area_y1=44,
        area_x2=40,
        area_y2=64,
        operation=-1,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.THREE,
        area_x1=24,
        area_y1=44,
        area_x2=40,
        area_y2=64,
        operation=Operation.MULTIPLY,
    )

    # --- #1319  P4 King   [display 1512]
    t = tm.add_trigger('P4 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95962, area_x1=140, area_y1=38, area_x2=141, area_y2=40, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        location_x=115,
        location_y=45,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        location_x=111,
        location_y=45,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        location_x=104,
        location_y=45,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        location_x=102,
        location_y=61,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        location_x=109,
        location_y=61,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        location_x=114,
        location_y=61,
        disable_sound=-1,
    )
    t.new_effect.remove_object(source_player=PlayerId.FOUR, object_state=-1, selected_object_ids=[95962])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p4 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        area_x1=101,
        area_y1=44,
        area_x2=116,
        area_y2=62,
        operation=-1,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FOUR,
        area_x1=101,
        area_y1=44,
        area_x2=116,
        area_y2=62,
        operation=Operation.MULTIPLY,
    )

    # --- #1320  P5 King   [display 1513]
    t = tm.add_trigger('P5 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95963, area_x1=2, area_y1=101, area_x2=3, area_y2=103, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        location_x=26,
        location_y=94,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        location_x=32,
        location_y=94,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        location_x=37,
        location_y=94,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        location_x=38,
        location_y=78,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        location_x=33,
        location_y=78,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        location_x=27,
        location_y=78,
        disable_sound=-1,
    )
    t.new_effect.remove_object(source_player=PlayerId.FIVE, object_state=-1, selected_object_ids=[95963])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p5 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        area_x1=24,
        area_y1=77,
        area_x2=39,
        area_y2=95,
        operation=-1,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.FIVE,
        area_x1=24,
        area_y1=77,
        area_x2=39,
        area_y2=96,
        operation=Operation.MULTIPLY,
    )

    # --- #1321  P6 King   [display 1514]
    t = tm.add_trigger('P6 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95964, area_x1=140, area_y1=99, area_x2=141, area_y2=101, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        location_x=115,
        location_y=78,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        location_x=110,
        location_y=78,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        location_x=104,
        location_y=78,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        location_x=102,
        location_y=94,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        location_x=109,
        location_y=94,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        location_x=114,
        location_y=94,
        disable_sound=-1,
    )
    t.new_effect.remove_object(source_player=PlayerId.SIX, object_state=-1, selected_object_ids=[95964])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p6 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        area_x1=101,
        area_y1=77,
        area_x2=116,
        area_y2=95,
        operation=-1,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SIX,
        area_x1=101,
        area_y1=77,
        area_x2=116,
        area_y2=95,
        operation=Operation.MULTIPLY,
    )

    # --- #1322  P7 King   [display 1515]
    t = tm.add_trigger('P7 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95965, area_x1=35, area_y1=140, area_x2=37, area_y2=141, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        location_x=46,
        location_y=102,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        location_x=46,
        location_y=108,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        location_x=46,
        location_y=113,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        location_x=62,
        location_y=101,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        location_x=62,
        location_y=107,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        location_x=62,
        location_y=113,
        disable_sound=-1,
    )
    t.new_effect.remove_object(source_player=PlayerId.SEVEN, object_state=-1, selected_object_ids=[95965])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p7 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        area_x1=45,
        area_y1=100,
        area_x2=63,
        area_y2=116,
        operation=-1,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.SEVEN,
        area_x1=45,
        area_y1=99,
        area_x2=63,
        area_y2=116,
        operation=Operation.MULTIPLY,
    )

    # --- #1323  P8 King   [display 1516]
    t = tm.add_trigger('P8 King', description_stid=0)
    t.new_condition.bring_object_to_area(unit_object=95966, area_x1=97, area_y1=140, area_x2=99, area_y2=141, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1315)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        location_x=79,
        location_y=102,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        location_x=79,
        location_y=108,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        location_x=79,
        location_y=113,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        location_x=95,
        location_y=102,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        location_x=95,
        location_y=108,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        location_x=94,
        location_y=114,
        disable_sound=-1,
    )
    t.new_effect.remove_object(source_player=PlayerId.EIGHT, object_state=-1, selected_object_ids=[95966])
    t.new_effect.display_instructions(source_player=-1, play_sound=-1, message='p8 kinged', use_tag_color_for_icon=1)
    t.new_effect.change_object_hp(
        quantity=10000,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        area_x1=78,
        area_y1=101,
        area_x2=96,
        area_y2=115,
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=232,
        object_list_unit_id=UnitInfo.SCORPION.ID,
        source_player=PlayerId.EIGHT,
        area_x1=78,
        area_y1=100,
        area_x2=96,
        area_y2=116,
        operation=Operation.MULTIPLY,
    )

    # --- #1324  ge kan   [display 1517]
    t = tm.add_trigger('ge kan', description_stid=0, short_description_stid=0, looping=1)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[109739])
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[109740])
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[109741])
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[109742])
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[98497])
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[98498])
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[98499])
    t.new_effect.change_object_hp(quantity=5, source_player=PlayerId.GAIA, selected_object_ids=[98500])
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[109739],
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[109740],
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[109741],
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[109742],
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[98497],
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[98498],
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[98499],
    )
    t.new_effect.change_object_attack(
        armour_attack_quantity=3,
        source_player=PlayerId.GAIA,
        operation=Operation.ADD,
        selected_object_ids=[98500],
    )

    # --- #1325  ber (p1)   [display 144]
    t = tm.add_trigger('ber (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1326)
    t.new_effect.activate_trigger(trigger_id=302)
    t.new_effect.activate_trigger(trigger_id=737)
    t.new_effect.activate_trigger(trigger_id=468)

    # --- #1326  camelarch (p1)   [display 152]
    t = tm.add_trigger('camelarch (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, object_type=ObjectType.MILITARY)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1327  camelarch (p2)   [display 153]
    t = tm.add_trigger('camelarch (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1328  camelarch (p3)   [display 154]
    t = tm.add_trigger('camelarch (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1329  camelarch (p4)   [display 155]
    t = tm.add_trigger('camelarch (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1330  camelarch (p5)   [display 156]
    t = tm.add_trigger('camelarch (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1331  camelarch (p6)   [display 157]
    t = tm.add_trigger('camelarch (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1332  camelarch (p7)   [display 158]
    t = tm.add_trigger('camelarch (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1333  camelarch (p8)   [display 159]
    t = tm.add_trigger('camelarch (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CAMEL_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1334  ber (p2)   [display 145]
    t = tm.add_trigger('ber (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1327)
    t.new_effect.activate_trigger(trigger_id=363)
    t.new_effect.activate_trigger(trigger_id=738)
    t.new_effect.activate_trigger(trigger_id=483)

    # --- #1335  ber (p3)   [display 146]
    t = tm.add_trigger('ber (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1328)
    t.new_effect.activate_trigger(trigger_id=364)
    t.new_effect.activate_trigger(trigger_id=739)
    t.new_effect.activate_trigger(trigger_id=484)

    # --- #1336  ber (p4)   [display 147]
    t = tm.add_trigger('ber (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1329)
    t.new_effect.activate_trigger(trigger_id=365)
    t.new_effect.activate_trigger(trigger_id=740)
    t.new_effect.activate_trigger(trigger_id=485)

    # --- #1337  ber (p5)   [display 148]
    t = tm.add_trigger('ber (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1330)
    t.new_effect.activate_trigger(trigger_id=366)
    t.new_effect.activate_trigger(trigger_id=741)
    t.new_effect.activate_trigger(trigger_id=486)

    # --- #1338  ber (p6)   [display 149]
    t = tm.add_trigger('ber (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1331)
    t.new_effect.activate_trigger(trigger_id=367)
    t.new_effect.activate_trigger(trigger_id=742)
    t.new_effect.activate_trigger(trigger_id=487)

    # --- #1339  ber (p7)   [display 150]
    t = tm.add_trigger('ber (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1332)
    t.new_effect.activate_trigger(trigger_id=368)
    t.new_effect.activate_trigger(trigger_id=743)
    t.new_effect.activate_trigger(trigger_id=488)

    # --- #1340  ber (p8)   [display 151]
    t = tm.add_trigger('ber (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.BERBERS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1333)
    t.new_effect.activate_trigger(trigger_id=369)
    t.new_effect.activate_trigger(trigger_id=744)
    t.new_effect.activate_trigger(trigger_id=489)

    # --- #1341  mali (p1)   [display 160]
    t = tm.add_trigger('mali (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1342)
    t.new_effect.activate_trigger(trigger_id=301)
    t.new_effect.activate_trigger(trigger_id=721)
    t.new_effect.activate_trigger(trigger_id=460)

    # --- #1342  gbeto (p1)   [display 168]
    t = tm.add_trigger('gbeto (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=81, object_type=ObjectType.MILITARY)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_GBETO.ID, location_x=48, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_GBETO.ID, location_x=52, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_GBETO.ID, location_x=55, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_GBETO.ID, location_x=59, location_y=22, disable_sound=-1)

    # --- #1343  mali (p2)   [display 161]
    t = tm.add_trigger('mali (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1350)
    t.new_effect.activate_trigger(trigger_id=328)
    t.new_effect.activate_trigger(trigger_id=722)
    t.new_effect.activate_trigger(trigger_id=490)

    # --- #1344  mali (p3)   [display 162]
    t = tm.add_trigger('mali (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1351)
    t.new_effect.activate_trigger(trigger_id=329)
    t.new_effect.activate_trigger(trigger_id=723)
    t.new_effect.activate_trigger(trigger_id=491)

    # --- #1345  mali (p4)   [display 163]
    t = tm.add_trigger('mali (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1352)
    t.new_effect.activate_trigger(trigger_id=330)
    t.new_effect.activate_trigger(trigger_id=724)
    t.new_effect.activate_trigger(trigger_id=492)

    # --- #1346  mali (p5)   [display 164]
    t = tm.add_trigger('mali (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1353)
    t.new_effect.activate_trigger(trigger_id=331)
    t.new_effect.activate_trigger(trigger_id=725)
    t.new_effect.activate_trigger(trigger_id=493)

    # --- #1347  mali (p6)   [display 165]
    t = tm.add_trigger('mali (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1354)
    t.new_effect.activate_trigger(trigger_id=332)
    t.new_effect.activate_trigger(trigger_id=726)
    t.new_effect.activate_trigger(trigger_id=494)

    # --- #1348  mali (p7)   [display 166]
    t = tm.add_trigger('mali (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1355)
    t.new_effect.activate_trigger(trigger_id=333)
    t.new_effect.activate_trigger(trigger_id=727)
    t.new_effect.activate_trigger(trigger_id=495)

    # --- #1349  mali (p8)   [display 167]
    t = tm.add_trigger('mali (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.MALIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1356)
    t.new_effect.activate_trigger(trigger_id=334)
    t.new_effect.activate_trigger(trigger_id=728)
    t.new_effect.activate_trigger(trigger_id=496)

    # --- #1350  gbeto (p2)   [display 169]
    t = tm.add_trigger('gbeto (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1351  gbeto (p3)   [display 170]
    t = tm.add_trigger('gbeto (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1352  gbeto (p4)   [display 171]
    t = tm.add_trigger('gbeto (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1353  gbeto (p5)   [display 172]
    t = tm.add_trigger('gbeto (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1354  gbeto (p6)   [display 173]
    t = tm.add_trigger('gbeto (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1355  gbeto (p7)   [display 174]
    t = tm.add_trigger('gbeto (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1356  gbeto (p8)   [display 175]
    t = tm.add_trigger('gbeto (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_GBETO.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1357  eth (p1)   [display 176]
    t = tm.add_trigger('eth (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1358)
    t.new_effect.activate_trigger(trigger_id=450)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=468)
    t.new_effect.activate_trigger(trigger_id=672)

    # --- #1358  shotel (p1)   [display 184]
    t = tm.add_trigger('shotel (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1359  shotel (p2)   [display 185]
    t = tm.add_trigger('shotel (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1360  shotel (p3)   [display 186]
    t = tm.add_trigger('shotel (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1361  shotel (p4)   [display 187]
    t = tm.add_trigger('shotel (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1362  shotel (p5)   [display 188]
    t = tm.add_trigger('shotel (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1363  shotel (p6)   [display 189]
    t = tm.add_trigger('shotel (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1364  shotel (p7)   [display 190]
    t = tm.add_trigger('shotel (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1365  shotel (p8)   [display 191]
    t = tm.add_trigger('shotel (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SHOTEL_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1366  eth (p2)   [display 177]
    t = tm.add_trigger('eth (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1359)
    t.new_effect.activate_trigger(trigger_id=321)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=483)
    t.new_effect.activate_trigger(trigger_id=673)

    # --- #1367  eth (p3)   [display 178]
    t = tm.add_trigger('eth (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1360)
    t.new_effect.activate_trigger(trigger_id=322)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=484)
    t.new_effect.activate_trigger(trigger_id=674)

    # --- #1368  eth (p4)   [display 179]
    t = tm.add_trigger('eth (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1361)
    t.new_effect.activate_trigger(trigger_id=323)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=485)
    t.new_effect.activate_trigger(trigger_id=675)

    # --- #1369  eth (p5)   [display 180]
    t = tm.add_trigger('eth (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1362)
    t.new_effect.activate_trigger(trigger_id=324)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=486)
    t.new_effect.activate_trigger(trigger_id=676)

    # --- #1370  eth (p6)   [display 181]
    t = tm.add_trigger('eth (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1363)
    t.new_effect.activate_trigger(trigger_id=325)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=487)
    t.new_effect.activate_trigger(trigger_id=677)

    # --- #1371  eth (p7)   [display 182]
    t = tm.add_trigger('eth (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1364)
    t.new_effect.activate_trigger(trigger_id=326)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=488)
    t.new_effect.activate_trigger(trigger_id=678)

    # --- #1372  eth (p8)   [display 183]
    t = tm.add_trigger('eth (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.ETHIOPIANS.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1365)
    t.new_effect.activate_trigger(trigger_id=327)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=489)
    t.new_effect.activate_trigger(trigger_id=679)

    # --- #1373  port (p1)   [display 192]
    t = tm.add_trigger('port (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1374)
    t.new_effect.activate_trigger(trigger_id=301)
    t.new_effect.activate_trigger(trigger_id=721)
    t.new_effect.activate_trigger(trigger_id=460)

    # --- #1374  orgun (p1)   [display 200]
    t = tm.add_trigger('orgun (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ORGAN_GUN.ID, location_x=48, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ORGAN_GUN.ID, location_x=52, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ORGAN_GUN.ID, location_x=55, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ORGAN_GUN.ID, location_x=59, location_y=22, disable_sound=-1)

    # --- #1375  orgun (p2)   [display 201]
    t = tm.add_trigger('orgun (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1376  orgun (p3)   [display 202]
    t = tm.add_trigger('orgun (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1377  orgun (p4)   [display 203]
    t = tm.add_trigger('orgun (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1378  orgun (p5)   [display 204]
    t = tm.add_trigger('orgun (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1379  orgun (p6)   [display 205]
    t = tm.add_trigger('orgun (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1380  orgun (p7)   [display 206]
    t = tm.add_trigger('orgun (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1381  orgun (p8)   [display 207]
    t = tm.add_trigger('orgun (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=34, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ORGAN_GUN.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1382  port (p2)   [display 193]
    t = tm.add_trigger('port (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1375)
    t.new_effect.activate_trigger(trigger_id=328)
    t.new_effect.activate_trigger(trigger_id=722)
    t.new_effect.activate_trigger(trigger_id=490)

    # --- #1383  port (p3)   [display 194]
    t = tm.add_trigger('port (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1376)
    t.new_effect.activate_trigger(trigger_id=329)
    t.new_effect.activate_trigger(trigger_id=723)
    t.new_effect.activate_trigger(trigger_id=491)

    # --- #1384  port (p4)   [display 195]
    t = tm.add_trigger('port (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1377)
    t.new_effect.activate_trigger(trigger_id=330)
    t.new_effect.activate_trigger(trigger_id=724)
    t.new_effect.activate_trigger(trigger_id=492)

    # --- #1385  port (p5)   [display 196]
    t = tm.add_trigger('port (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1378)
    t.new_effect.activate_trigger(trigger_id=331)
    t.new_effect.activate_trigger(trigger_id=725)
    t.new_effect.activate_trigger(trigger_id=493)

    # --- #1386  port (p6)   [display 197]
    t = tm.add_trigger('port (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1379)
    t.new_effect.activate_trigger(trigger_id=332)
    t.new_effect.activate_trigger(trigger_id=726)
    t.new_effect.activate_trigger(trigger_id=494)

    # --- #1387  port (p7)   [display 198]
    t = tm.add_trigger('port (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1380)
    t.new_effect.activate_trigger(trigger_id=333)
    t.new_effect.activate_trigger(trigger_id=727)
    t.new_effect.activate_trigger(trigger_id=495)

    # --- #1388  port (p8)   [display 199]
    t = tm.add_trigger('port (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.PORTUGUESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1381)
    t.new_effect.activate_trigger(trigger_id=334)
    t.new_effect.activate_trigger(trigger_id=728)
    t.new_effect.activate_trigger(trigger_id=496)

    # --- #1389  burm (p1)   [display 208]
    t = tm.add_trigger('burm (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1390)
    t.new_effect.activate_trigger(trigger_id=301)
    t.new_effect.activate_trigger(trigger_id=721)
    t.new_effect.activate_trigger(trigger_id=460)

    # --- #1390  aram (p1)   [display 216]
    t = tm.add_trigger('aram (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, object_type=ObjectType.MILITARY, include_changeable_weapon_objects=-1)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1391  aram (p2)   [display 217]
    t = tm.add_trigger('aram (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1392  aram (p3)   [display 218]
    t = tm.add_trigger('aram (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1393  aram (p4)   [display 219]
    t = tm.add_trigger('aram (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1394  aram (p5)   [display 220]
    t = tm.add_trigger('aram (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1395  aram (p6)   [display 221]
    t = tm.add_trigger('aram (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1396  aram (p7)   [display 222]
    t = tm.add_trigger('aram (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1397  aram (p8)   [display 223]
    t = tm.add_trigger('aram (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_ARAMBAI.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1398  burm (p2)   [display 209]
    t = tm.add_trigger('burm (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1391)
    t.new_effect.activate_trigger(trigger_id=328)
    t.new_effect.activate_trigger(trigger_id=722)
    t.new_effect.activate_trigger(trigger_id=490)

    # --- #1399  burm (p3)   [display 210]
    t = tm.add_trigger('burm (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1392)
    t.new_effect.activate_trigger(trigger_id=329)
    t.new_effect.activate_trigger(trigger_id=723)
    t.new_effect.activate_trigger(trigger_id=491)

    # --- #1400  burm (p4)   [display 211]
    t = tm.add_trigger('burm (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1393)
    t.new_effect.activate_trigger(trigger_id=330)
    t.new_effect.activate_trigger(trigger_id=724)
    t.new_effect.activate_trigger(trigger_id=492)

    # --- #1401  burm (p5)   [display 212]
    t = tm.add_trigger('burm (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1394)
    t.new_effect.activate_trigger(trigger_id=331)
    t.new_effect.activate_trigger(trigger_id=725)
    t.new_effect.activate_trigger(trigger_id=493)

    # --- #1402  burm (p6)   [display 213]
    t = tm.add_trigger('burm (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1395)
    t.new_effect.activate_trigger(trigger_id=332)
    t.new_effect.activate_trigger(trigger_id=726)
    t.new_effect.activate_trigger(trigger_id=494)

    # --- #1403  burm (p7)   [display 214]
    t = tm.add_trigger('burm (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1396)
    t.new_effect.activate_trigger(trigger_id=333)
    t.new_effect.activate_trigger(trigger_id=727)
    t.new_effect.activate_trigger(trigger_id=495)

    # --- #1404  burm (p8)   [display 215]
    t = tm.add_trigger('burm (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.BURMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1397)
    t.new_effect.activate_trigger(trigger_id=334)
    t.new_effect.activate_trigger(trigger_id=728)
    t.new_effect.activate_trigger(trigger_id=496)

    # --- #1405  khm (p1)   [display 224]
    t = tm.add_trigger('khm (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.KHMER.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1406)
    t.new_effect.activate_trigger(trigger_id=301)
    t.new_effect.activate_trigger(trigger_id=713)
    t.new_effect.activate_trigger(trigger_id=467)

    # --- #1406  be (p1)   [display 232]
    t = tm.add_trigger('be (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=31, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=14)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1407  be (p2)   [display 233]
    t = tm.add_trigger('be (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=31, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=14, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1408  be (p3)   [display 234]
    t = tm.add_trigger('be (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=31, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=14, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1409  be (p4)   [display 235]
    t = tm.add_trigger('be (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=31, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=14, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1410  be (p5)   [display 236]
    t = tm.add_trigger('be (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=31, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=14, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1411  be (p8)   [display 237]
    t = tm.add_trigger('be (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=31, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=14, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_BALLISTA_ELEPHANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1412  khm (p3)   [display 226]
    t = tm.add_trigger('khm (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.KHMER.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1408)
    t.new_effect.activate_trigger(trigger_id=329)
    t.new_effect.activate_trigger(trigger_id=715)
    t.new_effect.activate_trigger(trigger_id=588)

    # --- #1413  khm (p4)   [display 227]
    t = tm.add_trigger('khm (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.KHMER.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1409)
    t.new_effect.activate_trigger(trigger_id=330)
    t.new_effect.activate_trigger(trigger_id=716)
    t.new_effect.activate_trigger(trigger_id=589)

    # --- #1414  khm (p5)   [display 228]
    t = tm.add_trigger('khm (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.KHMER.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1410)
    t.new_effect.activate_trigger(trigger_id=331)
    t.new_effect.activate_trigger(trigger_id=717)
    t.new_effect.activate_trigger(trigger_id=590)

    # --- #1415  khm (p6)   [display 229]
    t = tm.add_trigger('khm (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.KHMER.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1885)
    t.new_effect.activate_trigger(trigger_id=332)
    t.new_effect.activate_trigger(trigger_id=718)
    t.new_effect.activate_trigger(trigger_id=591)

    # --- #1416  khm (p7)   [display 230]
    t = tm.add_trigger('khm (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.KHMER.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1886)
    t.new_effect.activate_trigger(trigger_id=333)
    t.new_effect.activate_trigger(trigger_id=719)
    t.new_effect.activate_trigger(trigger_id=592)

    # --- #1417  khm (p8)   [display 231]
    t = tm.add_trigger('khm (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.KHMER.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1411)
    t.new_effect.activate_trigger(trigger_id=334)
    t.new_effect.activate_trigger(trigger_id=720)
    t.new_effect.activate_trigger(trigger_id=600)

    # --- #1418  khm (p2)   [display 225]
    t = tm.add_trigger('khm (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.KHMER.ID)
    t.new_effect.activate_trigger(trigger_id=1407)
    t.new_effect.activate_trigger(trigger_id=328)
    t.new_effect.activate_trigger(trigger_id=714)
    t.new_effect.activate_trigger(trigger_id=587)

    # --- #1419  mala (p1)   [display 238]
    t = tm.add_trigger('mala (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1420)
    t.new_effect.activate_trigger(trigger_id=450)
    t.new_effect.activate_trigger(trigger_id=737)
    t.new_effect.activate_trigger(trigger_id=458)
    t.new_effect.activate_trigger(trigger_id=672)

    # --- #1420  kar (p1)   [display 246]
    t = tm.add_trigger('kar (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1421  mala (p2)   [display 239]
    t = tm.add_trigger('mala (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1428)
    t.new_effect.activate_trigger(trigger_id=321)
    t.new_effect.activate_trigger(trigger_id=738)
    t.new_effect.activate_trigger(trigger_id=525)
    t.new_effect.activate_trigger(trigger_id=673)

    # --- #1422  mala (p3)   [display 240]
    t = tm.add_trigger('mala (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1429)
    t.new_effect.activate_trigger(trigger_id=322)
    t.new_effect.activate_trigger(trigger_id=739)
    t.new_effect.activate_trigger(trigger_id=526)
    t.new_effect.activate_trigger(trigger_id=674)

    # --- #1423  mala (p4)   [display 241]
    t = tm.add_trigger('mala (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1430)
    t.new_effect.activate_trigger(trigger_id=323)
    t.new_effect.activate_trigger(trigger_id=740)
    t.new_effect.activate_trigger(trigger_id=527)
    t.new_effect.activate_trigger(trigger_id=675)

    # --- #1424  mala (p5)   [display 242]
    t = tm.add_trigger('mala (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1431)
    t.new_effect.activate_trigger(trigger_id=324)
    t.new_effect.activate_trigger(trigger_id=741)
    t.new_effect.activate_trigger(trigger_id=528)
    t.new_effect.activate_trigger(trigger_id=676)

    # --- #1425  mala (p6)   [display 243]
    t = tm.add_trigger('mala (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1432)
    t.new_effect.activate_trigger(trigger_id=325)
    t.new_effect.activate_trigger(trigger_id=742)
    t.new_effect.activate_trigger(trigger_id=529)
    t.new_effect.activate_trigger(trigger_id=677)

    # --- #1426  mala (p7)   [display 244]
    t = tm.add_trigger('mala (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1433)
    t.new_effect.activate_trigger(trigger_id=326)
    t.new_effect.activate_trigger(trigger_id=743)
    t.new_effect.activate_trigger(trigger_id=530)
    t.new_effect.activate_trigger(trigger_id=678)

    # --- #1427  mala (p8)   [display 245]
    t = tm.add_trigger('mala (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.MALAY.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1434)
    t.new_effect.activate_trigger(trigger_id=327)
    t.new_effect.activate_trigger(trigger_id=744)
    t.new_effect.activate_trigger(trigger_id=531)
    t.new_effect.activate_trigger(trigger_id=679)

    # --- #1428  kar (p2)   [display 247]
    t = tm.add_trigger('kar (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1429  kar (p3)   [display 248]
    t = tm.add_trigger('kar (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1430  kar (p4)   [display 249]
    t = tm.add_trigger('kar (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1431  kar (p5)   [display 250]
    t = tm.add_trigger('kar (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1432  kar (p6)   [display 251]
    t = tm.add_trigger('kar (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1433  kar (p7)   [display 252]
    t = tm.add_trigger('kar (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1434  kar (p8)   [display 253]
    t = tm.add_trigger('kar (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=6, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KARAMBIT_WARRIOR.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1435  viet (p1)   [display 254]
    t = tm.add_trigger('viet (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1436)
    t.new_effect.activate_trigger(trigger_id=297)
    t.new_effect.activate_trigger(trigger_id=737)
    t.new_effect.activate_trigger(trigger_id=452)

    # --- #1436  rata (p1)   [display 262]
    t = tm.add_trigger('rata (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=81, object_type=ObjectType.MILITARY, include_changeable_weapon_objects=-1)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1437  viet (p2)   [display 255]
    t = tm.add_trigger('viet (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1444)
    t.new_effect.activate_trigger(trigger_id=328)
    t.new_effect.activate_trigger(trigger_id=738)
    t.new_effect.activate_trigger(trigger_id=483)

    # --- #1438  viet (p3)   [display 256]
    t = tm.add_trigger('viet (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1445)
    t.new_effect.activate_trigger(trigger_id=329)
    t.new_effect.activate_trigger(trigger_id=739)
    t.new_effect.activate_trigger(trigger_id=484)

    # --- #1439  viet (p4)   [display 257]
    t = tm.add_trigger('viet (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1446)
    t.new_effect.activate_trigger(trigger_id=330)
    t.new_effect.activate_trigger(trigger_id=740)
    t.new_effect.activate_trigger(trigger_id=485)

    # --- #1440  viet (p5)   [display 258]
    t = tm.add_trigger('viet (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1447)
    t.new_effect.activate_trigger(trigger_id=331)
    t.new_effect.activate_trigger(trigger_id=741)
    t.new_effect.activate_trigger(trigger_id=486)

    # --- #1441  viet (p6)   [display 259]
    t = tm.add_trigger('viet (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1448)
    t.new_effect.activate_trigger(trigger_id=332)
    t.new_effect.activate_trigger(trigger_id=742)
    t.new_effect.activate_trigger(trigger_id=487)

    # --- #1442  viet (p7)   [display 260]
    t = tm.add_trigger('viet (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1449)
    t.new_effect.activate_trigger(trigger_id=333)
    t.new_effect.activate_trigger(trigger_id=743)
    t.new_effect.activate_trigger(trigger_id=488)

    # --- #1443  viet (p8)   [display 261]
    t = tm.add_trigger('viet (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.VIETNAMESE.ID, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=1450)
    t.new_effect.activate_trigger(trigger_id=334)
    t.new_effect.activate_trigger(trigger_id=744)
    t.new_effect.activate_trigger(trigger_id=489)

    # --- #1444  rata (p2)   [display 263]
    t = tm.add_trigger('rata (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=81, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1445  rata (p3)   [display 264]
    t = tm.add_trigger('rata (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1446  rata (p4)   [display 265]
    t = tm.add_trigger('rata (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1447  rata (p5)   [display 266]
    t = tm.add_trigger('rata (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1448  rata (p6)   [display 267]
    t = tm.add_trigger('rata (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1449  rata (p7)   [display 268]
    t = tm.add_trigger('rata (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1450  rata (p8)   [display 269]
    t = tm.add_trigger('rata (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=81,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATTAN_ARCHER.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1451  cuma (p1)   [display 270]
    t = tm.add_trigger('cuma (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1452)
    t.new_effect.activate_trigger(trigger_id=301)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=459)

    # --- #1452  kip (p1)   [display 278]
    t = tm.add_trigger('kip (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, object_type=ObjectType.MILITARY, include_changeable_weapon_objects=-1)
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        location_x=48,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        location_x=52,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        location_x=55,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        location_x=59,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1453  cuma (p2)   [display 271]
    t = tm.add_trigger('cuma (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1460)
    t.new_effect.activate_trigger(trigger_id=328)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=532)

    # --- #1454  cuma (p3)   [display 272]
    t = tm.add_trigger('cuma (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1461)
    t.new_effect.activate_trigger(trigger_id=329)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=533)

    # --- #1455  cuma (p4)   [display 273]
    t = tm.add_trigger('cuma (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1462)
    t.new_effect.activate_trigger(trigger_id=330)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=534)

    # --- #1456  cuma (p5)   [display 274]
    t = tm.add_trigger('cuma (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1463)
    t.new_effect.activate_trigger(trigger_id=331)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=535)

    # --- #1457  cuma (p6)   [display 275]
    t = tm.add_trigger('cuma (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1464)
    t.new_effect.activate_trigger(trigger_id=332)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=536)

    # --- #1458  cuma (p7)   [display 276]
    t = tm.add_trigger('cuma (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1465)
    t.new_effect.activate_trigger(trigger_id=333)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=537)

    # --- #1459  cuma (p8)   [display 277]
    t = tm.add_trigger('cuma (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.CUMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1466)
    t.new_effect.activate_trigger(trigger_id=334)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=538)

    # --- #1460  kip (p2)   [display 279]
    t = tm.add_trigger('kip (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1461  kip (p3)   [display 280]
    t = tm.add_trigger('kip (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )

    # --- #1462  kip (p4)   [display 281]
    t = tm.add_trigger('kip (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )

    # --- #1463  kip (p5)   [display 282]
    t = tm.add_trigger('kip (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )

    # --- #1464  kip (p6)   [display 283]
    t = tm.add_trigger('kip (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )

    # --- #1465  kip (p7)   [display 284]
    t = tm.add_trigger('kip (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )

    # --- #1466  kip (p8)   [display 285]
    t = tm.add_trigger('kip (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KIPCHAK.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )

    # --- #1467  tata (p1)   [display 286]
    t = tm.add_trigger('tata (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1468)
    t.new_effect.activate_trigger(trigger_id=302)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=452)

    # --- #1468  kesh (p1)   [display 294]
    t = tm.add_trigger('kesh (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=61, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_KESHIK.ID, location_x=48, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_KESHIK.ID, location_x=52, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_KESHIK.ID, location_x=55, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_KESHIK.ID, location_x=59, location_y=22, disable_sound=-1)

    # --- #1469  bulg (p1)   [display 302]
    t = tm.add_trigger('bulg (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1470)
    t.new_effect.activate_trigger(trigger_id=302)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=459)

    # --- #1470  kon (p1)   [display 310]
    t = tm.add_trigger('kon (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        location_x=48,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        location_x=52,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        location_x=55,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        location_x=59,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1471  bulg (p2)   [display 303]
    t = tm.add_trigger('bulg (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1478)
    t.new_effect.activate_trigger(trigger_id=391)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=483)

    # --- #1472  bulg (p3)   [display 304]
    t = tm.add_trigger('bulg (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1479)
    t.new_effect.activate_trigger(trigger_id=392)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=484)

    # --- #1473  bulg (p4)   [display 305]
    t = tm.add_trigger('bulg (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1480)
    t.new_effect.activate_trigger(trigger_id=365)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=485)

    # --- #1474  bulg (p5)   [display 306]
    t = tm.add_trigger('bulg (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1481)
    t.new_effect.activate_trigger(trigger_id=366)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=486)

    # --- #1475  bulg (p6)   [display 307]
    t = tm.add_trigger('bulg (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1482)
    t.new_effect.activate_trigger(trigger_id=367)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=487)

    # --- #1476  bulg (p7)   [display 308]
    t = tm.add_trigger('bulg (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1483)
    t.new_effect.activate_trigger(trigger_id=368)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=488)

    # --- #1477  bulg (p8)   [display 309]
    t = tm.add_trigger('bulg (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.BULGARIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1484)
    t.new_effect.activate_trigger(trigger_id=369)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=489)

    # --- #1478  kon (p2)   [display 311]
    t = tm.add_trigger('kon (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=41,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1479  kon (p3)   [display 312]
    t = tm.add_trigger('kon (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=41,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )

    # --- #1480  kon (p4)   [display 313]
    t = tm.add_trigger('kon (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=41,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )

    # --- #1481  kon (p5)   [display 314]
    t = tm.add_trigger('kon (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=41,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )

    # --- #1482  kon (p6)   [display 315]
    t = tm.add_trigger('kon (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )

    # --- #1483  kon (p7)   [display 316]
    t = tm.add_trigger('kon (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )

    # --- #1484  kon (p8)   [display 317]
    t = tm.add_trigger('kon (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KONNIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )

    # --- #1485  lith (p1)   [display 318]
    t = tm.add_trigger('lith (p1)', description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1486)
    t.new_effect.activate_trigger(trigger_id=301)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=460)

    # --- #1486  leth (p1)   [display 326]
    t = tm.add_trigger('leth (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, object_type=ObjectType.MILITARY, include_changeable_weapon_objects=-1)
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        location_x=48,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        location_x=52,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        location_x=55,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        location_x=59,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1487  lith (p2)   [display 319]
    t = tm.add_trigger('lith (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1494)
    t.new_effect.activate_trigger(trigger_id=328)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=490)

    # --- #1488  lith (p3)   [display 320]
    t = tm.add_trigger('lith (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1495)
    t.new_effect.activate_trigger(trigger_id=329)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=491)

    # --- #1489  lith (p4)   [display 321]
    t = tm.add_trigger('lith (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1496)
    t.new_effect.activate_trigger(trigger_id=330)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)

    # --- #1490  lith (p5)   [display 322]
    t = tm.add_trigger('lith (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1497)
    t.new_effect.activate_trigger(trigger_id=331)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)

    # --- #1491  lith (p6)   [display 323]
    t = tm.add_trigger('lith (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1498)
    t.new_effect.activate_trigger(trigger_id=332)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=494)

    # --- #1492  lith (p7)   [display 324]
    t = tm.add_trigger('lith (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1499)
    t.new_effect.activate_trigger(trigger_id=333)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)

    # --- #1493  lith (p8)   [display 325]
    t = tm.add_trigger('lith (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.LITHUANIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1500)
    t.new_effect.activate_trigger(trigger_id=334)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)

    # --- #1494  leth (p2)   [display 327]
    t = tm.add_trigger('leth (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        facet=0,
        disable_sound=-1,
    )

    # --- #1495  leth (p3)   [display 328]
    t = tm.add_trigger('leth (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )

    # --- #1496  leth (p4)   [display 329]
    t = tm.add_trigger('leth (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        facet=0,
        disable_sound=-1,
    )

    # --- #1497  leth (p5)   [display 330]
    t = tm.add_trigger('leth (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )

    # --- #1498  leth (p6)   [display 331]
    t = tm.add_trigger('leth (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        facet=0,
        disable_sound=-1,
    )

    # --- #1499  leth (p7)   [display 332]
    t = tm.add_trigger('leth (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
