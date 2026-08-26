"""Discovery of the modes that live under ``modes/``."""

from __future__ import annotations

from pathlib import Path

from aoe2modes.config import ConfigError, ModeSpec, load_mode_spec
from aoe2modes.paths import RepoPaths, paths

# Folders under modes/ that are scaffolding rather than buildable modes.
IGNORED_PREFIXES = ("_", ".")


def is_mode_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and not path.name.startswith(IGNORED_PREFIXES)
        and (path / "mode.toml").is_file()
    )


def discover(repo: RepoPaths | None = None) -> list[ModeSpec]:
    """All valid modes, sorted by id. Invalid ones raise rather than being skipped
    silently — a typo'd mode.toml should be loud."""
    repo = repo or paths()
    if not repo.modes.is_dir():
        return []
    return sorted(
        (load_mode_spec(entry) for entry in repo.modes.iterdir() if is_mode_dir(entry)),
        key=lambda spec: spec.id,
    )


def get(mode_id: str, repo: RepoPaths | None = None) -> ModeSpec:
    repo = repo or paths()
    directory = repo.modes / mode_id
    if not is_mode_dir(directory):
        known = ", ".join(spec.id for spec in discover(repo)) or "(none)"
        raise ConfigError(f"Unknown mode {mode_id!r}. Available: {known}")
    return load_mode_spec(directory)
