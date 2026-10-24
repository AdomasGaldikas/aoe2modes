"""The complete leader catalog must select land combat units and flag proxies."""

import importlib.util
import json
import math
import tomllib
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODE = ROOT / "modes/ram"
SPEC = importlib.util.spec_from_file_location("ram_leaders", MODE / "civilization_leaders.py")
leaders = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(leaders)


def test_every_leader_keeps_the_original_population_cost_without_economic_prices():
    original = (SimpleNamespace(type=1, amount=55, flag=1), SimpleNamespace(type=3, amount=65, flag=1),
                SimpleNamespace(type=4, amount=1, flag=0))
    costs = leaders._leader_costs(original)
    assert [(cost.type, cost.amount, cost.flag) for cost in costs] == [(1, 0, 1), (3, 0, 1), (4, 1, 0)]
    assert original[0].amount == 55 and original[1].amount == 65


def test_complete_catalog_and_requested_native_leaders():
    rows = leaders.load_leader_catalog(MODE)
    catalog = {row["civilization"]: row for row in rows}
    assert set(catalog) == set(range(1, 63))
    assert (catalog[1]["leader_name"], catalog[1]["source_unit_id"]) == ("Robin Hood", 200)
    assert (catalog[35]["leader_name"], catalog[35]["source_unit_id"]) == ("Lithuanian Grand Duke", 2701)
    assert catalog[12]["source_unit_id"] == 731
    assert catalog[60]["source_unit_id"] == 2701
    assert catalog[61]["source_unit_id"] == 2700
    assert not {203, 844} & {row["source_unit_id"] for row in rows}  # Both are ships.
    assert all(row["note"] for row in rows if row["fallback"])
    assert {row["role"] for row in rows} == {"ranged", "ranged_cavalry"}
    voices = json.loads((MODE / "assets/selection_audio/manifest.json").read_text())
    assert {row["civilization"]: row["civilization_name"] for row in rows} == {
        row["id"]: row["name"] for row in voices["civilizations"]
    }


@pytest.mark.parametrize("change", ["duplicate", "invalid_role", "missing_note"])
def test_rejects_ambiguous_or_undocumented_catalog(tmp_path, change):
    data = json.loads((MODE / "assets/leaders/catalog.json").read_text())
    if change == "duplicate":
        data["civilizations"].append(data["civilizations"][0])
    elif change == "invalid_role":
        data["civilizations"][0]["role"] = "ship"
    else:
        data["civilizations"][0]["note"] = ""
    path = tmp_path / "assets/leaders/catalog.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        leaders.load_leader_catalog(tmp_path)


def test_every_catalog_actor_has_a_documented_native_bow_or_firearm():
    rows = leaders.load_leader_catalog(MODE)
    assert len({row["source_unit_id"] for row in rows}) >= 30
    assert {row["weapon"] for row in rows} == {"bow", "crossbow", "firearm"}
    # These native heroes use melee, thrown axes/javelins/scimitars, or a sling.
    # They cannot meet the all-bow/firearm request by just changing range stats.
    excluded = {173, 1281, 165, 424, 426, 1036, 1075, 1296, 1298, 2721}
    assert not excluded & {row["source_unit_id"] for row in rows}
    for row in rows:
        assert row["source_projectile_unit_id"] >= 0
        assert row["source_attack_graphic"] >= 0
        assert row["source_projectile_unit_id"] not in {365, 366, 515, 736, 187, 1055, 2719, 2623}
    catalog = {row["civilization"]: row for row in rows}
    assert catalog[27]["source_unit_id"] == 1034  # Musa has a bow; Tariq throws javelins.
    assert catalog[50]["source_unit_id"] == 2042  # Native Wu mounted bow hero.
    assert catalog[59]["source_unit_id"] == 2642  # Native Arariboia bow variant.
    assert catalog[35]["fallback"] and "Vytautas" in catalog[35]["note"]


def _profile():
    return {"hit_points": 300, "attack": 25, "reload_seconds": 2.0, "melee_armour": 2,
            "pierce_armour": 2, "range": 5.0, "speed": 1.4, "accuracy_percent": 100}


