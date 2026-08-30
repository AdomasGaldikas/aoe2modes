from __future__ import annotations

from pathlib import Path

import aoe2modes.paths as paths_module


def _scenario_dir(profile_root: Path, profile_name: str) -> Path:
    directory = (
        profile_root
        / "Games"
        / "Age of Empires 2 DE"
        / profile_name
        / "resources"
        / "_common"
        / "scenario"
    )
    directory.mkdir(parents=True)
    return directory


def test_find_game_scenario_dir_prefers_real_steam_profile(tmp_path, monkeypatch):
    _scenario_dir(tmp_path, "0")
    steam_profile = _scenario_dir(tmp_path, "76561198817496389")

    monkeypatch.delenv("AOE2_SCENARIO_DIR", raising=False)
    monkeypatch.setattr(paths_module, "_profile_roots", lambda: [tmp_path])

    assert paths_module.find_game_scenario_dir() == steam_profile.resolve()


def test_find_game_scenario_dir_honors_override(tmp_path, monkeypatch):
    override = tmp_path / "custom-scenarios"
    monkeypatch.setenv("AOE2_SCENARIO_DIR", str(override))

    assert paths_module.find_game_scenario_dir() == override
