"""Group villagers together and keep the starting Genghis leader separate."""

import tomllib

from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, ObjectAttribute, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo

from .civilization_leaders import leader_unit_id, leaders_enabled


def _settings(ctx):
    settings = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())["selection"]
    groups = [settings[name] for name in ("villager_group", "genghis_army_group", "leader_group")]
    if any(type(group) is not int or not 1 <= group <= 254 for group in groups):
        raise ValueError("selection groups must be integers from 1 to 254")
    if len(set(groups)) != len(groups):
        raise ValueError("Villagers, army Genghis and starting leaders need distinct selection groups")
    return settings


def render_unit_selection(ctx):
    settings = _settings(ctx)
    if not settings["enabled"]:
        return ""
    group = settings["villager_group"]
    # The enclosing object-table loop first sets every type to 255. Override only
    # ordinary villagers, including their working forms, then split Genghis below.
    # All other types retain exact-ID selection, including later births.
    lines = ["        // Male/female villagers and all their jobs share one selection group."]
    for unit in sorted(UnitInfo.vils(), key=lambda unit: unit.ID):
        lines.append(
            f"        if (objectCount > {unit.ID}) xsEffectAmount(cSetAttribute, {unit.ID}, "
            f"{int(ObjectAttribute.RUN_PATTERN)}, {group}, worldPlayer);"
        )
    # Both sides must opt into groups: leaving army Genghis on exact-ID selection
    # would still let an army double-click collect the special same-ID leader.
    lines.append(
        f"        xsEffectAmount(cSetAttribute, {HeroInfo.GENGHIS_KHAN.ID}, "
        f"{int(ObjectAttribute.RUN_PATTERN)}, {settings['genghis_army_group']}, worldPlayer);"
    )
    return "\n".join(lines) + "\n"


def configure_leader_selection(ctx):
    settings = _settings(ctx)
    if not settings["enabled"]:
        return
    unit_id = leader_unit_id(ctx.mode_dir) if leaders_enabled(ctx.mode_dir) else HeroInfo.GENGHIS_KHAN.ID
    for color in PlayerId.all(exclude_gaia=True):
        leader, = [unit for unit in ctx.um.units[color] if unit.unit_const == unit_id]
        for owner in PlayerId.all(exclude_gaia=True):
            trigger = ctx.tm.add_trigger(f"RAM Selection — leader P{int(color)} W{int(owner)}")
            # Main initializes the shared table before this instance gets its own
            # master. Native owner aliases are deliberately separate from XS ids.
            trigger.new_condition.timer(timer=1)
            trigger.new_condition.variable_value(
                variable=32 + int(color) - 1, quantity=1, comparison=Comparison.EQUAL,
            )
            trigger.new_condition.variable_value(
                variable=40 + int(color) - 1, quantity=int(owner), comparison=Comparison.EQUAL,
            )
            trigger.new_effect.modify_object_attribute(
                source_player=owner, selected_object_ids=[leader.reference_id],
                object_attributes=ObjectAttribute.RUN_PATTERN,
                operation=Operation.SET, quantity=settings["leader_group"],
            )
