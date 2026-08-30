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
    """Triggers 1500..1749. Mostly: 1x 'leth (p8)', 1x 'kesh (p2)', 1x 'kesh (p3)'."""
    # --- #1500  leth (p8)   [display 333]
    t = tm.add_trigger('leth (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_LEITIS.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        facet=0,
        disable_sound=-1,
    )

    # --- #1501  kesh (p2)   [display 295]
    t = tm.add_trigger('kesh (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1502  kesh (p3)   [display 296]
    t = tm.add_trigger('kesh (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=51,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1503  kesh (p4)   [display 297]
    t = tm.add_trigger('kesh (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1504  kesh (p5)   [display 298]
    t = tm.add_trigger('kesh (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1505  kesh (p6)   [display 299]
    t = tm.add_trigger('kesh (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1506  kesh (p7)   [display 300]
    t = tm.add_trigger('kesh (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1507  kesh (p8)   [display 301]
    t = tm.add_trigger('kesh (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=61,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=12, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_KESHIK.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1508  tata (p4)   [display 289]
    t = tm.add_trigger('tata (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1503)
    t.new_effect.activate_trigger(trigger_id=365)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=485)

    # --- #1509  tata (p5)   [display 290]
    t = tm.add_trigger('tata (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1504)
    t.new_effect.activate_trigger(trigger_id=366)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=486)

    # --- #1510  tata (p6)   [display 291]
    t = tm.add_trigger('tata (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1505)
    t.new_effect.activate_trigger(trigger_id=367)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=487)

    # --- #1511  tata (p7)   [display 292]
    t = tm.add_trigger('tata (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1506)
    t.new_effect.activate_trigger(trigger_id=368)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=488)

    # --- #1512  tata (p8)   [display 293]
    t = tm.add_trigger('tata (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1507)
    t.new_effect.activate_trigger(trigger_id=369)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=489)

    # --- #1513  tata (p2)   [display 287]
    t = tm.add_trigger('tata (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1501)
    t.new_effect.activate_trigger(trigger_id=363)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=483)

    # --- #1514  tata (p3)   [display 288]
    t = tm.add_trigger('tata (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.TATARS.ID)
    t.new_effect.activate_trigger(trigger_id=1502)
    t.new_effect.activate_trigger(trigger_id=364)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=484)

    # --- #1515  ==UPS============   [display 847]
    t = tm.add_trigger('==UPS============', description_stid=0)

    # --- #1516  ==Resources======   [display 937]
    t = tm.add_trigger('==Resources======', description_stid=0)

    # --- #1517  ==TaskUnits======   [display 965]
    t = tm.add_trigger('==TaskUnits======', description_stid=0)

    # --- #1518  sic (p1)   [display 1519]
    t = tm.add_trigger('sic (p1)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1520)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=451)
    t.new_effect.activate_trigger(trigger_id=450)

    # --- #1519  <----NEW CIV FIX-->   [display 1518]
    t = tm.add_trigger('<----NEW CIV FIX-->', description_stid=0, short_description_stid=0)

    # --- #1520  serjeants (p1)   [display 1536]
    t = tm.add_trigger('serjeants (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=92, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1521  <-- Unit  Spawn -->   [display 1535]
    t = tm.add_trigger('<-- Unit  Spawn -->', description_stid=0, short_description_stid=0, header=1)

    # --- #1522  sic (p2)   [display 1520]
    t = tm.add_trigger('sic (p2)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1529)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=476)
    t.new_effect.activate_trigger(trigger_id=321)

    # --- #1523  sic (p3)   [display 1521]
    t = tm.add_trigger('sic (p3)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1530)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=477)
    t.new_effect.activate_trigger(trigger_id=322)

    # --- #1524  sic (p4)   [display 1522]
    t = tm.add_trigger('sic (p4)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1531)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=478)
    t.new_effect.activate_trigger(trigger_id=323)

    # --- #1525  sic (p5)   [display 1523]
    t = tm.add_trigger('sic (p5)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1532)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=479)
    t.new_effect.activate_trigger(trigger_id=324)

    # --- #1526  sic (p6)   [display 1524]
    t = tm.add_trigger('sic (p6)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1533)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=480)
    t.new_effect.activate_trigger(trigger_id=325)

    # --- #1527  sic (p7)   [display 1525]
    t = tm.add_trigger('sic (p7)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1534)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=481)
    t.new_effect.activate_trigger(trigger_id=326)

    # --- #1528  sic (p8)   [display 1526]
    t = tm.add_trigger('sic (p8)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.SICILIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1535)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=482)
    t.new_effect.activate_trigger(trigger_id=327)

    # --- #1529  serjeants (p2)   [display 1537]
    t = tm.add_trigger('serjeants (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1530  serjeants (p3)   [display 1538]
    t = tm.add_trigger('serjeants (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1531  serjeants (p4)   [display 1539]
    t = tm.add_trigger('serjeants (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1532  serjeants (p5)   [display 1540]
    t = tm.add_trigger('serjeants (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1533  serjeants (p6)   [display 1541]
    t = tm.add_trigger('serjeants (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1534  serjeants (p7)   [display 1542]
    t = tm.add_trigger('serjeants (p7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1535  serjeants (p8)   [display 1543]
    t = tm.add_trigger('serjeants (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_SERJEANT.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1536  <-- Goth Fix -->   [display 1552]
    t = tm.add_trigger('<-- Goth Fix -->', description_stid=0, short_description_stid=0)

    # --- #1537  husk (p2)   [display 1553]
    t = tm.add_trigger('husk (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer()
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1538  husk (p3)   [display 1554]
    t = tm.add_trigger('husk (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer()
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1539  husk (p4)   [display 1555]
    t = tm.add_trigger('husk (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer()
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1540  husk (p5)   [display 1556]
    t = tm.add_trigger('husk (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer()
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1541  husk (p6)   [display 1557]
    t = tm.add_trigger('husk (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=92, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer()
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1542  husk (p8)   [display 1558]
    t = tm.add_trigger('husk (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=92,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer()
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSKARL.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1543  bur (p1)   [display 1527]
    t = tm.add_trigger('bur (p1)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1551)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=297)

    # --- #1544  bur (p2)   [display 1528]
    t = tm.add_trigger('bur (p2)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1552)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=490)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1545  bur (p3)   [display 1529]
    t = tm.add_trigger('bur (p3)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1553)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=491)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1546  bur (p4)   [display 1530]
    t = tm.add_trigger('bur (p4)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1554)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1547  bur (p5)   [display 1531]
    t = tm.add_trigger('bur (p5)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1555)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1548  bur (p6)   [display 1532]
    t = tm.add_trigger('bur (p6)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1556)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=543)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1549  bur (p7)   [display 1533]
    t = tm.add_trigger('bur (p7)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1557)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1550  bur (p8)   [display 1534]
    t = tm.add_trigger('bur (p8)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.BURGUNDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1558)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1551  cous (p1)   [display 1544]
    t = tm.add_trigger('cous (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, object_type=ObjectType.MILITARY, include_changeable_weapon_objects=-1)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1552  cous (p2)   [display 1545]
    t = tm.add_trigger('cous (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1553  cous (p3)   [display 1546]
    t = tm.add_trigger('cous (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1554  cous (p4)   [display 1547]
    t = tm.add_trigger('cous (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1555  cous (p5)   [display 1548]
    t = tm.add_trigger('cous (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1556  cous (p6)   [display 1549]
    t = tm.add_trigger('cous (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1557  cous (p7)   [display 1550]
    t = tm.add_trigger('cous (p7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1558  cous (p8)   [display 1551]
    t = tm.add_trigger('cous (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COUSTILLIER.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1559  move short (p1)   [display 1560]
    t = tm.add_trigger('move short (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_effect.task_object(
        location_x=50,
        location_y=24,
        area_x1=48,
        area_y1=22,
        area_x2=48,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        location_x=52,
        location_y=25,
        area_x1=52,
        area_y1=22,
        area_x2=52,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        location_x=55,
        location_y=25,
        area_x1=55,
        area_y1=22,
        area_x2=55,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        location_x=57,
        location_y=25,
        area_x1=59,
        area_y1=22,
        area_x2=59,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1560  <--Move Fix-->   [display 1559]
    t = tm.add_trigger('<--Move Fix-->', description_stid=0, short_description_stid=0)

    # --- #1561  move short (p2)   [display 1561]
    t = tm.add_trigger('move short (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_effect.task_object(
        source_player=PlayerId.TWO,
        location_x=83,
        location_y=25,
        area_x1=81,
        area_y1=22,
        area_x2=81,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=25,
        area_x1=85,
        area_y1=22,
        area_x2=85,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=25,
        area_x1=88,
        area_y1=22,
        area_x2=88,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.TWO,
        location_x=90,
        location_y=25,
        area_x1=92,
        area_y1=22,
        area_x2=92,
        area_y2=22,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1562  move short (p3)   [display 1562]
    t = tm.add_trigger('move short (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_effect.task_object(
        source_player=PlayerId.THREE,
        location_x=25,
        location_y=49,
        area_x1=21,
        area_y1=48,
        area_x2=21,
        area_y2=48,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.THREE,
        location_x=25,
        location_y=50,
        area_x1=21,
        area_y1=52,
        area_x2=21,
        area_y2=52,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.THREE,
        location_x=25,
        location_y=54,
        area_x1=21,
        area_y1=55,
        area_x2=21,
        area_y2=55,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.THREE,
        location_x=25,
        location_y=55,
        area_x1=21,
        area_y1=59,
        area_x2=21,
        area_y2=59,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1563  move short (p4)   [display 1563]
    t = tm.add_trigger('move short (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_effect.task_object(
        source_player=PlayerId.FOUR,
        location_x=116,
        location_y=54,
        area_x1=119,
        area_y1=55,
        area_x2=119,
        area_y2=55,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.FOUR,
        location_x=116,
        location_y=56,
        area_x1=119,
        area_y1=59,
        area_x2=119,
        area_y2=59,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.FOUR,
        location_x=116,
        location_y=51,
        area_x1=119,
        area_y1=52,
        area_x2=119,
        area_y2=52,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )
    t.new_effect.task_object(
        source_player=PlayerId.FOUR,
        location_x=116,
        location_y=49,
        area_x1=119,
        area_y1=48,
        area_x2=119,
        area_y2=48,
        object_type=ObjectType.MILITARY,
        action_type=-1,
        disable_garrison_unload_sound=-1,
        issue_group_command=-1,
        queue_action=-1,
    )

    # --- #1564  <---Clear Instructions--->   [display 1564]
    t = tm.add_trigger('<---Clear Instructions--->', description_stid=0, short_description_stid=0)

    # --- #1565  poles (p1)   [display 1566]
    t = tm.add_trigger('poles (p1)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1590)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=298)

    # --- #1566  poles (p2)   [display 1567]
    t = tm.add_trigger('poles (p2)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1591)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=539)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1567  poles (p3)   [display 1568]
    t = tm.add_trigger('poles (p3)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1592)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=540)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1568  poles (p4)   [display 1569]
    t = tm.add_trigger('poles (p4)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1593)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1569  poles (p5)   [display 1570]
    t = tm.add_trigger('poles (p5)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1594)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1570  poles (p6)   [display 1571]
    t = tm.add_trigger('poles (p6)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1595)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=543)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1571  poles (p7)   [display 1572]
    t = tm.add_trigger('poles (p7)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1596)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1572  poles (p8)   [display 1573]
    t = tm.add_trigger('poles (p8)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.POLES.ID)
    t.new_effect.activate_trigger(trigger_id=1597)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1573  bohemians (p1)   [display 1582]
    t = tm.add_trigger('bohemians (p1)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1581)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=298)

    # --- #1574  bohemians (p2)   [display 1583]
    t = tm.add_trigger('bohemians (p2)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1582)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=539)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1575  bohemians (p3)   [display 1584]
    t = tm.add_trigger('bohemians (p3)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1583)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=540)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1576  bohemians (p4)   [display 1585]
    t = tm.add_trigger('bohemians (p4)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1584)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1577  bohemians (p5)   [display 1586]
    t = tm.add_trigger('bohemians (p5)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1585)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1578  bohemians (p6)   [display 1587]
    t = tm.add_trigger('bohemians (p6)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1586)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=543)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1579  bohemians (p7)   [display 1588]
    t = tm.add_trigger('bohemians (p7)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1587)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1580  bohemians (p8)   [display 1589]
    t = tm.add_trigger('bohemians (p8)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.BOHEMIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1588)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1581  hussite (p1)   [display 1590]
    t = tm.add_trigger('hussite (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=35, object_type=ObjectType.MILITARY, include_changeable_weapon_objects=-1)
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1582  hussite (p2)   [display 1591]
    t = tm.add_trigger('hussite (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=35,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1583  hussite (p3)   [display 1592]
    t = tm.add_trigger('hussite (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=35,
        source_player=PlayerId.THREE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1584  hussite (p4)   [display 1593]
    t = tm.add_trigger('hussite (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=35,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1585  hussite (p5)   [display 1594]
    t = tm.add_trigger('hussite (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=35,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1586  hussite (p6)   [display 1595]
    t = tm.add_trigger('hussite (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=35,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1587  hussite (p7)   [display 1596]
    t = tm.add_trigger('hussite (p7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=35,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1588  hussite (p8)   [display 1597]
    t = tm.add_trigger('hussite (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=35,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=15)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_HUSSITE_WAGON.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1589  <---Lords of West --->   [display 1565]
    t = tm.add_trigger('<---Lords of West --->', description_stid=0, short_description_stid=0, header=1)

    # --- #1590  obuch (p1)   [display 1574]
    t = tm.add_trigger('obuch (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_OBUCH.ID, location_x=48, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_OBUCH.ID, location_x=52, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_OBUCH.ID, location_x=55, location_y=22, disable_sound=-1)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_OBUCH.ID, location_x=59, location_y=22, disable_sound=-1)

    # --- #1591  obuch (p2)   [display 1575]
    t = tm.add_trigger('obuch (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.TWO,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1592  obuch (p3)   [display 1576]
    t = tm.add_trigger('obuch (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1593  obuch (p4)   [display 1577]
    t = tm.add_trigger('obuch (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FOUR,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1594  obuch (p5)   [display 1578]
    t = tm.add_trigger('obuch (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.FIVE,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1595  obuch (p6)   [display 1579]
    t = tm.add_trigger('obuch (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SIX,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1596  obuch (p7)   [display 1580]
    t = tm.add_trigger('obuch (p7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.SEVEN,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1597  obuch (p8)   [display 1581]
    t = tm.add_trigger('obuch (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(
        quantity=60,
        source_player=PlayerId.EIGHT,
        object_type=ObjectType.MILITARY,
        include_changeable_weapon_objects=-1,
    )
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_OBUCH.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1598  Bengalis (p1)   [display 1599]
    t = tm.add_trigger('Bengalis (p1)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1606)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=298)

    # --- #1599  Bengalis (p2)   [display 1600]
    t = tm.add_trigger('Bengalis (p2)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1607)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=539)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1600  Bengalis (p3)   [display 1601]
    t = tm.add_trigger('Bengalis (p3)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1608)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=540)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1601  Bengalis (p4)   [display 1602]
    t = tm.add_trigger('Bengalis (p4)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1609)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1602  Bengalis (p5)   [display 1603]
    t = tm.add_trigger('Bengalis (p5)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1610)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1603  Bengalis (p6)   [display 1604]
    t = tm.add_trigger('Bengalis (p6)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1611)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=543)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1604  Bengalis (p7)   [display 1605]
    t = tm.add_trigger('Bengalis (p7)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1612)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1605  Bengalis (p8)   [display 1606]
    t = tm.add_trigger('Bengalis (p8)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.BENGALIS.ID)
    t.new_effect.activate_trigger(trigger_id=1646)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1606  Ratha (p1)   [display 1607]
    t = tm.add_trigger('Ratha (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID, location_x=55, location_y=22)
    t.new_effect.create_object(object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID, location_x=59, location_y=22)

    # --- #1607  Ratha (p2)   [display 1608]
    t = tm.add_trigger('Ratha (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1608  Ratha (p3)   [display 1609]
    t = tm.add_trigger('Ratha (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1609  Ratha (p4)   [display 1610]
    t = tm.add_trigger('Ratha (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1610  Ratha (p5)   [display 1611]
    t = tm.add_trigger('Ratha (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_MELEE.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_MELEE.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1611  Ratha (p6)   [display 1612]
    t = tm.add_trigger('Ratha (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1612  Ratha (p7)   [display 1613]
    t = tm.add_trigger('Ratha (p7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1613  <---Dynasties of India--->   [display 1598]
    t = tm.add_trigger('<---Dynasties of India--->', description_stid=0, short_description_stid=0, header=1)

    # --- #1614  Dravidians (p1)   [display 1615]
    t = tm.add_trigger('Dravidians (p1)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1621)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=298)

    # --- #1615  Dravidians (p2)   [display 1616]
    t = tm.add_trigger('Dravidians (p2)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1622)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=539)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1616  Dravidians (p3)   [display 1617]
    t = tm.add_trigger('Dravidians (p3)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1623)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=540)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1617  Dravidians (p4)   [display 1618]
    t = tm.add_trigger('Dravidians (p4)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1624)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1618  Dravidians (p5)   [display 1619]
    t = tm.add_trigger('Dravidians (p5)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1625)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1619  Dravidians (p6)   [display 1620]
    t = tm.add_trigger('Dravidians (p6)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1626)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=543)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1620  Dravidians (p7)   [display 1621]
    t = tm.add_trigger('Dravidians (p7)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1627)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1621  Urumi (p1)   [display 1623]
    t = tm.add_trigger('Urumi (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1622  Urumi (p2)   [display 1624]
    t = tm.add_trigger('Urumi (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1623  Urumi (p3)   [display 1625]
    t = tm.add_trigger('Urumi (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1624  Urumi (p4)   [display 1626]
    t = tm.add_trigger('Urumi (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1625  Urumi (p5)   [display 1627]
    t = tm.add_trigger('Urumi (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1626  Urumi (p6)   [display 1628]
    t = tm.add_trigger('Urumi (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1627  Urumi (p7)   [display 1629]
    t = tm.add_trigger('Urumi (p7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1628  Dravidians (p8)   [display 1622]
    t = tm.add_trigger('Dravidians (p8)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.DRAVIDIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1645)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1629  Gurjaras (p1)\r (p (p1)1   [display 1631]
    t = tm.add_trigger('Gurjaras (p1)\r (p (p1)1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1637)
    t.new_effect.activate_trigger(trigger_id=721)
    t.new_effect.activate_trigger(trigger_id=463)
    t.new_effect.activate_trigger(trigger_id=298)

    # --- #1630  Gurjaras (p2)\r (p (p121   [display 1632]
    t = tm.add_trigger('Gurjaras (p2)\r (p (p121', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1638)
    t.new_effect.activate_trigger(trigger_id=722)
    t.new_effect.activate_trigger(trigger_id=560)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1631  Gurjaras (p3)\r (p (p1)1   [display 1633]
    t = tm.add_trigger('Gurjaras (p3)\r (p (p1)1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1639)
    t.new_effect.activate_trigger(trigger_id=723)
    t.new_effect.activate_trigger(trigger_id=561)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1632  Gurjaras (p4)\r (p (p1)1   [display 1634]
    t = tm.add_trigger('Gurjaras (p4)\r (p (p1)1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1640)
    t.new_effect.activate_trigger(trigger_id=724)
    t.new_effect.activate_trigger(trigger_id=562)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1633  Gurjaras (p5)\r (p (p1)1   [display 1635]
    t = tm.add_trigger('Gurjaras (p5)\r (p (p1)1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1641)
    t.new_effect.activate_trigger(trigger_id=725)
    t.new_effect.activate_trigger(trigger_id=563)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1634  Gurjaras (p6)\r (p (p1)1   [display 1636]
    t = tm.add_trigger('Gurjaras (p6)\r (p (p1)1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1642)
    t.new_effect.activate_trigger(trigger_id=726)
    t.new_effect.activate_trigger(trigger_id=564)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1635  Gurjaras (p7)\r (p (p1)1   [display 1637]
    t = tm.add_trigger('Gurjaras (p7)\r (p (p1)1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1643)
    t.new_effect.activate_trigger(trigger_id=727)
    t.new_effect.activate_trigger(trigger_id=565)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1636  Gurjaras (p8)\r (p (p1)1   [display 1638]
    t = tm.add_trigger('Gurjaras (p8)\r (p (p1)1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.GURJARAS.ID)
    t.new_effect.activate_trigger(trigger_id=1644)
    t.new_effect.activate_trigger(trigger_id=728)
    t.new_effect.activate_trigger(trigger_id=566)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1637  Chakram (p1)   [display 1639]
    t = tm.add_trigger('Chakram (p1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1638  Chakram (p2)   [display 1640]
    t = tm.add_trigger('Chakram (p2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1639  Chakram (p3)   [display 1641]
    t = tm.add_trigger('Chakram (p3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1640  Chakram (p4)   [display 1642]
    t = tm.add_trigger('Chakram (p4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1641  Chakram (p5)   [display 1643]
    t = tm.add_trigger('Chakram (p5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1642  Chakram (p6)   [display 1644]
    t = tm.add_trigger('Chakram (p6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1643  Chakram (p7)   [display 1645]
    t = tm.add_trigger('Chakram (p7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1644  Chakram (p8)   [display 1646]
    t = tm.add_trigger('Chakram (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=41, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=11)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CHAKRAM_THROWER.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1645  Urumi (p8)   [display 1630]
    t = tm.add_trigger('Urumi (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1646  Ratha (p8)   [display 1614]
    t = tm.add_trigger('Ratha (p8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=40, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_RATHA_RANGED.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
    )

    # --- #1647  _- New DLC RoR -_   [display 1647]
    t = tm.add_trigger('_- New DLC RoR -_', description_stid=0, short_description_stid=0)

    # --- #1648  Romans (P1)   [display 1648]
    t = tm.add_trigger('Romans (P1)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1655)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=298)

    # --- #1649  Romans (P2)   [display 1649]
    t = tm.add_trigger('Romans (P2)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1656)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=490)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1650  Romans (P3)   [display 1650]
    t = tm.add_trigger('Romans (P3)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1657)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=491)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1651  Romans (P4)   [display 1651]
    t = tm.add_trigger('Romans (P4)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1658)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1652  Romans (P5)   [display 1652]
    t = tm.add_trigger('Romans (P5)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1659)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1653  Romans (P6)   [display 1653]
    t = tm.add_trigger('Romans (P6)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1660)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=494)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1654  Romans (P7)   [display 1654]
    t = tm.add_trigger('Romans (P7)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1661)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1655  Centuria (P1)   [display 1656]
    t = tm.add_trigger('Centuria (P1)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1656  Centuria (P2)   [display 1657]
    t = tm.add_trigger('Centuria (P2)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1657  Centuria (P3)   [display 1658]
    t = tm.add_trigger('Centuria (P3)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1658  Centuria (P4)   [display 1659]
    t = tm.add_trigger('Centuria (P4)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1659  Centuria (P5)   [display 1660]
    t = tm.add_trigger('Centuria (P5)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1660  Centuria (P6)   [display 1661]
    t = tm.add_trigger('Centuria (P6)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1661  Centuria (P7)   [display 1662]
    t = tm.add_trigger('Centuria (P7)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1662  Centuria (P8)   [display 1663]
    t = tm.add_trigger('Centuria (P8)', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=60, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_CENTURION.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1663  Romans (P8)   [display 1655]
    t = tm.add_trigger('Romans (P8)', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.ROMANS.ID)
    t.new_effect.activate_trigger(trigger_id=1662)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1664  Antidelete P1   [display 1664]
    t = tm.add_trigger('Antidelete P1', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(selected_object_ids=[26939])
    t.new_effect.disable_object_deletion(selected_object_ids=[23131])
    t.new_effect.disable_object_deletion(selected_object_ids=[105993])
    t.new_effect.disable_object_deletion(selected_object_ids=[28539])
    t.new_effect.disable_object_deletion(selected_object_ids=[22923])
    t.new_effect.disable_object_deletion(selected_object_ids=[90052])
    t.new_effect.disable_object_deletion(selected_object_ids=[90053])
    t.new_effect.disable_object_deletion(selected_object_ids=[28541])
    t.new_effect.disable_object_deletion(selected_object_ids=[22926])
    t.new_effect.disable_object_deletion(selected_object_ids=[90055])
    t.new_effect.disable_object_deletion(selected_object_ids=[90056])

    # --- #1665  Antidelete P2   [display 1665]
    t = tm.add_trigger('Antidelete P2', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[26936])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[23094])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[26933])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[28543])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[23080])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[90058])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[90059])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[28545])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[23081])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[90061])
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, selected_object_ids=[90062])

    # --- #1666  Antidelete P3   [display 1666]
    t = tm.add_trigger('Antidelete P3', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[27380])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[23584])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[27377])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[28568])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[23651])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[90067])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[90068])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[28569])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[23653])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[90064])
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, selected_object_ids=[90065])

    # --- #1667  Antidelete P4   [display 1667]
    t = tm.add_trigger('Antidelete P4', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[26930])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[23208])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[26927])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[28547])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[23631])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[90073])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[90074])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[28549])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[23633])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[90070])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, selected_object_ids=[90071])

    # --- #1668  Antidelete P5   [display 1668]
    t = tm.add_trigger('Antidelete P5', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[26906])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[23590])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[26903])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[28566])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[23649])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[90079])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[90080])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[28564])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[23647])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[90076])
    t.new_effect.disable_object_deletion(source_player=PlayerId.FIVE, selected_object_ids=[78285])

    # --- #1669  Antidelete P6   [display 1669]
    t = tm.add_trigger('Antidelete P6', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[26924])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[23606])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[26921])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[28551])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[23637])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[90082])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[90083])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[28553])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[23634])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[90085])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SIX, selected_object_ids=[90086])

    # --- #1670  Antidelete P7   [display 1670]
    t = tm.add_trigger('Antidelete P7', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[26912])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[23594])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[26909])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[28561])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[23645])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[90091])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[90092])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[28559])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[39500])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[90088])
    t.new_effect.disable_object_deletion(source_player=PlayerId.SEVEN, selected_object_ids=[90089])

    # --- #1671  Antidelete P8   [display 1671]
    t = tm.add_trigger('Antidelete P8', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[26915])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[23600])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[26918])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[28558])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[23641])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[90097])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[90098])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[28556])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[23638])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[90094])
    t.new_effect.disable_object_deletion(source_player=PlayerId.EIGHT, selected_object_ids=[90095])

    # --- #1672  Elimina Walls P1   [display 1672]
    t = tm.add_trigger('Elimina Walls P1', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=65500)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        area_x1=43,
        area_y1=16,
        area_x2=64,
        area_y2=38,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        area_x1=43,
        area_y1=16,
        area_x2=64,
        area_y2=38,
    )

    # --- #1673  Elimina Walls P2   [display 1673]
    t = tm.add_trigger('Elimina Walls P2', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=23076)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        source_player=PlayerId.TWO,
        area_x1=76,
        area_y1=16,
        area_x2=97,
        area_y2=38,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        source_player=PlayerId.TWO,
        area_x1=76,
        area_y1=16,
        area_x2=97,
        area_y2=38,
    )

    # --- #1674  Elimina Walls P3   [display 1674]
    t = tm.add_trigger('Elimina Walls P3', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=23621)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        source_player=PlayerId.THREE,
        area_x1=15,
        area_y1=43,
        area_x2=38,
        area_y2=64,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        source_player=PlayerId.THREE,
        area_x1=15,
        area_y1=43,
        area_x2=38,
        area_y2=64,
    )

    # --- #1675  Elimina Walls P4   [display 1675]
    t = tm.add_trigger('Elimina Walls P4', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=23205)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        source_player=PlayerId.FOUR,
        area_x1=102,
        area_y1=43,
        area_x2=125,
        area_y2=64,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        source_player=PlayerId.FOUR,
        area_x1=102,
        area_y1=43,
        area_x2=125,
        area_y2=64,
    )

    # --- #1676  Elimina Walls P5   [display 1676]
    t = tm.add_trigger('Elimina Walls P5', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=23618)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        source_player=PlayerId.FIVE,
        area_x1=15,
        area_y1=76,
        area_x2=38,
        area_y2=97,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        source_player=PlayerId.FIVE,
        area_x1=15,
        area_y1=76,
        area_x2=38,
        area_y2=97,
    )

    # --- #1677  Elimina Walls P6   [display 1677]
    t = tm.add_trigger('Elimina Walls P6', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=23615)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        source_player=PlayerId.SIX,
        area_x1=102,
        area_y1=76,
        area_x2=125,
        area_y2=97,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        source_player=PlayerId.SIX,
        area_x1=102,
        area_y1=76,
        area_x2=125,
        area_y2=97,
    )

    # --- #1678  Elimina Walls P7   [display 1678]
    t = tm.add_trigger('Elimina Walls P7', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=23624)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        source_player=PlayerId.SEVEN,
        area_x1=43,
        area_y1=102,
        area_x2=64,
        area_y2=125,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        source_player=PlayerId.SEVEN,
        area_x1=43,
        area_y1=102,
        area_x2=64,
        area_y2=125,
    )

    # --- #1679  Elimina Walls P8   [display 1679]
    t = tm.add_trigger('Elimina Walls P8', description_stid=0, short_description_stid=0)
    t.new_condition.destroy_object(unit_object=23627)
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.STONE_WALL.ID,
        source_player=PlayerId.EIGHT,
        area_x1=76,
        area_y1=102,
        area_x2=97,
        area_y2=125,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
        source_player=PlayerId.EIGHT,
        area_x1=76,
        area_y1=102,
        area_x2=97,
        area_y2=125,
    )

    # --- #1680  Center View P1   [display 1680]
    t = tm.add_trigger('Center View P1', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(location_x=54, location_y=22)

    # --- #1681  Center View P2   [display 1681]
    t = tm.add_trigger('Center View P2', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(source_player=PlayerId.TWO, location_x=87, location_y=22)

    # --- #1682  Center View P3   [display 1682]
    t = tm.add_trigger('Center View P3', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(source_player=PlayerId.THREE, location_x=25, location_y=53)

    # --- #1683  Center View P4   [display 1683]
    t = tm.add_trigger('Center View P4', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(source_player=PlayerId.FOUR, location_x=119, location_y=53)

    # --- #1684  Center View P5   [display 1684]
    t = tm.add_trigger('Center View P5', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(source_player=PlayerId.FIVE, location_x=25, location_y=86)

    # --- #1685  Center View P6   [display 1685]
    t = tm.add_trigger('Center View P6', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(source_player=PlayerId.SIX, location_x=118, location_y=86)

    # --- #1686  Center View P7   [display 1686]
    t = tm.add_trigger('Center View P7', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(source_player=PlayerId.SEVEN, location_x=53, location_y=114)

    # --- #1687  Center View P8   [display 1687]
    t = tm.add_trigger('Center View P8', description_stid=0, short_description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_effect.change_view(source_player=PlayerId.EIGHT, location_x=87, location_y=115)

    # --- #1688  -- Armenians  --   [display 1688]
    t = tm.add_trigger('-- Armenians  --', description_stid=0, short_description_stid=0)

    # --- #1689  Armenians P1   [display 1689]
    t = tm.add_trigger('Armenians P1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1697)
    t.new_effect.activate_trigger(trigger_id=729)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=298)

    # --- #1690  Armenians P2   [display 1690]
    t = tm.add_trigger('Armenians P2', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1698)
    t.new_effect.activate_trigger(trigger_id=730)
    t.new_effect.activate_trigger(trigger_id=490)
    t.new_effect.activate_trigger(trigger_id=328)

    # --- #1691  Armenians P3   [display 1691]
    t = tm.add_trigger('Armenians P3', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1699)
    t.new_effect.activate_trigger(trigger_id=731)
    t.new_effect.activate_trigger(trigger_id=491)
    t.new_effect.activate_trigger(trigger_id=329)

    # --- #1692  Armenians P4   [display 1692]
    t = tm.add_trigger('Armenians P4', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1700)
    t.new_effect.activate_trigger(trigger_id=732)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=330)

    # --- #1693  Armenians P5   [display 1693]
    t = tm.add_trigger('Armenians P5', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1701)
    t.new_effect.activate_trigger(trigger_id=733)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=331)

    # --- #1694  Armenians P6   [display 1694]
    t = tm.add_trigger('Armenians P6', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1702)
    t.new_effect.activate_trigger(trigger_id=734)
    t.new_effect.activate_trigger(trigger_id=494)
    t.new_effect.activate_trigger(trigger_id=332)

    # --- #1695  Armenians P7   [display 1695]
    t = tm.add_trigger('Armenians P7', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1703)
    t.new_effect.activate_trigger(trigger_id=735)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=333)

    # --- #1696  Armenians P8   [display 1696]
    t = tm.add_trigger('Armenians P8', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.ARMENIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1704)
    t.new_effect.activate_trigger(trigger_id=736)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=334)

    # --- #1697  ArqComp P1   [display 1697]
    t = tm.add_trigger('ArqComp P1', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1698  ArqComp P2   [display 1698]
    t = tm.add_trigger('ArqComp P2', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1699  ArqComp P3   [display 1699]
    t = tm.add_trigger('ArqComp P3', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1700  ArqComp P4   [display 1700]
    t = tm.add_trigger('ArqComp P4', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1701  ArqComp P5   [display 1701]
    t = tm.add_trigger('ArqComp P5', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1702  ArqComp P6   [display 1702]
    t = tm.add_trigger('ArqComp P6', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1703  ArqComp P7   [display 1703]
    t = tm.add_trigger('ArqComp P7', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1704  ArqComp P8   [display 1704]
    t = tm.add_trigger('ArqComp P8', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_COMPOSITE_BOWMAN.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1705  Georgians P1   [display 1706]
    t = tm.add_trigger('Georgians P1', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1714)
    t.new_effect.activate_trigger(trigger_id=737)
    t.new_effect.activate_trigger(trigger_id=453)
    t.new_effect.activate_trigger(trigger_id=302)

    # --- #1706  Georgians P2   [display 1707]
    t = tm.add_trigger('Georgians P2', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1715)
    t.new_effect.activate_trigger(trigger_id=738)
    t.new_effect.activate_trigger(trigger_id=490)
    t.new_effect.activate_trigger(trigger_id=363)

    # --- #1707  Georgians P3   [display 1708]
    t = tm.add_trigger('Georgians P3', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1716)
    t.new_effect.activate_trigger(trigger_id=739)
    t.new_effect.activate_trigger(trigger_id=491)
    t.new_effect.activate_trigger(trigger_id=364)

    # --- #1708  Georgians P4   [display 1709]
    t = tm.add_trigger('Georgians P4', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1717)
    t.new_effect.activate_trigger(trigger_id=740)
    t.new_effect.activate_trigger(trigger_id=492)
    t.new_effect.activate_trigger(trigger_id=365)

    # --- #1709  Georgians P5   [display 1710]
    t = tm.add_trigger('Georgians P5', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1718)
    t.new_effect.activate_trigger(trigger_id=741)
    t.new_effect.activate_trigger(trigger_id=493)
    t.new_effect.activate_trigger(trigger_id=366)

    # --- #1710  Georgians P6   [display 1711]
    t = tm.add_trigger('Georgians P6', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1719)
    t.new_effect.activate_trigger(trigger_id=742)
    t.new_effect.activate_trigger(trigger_id=494)
    t.new_effect.activate_trigger(trigger_id=367)

    # --- #1711  Georgians P7   [display 1712]
    t = tm.add_trigger('Georgians P7', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1720)
    t.new_effect.activate_trigger(trigger_id=743)
    t.new_effect.activate_trigger(trigger_id=495)
    t.new_effect.activate_trigger(trigger_id=368)

    # --- #1712  Georgians P8   [display 1713]
    t = tm.add_trigger('Georgians P8', description_stid=0, short_description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.GEORGIANS.ID)
    t.new_effect.activate_trigger(trigger_id=1721)
    t.new_effect.activate_trigger(trigger_id=744)
    t.new_effect.activate_trigger(trigger_id=496)
    t.new_effect.activate_trigger(trigger_id=369)

    # --- #1713  -- Georgians --   [display 1705]
    t = tm.add_trigger('-- Georgians --', description_stid=0, short_description_stid=0)

    # --- #1714  Monaspa P1   [display 1714]
    t = tm.add_trigger('Monaspa P1', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1715  Monaspa P2   [display 1715]
    t = tm.add_trigger('Monaspa P2', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.TWO, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.TWO,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.TWO,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.TWO,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.TWO,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #1716  Monaspa P3   [display 1716]
    t = tm.add_trigger('Monaspa P3', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.THREE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.THREE,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #1717  Monaspa P4   [display 1717]
    t = tm.add_trigger('Monaspa P4', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FOUR, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FOUR,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #1718  Monaspa P5   [display 1718]
    t = tm.add_trigger('Monaspa P5', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.FIVE, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.FIVE,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #1719  Monaspa P6   [display 1719]
    t = tm.add_trigger('Monaspa P6', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SIX, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SIX,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #1720  Monaspa P7   [display 1720]
    t = tm.add_trigger('Monaspa P7', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.SEVEN, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SEVEN,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SEVEN,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SEVEN,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.SEVEN,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1721  Monaspa P8   [display 1721]
    t = tm.add_trigger('Monaspa P8', description_stid=0, short_description_stid=0, enabled=0, looping=1)
    t.new_condition.own_fewer_objects(quantity=80, source_player=PlayerId.EIGHT, object_type=ObjectType.MILITARY)
    t.new_condition.timer(timer=8)
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.EIGHT,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.EIGHT,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.EIGHT,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.ELITE_MONASPA.ID,
        source_player=PlayerId.EIGHT,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #1722  -- Vote Kick   [display 1722]
    t = tm.add_trigger('-- Vote Kick', description_stid=0, short_description_stid=0)

    # --- #1723  VoteKickP1-P2-P4   [display 1723]
    t = tm.add_trigger('VoteKickP1-P2-P4', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FOUR,
        area_x1=142,
        area_y1=31,
        area_x2=142,
        area_y2=31,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.TWO,
        area_x1=108,
        area_y1=0,
        area_x2=108,
        area_y2=0,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1753)

    # --- #1724  VoteKickP1-P3-P4   [display 1724]
    t = tm.add_trigger('VoteKickP1-P3-P4', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FOUR,
        area_x1=142,
        area_y1=31,
        area_x2=142,
        area_y2=31,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.THREE,
        area_x1=0,
        area_y1=31,
        area_x2=0,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1753)

    # --- #1725  VoteKickP1-P3-P2   [display 1725]
    t = tm.add_trigger('VoteKickP1-P3-P2', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.TWO,
        area_x1=108,
        area_y1=0,
        area_x2=108,
        area_y2=0,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.THREE,
        area_x1=0,
        area_y1=31,
        area_x2=0,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1753)

    # --- #1726  VoteKickP2-P1-P3   [display 1726]
    t = tm.add_trigger('VoteKickP2-P1-P3', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(quantity=1, object_list=598, area_x1=33, area_y1=0, area_x2=33, area_y2=0, inverted=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.THREE,
        area_x1=1,
        area_y1=31,
        area_x2=1,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1747)

    # --- #1727  VoteKickP2-P1-P4   [display 1727]
    t = tm.add_trigger('VoteKickP2-P1-P4', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(quantity=1, object_list=598, area_x1=33, area_y1=0, area_x2=33, area_y2=0, inverted=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FOUR,
        area_x1=143,
        area_y1=31,
        area_x2=143,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1747)

    # --- #1728  VoteKickP2-P3-P4   [display 1728]
    t = tm.add_trigger('VoteKickP2-P3-P4', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.THREE,
        area_x1=1,
        area_y1=31,
        area_x2=1,
        area_y2=31,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FOUR,
        area_x1=143,
        area_y1=31,
        area_x2=143,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1747)

    # --- #1729  VoteKickP3-P1-P2   [display 1729]
    t = tm.add_trigger('VoteKickP3-P1-P2', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(quantity=1, object_list=598, area_x1=32, area_y1=0, area_x2=32, area_y2=0, inverted=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.TWO,
        area_x1=107,
        area_y1=0,
        area_x2=107,
        area_y2=0,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1748)

    # --- #1730  VoteKickP3-P1-P4   [display 1730]
    t = tm.add_trigger('VoteKickP3-P1-P4', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(quantity=1, object_list=598, area_x1=32, area_y1=0, area_x2=32, area_y2=0, inverted=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FOUR,
        area_x1=141,
        area_y1=31,
        area_x2=141,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1748)

    # --- #1731  VoteKickP3-P2-P4   [display 1731]
    t = tm.add_trigger('VoteKickP3-P2-P4', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.TWO,
        area_x1=107,
        area_y1=0,
        area_x2=107,
        area_y2=0,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FOUR,
        area_x1=141,
        area_y1=31,
        area_x2=141,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1748)

    # --- #1732  VoteKickP4-P1-P3   [display 1732]
    t = tm.add_trigger('VoteKickP4-P1-P3', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(quantity=1, object_list=598, area_x1=34, area_y1=0, area_x2=34, area_y2=0, inverted=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.THREE,
        area_x1=2,
        area_y1=31,
        area_x2=2,
        area_y2=31,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1749)

    # --- #1733  VoteKickP4-P1-P2   [display 1733]
    t = tm.add_trigger('VoteKickP4-P1-P2', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(quantity=1, object_list=598, area_x1=34, area_y1=0, area_x2=34, area_y2=0, inverted=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.TWO,
        area_x1=109,
        area_y1=0,
        area_x2=109,
        area_y2=0,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1749)

    # --- #1734  VoteKickP4-P3-P2   [display 1734]
    t = tm.add_trigger('VoteKickP4-P3-P2', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.THREE,
        area_x1=2,
        area_y1=31,
        area_x2=2,
        area_y2=31,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.TWO,
        area_x1=109,
        area_y1=0,
        area_x2=109,
        area_y2=0,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1749)

    # --- #1735  VoteKickP5-P6-P7   [display 1735]
    t = tm.add_trigger('VoteKickP5-P6-P7', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SIX,
        area_x1=141,
        area_y1=107,
        area_x2=141,
        area_y2=107,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SEVEN,
        area_x1=30,
        area_y1=142,
        area_x2=30,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1750)

    # --- #1736  VoteKickP5-P6-P8   [display 1736]
    t = tm.add_trigger('VoteKickP5-P6-P8', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SIX,
        area_x1=141,
        area_y1=107,
        area_x2=141,
        area_y2=107,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.EIGHT,
        area_x1=103,
        area_y1=142,
        area_x2=103,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1750)

    # --- #1737  VoteKickP5-P7-P8   [display 1737]
    t = tm.add_trigger('VoteKickP5-P7-P8', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SEVEN,
        area_x1=30,
        area_y1=142,
        area_x2=30,
        area_y2=142,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.EIGHT,
        area_x1=103,
        area_y1=142,
        area_x2=103,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1750)

    # --- #1738  VoteKickP6-P5-P7   [display 1738]
    t = tm.add_trigger('VoteKickP6-P5-P7', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FIVE,
        area_x1=2,
        area_y1=111,
        area_x2=2,
        area_y2=111,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SEVEN,
        area_x1=32,
        area_y1=142,
        area_x2=32,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1751)

    # --- #1739  VoteKickP6-P5-P8   [display 1739]
    t = tm.add_trigger('VoteKickP6-P5-P8', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FIVE,
        area_x1=2,
        area_y1=111,
        area_x2=2,
        area_y2=111,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.EIGHT,
        area_x1=105,
        area_y1=142,
        area_x2=105,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1751)

    # --- #1740  VoteKickP6-P7-P8   [display 1740]
    t = tm.add_trigger('VoteKickP6-P7-P8', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SEVEN,
        area_x1=32,
        area_y1=142,
        area_x2=32,
        area_y2=142,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.EIGHT,
        area_x1=105,
        area_y1=142,
        area_x2=105,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1751)

    # --- #1741  VoteKickP7-P5-P6   [display 1741]
    t = tm.add_trigger('VoteKickP7-P5-P6', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FIVE,
        area_x1=0,
        area_y1=111,
        area_x2=0,
        area_y2=111,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SIX,
        area_x1=142,
        area_y1=107,
        area_x2=142,
        area_y2=107,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1752)

    # --- #1742  VoteKickP7-P5-P8   [display 1742]
    t = tm.add_trigger('VoteKickP7-P5-P8', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FIVE,
        area_x1=0,
        area_y1=111,
        area_x2=0,
        area_y2=111,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.EIGHT,
        area_x1=104,
        area_y1=142,
        area_x2=104,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1752)

    # --- #1743  VoteKickP7-P6-P8   [display 1743]
    t = tm.add_trigger('VoteKickP7-P6-P8', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SIX,
        area_x1=142,
        area_y1=107,
        area_x2=142,
        area_y2=107,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.EIGHT,
        area_x1=104,
        area_y1=142,
        area_x2=104,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1752)

    # --- #1744  VoteKickP8-P5-P6   [display 1744]
    t = tm.add_trigger('VoteKickP8-P5-P6', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FIVE,
        area_x1=1,
        area_y1=111,
        area_x2=1,
        area_y2=111,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SIX,
        area_x1=143,
        area_y1=107,
        area_x2=143,
        area_y2=107,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1754)

    # --- #1745  VoteKickP8-P5-P7   [display 1745]
    t = tm.add_trigger('VoteKickP8-P5-P7', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.FIVE,
        area_x1=1,
        area_y1=111,
        area_x2=1,
        area_y2=111,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SEVEN,
        area_x1=31,
        area_y1=142,
        area_x2=31,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1754)

    # --- #1746  VoteKickP8-P6-P7   [display 1746]
    t = tm.add_trigger('VoteKickP8-P6-P7', description_stid=0, short_description_stid=0)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SIX,
        area_x1=143,
        area_y1=107,
        area_x2=143,
        area_y2=107,
        inverted=1,
    )
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=598,
        source_player=PlayerId.SEVEN,
        area_x1=31,
        area_y1=142,
        area_x2=31,
        area_y2=142,
        inverted=1,
    )
    t.new_effect.activate_trigger(trigger_id=1754)

    # --- #1747  Kick P2   [display 1748]
    t = tm.add_trigger('Kick P2', description_stid=0, short_description_stid=0, enabled=0)
    t.new_effect.display_instructions(source_player=PlayerId.EIGHT, message='RED has been Vote-Kicked!!', use_tag_color_for_icon=1)
    t.new_effect.declare_victory(source_player=PlayerId.TWO, enabled=0)
    t.new_effect.disable_object_deletion(source_player=PlayerId.TWO, area_x1=107, area_y1=0, area_x2=109, area_y2=0)

    # --- #1748  Kick P3   [display 1749]
    t = tm.add_trigger('Kick P3', description_stid=0, short_description_stid=0, enabled=0)
    t.new_effect.display_instructions(
        source_player=PlayerId.EIGHT,
        message='GREEN has been Vote-Kicked!!',
        use_tag_color_for_icon=1,
    )
    t.new_effect.declare_victory(source_player=PlayerId.THREE, enabled=0)
    t.new_effect.disable_object_deletion(source_player=PlayerId.THREE, area_x1=0, area_y1=31, area_x2=2, area_y2=31)

    # --- #1749  Kick P4   [display 1750]
    t = tm.add_trigger('Kick P4', description_stid=0, short_description_stid=0, enabled=0)
    t.new_effect.display_instructions(
        source_player=PlayerId.EIGHT,
        message='YELLOW has been Vote-Kicked!!',
        use_tag_color_for_icon=1,
    )
    t.new_effect.declare_victory(source_player=PlayerId.FOUR, enabled=0)
    t.new_effect.disable_object_deletion(source_player=PlayerId.FOUR, area_x1=141, area_y1=31, area_x2=143, area_y2=31)
