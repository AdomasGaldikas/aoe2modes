"""Execute the emitted leader XS with independent sparse-player engine state."""

import importlib
import json
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest
from AoE2ScenarioParser.datasets.effects import EffectId

ROOT = Path(__file__).resolve().parents[1]
MODE = ROOT / "modes/ram"


def _emitted_runtime():
    package = "ram_leader_runtime_test_package"
    if package not in sys.modules:
        module = types.ModuleType(package)
        module.__path__ = [str(MODE)]
        sys.modules[package] = module
    runtime = importlib.import_module(f"{package}.leader_runtime")
    units = {color: [SimpleNamespace(unit_const=731, reference_id=100 + color)]
             for color in range(1, 9)}
    effects = [SimpleNamespace(effect_type=EffectId.CHANGE_OBJECT_ATTACK),
               SimpleNamespace(effect_type=EffectId.CHANGE_OBJECT_HP)]

    def script_call(**kwargs):
        effect = SimpleNamespace(effect_type=EffectId.SCRIPT_CALL, **kwargs)
        growth.effects.append(effect)
        return effect

    growth = SimpleNamespace(name="ge kan", effects=effects,
                             new_effect=SimpleNamespace(script_call=script_call))
    emitted = []
    ctx = SimpleNamespace(mode_dir=MODE, um=SimpleNamespace(units=units),
                          tm=SimpleNamespace(triggers=[growth]),
                          add_xs=lambda source, **_kwargs: emitted.append(source))
    runtime.configure_civilization_leaders(ctx)
    assert len(emitted) == 1
    assert all(group[0].unit_const == 2750 and group[0].reference_id == 100 + color
               for color, group in units.items())
    assert not any(e.effect_type == EffectId.CHANGE_OBJECT_ATTACK for e in growth.effects)
    assert sum(e.effect_type == EffectId.CHANGE_OBJECT_HP for e in growth.effects) == 1
    wrappers = [e.message for e in growth.effects if e.effect_type == EffectId.SCRIPT_CALL]
    assert len(wrappers) == 8
    assert all(re.fullmatch(r"void ramGrowLeader\d+\(\)\s*\{.*\}", w, flags=re.S)
               for w in wrappers)
    return emitted[0], wrappers


