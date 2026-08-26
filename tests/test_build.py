"""End-to-end: every mode in the repo must build into a file the parser can read back."""

from __future__ import annotations

import pytest
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes.builder import build_mode, build_order


@pytest.fixture(scope="module")
def built(tmp_path_factory, request):
    """Build every mode and reload the output immediately, in newest-first order.

    Both the build and the round-trip check must happen before the next (older)
    scenario touches the parser, because AoE2ScenarioParser leaks version-scoped
    global state: once a v1.51 scenario is loaded, a subsequent v1.58 load raises
    ``UnsupportedAttributeError`` on ``execute_on_load``. Building and reloading
    together keeps every operation within one version window.
    """
    out = tmp_path_factory.mktemp("dist")
    specs = request.getfixturevalue("specs")
    results = {}
    for spec in build_order(specs):
        result = build_mode(spec, out_dir=out)
        reloaded = AoE2DEScenario.from_file(str(result.output))
        results[spec.id] = (result, reloaded)
    return results


def test_every_mode_builds(built, specs):
    assert set(built) == {spec.id for spec in specs}
    for result, _ in built.values():
        assert result.output.is_file()
        assert result.output.stat().st_size > 0


def test_results_are_non_trivial(built):
    for mode_id, (result, _) in built.items():
        assert result.triggers > 0, f"{mode_id} produced no triggers"
        assert result.units > 0, f"{mode_id} placed no units"


def test_output_reloads_with_expected_shape(built, specs):
    """Every mode's written file re-reads with the trigger/player/map shape it built with.

    Modes with ``scenario.base`` skip the ``map.size``/``players.count`` check because
    the builder skips the declarative phase for them and the TOML values in those
    blocks are informational only — the base file is authoritative.
    """
    by_id = {spec.id: spec for spec in specs}
    for mode_id, (result, scenario) in built.items():
        spec = by_id[mode_id]
        if spec.base is None:
            assert scenario.map_manager.map_size == spec.map.size
            assert scenario.player_manager.active_players == spec.players.count
        assert len(scenario.trigger_manager.triggers) == result.triggers


def test_xs_is_embedded(built, specs):
    by_id = {spec.id: spec for spec in specs}
    for mode_id, (result, _) in built.items():
        if not (by_id[mode_id].xs.include or by_id[mode_id].xs.scripts):
            continue
        assert result.xs_lines > 0, f"{mode_id} declares XS but embedded none"


def test_cba_hero_has_one_castle_and_hero_per_player(built):
    result, scenario = built["cba_hero"]
    players = result.spec.players
    for player in players.ids:
        owned = scenario.unit_manager.get_player_units(player)
        assert len(owned) == 2, f"player {int(player)} should start with a castle and a hero"