def _donor():
    return SimpleNamespace(
        class_=0, hit_points=45, speed=0.8, line_of_sight=4.0,
        standing_graphic=(12, -1), dying_graphic=13,
        dead_fish=SimpleNamespace(walking_graphic=14, running_graphic=15),
        creatable=SimpleNamespace(displayed_pierce_armour=0),
        type_50=SimpleNamespace(projectile_unit_id=511, attack_graphic=16, max_range=6.0,
                                attacks=[SimpleNamespace(class_=3, amount=8)],
                                armours=[SimpleNamespace(class_=1, amount=4)], base_armor=0),
        selection_sound=11, wwise_selection_sound_id=111,
        bird=SimpleNamespace(tasks=[SimpleNamespace(action_type=7)], move_sound=22,
                             attack_sound=33, wwise_move_sound_id=222, wwise_attack_sound_id=333),
    )


def test_equal_profiles_and_native_visuals_survive_common_counter_normalization():
    settings = tomllib.loads((MODE / "mode.toml").read_text())["civilization_leaders"]
    assert leaders._profiles(settings) == {role: _profile() for role in leaders.ROLES}
    donor = _donor()
    original_visuals = leaders._native_visuals(donor)
    clone = deepcopy(donor)
    khan = SimpleNamespace(class_=36, type_50=SimpleNamespace(base_armor=10000, armours=[
        SimpleNamespace(class_=3, amount=0), SimpleNamespace(class_=4, amount=0),
        SimpleNamespace(class_=19, amount=0)]))
    leaders._copy_counter_template(clone, khan)
    leaders._normalise_ranged_stats(clone, _profile())
    assert clone.class_ == 36 and clone.type_50.base_armor == 10000
    assert {a.class_: a.amount for a in clone.type_50.armours} == {3: 2, 4: 2, 19: 0}
    assert {a.class_: a.amount for a in khan.type_50.armours} == {3: 0, 4: 0, 19: 0}
    assert [(a.class_, a.amount) for a in clone.type_50.attacks] == [(3, 25)]
    assert clone.hit_points == 300 and math.isclose(clone.speed, 1.4)
    assert clone.type_50.max_range == clone.type_50.displayed_range == 5
    assert clone.type_50.min_range == 0 and clone.line_of_sight >= 7
    assert clone.type_50.accuracy_percent == 100 and clone.type_50.accuracy_dispersion == 0
    assert clone.type_50.reload_time == clone.type_50.displayed_reload_time == 2
    assert leaders._native_visuals(clone) == original_visuals
    assert donor.class_ == 0 and donor.hit_points == 45 and donor.type_50.attacks[0].amount == 8


def test_three_custom_acknowledgements_leave_native_wwise_fallbacks_untouched():
    clone, voice = _donor(), _donor()
    voice.selection_sound, voice.bird.move_sound, voice.bird.attack_sound = 701, 702, 703
    voice.wwise_selection_sound_id, voice.bird.wwise_move_sound_id = 9991, 9992
    voice.bird.wwise_attack_sound_id = 9993
    leaders._copy_acknowledgements(clone, voice)
    assert leaders._acknowledgement_groups(clone) == {"selection": 701, "move": 702, "attack": 703}
    assert leaders._wwise_fallbacks(clone) == {"selection": 111, "move": 222, "attack": 333}


@pytest.mark.parametrize(("field", "value"), [("range", 0), ("range", 21), ("speed", 0),
                                                ("speed", float("nan")),
                                                ("accuracy_percent", 101),
                                                ("accuracy_percent", 99.5)])
def test_rejects_unbounded_leader_combat_profiles(field, value):
    profile = _profile()
    profile[field] = value
    with pytest.raises(ValueError):
        leaders._profiles({"profiles": {role: deepcopy(profile) for role in leaders.ROLES}})


def test_rejects_unequal_profiles_and_changed_native_actor_snapshots():
    with pytest.raises(ValueError, match="identical"):
        leaders._profiles({"profiles": {"ranged": _profile(),
                                        "ranged_cavalry": {**_profile(), "attack": 26}}})
    row = {"role": "ranged", "weapon": "bow",
           "source_projectile_unit_id": 511, "source_attack_graphic": 16}
    donor = _donor()
    leaders._validate_ranged_donor(donor, row, 1)
    donor.type_50.attack_graphic = 17
    with pytest.raises(ValueError, match="differs"):
        leaders._validate_ranged_donor(donor, row, 1)
    donor.type_50.attack_graphic = 16
    donor.type_50.projectile_unit_id = 515
    with pytest.raises(ValueError):
        leaders._validate_ranged_donor(donor, {**row, "source_projectile_unit_id": 515}, 1)
