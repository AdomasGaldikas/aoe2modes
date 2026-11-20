"""Serialized sea geometry and execution of the shipped XS with mocked engine APIs."""

from __future__ import annotations

import re
import shutil
import subprocess
from collections import deque
from pathlib import Path

import pytest
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import Attribute, ObjectAttribute
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes.builder import build_mode
from aoe2modes.lib.audit import audit_scenario
from aoe2modes.registry import discover


@pytest.fixture(scope="module")
def naval(repo, tmp_path_factory):
    spec = next(spec for spec in discover(repo) if spec.id == "cba_naval")
    result = build_mode(spec, out_dir=tmp_path_factory.mktemp("naval"))
    return AoE2DEScenario.from_file(str(result.output))


def test_restricted_construction_and_archers_without_transports_or_economy(naval):
    for color in range(1, 9):
        units = naval.unit_manager.units[color]
        assert sorted(u.unit_const for u in units) == sorted(
            [BuildingInfo.DOCK.ID] * 4 + [BuildingInfo.GUARD_TOWER.ID] * 2 + [UnitInfo.ARCHER.ID] * 2
            + [UnitInfo.LONGBOAT.ID, BuildingInfo.BARRACKS.ID]
        )
        player = naval.player_manager.players[color]
        assert (player.food, player.wood, player.gold, player.stone) == (0, 0, 0, 0)
        assert {UnitInfo.TRANSPORT_SHIP.ID, UnitInfo.VILLAGER_MALE.ID, UnitInfo.GALLEY.ID} <= set(
            player.disabled_units
        )
        assert UnitInfo.ARCHER.ID not in player.disabled_units
        allowed = {BuildingInfo.DOCK.ID, BuildingInfo.WATCH_TOWER.ID, BuildingInfo.ARCHERY_RANGE.ID}
        assert allowed.isdisjoint(player.disabled_buildings)
        assert {b.ID for b in BuildingInfo} - set(player.disabled_buildings) == allowed
        assert TechInfo.CARTOGRAPHY.ID not in player.disabled_techs
    assert naval.option_manager.lock_teams
    assert not naval.option_manager.random_start_points
    assert not naval.option_manager.victory_custom_conditions_required
    assert naval.sections["GlobalVictory"].retriever_map["conquest_required"].data == 0
    assert not audit_scenario(naval).findings


