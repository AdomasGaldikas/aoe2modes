"""Arena geometry: where each player's base, castle and unit spawn sit.

CBA-style maps are symmetric by construction, so the layouts here are computed from
the map size rather than hand-placed. Change ``map.size`` in mode.toml and every base,
castle and spawn point moves with it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.support.tile import Tile

from aoe2modes.config import PlayersSpec


@dataclass(frozen=True)
class Base:
    """One player's corner of the arena."""

    player: PlayerId
    team: int
    center: Tile
    castle: Tile
    spawn: Tile
    target: Tile
    """Where this player's units should attack-move to — the enemy side of the arena."""

    @property
    def camera(self) -> Tile:
        return self.center


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _tile(x: float, y: float, map_size: int) -> Tile:
    limit = map_size - 1
    return Tile(_clamp(int(round(x)), 0, limit), _clamp(int(round(y)), 0, limit))


def lane_bases(
    players: PlayersSpec,
    map_size: int,
    *,
    margin: int = 12,
    castle_offset: int = 6,
    spawn_offset: int = 10,
) -> dict[PlayerId, Base]:
    """Two facing lines of players — the classic CBA layout.

    Team 1 lines up along the west edge, team 2 along the east edge, each player
    evenly spaced along the north-south axis. Castles sit *behind* each player's
    centre (further from the middle), unit spawns sit *in front* of it.

    Falls back to :func:`ring_bases` when the mode does not declare exactly two teams.
    """
    if len(players.teams) != 2:
        return ring_bases(players, map_size)

    centre = (map_size - 1) / 2
    bases: dict[PlayerId, Base] = {}

    for team_index, team in enumerate(players.teams):
        # -1 for the west line, +1 for the east line.
        direction = -1 if team_index == 0 else 1
        x = centre + direction * (centre - margin)
        step = (map_size - 2 * margin) / (len(team) + 1)

        for slot, player in enumerate(team, start=1):
            y = margin + step * slot
            base_center = _tile(x, y, map_size)
            bases[player] = Base(
                player=player,
                team=team_index + 1,
                center=base_center,
                castle=_tile(x + direction * castle_offset, y, map_size),
                spawn=_tile(x - direction * spawn_offset, y, map_size),
                target=_tile(centre - direction * (centre - margin), y, map_size),
            )
    return bases


def ring_bases(
    players: PlayersSpec,
    map_size: int,
    *,
    margin: int = 12,
    castle_offset: int = 6,
    spawn_offset: int = 10,
) -> dict[PlayerId, Base]:
    """Players spaced evenly around a circle, all facing the middle.

    Works for any player count, and is the sane default for free-for-all modes.
    """
    centre = (map_size - 1) / 2
    radius = centre - margin
    ids = players.ids
    bases: dict[PlayerId, Base] = {}

    for index, player in enumerate(ids):
        angle = 2 * math.pi * index / len(ids)
        dx, dy = math.cos(angle), math.sin(angle)
        x, y = centre + radius * dx, centre + radius * dy
        bases[player] = Base(
            player=player,
            team=players.team_of(player),
            center=_tile(x, y, map_size),
            castle=_tile(x + dx * castle_offset, y + dy * castle_offset, map_size),
            spawn=_tile(x - dx * spawn_offset, y - dy * spawn_offset, map_size),
            target=_tile(centre, centre, map_size),
        )
    return bases


def line(start: Tile, end: Tile, count: int, map_size: int) -> list[Tile]:
    """``count`` tiles spread evenly between two points — handy for unit rows."""
    if count <= 1:
        return [start]
    return [
        _tile(
            start.x + (end.x - start.x) * i / (count - 1),
            start.y + (end.y - start.y) * i / (count - 1),
            map_size,
        )
        for i in range(count)
    ]


def block(origin: Tile, columns: int, rows: int, map_size: int, *, spacing: int = 1) -> list[Tile]:
    """A rectangular formation anchored at ``origin`` — used for spawning a wave."""
    return [
        _tile(origin.x + col * spacing, origin.y + row * spacing, map_size)
        for row in range(rows)
        for col in range(columns)
    ]
