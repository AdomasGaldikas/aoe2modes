"""Filesystem locations: the repo layout and the game's own folders."""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from pathlib import Path

AOE2_STEAM_APP_ID = "813780"


def repo_root() -> Path:
    """Walk up from this file until the repo root (the dir holding ``pyproject.toml``)."""
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "pyproject.toml").is_file():
            return candidate
    # Installed as a wheel outside the repo: fall back to the working directory.
    return Path.cwd()


@dataclass(frozen=True)
class RepoPaths:
    root: Path

    @property
    def modes(self) -> Path:
        return self.root / "modes"

    @property
    def shared_xs(self) -> Path:
        return self.root / "xs"

    @property
    def dist(self) -> Path:
        return self.root / "dist"

    @property
    def template(self) -> Path:
        return self.modes / "_template"


def paths() -> RepoPaths:
    return RepoPaths(repo_root())


def _profile_roots() -> list[Path]:
    """Candidate ``Games/Age of Empires 2 DE`` parents for the current OS."""
    home = Path.home()
    system = platform.system()

    if system == "Windows":
        return [home]
    if system == "Darwin":
        return [
            home / "Library/Application Support/Steam/steamapps/compatdata"
            / AOE2_STEAM_APP_ID / "pfx/drive_c/users/steamuser",
            home,
        ]
    # Linux — the game runs through Proton, so the profile lives inside the prefix.
    prefix_users = [
        home / ".steam/steam/steamapps/compatdata" / AOE2_STEAM_APP_ID / "pfx/drive_c/users",
        home / ".local/share/Steam/steamapps/compatdata" / AOE2_STEAM_APP_ID / "pfx/drive_c/users",
    ]
    roots: list[Path] = []
    for users in prefix_users:
        roots += [users / "steamuser", users / os.environ.get("USER", "steamuser")]
    return roots


def find_game_scenario_dir() -> Path | None:
    """Locate the folder AoE2:DE reads user scenarios from, or ``None`` if not found.

    ``AOE2_SCENARIO_DIR`` always wins, which is the escape hatch for non-Steam installs,
    WSL, network drives and CI.
    """
    override = os.environ.get("AOE2_SCENARIO_DIR")
    if override:
        return Path(override).expanduser()

    for profile in _profile_roots():
        de_dir = profile / "Games" / "Age of Empires 2 DE"
        if not de_dir.is_dir():
            continue
        # The profile folder is the numeric Steam ID; pick the one that actually has scenarios.
        for user_dir in sorted(de_dir.iterdir()):
            scenario_dir = user_dir / "resources" / "_common" / "scenario"
            if scenario_dir.is_dir():
                return scenario_dir
    return None
