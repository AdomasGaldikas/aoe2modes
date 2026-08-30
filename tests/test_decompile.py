"""The decompiler's contract: generated source must rebuild the scenario it came from.

The end-to-end test deliberately uses ``evolution_alpha``. Its generated package is
the direct decompilation of a v1.58 reference; the public Ascendants build applies
intentional gameplay and map patches after that generated baseline.
"""

from __future__ import annotations

import importlib.util
import sys

import pytest
from AoE2ScenarioParser.datasets.object_support import Civilization
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.scenario_variant import ScenarioVariant
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes import registry
from aoe2modes.context import BuildContext
from aoe2modes.lib.decompile import comment_safe, decompile, render
from aoe2modes.lib.verify import compare, snapshot


class TestRender:
    def test_players_become_named_constants(self):
        assert render(1, field_name="source_player") == "PlayerId.ONE"
        assert render(0, field_name="target_player") == "PlayerId.GAIA"

    def test_object_ids_resolve_against_the_info_datasets(self):
        assert render(4, field_name="object_list_unit_id") == "UnitInfo.ARCHER.ID"

    def test_unknown_field_names_stay_numeric(self):
        assert render(4, field_name="quantity") == "4"

    def test_negative_sentinels_are_never_resolved(self):
        """``-1`` means "unset" everywhere; resolving it would invent a constant."""
        assert render(-1, field_name="object_list_unit_id") == "-1"

    def test_non_int_enums_render_as_source_not_repr(self):
        """``Civilization`` is a plain Enum, so repr() would emit invalid Python."""
        assert render(Civilization.BYZANTINES) == "Civilization.BYZANTINES"

    def test_int_enums_outside_the_import_list_degrade_to_their_value(self):
        assert render(ScenarioVariant.ROR, field_name="quantity") == repr(int(ScenarioVariant.ROR))

    def test_whole_floats_render_as_ints(self):
        assert render(3.0) == "3"
        assert render(3.5) == "3.5"

    def test_player_id_enum_still_renders_by_name(self):
        assert render(PlayerId.THREE, field_name="source_player") == "PlayerId.THREE"


class TestCommentSafe:
    def test_carriage_return_is_escaped(self):
        """A bare CR inside a comment ends the line in Python source and breaks indentation."""
        assert "\r" not in comment_safe("Gurjaras (p1)\r (p1)")
        assert "\\r" in comment_safe("Gurjaras (p1)\r (p1)")

    def test_long_names_are_truncated(self):
        assert len(comment_safe("x" * 200)) == 70

    def test_ordinary_names_pass_through(self):
        assert comment_safe("Wave — P3") == "Wave — P3"


@pytest.fixture(scope="module")
def evolution_rebuild(tmp_path_factory, repo):
    spec = registry.get("evolution_alpha", repo)
    if spec.reference is None:
        pytest.skip("evolution_alpha has no scenario.reference to verify against")

    original = AoE2DEScenario.from_file(str(spec.reference))
    generated_dir = tmp_path_factory.mktemp("decompile") / "generated"
    decompile(original, generated_dir, source_label=spec.reference.name)

    scenario = AoE2DEScenario.from_default(spec.scenario_version)
    scenario.variant = spec.variant
    ctx = BuildContext(spec=spec, scenario=scenario, repo=repo)
    module_name = "aoe2modes._test_generated.evolution_alpha"
    loader_spec = importlib.util.spec_from_file_location(
        module_name,
        generated_dir / "__init__.py",
        submodule_search_locations=[str(generated_dir)],
    )
    assert loader_spec is not None and loader_spec.loader is not None
    module = importlib.util.module_from_spec(loader_spec)
    sys.modules[module_name] = module
    loader_spec.loader.exec_module(module)
    module.apply(ctx)

    return snapshot(scenario), snapshot(original)


def test_generated_source_rebuilds_the_original(evolution_rebuild):
    rebuilt, original = evolution_rebuild
    report = compare(original, rebuilt)
    assert report.checked > 10_000, "comparison covered suspiciously little"
    assert report.differences[:5] == []
    assert report.ok


def test_rebuild_has_no_version_gap(evolution_rebuild):
    """Same version on both sides, so every field should exist on both."""
    rebuilt, original = evolution_rebuild
    report = compare(original, rebuilt)
    assert report.version_only_total == 0, dict(report.version_only)


def test_trigger_variables_round_trip(evolution_rebuild):
    """Variables are addressed by id, so dropping one silently rewires trigger logic.

    An earlier decompiler emitted variables nowhere, and verification did not notice.
    Both their ids and names have to survive the round trip.
    """
    rebuilt, original = evolution_rebuild
    assert original["variables"], "fixture mode no longer declares variables"
    assert rebuilt["variables"] == original["variables"]
