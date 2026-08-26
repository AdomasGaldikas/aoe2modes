from __future__ import annotations

import pytest
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute

from aoe2modes.lib import heroes


def test_classic_pool_covers_eight_players():
    assert len(heroes.CLASSIC_LINES) == 8
    assigned = {heroes.CLASSIC_LINES.for_player(PlayerId(p)).key for p in range(1, 9)}
    assert assigned == set(heroes.CLASSIC_LINES.keys)


def test_tier_access_is_clamped():
    line = heroes.CLASSIC_LINES["paladin"]
    assert line.tier(1) is line.base
    assert line.tier(99) is line.top
    assert len(line.upgrades()) == len(line.tiers) - 1


def test_duplicate_keys_rejected():
    line = heroes.CLASSIC_LINES["paladin"]
    with pytest.raises(ValueError, match="duplicate"):
        heroes.HeroPool((line, line))


def test_empty_line_rejected():
    with pytest.raises(ValueError, match="no tiers"):
        heroes.HeroLine(key="x", label="X", tiers=())


def test_attack_must_go_through_buff_attack():
    class FakeTrigger:
        pass

    with pytest.raises(ValueError, match="per-damage-class"):
        heroes.buff(
            FakeTrigger(), PlayerId.ONE, heroes.CLASSIC_LINES["paladin"].top,
            ObjectAttribute.ATTACK, 5,
        )
