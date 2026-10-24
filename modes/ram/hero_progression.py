"""Extend RA's owner-resolved hero bands using the Adrenaline Rush roster.

Only heroes, their stats and production intervals are imported. Fire-rate changes
and global unit-type mutations belong to a future adrenaline variant.
"""

import re
import tomllib
from copy import deepcopy

from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.trigger_lists import Attribute, Operation


def _set_band(trigger, lower, upper):
    kill_conditions = [c for c in trigger.conditions
                       if c.condition_type == ConditionId.ACCUMULATE_ATTRIBUTE
                       and c.attribute == Attribute.UNITS_KILLED]
    lower_condition, = [c for c in kill_conditions if not c.inverted]
    lower_condition.quantity = lower
    if upper is not None:
        upper_condition, = [c for c in kill_conditions if c.inverted]
        upper_condition.quantity = upper


def _set_stats(trigger, stats):
    create, = [e for e in trigger.effects if e.effect_type == EffectId.CREATE_OBJECT]
    trigger.effects = [e for e in trigger.effects if e.effect_type not in {
        EffectId.CHANGE_OBJECT_ATTACK, EffectId.CHANGE_OBJECT_HP, EffectId.CHANGE_OBJECT_RANGE,
    }]
    # Restrict all buffs to a pad proven empty before creating this one new hero.
    area = dict(source_player=create.source_player, object_list_unit_id=create.object_list_unit_id,
                area_x1=create.location_x, area_y1=create.location_y,
                area_x2=create.location_x, area_y2=create.location_y)
    if stats.get("attack_bonus"):
        trigger.new_effect.change_object_attack(
            armour_attack_quantity=stats["attack_bonus"], operation=Operation.ADD, **area,
        )
    if stats.get("hp_bonus"):
        trigger.new_effect.change_object_hp(quantity=stats["hp_bonus"], operation=Operation.ADD, **area)
    if stats.get("range"):
        trigger.new_effect.change_object_range(quantity=stats["range"], operation=Operation.SET, **area)
    trigger.effect_order = list(range(len(trigger.effects)))


def configure_extra_hero_tiers(ctx):
    with (ctx.mode_dir / "mode.toml").open("rb") as handle:
        settings = tomllib.load(handle)["hero_progression"]
    extras = settings["extra_tiers"]
    thresholds = [row["kills"] for row in extras]
    if thresholds != sorted(set(thresholds)) or any(t <= 0 for t in thresholds):
        raise ValueError("Extra hero thresholds must be positive, unique and increasing")
    for row in extras:
        HeroInfo[row["hero"]]  # Fail on a misspelled dataset name before changing the graph.
        if row["interval"] <= 0:
            raise ValueError("Hero intervals must be positive")

    pattern = re.compile(r"Hero (?:Milestone S([1-8]) W([1-8]) K(\d+)"
                         r"|Boost (K\d+[AB]?) S([1-8]) W([1-8]))")
    existing = {}
    for trigger in ctx.tm.triggers:
        if match := pattern.fullmatch(trigger.name):
            color, owner, kills, label, boost_color, boost_owner = match.groups()
            key = (int(color or boost_color), int(owner or boost_owner))
            existing.setdefault(key, {})[int(kills or re.search(r"\d+", label)[0])] = trigger

    if len(existing) != 64:
        raise RuntimeError("Hero extension expects every color/native-owner pairing")
    for (color, owner), tiers in existing.items():
        if set(thresholds) & tiers.keys():
            raise ValueError("Extra hero threshold overlaps an existing RA tier")
        bounds = sorted(set(tiers) | set(thresholds))
        upper = dict(zip(bounds, bounds[1:] + [None], strict=True))
        # Copy templates before closing their old bands. New tiers are authored
        # as state checks, never as one-shot activation chains that can catch up.
        milestone = deepcopy(tiers[1000])
        boosted = deepcopy(tiers[3500])
        for threshold, trigger in tiers.items():
            _set_band(trigger, threshold, upper[threshold])
        for row in extras:
            threshold = row["kills"]
            is_boost = bool(row.get("attack_bonus") or row.get("hp_bonus"))
            name = (f"Hero Boost K{threshold} S{color} W{owner}" if is_boost
                    else f"Hero Milestone S{color} W{owner} K{threshold}")
            template = boosted if is_boost else milestone
            trigger = ctx.tm.add_trigger(name, enabled=1, looping=1,
                                         description_stid=0, short_description_stid=0)
            trigger.conditions = deepcopy(template.conditions)
            trigger.effects = deepcopy(template.effects)
            _set_band(trigger, threshold, upper[threshold])
            timer, = [c for c in trigger.conditions if c.condition_type == ConditionId.TIMER]
            timer.timer = row["interval"]
            unit_id = HeroInfo[row["hero"]].ID
            for effect in trigger.effects:
                if effect.effect_type == EffectId.CREATE_OBJECT:
                    effect.object_list_unit_id = unit_id
            _set_stats(trigger, row)
            trigger.condition_order = list(range(len(trigger.conditions)))

    # Both 5000 loops share a threshold, so visit all triggers rather than the
    # threshold lookup (which deliberately uses one representative per band).
    for trigger in ctx.tm.triggers:
        if re.fullmatch(r"Hero Boost K(?:3500|5000[AB]) S[1-8] W[1-8]", trigger.name):
            _set_stats(trigger, settings["late_stats"])
