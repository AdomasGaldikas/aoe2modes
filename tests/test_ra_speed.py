"""Serialized base parity and executable contracts for the independent Speed mode."""

import json
import re
import shutil
import subprocess

import pytest
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes import registry
from aoe2modes.builder import _load_build_module, build_mode
from aoe2modes.lib.audit import audit_scenario
from aoe2modes.lib.verify import snapshot
from ascendants_runtime import xs_source


@pytest.fixture(scope="module")
def candidates(repo, tmp_path_factory):
    directory = tmp_path_factory.mktemp("ra-speed")
    result = {}
    for mode in ("evolution_alpha", "ra_speed"):
        artifact = build_mode(registry.get(mode, repo), out_dir=directory, xs_check=False)
        result[mode] = AoE2DEScenario.from_file(str(artifact.output))
    return result


def test_speed_preserves_ra_map_units_players_and_every_gameplay_trigger(candidates, repo):
    base, speed = (snapshot(candidates[name]) for name in ("evolution_alpha", "ra_speed"))
    for field in ("map_size", "active_players", "terrain", "players", "options", "units"):
        assert base[field] == speed[field], field
    assert speed["variables"][:-2] == base["variables"]
    assert [name for _id, name in speed["variables"][-2:]] == ["speed_t1seconds", "speed_t2seconds"]
    normal_spec, speed_spec = (registry.get(name, repo) for name in ("evolution_alpha", "ra_speed"))
    normal_name = f"{normal_spec.name} v{normal_spec.version}"
    speed_name = f"{speed_spec.name} v{speed_spec.version}"
    variants = {trigger["name"]: trigger for trigger in speed["triggers"]}
    assert set(variants) - {trigger["name"] for trigger in base["triggers"]} == {
        "Speed Rush HUD Team 1", "Speed Rush HUD Team 2",
    }
    for normal in base["triggers"]:
        variant = variants[normal["name"]]
        if normal["name"] == "XS SCRIPT":
            assert normal["attrs"] == variant["attrs"]
            continue
        expected = json.loads(json.dumps(normal).replace(normal_name, speed_name))
        assert expected == json.loads(json.dumps(variant)), normal["name"]
    assert "cbaSpeedTick" not in xs_source(candidates["evolution_alpha"])
    source = xs_source(candidates["ra_speed"])
    assert source.count("void main() {") == 1
    assert source.index("void cbaSpeedInitialize()") < source.index("void main() {")
    assert "void main() {\n    cbaSpeedInitialize();" in source
    assert "rule cbaSpeedRush" in source
    assert "SPEED RUSH" in candidates["ra_speed"].message_manager.instructions


def test_speed_passes_strict_serialized_audit(candidates):
    report = audit_scenario(candidates["ra_speed"])
    assert report.errors == report.warnings == [], report


