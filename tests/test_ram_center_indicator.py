"""Written-scenario safeguards for RAM's single physical center meter."""

import re
import tomllib

import pytest
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.trigger_lists import (
    AttackStance,
    HeroStatusFlag,
    ObjectAttribute,
    ObstructionType,
    Operation,
)
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes import registry
from aoe2modes.builder import build_mode


@pytest.fixture(scope="module")
def indicator_scenario(repo, tmp_path_factory):
    spec = registry.get("ram", repo)
    result = build_mode(spec, out_dir=tmp_path_factory.mktemp("ram-indicator"), repo=repo)
    scenario = AoE2DEScenario.from_file(str(result.output))
    source = next(t for t in scenario.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    settings = tomllib.loads((spec.directory / "mode.toml").read_text())["center"]
    return scenario, source, settings


def test_center_ram_is_one_gaia_reference_aligned_with_both_flags(indicator_scenario):
    scenario, source, settings = indicator_scenario
    reference = int(re.search(r"const int cRamCenterRam = (\d+);", source)[1])
    units = [(owner, unit) for owner, group in enumerate(scenario.unit_manager.units)
             for unit in group if unit.reference_id == reference]
    assert len(units) == 1
    owner, unit = units[0]
    assert owner == 0 and unit.unit_const == UnitInfo.BATTERING_RAM.ID
    assert unit.x == (settings["x1"] + settings["x2"]) / 2
    assert unit.y == (settings["y1"] + settings["y2"]) / 2
    flags = []
    for name in ("cRamTeamOneFlag", "cRamTeamTwoFlag"):
        flag_reference = int(re.search(rf"const int {name} = (\d+);", source)[1])
        flags.append(next(u for u in scenario.unit_manager.units[0] if u.reference_id == flag_reference))
    assert flags[0].x == settings["x1"] + 0.5
    assert flags[1].x == settings["x2"] - 0.5
    assert flags[0].y == flags[1].y == unit.y
    assert f"const float cRamCenterRamMidX = {unit.x};" in source
    assert f"const float cRamCenterRamHalfTravel = {(flags[1].x - flags[0].x) / 2};" in source


def test_center_ram_native_safeguards_are_instance_scoped(indicator_scenario):
    scenario, source, _settings = indicator_scenario
    reference = int(re.search(r"const int cRamCenterRam = (\d+);", source)[1])
    protect = next(t for t in scenario.trigger_manager.triggers
                   if t.name == "RAM — protect center control ram")
    assert protect.enabled and not protect.looping and not protect.conditions
    for effect_id in (EffectId.DISABLE_UNIT_ATTACKABLE, EffectId.DISABLE_UNIT_TARGETING,
                      EffectId.DISABLE_OBJECT_DELETION, EffectId.DISABLE_OBJECT_SELECTION):
        effect, = [e for e in protect.effects if e.effect_type == effect_id]
        assert effect.source_player == 0 and effect.selected_object_ids == [reference]
    attributes = {e.object_attributes: e for e in protect.effects
                  if e.effect_type == EffectId.MODIFY_OBJECT_ATTRIBUTE}
    for attribute, value in (
        (ObjectAttribute.HERO_STATUS, int(HeroStatusFlag.CANNOT_BE_CONVERTED)),
        (ObjectAttribute.FRIENDLY_FIRE_DAMAGE, 0),
        (ObjectAttribute.MOVEMENT_SPEED, 0), (ObjectAttribute.SEARCH_RADIUS, 0),
        (ObjectAttribute.GARRISON_CAPACITY, 0), (ObjectAttribute.GARRISON_TYPE, 0),
        (ObjectAttribute.UNIT_SIZE_X, 0), (ObjectAttribute.UNIT_SIZE_Y, 0),
        (ObjectAttribute.OBSTRUCTION_TYPE, int(ObstructionType.NO_OUTLINE_PASSABLE)),
    ):
        effect = attributes[attribute]
        # The pinned parser misreads serialized float zero as integer -1; inspect
        # that field in the underlying written trigger struct below.
        quantity = effect.quantity
        if value == 0 and ObjectAttribute._storage_type(attribute) == "float":
            raw_trigger = scenario.sections["Triggers"].retriever_map["trigger_data"].data[protect.trigger_id]
            raw_effects = raw_trigger.retriever_map["effect_data"].data
            quantity = raw_effects[protect.effects.index(effect)].retriever_map["quantity_float"].data
        assert quantity == value and effect.operation == Operation.SET
        assert effect.source_player == 0 and effect.selected_object_ids == [reference]
    stance, = [e for e in protect.effects if e.effect_type == EffectId.CHANGE_OBJECT_STANCE]
    assert stance.attack_stance == AttackStance.NO_ATTACK_STANCE
    assert stance.source_player == 0 and stance.selected_object_ids == [reference]
    setup, = [e for e in protect.effects if e.effect_type == EffectId.SCRIPT_CALL]
    assert setup.message == "ramProtectCenterRam"
    guard = source.split("void ramProtectCenterRam()", 1)[1].split("void ramMoveCenterRam()", 1)[0]
    assert "xsSetUnitOwner(cRamCenterRam, 0, false)" in guard
    assert "xsEffectAmount(cSetUnitAttribute, cRamCenterRam, 129, 1.0, 0);" in guard
    for property_id in range(6, 11):
        assert f"ramKeepCenterRamProperty({property_id}, 0.0);" in guard


def test_center_ram_uses_native_position_without_recreation_or_local_state(indicator_scenario):
    _scenario, source, _settings = indicator_scenario
    movement = source.split("void ramMoveCenterRam()", 1)[1].split("void ramTint(", 1)[0]
    assert "xsSetUnitPosition(cRamCenterRam, destination, false)" in movement
    assert "xsVectorSet(x, cRamCenterRamY, -1.0)" in movement
    assert "gRamBalance / cRamControlScale" in movement
    assert "fraction > 1.0" in movement and "fraction < -1.0" in movement
    assert "xsCreateUnit" not in movement and "xsRemoveUnit" not in movement
    assert "xsUnsync" not in movement
    assert source.count("ramMoveCenterRam();") == 1


def test_legacy_gaia_cleanup_cannot_match_the_meter_track(indicator_scenario):
    scenario, source, settings = indicator_scenario
    reference = int(re.search(r"const int cRamCenterRam = (\d+);", source)[1])
    y = (settings["y1"] + settings["y2"]) / 2
    minimum_x, maximum_x = settings["x1"] + 0.5, settings["x2"] - 0.5
    hazards = []
    for trigger in scenario.trigger_manager.triggers:
        for effect in trigger.effects:
            if effect.effect_type not in {EffectId.KILL_OBJECT, EffectId.REMOVE_OBJECT}:
                continue
            selected = effect.selected_object_ids or []
            if selected:
                if reference in selected:
                    hazards.append(trigger.name)
                continue  # Explicit references override owner, class and area.
            if effect.source_player > 0:
                continue
            if effect.object_list_unit_id >= 0 and effect.object_list_unit_id != UnitInfo.BATTERING_RAM.ID:
                continue
            if effect.object_group >= 0 and effect.object_group != 13:  # Native siege class.
                continue
            area = effect.area_x1, effect.area_y1, effect.area_x2, effect.area_y2
            if min(area) >= 0:
                x1, y1, x2, y2 = area
                if y < y1 or y > y2 or maximum_x < x1 or minimum_x > x2:
                    continue
            hazards.append(trigger.name)
    assert not hazards, f"Legacy Gaia/wildcard removal could match the meter: {hazards}"
