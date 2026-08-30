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
    """Triggers 500..749. Mostly: 25x '450 kills', 21x '500 kills', 14x '650 kills'."""
    # --- #500  450 kills   [display 721]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>450 Kills - Imperial Age')

    # --- #501  450 kills   [display 740]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>450 Kills - Imperial Age')

    # --- #502  450 kills   [display 759]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>450 Kills - Imperial Age')

    # --- #503  450 kills   [display 778]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>450 Kills - Imperial Age')

    # --- #504  500 kills   [display 665]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>500 Kills - Imperial Age')

    # --- #505  500 kills   [display 684]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>500 Kills - Imperial Age')

    # --- #506  500 kills   [display 703]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>500 Kills - Imperial Age')

    # --- #507  500 kills   [display 722]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>500 Kills - Imperial Age')

    # --- #508  500 kills   [display 741]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>500 Kills - Imperial Age')

    # --- #509  500 kills   [display 760]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>500 Kills - Imperial Age')

    # --- #510  500 kills   [display 779]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>500 Kills - Imperial Age')

    # --- #511  450 kills   [display 666]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>450 Kills - Imperial Age')

    # --- #512  450 kills   [display 685]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>450 Kills - Imperial Age')

    # --- #513  450 kills   [display 704]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>450 Kills - Imperial Age')

    # --- #514  450 kills   [display 723]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>450 Kills - Imperial Age')

    # --- #515  450 kills   [display 742]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>450 Kills - Imperial Age')

    # --- #516  450 kills   [display 761]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>450 Kills - Imperial Age')

    # --- #517  450 kills   [display 780]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>450 Kills - Imperial Age')

    # --- #518  350 kills   [display 667]
    t = tm.add_trigger('350 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=350, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>350 Kills - Imperial Age')
    t.new_effect.deactivate_trigger(trigger_id=681)

    # --- #519  350 kills   [display 686]
    t = tm.add_trigger('350 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=350, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>350 Kills - Imperial Age')
    t.new_effect.deactivate_trigger(trigger_id=682)

    # --- #520  350 kills   [display 705]
    t = tm.add_trigger('350 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=350, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>350 Kills - Imperial Age')
    t.new_effect.deactivate_trigger(trigger_id=683)

    # --- #521  350 kills   [display 724]
    t = tm.add_trigger('350 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=350, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>350 Kills - Imperial Age')
    t.new_effect.deactivate_trigger(trigger_id=684)

    # --- #522  350 kills   [display 743]
    t = tm.add_trigger('350 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=350, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>350 Kills - Imperial Age')
    t.new_effect.deactivate_trigger(trigger_id=685)

    # --- #523  350 kills   [display 762]
    t = tm.add_trigger('350 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=350, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>350 Kills - Imperial Age')
    t.new_effect.deactivate_trigger(trigger_id=686)

    # --- #524  350 kills   [display 781]
    t = tm.add_trigger('350 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=350, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>350 Kills - Imperial Age')
    t.new_effect.deactivate_trigger(trigger_id=687)

    # --- #525  400 kills   [display 668]
    t = tm.add_trigger('400 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=400, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>400 Kills - Imperial Age')

    # --- #526  400 kills   [display 687]
    t = tm.add_trigger('400 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=400, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>400 Kills - Imperial Age')

    # --- #527  400 kills   [display 706]
    t = tm.add_trigger('400 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=400, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>400 Kills - Imperial Age')

    # --- #528  400 kills   [display 725]
    t = tm.add_trigger('400 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=400, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>400 Kills - Imperial Age')

    # --- #529  400 kills   [display 744]
    t = tm.add_trigger('400 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=400, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>400 Kills - Imperial Age')

    # --- #530  400 kills   [display 763]
    t = tm.add_trigger('400 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=400, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>400 Kills - Imperial Age')

    # --- #531  400 kills   [display 782]
    t = tm.add_trigger('400 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=400, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>400 Kills - Imperial Age')

    # --- #532  500 kills   [display 669]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>500 Kills - Imperial Age')

    # --- #533  500 kills   [display 688]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>500 Kills - Imperial Age')

    # --- #534  500 kills   [display 707]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>500 Kills - Imperial Age')

    # --- #535  500 kills   [display 726]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>500 Kills - Imperial Age')

    # --- #536  500 kills   [display 745]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>500 Kills - Imperial Age')

    # --- #537  500 kills   [display 764]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>500 Kills - Imperial Age')

    # --- #538  500 kills   [display 783]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>500 Kills - Imperial Age')

    # --- #539  600 kills   [display 670]
    t = tm.add_trigger('600 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=600, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>600 Kills - Imperial Age')

    # --- #540  600 kills   [display 689]
    t = tm.add_trigger('600 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=600, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>600 Kills - Imperial Age')

    # --- #541  600 kills   [display 708]
    t = tm.add_trigger('600 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=600, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>600 Kills - Imperial Age')

    # --- #542  600 kills   [display 727]
    t = tm.add_trigger('600 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=600, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>600 Kills - Imperial Age')

    # --- #543  600 kills   [display 746]
    t = tm.add_trigger('600 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=600, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>600 Kills - Imperial Age')

    # --- #544  600 kills   [display 765]
    t = tm.add_trigger('600 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=600, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>600 Kills - Imperial Age')

    # --- #545  600 kills   [display 784]
    t = tm.add_trigger('600 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=600, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>600 Kills - Imperial Age')

    # --- #546  450 kills   [display 671]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>450 Kills - Imperial Age')

    # --- #547  450 kills   [display 690]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>450 Kills - Imperial Age')

    # --- #548  450 kills   [display 709]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>450 Kills - Imperial Age')

    # --- #549  450 kills   [display 728]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>450 Kills - Imperial Age')

    # --- #550  450 kills   [display 747]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>450 Kills - Imperial Age')

    # --- #551  450 kills   [display 766]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>450 Kills - Imperial Age')

    # --- #552  450 kills   [display 785]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>450 Kills - Imperial Age')

    # --- #553  650 kills   [display 672]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>650 Kills - Imperial Age')

    # --- #554  650 kills   [display 691]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>650 Kills - Imperial Age')

    # --- #555  650 kills   [display 710]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>650 Kills - Imperial Age')

    # --- #556  650 kills   [display 729]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>650 Kills - Imperial Age')

    # --- #557  650 kills   [display 748]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>650 Kills - Imperial Age')

    # --- #558  650 kills   [display 767]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>650 Kills - Imperial Age')

    # --- #559  650 kills   [display 786]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>650 Kills - Imperial Age')

    # --- #560  750 kills   [display 673]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>750 Kills - Imperial Age')

    # --- #561  750 kills   [display 692]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>750 Kills - Imperial Age')

    # --- #562  750 kills   [display 711]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>750 Kills - Imperial Age')

    # --- #563  750 kills   [display 730]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>750 Kills - Imperial Age')

    # --- #564  750 kills   [display 749]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>750 Kills - Imperial Age')

    # --- #565  750 kills   [display 768]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN)
    t.new_effect.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.IMPERIAL_AGE.ID)
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>750 Kills - Imperial Age')

    # --- #566  750 kills   [display 787]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>750 Kills - Imperial Age')

    # --- #567  650 kills   [display 674]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>650 Kills - Imperial Age')

    # --- #568  650 kills   [display 693]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>650 Kills - Imperial Age')

    # --- #569  650 kills   [display 712]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>650 Kills - Imperial Age')

    # --- #570  650 kills   [display 731]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>650 Kills - Imperial Age')

    # --- #571  650 kills   [display 750]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>650 Kills - Imperial Age')

    # --- #572  650 kills   [display 769]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>650 Kills - Imperial Age')

    # --- #573  750 kills   [display 675]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>750 Kills - Imperial Age')

    # --- #574  750 kills   [display 694]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>750 Kills - Imperial Age')

    # --- #575  750 kills   [display 713]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>750 Kills - Imperial Age')

    # --- #576  750 kills   [display 732]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>750 Kills - Imperial Age')

    # --- #577  750 kills   [display 751]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>750 Kills - Imperial Age')

    # --- #578  750 kills   [display 770]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>750 Kills - Imperial Age')

    # --- #579  750 kills   [display 789]
    t = tm.add_trigger('750 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=750, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>750 Kills - Imperial Age')

    # --- #580  450 kills   [display 676]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>450 Kills - Imperial Age')

    # --- #581  450 kills   [display 695]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>450 Kills - Imperial Age')

    # --- #582  450 kills   [display 714]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>450 Kills - Imperial Age')

    # --- #583  450 kills   [display 733]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>450 Kills - Imperial Age')

    # --- #584  450 kills   [display 752]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>450 Kills - Imperial Age')

    # --- #585  450 kills   [display 771]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>450 Kills - Imperial Age')

    # --- #586  450 kills   [display 790]
    t = tm.add_trigger('450 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=450, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>450 Kills - Imperial Age')

    # --- #587  700 kills   [display 677]
    t = tm.add_trigger('700 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=700, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>700 Kills - Imperial Age')

    # --- #588  700 kills   [display 696]
    t = tm.add_trigger('700 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=700, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>700 Kills - Imperial Age')

    # --- #589  700 kills   [display 715]
    t = tm.add_trigger('700 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=700, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>700 Kills - Imperial Age')

    # --- #590  700 kills   [display 734]
    t = tm.add_trigger('700 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=700, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>700 Kills - Imperial Age')

    # --- #591  700 kills   [display 753]
    t = tm.add_trigger('700 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=700, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>700 Kills - Imperial Age')

    # --- #592  700 kills   [display 772]
    t = tm.add_trigger('700 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=700, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>700 Kills - Imperial Age')

    # --- #593  500 kills   [display 678]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>500 Kills - Imperial Age')

    # --- #594  500 kills   [display 697]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>500 Kills - Imperial Age')

    # --- #595  500 kills   [display 716]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>500 Kills - Imperial Age')

    # --- #596  500 kills   [display 735]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>500 Kills - Imperial Age')

    # --- #597  500 kills   [display 754]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>500 Kills - Imperial Age')

    # --- #598  500 kills   [display 773]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>500 Kills - Imperial Age')

    # --- #599  500 kills   [display 792]
    t = tm.add_trigger('500 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=500, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>500 Kills - Imperial Age')

    # --- #600  700 kills   [display 791]
    t = tm.add_trigger('700 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=700, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>700 Kills - Imperial Age')

    # --- #601  650 kills   [display 788]
    t = tm.add_trigger('650 kills', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=650, attribute=Attribute.UNITS_KILLED, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IMPERIAL_AGE.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>650 Kills - Imperial Age')

    # --- #602  ==Reasearch============   [display 793]
    t = tm.add_trigger('==Reasearch============', description_stid=0)

    # --- #603  Research Cartography   [display 794]
    t = tm.add_trigger('Research Cartography', description_stid=0, short_description_stid=0)
    t.new_effect.research_technology(technology=TechInfo.CARTOGRAPHY.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.TWO, technology=TechInfo.CARTOGRAPHY.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.CARTOGRAPHY.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.CARTOGRAPHY.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.CARTOGRAPHY.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.SIX, technology=TechInfo.CARTOGRAPHY.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.CARTOGRAPHY.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.CARTOGRAPHY.ID,
        force_research_technology=-1,
    )

    # --- #604  Research Walls   [display 795]
    t = tm.add_trigger('Research Walls', description_stid=0, short_description_stid=0)
    t.new_effect.research_technology(technology=TechInfo.FORTIFIED_WALL.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.FORTIFIED_WALL.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.FORTIFIED_WALL.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.FORTIFIED_WALL.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.FORTIFIED_WALL.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.FORTIFIED_WALL.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.FORTIFIED_WALL.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.FORTIFIED_WALL.ID,
        force_research_technology=-1,
    )

    # --- #605  ==Hay=================   [display 796]
    t = tm.add_trigger('==Hay=================', description_stid=0)

    # --- #606  hay1 (p1)   [display 797]
    t = tm.add_trigger('hay1 (p1)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=9761, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=48,
        location_y=22,
        disable_sound=-1,
    )

    # --- #607  hay2 (p1)   [display 798]
    t = tm.add_trigger('hay2 (p1)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22013, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=52,
        location_y=22,
        disable_sound=-1,
    )

    # --- #608  hay3 (p1)   [display 799]
    t = tm.add_trigger('hay3 (p1)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22014, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=55,
        location_y=22,
        disable_sound=-1,
    )

    # --- #609  hay4 (p1)   [display 800]
    t = tm.add_trigger('hay4 (p1)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22015, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=59,
        location_y=22,
        disable_sound=-1,
    )

    # --- #610  hay1 (p2)   [display 801]
    t = tm.add_trigger('hay1 (p2)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=78945, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=81,
        location_y=22,
        disable_sound=-1,
    )

    # --- #611  hay2 (p2)   [display 802]
    t = tm.add_trigger('hay2 (p2)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=78946, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=85,
        location_y=22,
        disable_sound=-1,
    )

    # --- #612  hay3 (p2)   [display 803]
    t = tm.add_trigger('hay3 (p2)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=78947, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=88,
        location_y=22,
        disable_sound=-1,
    )

    # --- #613  hay4 (p2)   [display 804]
    t = tm.add_trigger('hay4 (p2)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=78948, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=92,
        location_y=22,
        disable_sound=-1,
    )

    # --- #614  hay1 (p3)   [display 805]
    t = tm.add_trigger('hay1 (p3)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35044, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=59,
        disable_sound=-1,
    )

    # --- #615  hay2 (p3)   [display 806]
    t = tm.add_trigger('hay2 (p3)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35045, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=55,
        disable_sound=-1,
    )

    # --- #616  hay3 (p3)   [display 807]
    t = tm.add_trigger('hay3 (p3)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35046, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=52,
        disable_sound=-1,
    )

    # --- #617  hay4 (p3)   [display 808]
    t = tm.add_trigger('hay4 (p3)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35043, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=48,
        disable_sound=-1,
    )

    # --- #618  hay1 (p4)   [display 809]
    t = tm.add_trigger('hay1 (p4)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22019, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=48,
        disable_sound=-1,
    )

    # --- #619  hay2 (p4)   [display 810]
    t = tm.add_trigger('hay2 (p4)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22020, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=52,
        disable_sound=-1,
    )

    # --- #620  hay3 (p4)   [display 811]
    t = tm.add_trigger('hay3 (p4)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22021, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=55,
        disable_sound=-1,
    )

    # --- #621  hay4 (p4)   [display 812]
    t = tm.add_trigger('hay4 (p4)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22022, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=59,
        disable_sound=-1,
    )

    # --- #622  hay1 (p5)   [display 813]
    t = tm.add_trigger('hay1 (p5)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35050, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=81,
        disable_sound=-1,
    )

    # --- #623  hay2 (p5)   [display 814]
    t = tm.add_trigger('hay2 (p5)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35049, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=85,
        disable_sound=-1,
    )

    # --- #624  hay3 (p5)   [display 815]
    t = tm.add_trigger('hay3 (p5)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35048, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=88,
        disable_sound=-1,
    )

    # --- #625  hay4 (p5)   [display 816]
    t = tm.add_trigger('hay4 (p5)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35047, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=21,
        location_y=92,
        disable_sound=-1,
    )

    # --- #626  hay1 (p6)   [display 817]
    t = tm.add_trigger('hay1 (p6)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22023, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=81,
        disable_sound=-1,
    )

    # --- #627  hay2 (p6)   [display 818]
    t = tm.add_trigger('hay2 (p6)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22024, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=85,
        disable_sound=-1,
    )

    # --- #628  hay3 (p6)   [display 819]
    t = tm.add_trigger('hay3 (p6)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22025, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=88,
        disable_sound=-1,
    )

    # --- #629  hay4 (p6)   [display 820]
    t = tm.add_trigger('hay4 (p6)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=22026, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=119,
        location_y=92,
        disable_sound=-1,
    )

    # --- #630  hay1 (p7)   [display 821]
    t = tm.add_trigger('hay1 (p7)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=79333, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=48,
        location_y=119,
        disable_sound=-1,
    )

    # --- #631  hay2 (p7)   [display 822]
    t = tm.add_trigger('hay2 (p7)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=79334, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=52,
        location_y=119,
        disable_sound=-1,
    )

    # --- #632  hay3 (p7)   [display 823]
    t = tm.add_trigger('hay3 (p7)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=79335, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=55,
        location_y=119,
        disable_sound=-1,
    )

    # --- #633  hay4 (p7)   [display 824]
    t = tm.add_trigger('hay4 (p7)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=79336, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=59,
        location_y=119,
        disable_sound=-1,
    )

    # --- #634  hay1 (p8)   [display 825]
    t = tm.add_trigger('hay1 (p8)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35057, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=81,
        location_y=119,
        disable_sound=-1,
    )

    # --- #635  hay2 (p8)   [display 826]
    t = tm.add_trigger('hay2 (p8)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35055, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=85,
        location_y=119,
        disable_sound=-1,
    )

    # --- #636  hay3 (p8)   [display 827]
    t = tm.add_trigger('hay3 (p8)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35056, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=88,
        location_y=119,
        disable_sound=-1,
    )

    # --- #637  hay4 (p8)   [display 828]
    t = tm.add_trigger('hay4 (p8)', description_stid=0, looping=1)
    t.new_condition.destroy_object(unit_object=35058, inverted=-1)
    t.new_effect.create_object(
        object_list_unit_id=OtherInfo.HAY_STACK.ID,
        source_player=PlayerId.GAIA,
        location_x=92,
        location_y=119,
        disable_sound=-1,
    )

    # --- #638  =KILLSP1================   [display 829]
    t = tm.add_trigger('=KILLSP1================', description_stid=0)

    # --- #639  =KILLSP2================   [display 830]
    t = tm.add_trigger('=KILLSP2================', description_stid=0)

    # --- #640  =KILLSP3================   [display 831]
    t = tm.add_trigger('=KILLSP3================', description_stid=0)

    # --- #641  =KILLSP4================   [display 832]
    t = tm.add_trigger('=KILLSP4================', description_stid=0)

    # --- #642  =KILLSP5================   [display 833]
    t = tm.add_trigger('=KILLSP5================', description_stid=0)

    # --- #643  =KILLSP6================   [display 834]
    t = tm.add_trigger('=KILLSP6================', description_stid=0)

    # --- #644  =KILLSP7================   [display 835]
    t = tm.add_trigger('=KILLSP7================', description_stid=0)

    # --- #645  =KILLSP8================   [display 836]
    t = tm.add_trigger('=KILLSP8================', description_stid=0)

    # --- #646  ====Defeated===   [display 837]
    t = tm.add_trigger('====Defeated===', description_stid=0)

    # --- #647  remove (p1)   [display 838]
    t = tm.add_trigger('remove (p1)', description_stid=0)
    t.new_condition.player_defeated(inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID)

    # --- #648  remove (p2)   [display 839]
    t = tm.add_trigger('remove (p2)', description_stid=0)
    t.new_condition.player_defeated(source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID, source_player=PlayerId.TWO)

    # --- #649  remove (p3)   [display 840]
    t = tm.add_trigger('remove (p3)', description_stid=0)
    t.new_condition.player_defeated(source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID, source_player=PlayerId.THREE, object_state=-1)

    # --- #650  remove (p4)   [display 841]
    t = tm.add_trigger('remove (p4)', description_stid=0)
    t.new_condition.player_defeated(source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID, source_player=PlayerId.FOUR, object_state=-1)

    # --- #651  remove (p5)   [display 842]
    t = tm.add_trigger('remove (p5)', description_stid=0)
    t.new_condition.player_defeated(source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID, source_player=PlayerId.FIVE, object_state=-1)

    # --- #652  remove (p6)   [display 843]
    t = tm.add_trigger('remove (p6)', description_stid=0)
    t.new_condition.player_defeated(source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID, source_player=PlayerId.SIX, object_state=-1)

    # --- #653  remove (p7)   [display 844]
    t = tm.add_trigger('remove (p7)', description_stid=0)
    t.new_condition.player_defeated(source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID, source_player=PlayerId.SEVEN, object_state=-1)

    # --- #654  remove (p8)   [display 845]
    t = tm.add_trigger('remove (p8)', description_stid=0)
    t.new_condition.player_defeated(source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.remove_object(object_list_unit_id=BuildingInfo.CASTLE.ID, source_player=PlayerId.EIGHT, object_state=-1)

    # --- #655  ==Rename==   [display 846]
    t = tm.add_trigger('==Rename==', description_stid=0)
    t.new_effect.change_object_name(message='Look at my +attack for raze count!', selected_object_ids=[48430])
    t.new_effect.change_object_name(message='Look at my +attack for raze count!', selected_object_ids=[48431])
    t.new_effect.change_object_name(source_player=-1, message='Look at my +attack for raze count!', selected_object_ids=[48437])
    t.new_effect.change_object_name(message='Look at my +attack for raze count!', selected_object_ids=[48432])
    t.new_effect.change_object_name(message='Look at my +attack for raze count!', selected_object_ids=[48433])
    t.new_effect.change_object_name(message='Look at my +attack for raze count!', selected_object_ids=[48434])
    t.new_effect.change_object_name(message='Look at my +attack for raze count!', selected_object_ids=[48435])
    t.new_effect.change_object_name(source_player=-1, message='Look at my +attack for raze count!', selected_object_ids=[48436])
    t.new_effect.change_ownership(target_player=PlayerId.GAIA, selected_object_ids=[48430])
    t.new_effect.change_ownership(source_player=PlayerId.TWO, target_player=PlayerId.GAIA, selected_object_ids=[48431])
    t.new_effect.change_ownership(source_player=PlayerId.THREE, target_player=PlayerId.GAIA, selected_object_ids=[48437])
    t.new_effect.change_ownership(source_player=PlayerId.FOUR, target_player=PlayerId.GAIA, selected_object_ids=[48432])
    t.new_effect.change_ownership(source_player=PlayerId.FIVE, target_player=PlayerId.GAIA, selected_object_ids=[48433])
    t.new_effect.change_ownership(source_player=PlayerId.SIX, target_player=PlayerId.GAIA, selected_object_ids=[48434])
    t.new_effect.change_ownership(source_player=PlayerId.SEVEN, target_player=PlayerId.GAIA, selected_object_ids=[48435])
    t.new_effect.change_ownership(
        source_player=PlayerId.EIGHT,
        target_player=PlayerId.GAIA,
        flash_object=-1,
        selected_object_ids=[48436],
    )

    # --- #656  feudal ups (p1)   [display 848]
    t = tm.add_trigger('feudal ups (p1)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        area_x1=49,
        area_y1=1,
        area_x2=57,
        area_y2=6,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(technology=TechInfo.PADDED_ARCHER_ARMOR.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.SCALE_BARDING_ARMOR.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.SCALE_MAIL_ARMOR.ID, force_research_technology=-1)
    t.new_effect.send_chat(message='<BLUE>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #657  feudal ups (p2)   [display 849]
    t = tm.add_trigger('feudal ups (p2)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        source_player=PlayerId.TWO,
        area_x1=84,
        area_y1=1,
        area_x2=92,
        area_y2=6,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.PADDED_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.TWO, technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.TWO, technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.SCALE_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.SCALE_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(source_player=PlayerId.TWO, technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(source_player=PlayerId.TWO, technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(source_player=PlayerId.TWO, technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #658  feudal ups (p3)   [display 850]
    t = tm.add_trigger('feudal ups (p3)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        source_player=PlayerId.THREE,
        area_x1=1,
        area_y1=50,
        area_x2=6,
        area_y2=58,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.PADDED_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.THREE, technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.THREE, technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.SCALE_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.SCALE_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(source_player=PlayerId.THREE, technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(source_player=PlayerId.THREE, technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(source_player=PlayerId.THREE, technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #659  feudal ups (p4)   [display 851]
    t = tm.add_trigger('feudal ups (p4)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        source_player=PlayerId.FOUR,
        area_x1=137,
        area_y1=49,
        area_x2=142,
        area_y2=57,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.PADDED_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.SCALE_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.SCALE_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #660  feudal ups (p5)   [display 852]
    t = tm.add_trigger('feudal ups (p5)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        source_player=PlayerId.FIVE,
        area_x1=1,
        area_y1=83,
        area_x2=6,
        area_y2=91,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.PADDED_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.SCALE_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.SCALE_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #661  feudal ups (p6)   [display 853]
    t = tm.add_trigger('feudal ups (p6)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        source_player=PlayerId.SIX,
        area_x1=137,
        area_y1=82,
        area_x2=142,
        area_y2=90,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.PADDED_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.SIX, technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.SIX, technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.SCALE_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.SCALE_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(source_player=PlayerId.SIX, technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(source_player=PlayerId.SIX, technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(source_player=PlayerId.SIX, technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #662  feudal ups (p7)   [display 854]
    t = tm.add_trigger('feudal ups (p7)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        source_player=PlayerId.SEVEN,
        area_x1=47,
        area_y1=137,
        area_x2=55,
        area_y2=142,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.PADDED_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.SCALE_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.SCALE_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #663  feudal ups (p8)   [display 855]
    t = tm.add_trigger('feudal ups (p8)', description_stid=0)
    t.new_condition.timer(timer=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=103,
        source_player=PlayerId.EIGHT,
        area_x1=80,
        area_y1=137,
        area_x2=88,
        area_y2=142,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.PADDED_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.FLETCHING.ID, force_research_technology=-1)
    t.new_effect.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.FORGING.ID, force_research_technology=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.SCALE_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.SCALE_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>Feudal Age Upgrades Researched')
    t.new_effect.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.ELITE_TIGER_CAVALRY.ID)
    t.new_effect.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.ELITE_IMMORTAL.ID)
    t.new_effect.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.ELITE_STRATEGOS.ID)

    # --- #664  tc (p1)   [display 856]
    t = tm.add_trigger('tc (p1)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )

    # --- #665  tc (p2)   [display 857]
    t = tm.add_trigger('tc (p2)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        source_player=PlayerId.TWO,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=PlayerId.TWO,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        object_state=-1,
    )

    # --- #666  tc (p3)   [display 858]
    t = tm.add_trigger('tc (p3)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        source_player=PlayerId.THREE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=PlayerId.THREE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        object_state=-1,
    )

    # --- #667  tc (p4)   [display 859]
    t = tm.add_trigger('tc (p4)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        source_player=PlayerId.FOUR,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=PlayerId.FOUR,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )

    # --- #668  tc (p5)   [display 860]
    t = tm.add_trigger('tc (p5)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        source_player=PlayerId.FIVE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=PlayerId.FIVE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        object_state=-1,
    )

    # --- #669  tc (p6)   [display 861]
    t = tm.add_trigger('tc (p6)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        source_player=PlayerId.SIX,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=PlayerId.SIX,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        object_state=-1,
    )

    # --- #670  tc (p7)   [display 862]
    t = tm.add_trigger('tc (p7)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        source_player=PlayerId.SEVEN,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=PlayerId.SEVEN,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        object_state=-1,
    )

    # --- #671  tc (p8)   [display 863]
    t = tm.add_trigger('tc (p8)', description_stid=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=109,
        source_player=PlayerId.EIGHT,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.remove_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=PlayerId.EIGHT,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        object_state=-1,
    )

    # --- #672  castle ups (p1)   [display 864]
    t = tm.add_trigger('castle ups (p1)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(technology=TechInfo.CHAIN_BARDING_ARMOR.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.CHAIN_MAIL_ARMOR.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.IRON_CASTING.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.BODKIN_ARROW.ID, force_research_technology=-1)
    t.new_effect.research_technology(technology=TechInfo.LEATHER_ARCHER_ARMOR.ID, force_research_technology=-1)
    t.new_effect.send_chat(message='<BLUE>Castle Age Upgrades Researched')

    # --- #673  castle ups (p2)   [display 865]
    t = tm.add_trigger('castle ups (p2)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.CHAIN_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.CHAIN_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.IRON_CASTING.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.BODKIN_ARROW.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.TWO,
        technology=TechInfo.LEATHER_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='<RED>Castle Age Upgrades Researched')

    # --- #674  castle ups (p3)   [display 866]
    t = tm.add_trigger('castle ups (p3)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.CHAIN_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.CHAIN_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.IRON_CASTING.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.BODKIN_ARROW.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.THREE,
        technology=TechInfo.LEATHER_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='<GREEN>Castle Age Upgrades Researched')

    # --- #675  castle ups (p4)   [display 867]
    t = tm.add_trigger('castle ups (p4)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.CHAIN_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.CHAIN_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.IRON_CASTING.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.BODKIN_ARROW.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FOUR,
        technology=TechInfo.LEATHER_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='<YELLOW>Castle Age Upgrades Researched')

    # --- #676  castle ups (p5)   [display 868]
    t = tm.add_trigger('castle ups (p5)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.CHAIN_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.CHAIN_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.IRON_CASTING.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.BODKIN_ARROW.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.FIVE,
        technology=TechInfo.LEATHER_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='<AQUA>Castle Age Upgrades Researched')

    # --- #677  castle ups (p6)   [display 869]
    t = tm.add_trigger('castle ups (p6)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.CHAIN_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.CHAIN_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.IRON_CASTING.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.BODKIN_ARROW.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SIX,
        technology=TechInfo.LEATHER_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='<PURPLE>Castle Age Upgrades Researched')

    # --- #678  castle ups (p7)   [display 870]
    t = tm.add_trigger('castle ups (p7)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.CHAIN_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.CHAIN_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.IRON_CASTING.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.BODKIN_ARROW.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.SEVEN,
        technology=TechInfo.LEATHER_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='<GREY>Castle Age Upgrades Researched')

    # --- #679  castle ups (p8)   [display 871]
    t = tm.add_trigger('castle ups (p8)', description_stid=0, enabled=0)
    t.new_condition.timer(timer=8, inverted=-1)
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.CHAIN_BARDING_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.CHAIN_MAIL_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.IRON_CASTING.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.BODKIN_ARROW.ID,
        force_research_technology=-1,
    )
    t.new_effect.research_technology(
        source_player=PlayerId.EIGHT,
        technology=TechInfo.LEATHER_ARCHER_ARMOR.ID,
        force_research_technology=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='<ORANGE>Castle Age Upgrades Researched')

    # --- #680  goth barracks (p1)   [display 872]
    t = tm.add_trigger('goth barracks (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(object_list_unit_id=BuildingInfo.BARRACKS.ID, area_x1=0, area_y1=0, area_x2=143, area_y2=143)
    t.new_effect.send_chat(message="<BLUE> Goth's cannot make Barracks until Imperial Age!")

    # --- #681  goth barracks (p2)   [display 873]
    t = tm.add_trigger('goth barracks (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        source_player=PlayerId.TWO,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.BARRACKS.ID,
        source_player=PlayerId.TWO,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message="<RED> Goth's cannot make Barracks until Imperial Age!")

    # --- #682  goth barracks (p3)   [display 874]
    t = tm.add_trigger('goth barracks (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        source_player=PlayerId.THREE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.BARRACKS.ID,
        source_player=PlayerId.THREE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.send_chat(
        source_player=PlayerId.THREE,
        message="<GREEN> Goth's cannot make Barracks until Imperial Age!",
    )

    # --- #683  goth barracks (p4)   [display 875]
    t = tm.add_trigger('goth barracks (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        source_player=PlayerId.FOUR,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.BARRACKS.ID,
        source_player=PlayerId.FOUR,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.send_chat(
        source_player=PlayerId.FOUR,
        message="<YELLOW> Goth's cannot make Barracks until Imperial Age!",
    )

    # --- #684  goth barracks (p5)   [display 876]
    t = tm.add_trigger('goth barracks (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        source_player=PlayerId.FIVE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.BARRACKS.ID,
        source_player=PlayerId.FIVE,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.send_chat(
        source_player=PlayerId.FIVE,
        message="<AQUA> Goth's cannot make Barracks until Imperial Age!",
    )

    # --- #685  goth barracks (p6)   [display 877]
    t = tm.add_trigger('goth barracks (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        source_player=PlayerId.SIX,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.BARRACKS.ID,
        source_player=PlayerId.SIX,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.send_chat(
        source_player=PlayerId.SIX,
        message="<PURPLE> Goth's cannot make Barracks until Imperial Age!",
    )

    # --- #686  goth barracks (p7)   [display 878]
    t = tm.add_trigger('goth barracks (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        source_player=PlayerId.SEVEN,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.BARRACKS.ID,
        source_player=PlayerId.SEVEN,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.send_chat(
        source_player=PlayerId.SEVEN,
        message="<GREY> Goth's cannot make Barracks until Imperial Age!",
    )

    # --- #687  goth barracks (p8)   [display 879]
    t = tm.add_trigger('goth barracks (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.objects_in_area(
        quantity=1,
        object_list=12,
        source_player=PlayerId.EIGHT,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
        inverted=-1,
        object_state=-1,
        include_changeable_weapon_objects=-1,
    )
    t.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.BARRACKS.ID,
        source_player=PlayerId.EIGHT,
        area_x1=0,
        area_y1=0,
        area_x2=143,
        area_y2=143,
    )
    t.new_effect.send_chat(
        source_player=PlayerId.EIGHT,
        message="<ORANGE> Goth's cannot make Barracks until Imperial Age!",
    )

    # --- #688  goth anarchy (p1)   [display 880]
    t = tm.add_trigger('goth anarchy (p1)', description_stid=0)
    t.new_condition.research_technology(inverted=-1)
    t.new_effect.activate_trigger(trigger_id=680)
    t.new_effect.send_chat(message='<BLUE>You have research Anarchy, No Barracks until Imperial Age')

    # --- #689  goth anarchy (p2)   [display 881]
    t = tm.add_trigger('goth anarchy (p2)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=681)
    t.new_effect.send_chat(
        source_player=PlayerId.TWO,
        message='<RED>You researched Anarchy, No Barracks until Imperial Age',
    )

    # --- #690  goth anarchy (p3)   [display 882]
    t = tm.add_trigger('goth anarchy (p3)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=682)
    t.new_effect.send_chat(
        source_player=PlayerId.THREE,
        message='<GREEN>You researched Anarchy, No Barracks until Imperial Age',
    )

    # --- #691  goth anarchy (p4)   [display 883]
    t = tm.add_trigger('goth anarchy (p4)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=683)
    t.new_effect.send_chat(
        source_player=PlayerId.FOUR,
        message='<YELLOW>You researched Anarchy, No Barracks until Imperial Age',
    )

    # --- #692  goth anarchy (p5)   [display 884]
    t = tm.add_trigger('goth anarchy (p5)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=684)
    t.new_effect.send_chat(
        source_player=PlayerId.FIVE,
        message='<AQUA>You researched Anarchy, No Barracks until Imperial Age',
    )

    # --- #693  goth anarchy (p6)   [display 885]
    t = tm.add_trigger('goth anarchy (p6)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=685)
    t.new_effect.send_chat(
        source_player=PlayerId.SIX,
        message='<PURPLE>You researched Anarchy, No Barracks until Imperial Age',
    )

    # --- #694  goth anarchy (p7)   [display 886]
    t = tm.add_trigger('goth anarchy (p7)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=686)
    t.new_effect.send_chat(
        source_player=PlayerId.SEVEN,
        message='<GREY>You researched Anarchy, No Barracks until Imperial Age',
    )

    # --- #695  goth anarchy (p8)   [display 887]
    t = tm.add_trigger('goth anarchy (p8)', description_stid=0)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.activate_trigger(trigger_id=687)
    t.new_effect.send_chat(
        source_player=PlayerId.EIGHT,
        message='<ORANGE>You researched Anarchy, No Barracks until Imperial Age',
    )

    # --- #696  goth imp (p1)   [display 888]
    t = tm.add_trigger('goth imp (p1)', description_stid=0, looping=1)
    t.new_condition.research_technology(technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=688)
    t.new_effect.deactivate_trigger(trigger_id=680)

    # --- #697  goth imp (p2)   [display 889]
    t = tm.add_trigger('goth imp (p2)', description_stid=0, looping=1)
    t.new_condition.research_technology(source_player=PlayerId.TWO, technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=689)
    t.new_effect.deactivate_trigger(trigger_id=681)

    # --- #698  goth imp (p3)   [display 890]
    t = tm.add_trigger('goth imp (p3)', description_stid=0, looping=1)
    t.new_condition.research_technology(source_player=PlayerId.THREE, technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=690)
    t.new_effect.deactivate_trigger(trigger_id=682)

    # --- #699  goth imp (p4)   [display 891]
    t = tm.add_trigger('goth imp (p4)', description_stid=0, looping=1)
    t.new_condition.research_technology(source_player=PlayerId.FOUR, technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=691)
    t.new_effect.deactivate_trigger(trigger_id=683)

    # --- #700  goth imp (p5)   [display 892]
    t = tm.add_trigger('goth imp (p5)', description_stid=0, looping=1)
    t.new_condition.research_technology(source_player=PlayerId.FIVE, technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=692)
    t.new_effect.deactivate_trigger(trigger_id=684)

    # --- #701  goth imp (p6)   [display 893]
    t = tm.add_trigger('goth imp (p6)', description_stid=0, looping=1)
    t.new_condition.research_technology(source_player=PlayerId.SIX, technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=693)
    t.new_effect.deactivate_trigger(trigger_id=685)

    # --- #702  goth imp (p7)   [display 894]
    t = tm.add_trigger('goth imp (p7)', description_stid=0, looping=1)
    t.new_condition.research_technology(source_player=PlayerId.SEVEN, technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=694)
    t.new_effect.deactivate_trigger(trigger_id=686)

    # --- #703  goth imp (p8)   [display 895]
    t = tm.add_trigger('goth imp (p8)', description_stid=0, looping=1)
    t.new_condition.research_technology(source_player=PlayerId.EIGHT, technology=TechInfo.IMPERIAL_AGE.ID, inverted=-1)
    t.new_effect.deactivate_trigger(trigger_id=695)
    t.new_effect.deactivate_trigger(trigger_id=687)

    # --- #704  ==Razings======   [display 896]
    t = tm.add_trigger('==Razings======', description_stid=0, enabled=0)

    # --- #705  5 razes (p1)   [display 897]
    t = tm.add_trigger('5 razes (p1)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=1,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48430])
    t.new_effect.activate_trigger(trigger_id=713)

    # --- #706  5 razes (p2)   [display 898]
    t = tm.add_trigger('5 razes (p2)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.TWO, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=3,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48431])
    t.new_effect.activate_trigger(trigger_id=714)

    # --- #707  5 razes (p3)   [display 899]
    t = tm.add_trigger('5 razes (p3)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.THREE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=5,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48437])
    t.new_effect.activate_trigger(trigger_id=715)

    # --- #708  5 razes (p4)   [display 900]
    t = tm.add_trigger('5 razes (p4)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FOUR, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=7,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48432])
    t.new_effect.activate_trigger(trigger_id=716)

    # --- #709  5 razes (p5)   [display 901]
    t = tm.add_trigger('5 razes (p5)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FIVE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=9,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48433])
    t.new_effect.activate_trigger(trigger_id=717)

    # --- #710  5 razes (p6)   [display 902]
    t = tm.add_trigger('5 razes (p6)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SIX, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=11,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48434])
    t.new_effect.activate_trigger(trigger_id=718)

    # --- #711  5 razes (p7)   [display 903]
    t = tm.add_trigger('5 razes (p7)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SEVEN, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=13,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48435])
    t.new_effect.activate_trigger(trigger_id=719)

    # --- #712  5 razes (p8)   [display 904]
    t = tm.add_trigger('5 razes (p8)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.EIGHT, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=15,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48436])
    t.new_effect.activate_trigger(trigger_id=720)

    # --- #713  4 razes (p1)   [display 905]
    t = tm.add_trigger('4 razes (p1)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=1,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48430])
    t.new_effect.activate_trigger(trigger_id=721)

    # --- #714  4 razes (p2)   [display 906]
    t = tm.add_trigger('4 razes (p2)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.TWO, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=3,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48431])
    t.new_effect.activate_trigger(trigger_id=722)

    # --- #715  4 razes (p3)   [display 907]
    t = tm.add_trigger('4 razes (p3)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.THREE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=5,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48437])
    t.new_effect.activate_trigger(trigger_id=723)

    # --- #716  4 razes (p4)   [display 908]
    t = tm.add_trigger('4 razes (p4)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FOUR, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=7,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48432])
    t.new_effect.activate_trigger(trigger_id=724)

    # --- #717  4 razes (p5)   [display 909]
    t = tm.add_trigger('4 razes (p5)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FIVE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=9,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48433])
    t.new_effect.activate_trigger(trigger_id=725)

    # --- #718  4 razes (p6)   [display 910]
    t = tm.add_trigger('4 razes (p6)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SIX, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=11,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48434])
    t.new_effect.activate_trigger(trigger_id=726)

    # --- #719  4 razes (p7)   [display 911]
    t = tm.add_trigger('4 razes (p7)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SEVEN, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=13,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48435])
    t.new_effect.activate_trigger(trigger_id=727)

    # --- #720  4 razes (p8)   [display 912]
    t = tm.add_trigger('4 razes (p8)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.EIGHT, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=15,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48436])
    t.new_effect.activate_trigger(trigger_id=728)

    # --- #721  3 razes (p1)   [display 913]
    t = tm.add_trigger('3 razes (p1)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=1,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48430])
    t.new_effect.activate_trigger(trigger_id=729)

    # --- #722  3 razes (p2)   [display 914]
    t = tm.add_trigger('3 razes (p2)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.TWO, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=3,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48431])
    t.new_effect.activate_trigger(trigger_id=730)

    # --- #723  3 razes (p3)   [display 915]
    t = tm.add_trigger('3 razes (p3)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.THREE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=5,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48437])
    t.new_effect.activate_trigger(trigger_id=731)

    # --- #724  3 razes (p4)   [display 916]
    t = tm.add_trigger('3 razes (p4)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FOUR, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=7,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48432])
    t.new_effect.activate_trigger(trigger_id=732)

    # --- #725  3 razes (p5)   [display 917]
    t = tm.add_trigger('3 razes (p5)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FIVE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=9,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48433])
    t.new_effect.activate_trigger(trigger_id=733)

    # --- #726  3 razes (p6)   [display 918]
    t = tm.add_trigger('3 razes (p6)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SIX, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=11,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48434])
    t.new_effect.activate_trigger(trigger_id=734)

    # --- #727  3 razes (p7)   [display 919]
    t = tm.add_trigger('3 razes (p7)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SEVEN, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=13,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48435])
    t.new_effect.activate_trigger(trigger_id=735)

    # --- #728  3 razes (p8)   [display 920]
    t = tm.add_trigger('3 razes (p8)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.EIGHT, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=15,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48436])
    t.new_effect.activate_trigger(trigger_id=736)

    # --- #729  2 razes (p1)   [display 921]
    t = tm.add_trigger('2 razes (p1)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=1,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48430])
    t.new_effect.activate_trigger(trigger_id=737)

    # --- #730  2 razes (p2)   [display 922]
    t = tm.add_trigger('2 razes (p2)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.TWO, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=3,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48431])
    t.new_effect.activate_trigger(trigger_id=738)

    # --- #731  2 razes (p3)   [display 923]
    t = tm.add_trigger('2 razes (p3)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.THREE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=5,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48437])
    t.new_effect.activate_trigger(trigger_id=739)

    # --- #732  2 razes (p4)   [display 924]
    t = tm.add_trigger('2 razes (p4)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FOUR, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=7,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48432])
    t.new_effect.activate_trigger(trigger_id=740)

    # --- #733  2 razes (p5)   [display 925]
    t = tm.add_trigger('2 razes (p5)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FIVE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=9,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48433])
    t.new_effect.activate_trigger(trigger_id=741)

    # --- #734  2 razes (p6)   [display 926]
    t = tm.add_trigger('2 razes (p6)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SIX, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=11,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48434])
    t.new_effect.activate_trigger(trigger_id=742)

    # --- #735  2 razes (p7)   [display 927]
    t = tm.add_trigger('2 razes (p7)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SEVEN, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=13,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, selected_object_ids=[48435])
    t.new_effect.activate_trigger(trigger_id=743)

    # --- #736  2 razes (p8)   [display 928]
    t = tm.add_trigger('2 razes (p8)', description_stid=0, enabled=0)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.EIGHT, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=15,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, selected_object_ids=[48436])
    t.new_effect.activate_trigger(trigger_id=744)

    # --- #737  1 raze (p1)   [display 929]
    t = tm.add_trigger('1 raze (p1)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=1,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.send_chat(message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        location_x=40,
        location_y=23,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        location_x=40,
        location_y=24,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48430])

    # --- #738  1 raze (p2)   [display 930]
    t = tm.add_trigger('1 raze (p2)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.TWO, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.TWO, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=3,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        facet=0,
        disable_sound=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.TWO, message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=PlayerId.TWO,
        location_x=100,
        location_y=23,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=PlayerId.TWO,
        location_x=100,
        location_y=24,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48431])

    # --- #739  1 raze (p3)   [display 931]
    t = tm.add_trigger('1 raze (p3)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.THREE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.THREE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=5,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.THREE, message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=PlayerId.THREE,
        location_x=23,
        location_y=40,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=PlayerId.THREE,
        location_x=22,
        location_y=40,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48437])

    # --- #740  1 raze (p4)   [display 932]
    t = tm.add_trigger('1 raze (p4)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FOUR, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FOUR, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=7,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FOUR, message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=PlayerId.FOUR,
        location_x=118,
        location_y=40,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=PlayerId.FOUR,
        location_x=117,
        location_y=40,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48432])

    # --- #741  1 raze (p5)   [display 933]
    t = tm.add_trigger('1 raze (p5)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.FIVE, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.FIVE, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=9,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.FIVE, message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=PlayerId.FIVE,
        location_x=23,
        location_y=100,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=PlayerId.FIVE,
        location_x=22,
        location_y=100,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48433])

    # --- #742  1 raze (p6)   [display 934]
    t = tm.add_trigger('1 raze (p6)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SIX, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SIX, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=11,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SIX, message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=PlayerId.SIX,
        location_x=118,
        location_y=100,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=PlayerId.SIX,
        location_x=117,
        location_y=100,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48434])

    # --- #743  1 raze (p7)   [display 935]
    t = tm.add_trigger('1 raze (p7)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.SEVEN, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.SEVEN, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=13,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.SEVEN, message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=PlayerId.SEVEN,
        location_x=40,
        location_y=117,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=PlayerId.SEVEN,
        location_x=40,
        location_y=118,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, selected_object_ids=[48435])

    # --- #744  1 raze (p8)   [display 936]
    t = tm.add_trigger('1 raze (p8)', description_stid=0, enabled=0, looping=1)
    t.new_condition.accumulate_attribute(quantity=1, attribute=Attribute.RAZINGS, source_player=PlayerId.EIGHT, inverted=-1)
    t.new_effect.tribute(quantity=1, tribute_list=43, source_player=PlayerId.EIGHT, target_player=PlayerId.GAIA)
    t.new_effect.create_object(
        object_list_unit_id=162,
        source_player=PlayerId.GAIA,
        location_x=142,
        location_y=15,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.HAWK.ID,
        source_player=PlayerId.GAIA,
        location_x=4,
        location_y=143,
        disable_sound=-1,
    )
    t.new_effect.send_chat(source_player=PlayerId.EIGHT, message='Villager Created')
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=PlayerId.EIGHT,
        location_x=100,
        location_y=117,
        disable_sound=-1,
    )
    t.new_effect.create_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=PlayerId.EIGHT,
        location_x=100,
        location_y=118,
        disable_sound=-1,
    )
    t.new_effect.change_object_hp(quantity=1, source_player=PlayerId.GAIA, operation=-1, selected_object_ids=[48436])

    # --- #745  pop (p1)   [display 938]
    t = tm.add_trigger('pop (p1)', description_stid=0)
    t.new_effect.tribute(quantity=-195, tribute_list=4, target_player=PlayerId.GAIA)

    # --- #746  pop (p2)   [display 939]
    t = tm.add_trigger('pop (p2)', description_stid=0)
    t.new_effect.tribute(quantity=-195, tribute_list=4, source_player=PlayerId.TWO, target_player=PlayerId.GAIA)

    # --- #747  pop (p3)   [display 940]
    t = tm.add_trigger('pop (p3)', description_stid=0)
    t.new_effect.tribute(quantity=-195, tribute_list=4, source_player=PlayerId.THREE, target_player=PlayerId.GAIA)

    # --- #748  pop (p4)   [display 941]
    t = tm.add_trigger('pop (p4)', description_stid=0)
    t.new_effect.tribute(quantity=-195, tribute_list=4, source_player=PlayerId.FOUR, target_player=PlayerId.GAIA)

    # --- #749  pop (p5)   [display 942]
    t = tm.add_trigger('pop (p5)', description_stid=0)
    t.new_effect.tribute(quantity=-195, tribute_list=4, source_player=PlayerId.FIVE, target_player=PlayerId.GAIA)