def test_speed_emitted_state_machine_handles_losses_refresh_expiry_and_independent_owners(
    candidates, repo, tmp_path,
):
    compiler = shutil.which("g++")
    assert compiler, "g++ is required to execute the emitted Speed runtime contracts"
    source = xs_source(candidates["ra_speed"])
    runtime = "// RA Speed Rush:" + source.split("// RA Speed Rush:", 1)[1].split("void cbaCreateWave(", 1)[0]
    runtime = re.sub(r"for \((\w+) = (\d+); <= (\d+)\)",
                     lambda m: f"for (int {m[1]} = {m[2]}; {m[1]} <= {m[3]}; ++{m[1]})", runtime)
    harness = (repo.root / "tests/ra_speed_runtime.cpp").read_text()
    output = tmp_path / "speed-runtime.cpp"
    output.write_text(harness.replace("// GENERATED_RUNTIME", runtime))
    binary = tmp_path / "speed-runtime"
    compiled = subprocess.run(
        [compiler, "-std=c++17", "-O2", "-Wall", "-Werror", str(output), "-o", str(binary)],
        capture_output=True, text=True, timeout=60,
    )
    assert compiled.returncode == 0, compiled.stderr
    result = subprocess.run([str(binary)], capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Speed runtime contracts passed" in result.stdout


@pytest.mark.parametrize("field, value", [
    ("delay_seconds", -1), ("duration_seconds", 0), ("delay_seconds", 0.5),
    ("movement_multiplier", 0), ("fire_rate_multiplier", 5),
    ("movement_multiplier", float("nan")), ("fire_rate_multiplier", True),
])
def test_speed_rejects_invalid_settings(field, value, repo, tmp_path):
    module = _load_build_module(registry.get("ra_speed", repo))
    rush = __import__(module.__package__ + ".rush", fromlist=["load_settings"])
    values = dict(delay_seconds=900, duration_seconds=300, movement_multiplier=2.0, fire_rate_multiplier=3.0)
    values[field] = value
    def toml(value):
        if isinstance(value, bool):
            return str(value).lower()
        return str(value)
    (tmp_path / "mode.toml").write_text("[speed_rush]\n" + "\n".join(
        f"{key} = {toml(value)}" for key, value in values.items()))
    with pytest.raises(ValueError):
        rush.load_settings(tmp_path)


@pytest.mark.parametrize("mode", ["evolution_alpha", "ra_speed"])
def test_same_type_selection_initializes_every_runtime_owner_and_future_type(candidates, mode, tmp_path):
    source = xs_source(candidates[mode])
    marker = "int objectCount = xsGetPlayerNumberOfObjects(worldPlayer);"
    assert source.count(marker) == 1
    initialization = marker + source.split(marker, 1)[1].split("cbaRefreshCombatValues(worldPlayer);", 1)[0]
    assert "xsEffectAmount(cSetAttribute, objectId, 140, 255, worldPlayer);" in initialization
    initialization = re.sub(r"for \((\w+) = (\d+); < (\w+)\)",
                            lambda m: f"for (int {m[1]} = {m[2]}; {m[1]} < {m[3]}; ++{m[1]})",
                            initialization)
    # Execute the serialized initialization with independently numbered owners and
    # differing table lengths. High IDs stand for future/DLC/upgraded definitions.
    harness = r'''
#include <cassert>
#include <map>
#include <tuple>
constexpr int cSetAttribute = 0;
constexpr int cFoodCost = 103, cWoodCost = 104, cGoldCost = 105, cStoneCost = 106;
std::map<std::tuple<int,int,int>, float> writes;
int xsGetPlayerNumberOfObjects(int owner) { return 2400 + owner * 3; }
void xsEffectAmount(int operation, int type, int attribute, float value, int owner) {
    assert(operation == cSetAttribute && owner >= 1 && owner <= 8);
    assert(attribute == 140 || (attribute >= 103 && attribute <= 106));
    assert(type >= 0 && type < xsGetPlayerNumberOfObjects(owner));
    assert(writes.emplace(std::make_tuple(owner, type, attribute), value).second);
}
void initialize(int worldPlayer) {
// INITIALIZATION
}
int main() {
    for (int owner : {7, 2, 5, 8, 3, 1, 4, 6}) initialize(owner);
    for (int owner = 1; owner <= 8; ++owner) {
        for (int type = 0; type < xsGetPlayerNumberOfObjects(owner); ++type) {
            assert(writes.at({owner, type, 140}) == 255);
            for (int cost = 103; cost <= 106; ++cost) assert(writes.at({owner, type, cost}) == 0);
        }
    }
}
'''
    cpp = tmp_path / "selection.cpp"
    cpp.write_text(harness.replace("// INITIALIZATION", initialization))
    binary = tmp_path / "selection"
    compiler = shutil.which("g++")
    assert compiler, "g++ is required for the emitted selection initialization test"
    result = subprocess.run([compiler, "-std=c++17", "-Wall", "-Werror", str(cpp), "-o", str(binary)],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    subprocess.run([str(binary)], check=True, timeout=15)
