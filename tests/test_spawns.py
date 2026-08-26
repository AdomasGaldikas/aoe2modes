from __future__ import annotations

from AoE2ScenarioParser.datasets.players import PlayerId

from aoe2modes.config import PlayersSpec
from aoe2modes.lib import spawns


def make_players(count=8, teams=((1, 2, 3, 4), (5, 6, 7, 8))):
    return PlayersSpec(
        count=count,
        teams=tuple(tuple(PlayerId(p) for p in team) for team in teams),
    )


def test_lane_bases_are_mirrored():
    size = 144
    bases = spawns.lane_bases(make_players(), size)
    assert len(bases) == 8

    west = [b for b in bases.values() if b.team == 1]
    east = [b for b in bases.values() if b.team == 2]
    # Each team lines up on its own side of the map.
    assert all(b.center.x < size / 2 for b in west)
    assert all(b.center.x > size / 2 for b in east)
    # And the two lines mirror each other around the centre.
    assert sorted(b.center.y for b in west) == sorted(b.center.y for b in east)


def test_castle_is_behind_and_spawn_is_in_front():
    bases = spawns.lane_bases(make_players(), 144)
    for base in bases.values():
        outward = base.castle.x < base.center.x if base.team == 1 else base.castle.x > base.center.x
        inward = base.spawn.x > base.center.x if base.team == 1 else base.spawn.x < base.center.x
        assert outward, "castle should sit further from the middle than the player centre"
        assert inward, "spawn should sit closer to the middle than the player centre"


def test_everything_stays_on_the_map():
    size = 96
    for players in (make_players(), make_players(2, ((1,), (2,)))):
        for base in spawns.lane_bases(players, size).values():
            for tile in (base.center, base.castle, base.spawn, base.target):
                assert 0 <= tile.x < size and 0 <= tile.y < size


def test_ring_bases_used_when_not_two_teams():
    players = PlayersSpec(count=5, teams=())
    bases = spawns.lane_bases(players, 120)
    assert len(bases) == 5
    # A free-for-all points everyone at the middle.
    assert len({base.target for base in bases.values()}) == 1


def test_block_and_line_shapes():
    origin = spawns.Tile(10, 10)
    assert len(spawns.block(origin, columns=4, rows=3, map_size=120)) == 12
    row = spawns.line(spawns.Tile(0, 0), spawns.Tile(10, 0), 6, 120)
    assert [t.x for t in row] == [0, 2, 4, 6, 8, 10]