def test_emitted_leader_xs_sparse_identity_damage_growth_and_persistent_names(tmp_path):
    compiler = shutil.which("g++")
    if compiler is None:
        pytest.skip("g++ is needed to execute emitted XS against independent engine state")
    source, wrappers = _emitted_runtime()
    source = re.sub(r"rule ramCivilizationLeaderNames\s+active\s+minInterval 1",
                    "void ramCivilizationLeaderNames()", source)
    rows = json.loads((MODE / "assets/leaders/catalog.json").read_text())["civilizations"]
    catalogue_checks = "\n".join(
        f"assert(ramCivilizationLeaderName({row['civilization']}) == "
        f"{json.dumps(row['leader_name'])});" for row in rows
    )
    prelude = r'''
#include <cassert>
#include <map>
#include <string>
#include <tuple>
#include <vector>
using string = std::string;
struct Unit { int owner; float hp; int melee; int pierce; };
std::map<int, Unit> units;
std::vector<std::vector<int>> arrays;
std::map<int,int> variables;
std::map<int,string> names;
std::map<int,int> nameWrites;
std::vector<std::tuple<int,int>> damage;
int owners[9] = {0,7,0,2,0,0,0,0,4};
std::map<int,int> civilizations = {{7,35},{2,1},{4,62}};
bool rejectNextName = false;
const int cAddUnitAttribute = 5;
int cbaWorldPlayerForColor(int color) { return owners[color]; }
int xsTriggerVariable(int id) { return variables[id]; }
int xsArrayCreateInt(int count,int value,const char*) {
    arrays.emplace_back(count,value); return arrays.size()-1;
}
int xsArrayGetInt(int array,int index) { return arrays.at(array).at(index); }
void xsArraySetInt(int array,int index,int value) { arrays.at(array).at(index)=value; }
bool xsDoesUnitExist(int reference) { return units.count(reference)>0; }
float xsGetUnitHitpoints(int reference) { return units.at(reference).hp; }
int xsGetUnitOwner(int reference) { return units.at(reference).owner; }
int xsGetPlayerCivilization(int owner) { return civilizations.at(owner); }
float xsGetUnitAttribute(int reference,int attribute,int damageClass) {
    assert(attribute==9);
    assert(damageClass==3 || damageClass==4);
    return damageClass==4 ? units.at(reference).melee : units.at(reference).pierce;
}
void xsEffectAmount(int kind,int reference,int attribute,int amount,int player) {
    assert(kind==cAddUnitAttribute && attribute==9 && player==0);
    damage.emplace_back(reference,amount);
    int damageClass=amount/256, increment=amount%256;
    assert(increment==3);
    if(damageClass==3) units.at(reference).pierce+=increment;
    else { assert(damageClass==4); units.at(reference).melee+=increment; }
}
bool xsSetUnitName(int reference,const string& name) {
    if(rejectNextName) { rejectNextName=false; return false; }
    names[reference]=name; nameWrites[reference]++; return true;
}
'''
    main = r'''
int main() {
    // Colors 1/3/8 resolve to independent XS owners 7/2/4.
    units[101]={7,100,16,0};
    units[103]={2,100,0,12};
    units[108]={7,100,0,12}; // Wrong owner must not get color 8's name.
    variables[34]=1; variables[39]=1;
    ramCivilizationLeaderNames();
    assert(names.size()==1 && names.at(103)=="Robin Hood");
    assert(!names.count(101) && !names.count(108));
    variables[32]=1;
    rejectNextName=true;
    ramCivilizationLeaderNames();
    assert(!names.count(101)); // A failed native setter remains retryable.
    ramCivilizationLeaderNames();
    assert(names.at(101)=="Lithuanian Grand Duke");
    units.at(108).owner=4; units.at(108).hp=0;
    ramCivilizationLeaderNames();
    assert(!names.count(108)); // Existing but dead reference stays untouched.
    units.at(108).hp=100;
    ramCivilizationLeaderNames();
    assert(names.at(108)=="Danish Bow Jarl");
    for(int tick=0;tick<20;tick++) ramCivilizationLeaderNames();
    assert(nameWrites.at(101)==1 && nameWrites.at(103)==1 && nameWrites.at(108)==1);
    ramGrowLeader101();
    ramGrowLeader108();
    assert(damage.size()==2);
    assert(damage.at(0)==std::make_tuple(101,4*256+3));
    assert(damage.at(1)==std::make_tuple(108,3*256+3));
    assert(units.at(101).melee==19 && units.at(108).pierce==15);
    for(int cycle=0;cycle<7;cycle++) { ramGrowLeader101(); ramGrowLeader108(); }
    assert(units.at(101).melee==16+8*3 && units.at(108).pierce==12+8*3);
    assert(damage.size()==16);
    units.at(103).hp=0;
    ramGrowLeader103(); ramGrowLeader102();
    assert(damage.size()==16);
    // Persisted XS arrays and exact references resume without births or renaming.
    auto savedArrays=arrays;
    int savedHandle=gRamNamedLeaders;
    arrays=savedArrays; gRamNamedLeaders=savedHandle;
    ramCivilizationLeaderNames();
    assert(units.size()==3 && names.size()==3 && nameWrites.at(101)==1);
    assert(ramCivilizationLeaderName(0)=="Commander");
CATALOGUE_CHECKS
}
'''.replace("CATALOGUE_CHECKS", catalogue_checks)
    cpp = tmp_path / "leaders.cpp"
    cpp.write_text(prelude + source + "\n" + "\n".join(wrappers) + main)
    executable = tmp_path / "leaders"
    subprocess.run([compiler, "-std=c++17", "-O0", str(cpp), "-o", str(executable)],
                   check=True, capture_output=True, text=True)
    subprocess.run([str(executable)], check=True, capture_output=True, text=True)


def test_native_eight_second_plus_five_hp_growth_survives_leader_rebinding():
    from AoE2ScenarioParser.datasets.conditions import ConditionId
    from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

    _emitted_runtime()
    part = importlib.import_module("ram_leader_runtime_test_package.scenario.triggers.part_005")
    scenario = AoE2DEScenario.from_default()
    part.emit(scenario.trigger_manager)
    growth, = [t for t in scenario.trigger_manager.triggers if t.name == "ge kan"]
    timer, = [c for c in growth.conditions if c.condition_type == ConditionId.TIMER]
    assert growth.looping and timer.timer == 8
    hp = [e for e in growth.effects if e.effect_type == EffectId.CHANGE_OBJECT_HP]
    assert len(hp) == 8 and all(e.quantity == 5 for e in hp)
    before = [(e.quantity, e.operation, e.source_player, list(e.selected_object_ids)) for e in hp]
    units = {color: [SimpleNamespace(unit_const=731, reference_id=effect.selected_object_ids[0])]
             for color, effect in enumerate(hp, 1)}
    runtime = importlib.import_module("ram_leader_runtime_test_package.leader_runtime")
    runtime.configure_civilization_leaders(SimpleNamespace(
        mode_dir=MODE, um=SimpleNamespace(units=units),
        tm=SimpleNamespace(triggers=[growth]), add_xs=lambda *_args, **_kwargs: None))
    after = [(e.quantity, e.operation, e.source_player, list(e.selected_object_ids))
             for e in growth.effects if e.effect_type == EffectId.CHANGE_OBJECT_HP]
    assert after == before and timer.timer == 8 and growth.looping
