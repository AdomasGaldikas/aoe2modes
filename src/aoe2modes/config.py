"""Declarative part of a mode: everything expressible in ``mode.toml``.

The split is deliberate. Anything that is "just settings" (map size, teams, starting
resources, which XS files to bundle) lives in TOML so it can be diffed and reviewed.
Anything that is logic (triggers, unit placement) lives in the mode's ``build.py``.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from AoE2ScenarioParser.datasets.object_support import StartingAge
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.scenario_variant import ScenarioVariant
from AoE2ScenarioParser.datasets.terrains import TerrainId


class ConfigError(ValueError):
    """Raised when a ``mode.toml`` is malformed."""


def _enum(enum_cls: Any, value: Any, field_name: str) -> Any:
    if isinstance(value, int):
        return enum_cls(value)
    try:
        return enum_cls[str(value).upper()]
    except KeyError as exc:
        options = ", ".join(sorted(m.name for m in enum_cls))
        raise ConfigError(f"{field_name}: unknown value {value!r}. Options: {options}") from exc


@dataclass(frozen=True)
class Resources:
    food: int = 0
    wood: int = 0
    gold: int = 0
    stone: int = 0

    def items(self) -> list[tuple[str, int]]:
        return [("food", self.food), ("wood", self.wood), ("gold", self.gold), ("stone", self.stone)]


@dataclass(frozen=True)
class MapSpec:
    size: int = 120
    terrain: TerrainId = TerrainId.GRASS_1
    elevation: int = 0


@dataclass(frozen=True)
class PlayersSpec:
    count: int = 8
    teams: tuple[tuple[PlayerId, ...], ...] = ()
    starting_age: StartingAge = StartingAge.CASTLE_AGE
    population_cap: int = 200
    lock_civilization: bool = False
    resources: Resources = field(default_factory=Resources)

    @property
    def ids(self) -> tuple[PlayerId, ...]:
        return tuple(PlayerId(i) for i in range(1, self.count + 1))

    def team_of(self, player: PlayerId) -> int:
        """1-based team index, or 0 when the player is not on a declared team."""
        for index, team in enumerate(self.teams, start=1):
            if player in team:
                return index
        return 0

    def opponents_of(self, player: PlayerId) -> tuple[PlayerId, ...]:
        team = self.team_of(player)
        if team == 0:
            return tuple(p for p in self.ids if p != player)
        return tuple(p for p in self.ids if self.team_of(p) not in (0, team))


@dataclass(frozen=True)
class XsSpec:
    """XS scripts to bundle, in order. Paths are repo-relative for ``include``,
    mode-relative for ``scripts``."""

    include: tuple[str, ...] = ()
    scripts: tuple[str, ...] = ()
    ignore_warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class ModeSpec:
    id: str
    name: str
    directory: Path
    version: str = "0.1.0"
    description: str = ""
    authors: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    base: Path | None = None
    scenario_version: str | None = None
    variant: ScenarioVariant = ScenarioVariant.AOE2
    filename: str = "{name}"
    map: MapSpec = field(default_factory=MapSpec)
    players: PlayersSpec = field(default_factory=PlayersSpec)
    xs: XsSpec = field(default_factory=XsSpec)

    @property
    def build_script(self) -> Path:
        return self.directory / "build.py"

    @property
    def output_stem(self) -> str:
        return self.filename.format(id=self.id, name=self.name, version=self.version)

    @property
    def output_name(self) -> str:
        return f"{self.output_stem}.aoe2scenario"


def _parse_teams(raw: Any, count: int) -> tuple[tuple[PlayerId, ...], ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not all(isinstance(team, list) for team in raw):
        raise ConfigError("players.teams must be a list of lists, e.g. [[1,2,3,4],[5,6,7,8]]")

    seen: set[int] = set()
    teams: list[tuple[PlayerId, ...]] = []
    for team in raw:
        members: list[PlayerId] = []
        for pid in team:
            if not isinstance(pid, int) or not 1 <= pid <= count:
                raise ConfigError(f"players.teams: player {pid!r} is outside 1..{count}")
            if pid in seen:
                raise ConfigError(f"players.teams: player {pid} appears on more than one team")
            seen.add(pid)
            members.append(PlayerId(pid))
        teams.append(tuple(members))
    return tuple(teams)


def load_mode_spec(directory: Path) -> ModeSpec:
    """Read and validate ``<directory>/mode.toml``."""
    toml_path = directory / "mode.toml"
    if not toml_path.is_file():
        raise ConfigError(f"No mode.toml in {directory}")

    with toml_path.open("rb") as handle:
        data = tomllib.load(handle)

    mode = data.get("mode", {})
    if "id" not in mode:
        raise ConfigError(f"{toml_path}: [mode] must define an 'id'")
    mode_id = str(mode["id"])
    if mode_id != directory.name:
        raise ConfigError(f"{toml_path}: mode.id {mode_id!r} must match its folder name {directory.name!r}")

    scenario = data.get("scenario", {})
    base_raw = scenario.get("base")
    base = None
    if base_raw:
        base = (directory / base_raw).resolve()
        if not base.is_file():
            raise ConfigError(f"{toml_path}: scenario.base not found at {base}")

    map_raw = data.get("map", {})
    map_spec = MapSpec(
        size=int(map_raw.get("size", 120)),
        terrain=_enum(TerrainId, map_raw.get("terrain", "GRASS_1"), "map.terrain"),
        elevation=int(map_raw.get("elevation", 0)),
    )
    if not 8 <= map_spec.size <= 480:
        raise ConfigError(f"{toml_path}: map.size {map_spec.size} is outside the supported 8..480 range")

    players_raw = data.get("players", {})
    count = int(players_raw.get("count", 8))
    if not 1 <= count <= 8:
        raise ConfigError(f"{toml_path}: players.count must be 1..8, got {count}")
    resources_raw = players_raw.get("resources", {})
    players_spec = PlayersSpec(
        count=count,
        teams=_parse_teams(players_raw.get("teams"), count),
        starting_age=_enum(
            StartingAge, players_raw.get("starting_age", "CASTLE_AGE"), "players.starting_age"
        ),
        population_cap=int(players_raw.get("population_cap", 200)),
        lock_civilization=bool(players_raw.get("lock_civilization", False)),
        resources=Resources(
            food=int(resources_raw.get("food", 0)),
            wood=int(resources_raw.get("wood", 0)),
            gold=int(resources_raw.get("gold", 0)),
            stone=int(resources_raw.get("stone", 0)),
        ),
    )

    xs_raw = data.get("xs", {})
    xs_spec = XsSpec(
        include=tuple(xs_raw.get("include", ())),
        scripts=tuple(xs_raw.get("scripts", ())),
        ignore_warnings=tuple(xs_raw.get("ignore_warnings", ())),
    )

    return ModeSpec(
        id=mode_id,
        name=str(mode.get("name", mode_id)),
        directory=directory,
        version=str(mode.get("version", "0.1.0")),
        description=str(mode.get("description", "")),
        authors=tuple(mode.get("authors", ())),
        tags=tuple(mode.get("tags", ())),
        base=base,
        scenario_version=scenario.get("version"),
        variant=_enum(ScenarioVariant, scenario.get("variant", "AOE2"), "scenario.variant"),
        filename=str(scenario.get("filename", "{name}")),
        map=map_spec,
        players=players_spec,
        xs=xs_spec,
    )
