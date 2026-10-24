"""Balance tuning must be bounded, optional, and independent of player color."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ram_balance", ROOT / "modes/ram/civilization_balance.py")
balance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(balance)
BASELINE = {35: (1236, 60, 10), 43: (1792, 60, 8), 61: (2709, 80, 8), 62: (2712, 80, 8)}


def test_release_tunes_only_explicit_factions_and_preserves_unit_identity():
    ctx = SimpleNamespace(mode_dir=ROOT / "modes/ram")
    rules = balance.balanced_spawn_rules(ctx, BASELINE)
    assert rules == {35: (1236, 64, 10), 43: (1792, 60, 9), 61: (2709, 72, 9), 62: (2712, 80, 8)}
    assert BASELINE[35] == (1236, 60, 10)
    script = balance.render_civilization_balance(ctx, BASELINE)
    assert "xsGetPlayerCivilization(worldPlayer) == 35" in script
    assert "xsEffectAmount(cAddAttribute, 1236, 0, 8, worldPlayer);" in script
    assert "scenarioPlayer" not in script
    assert "cAttack" not in script


def test_disabled_balance_emits_no_stat_or_spawn_changes(tmp_path):
    (tmp_path / "mode.toml").write_text('[civilization_balance]\nenabled = false\n')
    ctx = SimpleNamespace(mode_dir=tmp_path)
    assert balance.balanced_spawn_rules(ctx, BASELINE) == BASELINE
    assert balance.render_civilization_balance(ctx, BASELINE) == ""


@pytest.mark.parametrize("row", [
    "civilization=99\narmy_cap=64", "civilization=35\narmy_cap=1000",
    "civilization=35\nspawn_seconds=0", "civilization=35\nhit_points_bonus=100",
    "civilization=35\narmy_cap=true",
])
def test_rejects_invalid_or_large_adjustments(tmp_path, row):
    (tmp_path / "mode.toml").write_text(
        '[civilization_balance]\nenabled=true\n[[civilization_balance.adjustments]]\n'
        + row + '\nreason="test"\n',
    )
    with pytest.raises(ValueError):
        balance.balanced_spawn_rules(SimpleNamespace(mode_dir=tmp_path), BASELINE)
