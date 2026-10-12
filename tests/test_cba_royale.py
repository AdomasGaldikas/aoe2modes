"""Geometry, serialization and execution of Last Caravan's emitted XS.

The C++ engine mocks do not establish native DE placement, scheduling or save/load.
"""

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
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes.builder import build_mode
from aoe2modes.lib.audit import audit_scenario
from aoe2modes.registry import discover


@pytest.fixture(scope="module")
def royale(repo, tmp_path_factory):
    spec = next(s for s in discover(repo) if s.id == "cba_royale")
    result = build_mode(spec, out_dir=tmp_path_factory.mktemp("royale"))
    return AoE2DEScenario.from_file(str(result.output))


def test_starting_objects_settings_and_owner_guarded_victories(royale):
    allowed = {
        BuildingInfo.WATCH_TOWER.ID,
        BuildingInfo.PALISADE_WALL.ID,
        BuildingInfo.PALISADE_GATE.ID,
        BuildingInfo.BARRACKS.ID,
        BuildingInfo.ARCHERY_RANGE.ID,
        BuildingInfo.STABLE.ID,
    }
    allowed.update(b.ID for b in BuildingInfo if "PALISADE_GATE" in b.name)
    for color in range(1, 9):
        units = royale.unit_manager.units[color]
        assert len(units) == 3
        wagon = next(u for u in units if u.unit_const == UnitInfo.OX_WAGON.ID)
        assert (wagon.x, wagon.y) == (32 if color <= 4 else 208, 84 + (color - 1) % 4 * 24)
        player = royale.player_manager.players[color]
        assert not player.lock_civ
        assert {b.ID for b in BuildingInfo} - set(player.disabled_buildings) == allowed
        assert (player.food, player.wood, player.gold, player.stone) == (0, 0, 0, 0)
    assert royale.option_manager.lock_teams
    assert royale.sections["Options"].retriever_map["all_techs"].data == 0
    assert royale.sections["GlobalVictory"].retriever_map["conquest_required"].data == 0
    variables = royale.trigger_manager.variables
    assert sorted(v.variable_id for v in variables) == list(range(78))
    victories = [t for t in royale.trigger_manager.triggers if t.name.startswith("Caravan victory")]
    assert len(victories) == 64
    for trigger in victories:
        assert len(trigger.conditions) == len(trigger.effects) == 1
        assert trigger.conditions[0].condition_type == ConditionId.SCRIPT_CALL
        assert trigger.effects[0].effect_type == EffectId.DECLARE_VICTORY
        assert trigger.effects[0].enabled
    assert not audit_scenario(royale).findings


def test_connected_routes_flat_final_arenas_and_equal_team_travel(royale):
    mm = royale.map_manager
    for x in range(240):
        for y in range(240):
            a, b = mm.get_tile(x, y), mm.get_tile(239 - x, y)
            assert (a.terrain_id, a.elevation) == (b.terrain_id, b.elevation)
    water = {int(TerrainId.WATER_DEEP), int(TerrainId.WATER_MEDIUM)}
    land = {(x, y) for x in range(240) for y in range(240) if mm.get_tile(x, y).terrain_id not in water}
    distances = {(120, 120): 0}
    pending = deque(distances)
    while pending:
        x, y = pending.popleft()
        for p in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if p in land and p not in distances:
                distances[p] = distances[x, y] + 1
                pending.append(p)
    assert set(distances) == land
    for y in (84, 108, 132, 156):
        assert distances[32, y] == distances[208, y]
    for y in (84, 120, 156):
        assert all((x, py) in land for x in range(32, 209) for py in range(y - 6, y + 6))
    for cx in (80, 120, 160):
        for cy in (80, 120, 160):
            arena = {
                (x, y)
                for x in range(cx - 14, cx + 15)
                for y in range(cy - 14, cy + 15)
                if (x - cx) ** 2 + (y - cy) ** 2 <= 14**2
            }
            assert arena <= land
            assert all(mm.get_tile(x, y).elevation == 1 for x, y in arena)
    assert not royale.unit_manager.units[0] or all(
        u.unit_const not in {UnitInfo.SHEEP.ID, UnitInfo.DEER.ID} for u in royale.unit_manager.units[0]
    )


def test_emitted_xs_runtime(royale, tmp_path):
    compiler = shutil.which("g++")
    if compiler is None:
        pytest.skip("XS execution harness requires g++")
    xs = next(t for t in royale.trigger_manager.triggers if t.name == "XS SCRIPT").effects[0].message
    assert "${" not in xs
    xs = re.sub(r"rule royaleHeartbeat\s+active\s+minInterval 1\s*\{\s*royaleTick\(\);\s*\}", "", xs)
    xs = re.sub(r"\bvector\b", "Vec", xs).replace("void main()", "void royaleMain()")
    xs = re.sub(
        r"for \((\w+) = ([^;]+); (<|<=) ((?:[^()]|\([^()]*\))+)\)", r"for (int \1 = \2; \1 \3 \4; ++\1)", xs
    )
    # XS supports concatenation of strings/numbers. Presentation is not an engine contract mocked here.
    xs = re.sub(r"xsChatData\(.*?\);", 'xsChatData("event");', xs, flags=re.DOTALL)
    (tmp_path / "royale-runtime.h").write_text(xs)
    initial = []
    for color, units in enumerate(royale.unit_manager.units):
        for u in units:
            initial.append(
                f"objects[{u.reference_id}] = Object{{owners[{color}], {u.unit_const}, "
                f"100, Vec({u.x}, {u.y}, -1)}};"
            )
    (tmp_path / "royale-initial.h").write_text("\n".join(initial))
    replay = ["void nativeOutcomes() {"]
    for trigger in royale.trigger_manager.triggers:
        if not trigger.name.startswith("Caravan victory"):
            continue
        guard = trigger.conditions[0].xs_function
        selector = trigger.effects[0].source_player
        replay.append(f"if ({guard}()) winners.push_back(xsGetWorldPlayerId({selector}));")
    replay.append("}")
    (tmp_path / "royale-effects.h").write_text("\n".join(replay))
    binary = tmp_path / "royale-test"
    result = subprocess.run(
        [
            compiler,
            "-std=c++17",
            "-O2",
            "-I",
            str(tmp_path),
            str(Path(__file__).with_name("royale_runtime.cpp")),
            "-o",
            str(binary),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    result = subprocess.run([str(binary)], capture_output=True, text=True, timeout=90)
    assert result.returncode == 0, result.stderr
    assert "2000 seeded paths" in result.stdout
