"""Combat-screen contracts; no claim that this reproduces native DE outcomes."""

import importlib.util
from copy import deepcopy
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "ram_army_balance", Path(__file__).resolve().parents[1] / "modes/ram/army_balance.py"
)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def unit(**changes):
    result = {
        "hp": 100.0,
        "speed": 1.0,
        "range": 0.0,
        "reload": 2.0,
        "attack": {4: 10.0},
        "armour": {3: 0.0, 4: 0.0},
        "cap": 60,
        "seconds": 10,
        "accuracy": 1.0,
        "projectiles": 1.0,
        "splash": 0.0,
        "unit_id": 100,
        "class": 6,
        "automatic_tech_candidates": [],
    }
    result.update(changes)
    return result


def test_armour_classes_preserve_counter_and_do_not_invent_damage_to_unrelated_classes():
    spear = unit(attack={4: 4, 8: 15})
    infantry = unit(armour={4: 1, 3: 0, 1: 0})
    cavalry = unit(armour={4: 1, 3: 0, 8: 0})
    assert a.hit_damage(spear, infantry) == 3
    assert a.hit_damage(spear, cavalry) == 18


def test_leitis_ignores_melee_armour_but_does_not_ignore_cavalry_counter_damage():
    leitis = unit(attack={4: 16}, ignore_armour=True, armour={4: 2, 3: 1, 8: 0})
    heavy = unit(armour={4: 8, 3: 2})
    assert a.hit_damage(leitis, heavy) == 16
    ordinary = deepcopy(leitis)
    ordinary["ignore_armour"] = False
    assert a.hit_damage(ordinary, heavy) == 8
    assert a.hit_damage(unit(attack={4: 4, 8: 15}), leitis) == 17


def test_secondary_projectiles_are_not_full_strength_primary_shots():
    shooter = unit(attack={3: 8}, range=5, projectiles=5)
    target = unit(armour={4: 0, 3: 2})
    assert a.damage_per_second(shooter, target) == 5


def test_special_charge_type_is_not_misread_as_infinite_damage():
    ordinary = unit()
    weird = unit(charge=1.0, recharge=1e18, charge_type=6)
    assert a.damage_per_second(weird, ordinary) == a.damage_per_second(ordinary, ordinary)
    charge = unit(charge=25.0, recharge=0.625, charge_type=1)
    assert a.damage_per_second(charge, ordinary) > a.damage_per_second(ordinary, ordinary)


def test_passive_civ_hp_bonus_requires_actual_prerequisite_and_native_target():
    base = unit(class_=12)
    base["class"] = 12
    base["automatic_tech_candidates"] = [
        {"id": 0, "requirements": [-1] * 6, "required_count": 0},
        {"id": 1, "requirements": [102, -1, -1, -1, -1, -1], "required_count": 1},
    ]
    techs = [{"civ": 9, "effect_id": 0}, {"civ": 9, "effect_id": 1}]
    techs += [{"civ": -1, "effect_id": -1} for _ in range(103)]
    snapshot = {
        "units": {9: base},
        "techs": techs,
        "effects": [
            {"commands": [{"type": 5, "a": -1, "b": 12, "c": 0, "d": 1.25}]},
            {"commands": [{"type": 4, "a": 100, "b": -1, "c": 9, "d": 1026.0}]},
        ],
    }
    early = a.apply_passive_technologies(snapshot)
    later = a.apply_passive_technologies(snapshot, age="castle")
    assert early[9]["hp"] == 125
    assert early[9]["attack"][4] == 10
    assert later[9]["attack"][4] == 12
    assert base["hp"] == 100


def test_mixed_team_trials_are_reproducible_and_use_distinct_lineups():
    units = {
        1: unit(),
        2: unit(hp=180, armour={4: 3, 3: 2}, speed=0.85),
        3: unit(hp=50, range=6, attack={3: 7}),
        4: unit(hp=70, range=4, attack={3: 5, 1: 8}),
    }
    first = a.mixed_team_screen(units, draws=4, team_sizes=(1, 2))
    assert first == a.mixed_team_screen(units, draws=4, team_sizes=(1, 2))
    assert len(first["trials"]) == 16
    for trial in first["trials"]:
        assert set(trial["left"]).isdisjoint(trial["right"])
    trial = next(t for t in first["trials"] if len(t["left"]) == 2)
    assert len(set(trial["left"] + trial["right"])) == 4


def test_mixed_team_combat_is_symmetric_under_side_swap_and_not_a_pure_mirror():
    frontline = unit(hp=200, attack={4: 14}, armour={4: 3, 3: 3}, speed=0.8)
    archer = unit(hp=40, attack={3: 7}, range=6)
    cavalry = unit(hp=120, attack={4: 12}, speed=1.4, armour={4: 2, 3: 2})
    skirmisher = unit(hp=50, attack={3: 4, 15: 6}, range=4)
    left = [frontline, archer]
    right = [cavalry, skirmisher]
    forward = a.simulate_teams(left, right, seconds=45)
    reverse = a.simulate_teams(right, left, seconds=45)
    assert forward["advantage"] == pytest.approx(-reverse["advantage"])
    assert forward["remaining_hp"] == pytest.approx(reverse["remaining_hp"][::-1])
    assert sum(forward["kills"]) > 0


