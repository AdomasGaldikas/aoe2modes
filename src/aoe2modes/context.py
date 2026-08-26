"""The object every mode's ``build(ctx)`` receives."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from AoE2ScenarioParser.objects.managers.map_manager import MapManager
from AoE2ScenarioParser.objects.managers.message_manager import MessageManager
from AoE2ScenarioParser.objects.managers.player_manager import PlayerManager
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.objects.managers.unit_manager import UnitManager
from AoE2ScenarioParser.objects.managers.xs_manager import XsManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes.config import ModeSpec, PlayersSpec
from aoe2modes.paths import RepoPaths


@dataclass
class BuildContext:
    """Everything a mode needs to assemble itself.

    Managers are exposed under both their long and short names because trigger-heavy
    build scripts read much better as ``ctx.tm.add_trigger(...)``.
    """

    spec: ModeSpec
    scenario: AoE2DEScenario
    repo: RepoPaths
    verbose: bool = False
    xs_chunks: list[tuple[str, str]] = field(default_factory=list)
    xs_vars: dict[str, object] = field(default_factory=dict)
    """Build-time constants substituted into ``${NAME}`` placeholders in XS sources."""

    # --- managers -------------------------------------------------------------
    @property
    def trigger_manager(self) -> TriggerManager:
        return self.scenario.trigger_manager

    @property
    def unit_manager(self) -> UnitManager:
        return self.scenario.unit_manager

    @property
    def map_manager(self) -> MapManager:
        return self.scenario.map_manager

    @property
    def player_manager(self) -> PlayerManager:
        return self.scenario.player_manager

    @property
    def xs_manager(self) -> XsManager:
        return self.scenario.xs_manager

    @property
    def message_manager(self) -> MessageManager:
        return self.scenario.message_manager

    tm = trigger_manager
    um = unit_manager
    mm = map_manager
    pm = player_manager
    xm = xs_manager

    # --- convenience ----------------------------------------------------------
    @property
    def players(self) -> PlayersSpec:
        return self.spec.players

    @property
    def map_size(self) -> int:
        return self.map_manager.map_size

    @property
    def mode_dir(self) -> Path:
        return self.spec.directory

    def log(self, message: str) -> None:
        if self.verbose:
            print(f"    {message}")

    def add_xs(self, source: str, *, label: str = "inline") -> None:
        """Append raw XS source to the bundle that gets embedded on write."""
        self.xs_chunks.append((label, source))

    def set_xs_vars(self, **values: object) -> None:
        """Expose build-time constants to the mode's XS files."""
        self.xs_vars.update(values)
