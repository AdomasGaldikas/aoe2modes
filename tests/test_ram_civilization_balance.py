"""All-civilization decisions and owner-aware native stat edits remain explicit."""

import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

MODULE = Path(__file__).resolve().parents[1] / "modes/ram/civilization_balance.py"
spec = importlib.util.spec_from_file_location("ram_balance_config", MODULE)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
BASE = {9: (556, 68, 12), 14: (771, 60, 10), 35: (1236, 60, 10)}


def context(tmp_path, rows, enabled=True):
    text = "[civilization_balance]\nenabled = " + str(enabled).lower() + "\n"
    for row in rows:
        text += "\n[[civilization_balance.adjustments]]\n"
        for k, v in row.items():
            text += f'{k} = "{v}"\n' if isinstance(v, str) else f"{k} = {v}\n"
    (tmp_path / "mode.toml").write_text(text)
    return SimpleNamespace(mode_dir=tmp_path)


def rows():
    return [
        {"civilization": 9, "army_cap": 56, "spawn_seconds": 14, "reason": "Reported excessive camel mass."},
        {
            "civilization": 14,
            "army_cap": 48,
            "spawn_seconds": 12,
            "reason": "Reported excessive gunpowder mass.",
        },
        {
            "civilization": 35,
            "army_cap": 72,
            "spawn_seconds": 9,
            "hit_points_bonus": 18,
            "reason": "Reported insufficient mounted frontline.",
        },
    ]


def test_live_report_changes_preserve_native_ids_and_keep_other_stats_out_of_xs(tmp_path):
    ctx = context(tmp_path, rows())
    assert b.balanced_spawn_rules(ctx, BASE) == {9: (556, 56, 14), 14: (771, 48, 12), 35: (1236, 72, 9)}
    source = b.render_civilization_balance(ctx, BASE)
    assert "xsGetPlayerCivilization(worldPlayer) == 35" in source
    assert "cAddAttribute, 1236, 0, 18, worldPlayer" in source
    assert source.count("xsEffectAmount") == 1
    assert BASE[35] == (1236, 60, 10)


def test_enabled_review_requires_every_civilization_and_detects_new_civ(tmp_path):
    ctx = context(tmp_path, rows()[:-1])
    with pytest.raises(ValueError, match="every civilization"):
        b.balanced_spawn_rules(ctx, BASE)
    ctx = context(tmp_path, rows())
    with pytest.raises(ValueError, match="missing="):
        b.balanced_spawn_rules(ctx, {**BASE, 63: (2800, 80, 8)})


def test_disabled_balance_is_a_complete_noop(tmp_path):
    ctx = context(tmp_path, [], enabled=False)
    assert b.balanced_spawn_rules(ctx, BASE) == BASE
    assert b.render_civilization_balance(ctx, BASE) == ""


@pytest.mark.parametrize(
    "mutation",
    [
        {"civilization": 99},
        {"army_cap": 1000},
        {"spawn_seconds": 0},
        {"hit_points_bonus": 21},
        {"hit_points_bonus": -1},
        {"army_cap": True},
        {"reason": " "},
        {"attack_bonus": 20},
    ],
)
def test_out_of_scope_or_unbounded_edits_are_rejected(tmp_path, mutation):
    data = rows()
    data[-1].update(mutation)
    with pytest.raises(ValueError):
        b.balanced_spawn_rules(context(tmp_path, data), BASE)


def test_release_reports_are_applied_without_changing_native_unit_identity():
    root = Path(__file__).resolve().parents[1]
    tree = ast.parse((root / "modes/ram/build.py").read_text())
    baseline = next(
        ast.literal_eval(n.value)
        for n in tree.body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "CIV_SPAWN_RULES" for t in n.targets)
    )
    ctx = SimpleNamespace(mode_dir=root / "modes/ram")
    rules = b.balanced_spawn_rules(ctx, baseline)
    assert set(rules) == set(baseline)
    assert rules[9] == (556, 56, 14)
    assert rules[14] == (771, 48, 12)
    assert rules[35] == (1236, 72, 9)
    assert rules[43] == (1792, 56, 10)
    assert rules[61] == (2709, 64, 10)
    assert all(rules[civ][0] == baseline[civ][0] for civ in baseline)
    source = b.render_civilization_balance(ctx, baseline)
    assert "cAddAttribute, 1236, 0, 18, worldPlayer" in source
    import tomllib

    rows = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())["civilization_balance"]["adjustments"]
    assert source.count("xsEffectAmount") == sum(row.get("hit_points_bonus", 0) > 0 for row in rows)



def test_whole_roster_report_matches_shipped_targets_and_preserves_pace():
    import json
    import tomllib

    mode = Path(__file__).resolve().parents[1] / "modes/ram"
    rows = tomllib.loads((mode / "mode.toml").read_text())["civilization_balance"]["adjustments"]
    review = json.loads((mode / "assets/balance/review.json").read_text())
    inputs = json.loads((mode / "assets/balance/screen-inputs.json").read_text())
    targets = {row["civilization"]: row for row in rows}
    assert set(targets) == set(range(1, 63))
    before_rate = after_rate = 0
    for row in review["rules"]:
        target = targets[row["civilization"]]
        for field in ("army_cap", "spawn_seconds", "reason"):
            assert target[field] == row[field]
        assert target.get("hit_points_bonus", 0) == row["hit_points_bonus"]
        assert row["role"] and row["native_mechanics_note"]
        native = inputs["units"][str(row["civilization"])]
        assert row["unit_id"] == native["unit_id"]
        # Small flat additions support survival without turning glass units into tanks.
        assert 0 <= row["hit_points_bonus"] <= 0.20 * native["hp"]
        before_rate += 4 / row["previous"]["spawn_seconds"]
        after_rate += 4 / row["spawn_seconds"]
    assert 0.95 <= after_rate / before_rate <= 1.05
    assert inputs["units"]["44"]["ignore_armour"] is True
    assert inputs["units"]["35"]["ignore_armour"] is True
    assert inputs["units"]["29"]["population_per_body"] == 0.5