def test_more_replacements_and_durability_improve_same_matchup_screen():
    baseline = unit()
    opponent = unit(range=3, attack={4: 10})
    stronger = unit(hp=118, cap=72, seconds=9)
    old = a.simulate_teams([baseline], [opponent], seconds=60)
    new = a.simulate_teams([stronger], [opponent], seconds=60)
    assert new["advantage"] > old["advantage"]


def test_all_civilization_rules_are_complete_and_bounded_without_changing_unit_identity():
    units = {1: unit(hp=40), 2: unit(hp=300, range=6)}
    rules = a.propose_rules(units)
    updated = a.with_rules(units, rules)
    assert set(rules) == set(units)
    for cid, row in rules.items():
        assert 0.75 <= row["army_cap"] / units[cid]["cap"] <= 1.25
        assert 0.75 <= row["spawn_seconds"] / units[cid]["seconds"] <= 1.25
        assert updated[cid]["attack"] == units[cid]["attack"]
        assert updated[cid]["range"] == units[cid]["range"]
    with pytest.raises(ValueError, match="every civilization"):
        a.with_rules(units, {1: rules[1]})


def test_composite_bowman_bypasses_pierce_armour_from_native_id_or_mechanics_bit():
    archer = unit(unit_id=1802, attack={3: 4}, range=4)
    heavy = unit(armour={4: 8, 3: 9})
    assert a.hit_damage(archer, heavy) == 4
    explicit = unit(attack={3: 7}, range=5, break_off_combat=1)
    assert a.hit_damage(explicit, heavy) == 7
    ordinary = unit(attack={3: 7}, range=5)
    assert a.hit_damage(ordinary, heavy) == 1


def test_half_population_caps_are_explicit_sensitivity_choices_not_engine_claims():
    karambit = unit(cap=60, population_per_body=0.5)
    assert a.unit_limit(karambit) == 60
    assert a.unit_limit(karambit, "population") == 120
    defaults = unit(cap=60)
    assert a.unit_limit(defaults, "population") == 60
    full_body = a.simulate_teams([karambit], [defaults], seconds=1, full_start=True)
    full_population = a.simulate_teams(
        [karambit], [defaults], seconds=1, full_start=True, cap_basis="population"
    )
    assert full_body["body_limits"][0] == [60]
    assert full_population["body_limits"][0] == [120]
    assert full_population["cap_basis"] == "population"
    with pytest.raises(ValueError, match="finite and positive"):
        a.unit_limit(unit(population_per_body=0))


def test_paired_rounds_give_each_civ_equal_exposure_in_every_lineup_position():
    units = {i: unit(hp=40 + i * 10, range=4 if i % 2 else 0) for i in range(1, 10)}
    report = a.mixed_team_screen(units, draws=19, team_sizes=(1, 2, 4))
    assert set(report["by_team_size"]) == {"1", "2", "4"}
    for size, section in report["by_team_size"].items():
        assert len(set(section["sample_count"].values())) == 1
        expected = section["paired_rounds"] * 4 * int(size)
        assert set(section["sample_count"].values()) == {expected}
        assert all(len(set(v)) == 1 for v in section["lineup_position_counts"].values())
        trials = section["trials"]
        for first, second in zip(trials[::2], trials[1::2], strict=True):
            assert first["left"] == second["right"]
            assert first["right"] == second["left"]
            assert first["normalized_hp_advantage"] == pytest.approx(-second["normalized_hp_advantage"])
            assert first["killfeed_advantage"] == pytest.approx(-second["killfeed_advantage"])


def test_fresh_build_up_and_full_field_are_distinct_scenarios():
    ordinary = unit()
    fresh = a.simulate_teams([ordinary], [ordinary], seconds=1)
    full = a.simulate_teams([ordinary], [ordinary], seconds=1, full_start=True)
    assert fresh["remaining_units"][0][0] == pytest.approx(0.4)
    assert full["remaining_units"][0][0] == 60
    assert fresh["kills"] == full["kills"] == [0, 0]
    assert fresh["remaining_hp_fraction"][0] < full["remaining_hp_fraction"][0]


def test_wide_contacts_allow_melee_to_use_more_of_its_existing_field_force():
    melee = unit(hp=100, attack={4: 10}, cap=100)
    ranged = unit(hp=40, attack={3: 6}, range=5, cap=100)
    frontal = a.simulate_teams([melee], [ranged], seconds=30, full_start=True, frontage=8)
    wide = a.simulate_teams([melee], [ranged], seconds=30, full_start=True, frontage=8, contact_mode="wide")
    assert wide["normalized_hp_advantage"] > frontal["normalized_hp_advantage"]


def test_equal_hp_trades_can_feed_unequal_native_hero_progress():
    small = unit(hp=50, attack={4: 5}, cap=40, seconds=100)
    large = unit(hp=100, attack={4: 10}, cap=20, seconds=100)
    outcome = a.simulate_teams([small], [large], seconds=15, full_start=True, frontage=100)
    assert outcome["kills"][1] > outcome["kills"][0] * 1.5
    assert outcome["hp_per_kill"] == pytest.approx([100, 50])
    assert outcome["hp_trade_ratio"] == pytest.approx(1, abs=0.08)
    assert outcome["kill_trade_ratio"] < 0.65
    assert outcome["enemy_hero_kills_fed"] == outcome["kills"][::-1]