def test_ocean_connects_hero_berths_dock_exits_and_center_without_crossing_land(naval):
    mm = naval.map_manager
    water = {int(TerrainId.WATER_DEEP), int(TerrainId.WATER_MEDIUM), int(TerrainId.WATER_AZURE)}
    sea = {(x, y) for x in range(144) for y in range(144) if mm.get_tile(x, y).terrain_id in water}
    # Dock footprints block ships. Keep the connectivity check independent of the mode's geometry helpers.
    for units in naval.unit_manager.units:
        for unit in units:
            if unit.unit_const in (BuildingInfo.DOCK.ID, BuildingInfo.GUARD_TOWER.ID):
                sea -= {(x, y) for x in range(int(unit.x) - 1, int(unit.x) + 2)
                        for y in range(int(unit.y) - 1, int(unit.y) + 2)}
    seen = {(72, 72)}
    pending = deque(seen)
    while pending:
        x, y = pending.popleft()
        for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if neighbor in sea and neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)
    for units in naval.unit_manager.units:
        for unit in units:
            if unit.unit_const in (UnitInfo.GALLEY.ID, UnitInfo.FIRE_GALLEY.ID, UnitInfo.LONGBOAT.ID):
                assert (int(unit.x), int(unit.y)) in seen
    xs = next(t for t in naval.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    assert "gStaging" not in xs and "gBattle" not in xs
    assert "xsTaskUnits(unitIds, 1, clear, -1, false" in xs
    assert "xsTaskUnits(unitIds, 17, vector(72.5, 72.5, -1), -1, true" in xs
    # Check the first launch candidate independently for all 32 starting ports.
    for color in range(1, 9):
        for port in (u for u in naval.unit_manager.units[color] if u.unit_const == BuildingInfo.DOCK.ID):
            dx, dy = {1: (0, 3), 2: (0, 3), 3: (3, 0), 4: (-3, 0),
                      5: (3, 0), 6: (-3, 0), 7: (0, -3), 8: (0, -3)}[color]
            assert (int(port.x + dx), int(port.y + dy)) in seen
            assert (int(port.x + 2 * dx), int(port.y + 2 * dy)) in seen
    assert len(sea) > 144 * 144 * 0.7


def test_equal_harbors_and_exact_terrain_symmetry(naval):
    mm = naval.map_manager
    for x in range(144):
        for y in range(144):
            kind = mm.get_tile(x, y).terrain_id
            assert kind == mm.get_tile(143 - x, y).terrain_id
            assert kind == mm.get_tile(y, x).terrain_id
    anchors = []
    for color in range(1, 9):
        ports = [u for u in naval.unit_manager.units[color] if u.unit_const == BuildingInfo.DOCK.ID]
        anchors.append(sorted(round((u.x - 72) ** 2 + (u.y - 72) ** 2, 2) for u in ports))
    assert all(anchor == anchors[0] for anchor in anchors)


def test_land_units_are_isolated_and_lagoons_have_one_four_tile_entrance(naval):
    mm = naval.map_manager
    water = {int(TerrainId.WATER_DEEP), int(TerrainId.WATER_MEDIUM), int(TerrainId.WATER_AZURE)}
    land = {(x, y) for x in range(144) for y in range(144) if mm.get_tile(x, y).terrain_id not in water}

    def flood(start, allowed, diagonal=False):
        seen, pending = {start}, deque([start])
        while pending:
            x, y = pending.popleft()
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if diagonal:
                neighbors.extend((x + dx, y + dy) for dx in (-1, 1) for dy in (-1, 1))
            for point in neighbors:
                if point in allowed and point not in seen:
                    seen.add(point)
                    pending.append(point)
        return seen

    islands = []
    for color in range(1, 9):
        units = naval.unit_manager.units[color]
        archers = [u for u in units if u.unit_const == UnitInfo.ARCHER.ID]
        island = flood((int(archers[0].x), int(archers[0].y)), land, diagonal=True)
        assert len(island) >= 500
        assert all((int(a.x), int(a.y)) in island for a in archers)
        assert all(island.isdisjoint(other) for other in islands)
        islands.append(island)
    # Independent source-harbor check (P3, on the west side).
    assert all((x, y) not in land for x in range(32, 38) for y in range(53, 57))
    assert all((x, y) in land for x in range(32, 38) for y in (*range(43, 53), *range(57, 67)))
    sea = {(x, y) for x in range(144) for y in range(144)} - land
    sealed = sea - {(32, y) for y in range(53, 57)}
    assert (24, 52) in flood((72, 72), sea)
    assert (24, 52) not in flood((72, 72), sealed)
    # Example additional dock foundations leave room for ships and land circulation.
    for cx, cy in ((24, 46), (24, 63)):
        footprint = {(x, y) for x in range(cx - 1, cx + 2) for y in range(cy - 1, cy + 2)}
        sea -= footprint
        land -= footprint
    assert all((24, y) in flood((72, 72), sea) for y in (49, 52, 57, 60))
    assert (34, 49) in flood((10, 54), land) and (34, 60) in flood((10, 54), land)


def test_results_use_guarded_native_selectors_and_no_army_retasking(naval):
    defeats, wins = [], []
    for trigger in naval.trigger_manager.triggers:
        assert all(effect.effect_type != EffectId.TASK_OBJECT for effect in trigger.effects)
        if trigger.name.startswith("Harbor defeat"):
            defeats.append(trigger)
        elif trigger.name.startswith("Sea victory"):
            wins.append(trigger)
        else:
            continue
        assert any(c.condition_type == ConditionId.SCRIPT_CALL for c in trigger.conditions)
        selector = int(trigger.name.rsplit("W", 1)[1])
        assert all(e.source_player == selector for e in trigger.effects
                   if e.effect_type in (EffectId.REMOVE_OBJECT, EffectId.DECLARE_VICTORY))
    assert len(defeats) == len(wins) == 64


def test_embedded_startup_clock_and_allied_vision(naval):
    xs = next(t for t in naval.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    assert "void main()" in xs
    assert "xsGetTime()" not in xs
    assert "int now = xsGetGameTime();" in xs
    assert "xsSetPlayerAttribute(owner, 285, bitCastToFloat(mask));" in xs
    assert "xsSetPlayerAttribute(owner, 286, bitCastToFloat(mask));" in xs
    setup = next(t for t in naval.trigger_manager.triggers if t.name == "Harbor setup")
    cartography = [e for e in setup.effects if e.effect_type == EffectId.RESEARCH_TECHNOLOGY
                   and e.technology == TechInfo.CARTOGRAPHY.ID]
    assert {e.source_player for e in cartography} == set(range(1, 9))
    assert all(e.force_research_technology for e in cartography)
    housing = [e for e in setup.effects if e.effect_type == EffectId.MODIFY_RESOURCE
               and e.tribute_list == Attribute.POPULATION_HEADROOM]
    assert {e.source_player for e in housing} == set(range(1, 9))
    assert all(e.quantity == 200 for e in housing)
    assert len(naval.trigger_manager.variables) == 56


def test_harbor_prerequisite_hero_berths_and_port_health(naval):
    setup = next(t for t in naval.trigger_manager.triggers if t.name == "Harbor setup")
    maximums = [e for e in setup.effects if e.effect_type == EffectId.MODIFY_ATTRIBUTE
                and e.object_list_unit_id == BuildingInfo.DOCK.ID
                and e.object_attributes == ObjectAttribute.HIT_POINTS]
    assert {e.source_player for e in maximums} == set(range(1, 9))
    assert all(e.quantity == 3000 for e in maximums)
    xs = next(t for t in naval.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    assert "gSpawns" not in xs
    berths = re.findall(r"xsArraySetVector\(gHeroPads, (\d+), vector\(([^,]+), ([^,]+), -1\)\)", xs)
    assert len(berths) == 8
    for color, x, y in berths:
        units = naval.unit_manager.units[int(color)]
        hero = next(u for u in units if u.unit_const == UnitInfo.LONGBOAT.ID)
        assert (hero.x, hero.y) == (float(x), float(y))
        quarters = next(u for u in units if u.unit_const == BuildingInfo.BARRACKS.ID)
        assert naval.map_manager.get_tile(int(quarters.x), int(quarters.y)).terrain_id == TerrainId.GRASS_1
        assert all(e.selected_object_ids != [hero.reference_id] for e in setup.effects
                   if e.effect_type == EffectId.TASK_OBJECT)
    labels = [e for e in setup.effects if e.effect_type == EffectId.CHANGE_OBJECT_NAME
              and e.object_list_unit_id == BuildingInfo.BARRACKS.ID]
    assert {e.source_player for e in labels} == set(range(1, 9))


def test_de_conditions_do_not_mix_modulo_and_logical_operators(naval):
    """DE rejected the center reward condition; xs-check and C++ accepted it.

    Inspect the emitted script before the C++ translator can hide that engine syntax issue.
    The screenshot's default0.xs line 649 refers to the first center reward condition.
    """
    xs = next(t for t in naval.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    # Extract balanced condition parentheses, including nested API calls.
    for match in re.finditer(r"\bif\s*\(", xs):
        start, depth, end = match.end(), 1, match.end()
        while depth:
            assert end < len(xs), "unterminated condition"
            depth += (xs[end] == "(") - (xs[end] == ")")
            end += 1
        condition = xs[start:end - 1]
        assert not ("%" in condition and ("&&" in condition or "||" in condition)), condition


def test_shipped_xs_runtime(naval, tmp_path):
    """Execute the real emitted function bodies, not a second Python model of the rules.

    C++ supplies mocked engine APIs; only XS loop syntax and the rule header are translated.
    This does not establish DE engine scheduling, placement or pathfinding acceptance.
    """
    compiler = shutil.which("g++")
    if compiler is None:
        pytest.skip("the optional XS execution harness needs g++")
    xs = next(t for t in naval.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    xs = re.sub(r"rule navalHeartbeat\s+active\s+minInterval 1\s*\{\s*navalTick\(\);\s*\}", "", xs)
    xs = re.sub(r"\bvector\b", "Vec", xs)
    xs = xs.replace("void main()", "void navalMain()")
    xs = re.sub(r"for \((\w+) = ([^;]+); (<|<=) ([^)]+)\)",
                r"for (int \1 = \2; \1 \3 \4; ++\1)", xs)
    (tmp_path / "naval-runtime.h").write_text(xs, encoding="utf-8")
    initial = []
    for color, units in enumerate(naval.unit_manager.units):
        for unit in units:
            hp = 3000 if unit.unit_const == BuildingInfo.DOCK.ID else 1100
            if unit.unit_const in (UnitInfo.GALLEY.ID, UnitInfo.FIRE_GALLEY.ID, UnitInfo.LONGBOAT.ID):
                hp = 100
            initial.append(f"objects[{unit.reference_id}] = Object{{owners[{color}], {unit.unit_const}, "
                           f"{hp}, Vec({unit.x}, {unit.y}, -1)}};")
    (tmp_path / "naval-initial.h").write_text("\n".join(initial), encoding="utf-8")
    water = {int(TerrainId.WATER_DEEP), int(TerrainId.WATER_MEDIUM), int(TerrainId.WATER_AZURE)}
    tiles = [str(int(naval.map_manager.get_tile(x, y).terrain_id in water))
             for y in range(144) for x in range(144)]
    (tmp_path / "naval-map.h").write_text(
        "const bool navalWater[] = {" + ",".join(tiles) + "};\n"
        "bool waterAt(Vec p) { return p.x>=0 && p.y>=0 && p.x<144 && p.y<144 "
        "&& navalWater[int(p.y)*144+int(p.x)]; }\n", encoding="utf-8",
    )
    replay = ["void replayNativeDefeat(int color) {"]
    for trigger in naval.trigger_manager.triggers:
        if not trigger.name.startswith("Harbor defeat"):
            continue
        color = int(re.search(r"P(\d+)", trigger.name)[1])
        guard = next(c.xs_function for c in trigger.conditions if c.condition_type == ConditionId.SCRIPT_CALL)
        replay.append(f"if (color == {color} && {guard}()) {{")
        for effect in trigger.effects:
            if effect.effect_type == EffectId.REMOVE_OBJECT:
                replay.append(f"nativeRemove({effect.source_player});")
            elif effect.effect_type == EffectId.DECLARE_VICTORY:
                assert not effect.enabled
                replay.append(f"nativeDefeat({effect.source_player});")
            else:
                assert effect.effect_type == EffectId.SCRIPT_CALL
                replay.append(f"{effect.message}();")
        replay.append("}")
    replay.append("}")
    (tmp_path / "naval-effects.h").write_text("\n".join(replay), encoding="utf-8")
    harness = Path(__file__).with_name("naval_runtime.cpp")
    compiled = subprocess.run([compiler, "-std=c++17", "-I", str(tmp_path), str(harness), "-o",
                               str(tmp_path / "naval-test")], capture_output=True, text=True)
    assert compiled.returncode == 0, compiled.stderr
    executed = subprocess.run([str(tmp_path / "naval-test")], capture_output=True, text=True)
    assert executed.returncode == 0, executed.stderr
