"""Player, team and diplomacy setup."""

from __future__ import annotations

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import DiplomacyState
from AoE2ScenarioParser.objects.managers.player_manager import PlayerManager

from aoe2modes.config import PlayersSpec, Resources


def apply_players_spec(pm: PlayerManager, spec: PlayersSpec) -> None:
    """Turn the declarative ``[players]`` block into scenario state."""
    pm.active_players = spec.count

    for player_id in spec.ids:
        player = pm.players[player_id]
        player.starting_age = spec.starting_age
        player.population_cap = spec.population_cap
        player.lock_civ = spec.lock_civilization
        set_resources(pm, player_id, spec.resources)

    apply_teams(pm, spec)


def set_resources(pm: PlayerManager, player_id: PlayerId, resources: Resources) -> None:
    player = pm.players[player_id]
    for name, amount in resources.items():
        setattr(player, name, amount)


def apply_teams(pm: PlayerManager, spec: PlayersSpec) -> None:
    """Ally within each declared team, enemy across teams.

    ``set_diplomacy_teams`` handles the within/across split in one call, so teams
    declared in mode.toml map straight onto it.
    """
    if not spec.teams:
        return
    pm.set_diplomacy_teams(*[list(team) for team in spec.teams], diplomacy=DiplomacyState.ALLY)


def set_camera(pm: PlayerManager, player_id: PlayerId, x: int, y: int) -> None:
    """Point a player's opening camera at a tile (their base, usually).

    ``initial_camera_*`` is deprecated and unused by the game; the view fields are
    the ones the scenario actually reads.
    """
    player = pm.players[player_id]
    player.initial_player_view_x = x
    player.initial_player_view_y = y
