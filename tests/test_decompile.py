"""The decompiler's contract: generated source must rebuild the scenario it came from.

The end-to-end test uses ``chieftains_4v4``, a mode that genuinely still is a decompile of
its ``scenario.reference``. It decompiles that reference into a tempdir, rebuilds from
the fresh output, and diffs — so it tests the decompiler, not any committed package.

It deliberately does **not** use ``evolution_alpha``: Ascendants is code-defined and
has no reference to round-trip against. Pointing this test at a mode whose committed
source is hand-maintained would prove nothing about either the mode or the decompiler.
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


#: A mode that genuinely still is a decompile of its reference, at the current
#: scenario version. ``big_ytri`` is deliberately not used: its reference is v1.51,
#: and loading that after a v1.58 scenario trips the parser's version-scoped global
#: state leak (see ``toolchain.py``).
DECOMPILE_ROUND_TRIP_MODE = "chieftains_4v4"


@pytest.fixture(scope="module")
def decompiler_rebuild(tmp_path_factory, repo):
    """Decompile a real reference into a tempdir, rebuild from it, and snapshot both."""
    spec = registry.get(DECOMPILE_ROUND_TRIP_MODE, repo)
    if spec.reference is None:
        pytest.skip(f"{DECOMPILE_ROUND_TRIP_MODE} has no scenario.reference to verify against")

    original = AoE2DEScenario.from_file(str(spec.reference))
    generated_dir = tmp_path_factory.mktemp("decompile") / "generated"
    decompile(original, generated_dir, source_label=spec.reference.name)

    scenario = AoE2DEScenario.from_default(spec.scenario_version)
    scenario.variant = spec.variant
    ctx = BuildContext(spec=spec, scenario=scenario, repo=repo)
    module_name = f"aoe2modes._test_generated.{DECOMPILE_ROUND_TRIP_MODE}"
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


def test_freshly_decompiled_source_rebuilds_the_original(decompiler_rebuild):
    rebuilt, original = decompiler_rebuild
    report = compare(original, rebuilt)
    assert report.checked > 10_000, "comparison covered suspiciously little"
    assert report.differences[:5] == []
    assert report.ok


def test_rebuild_has_no_version_gap(decompiler_rebuild):
    """Same version on both sides, so every field should exist on both."""
    rebuilt, original = decompiler_rebuild
    report = compare(original, rebuilt)
    assert report.version_only_total == 0, dict(report.version_only)


def test_ascendants_is_code_defined_not_decompiled(repo):
    """Ascendants must not regrow a reference: its Python is the only source of truth.

    A `scenario.reference` here would re-create the v1.0.8 trap, where `verify` and
    `decompile` looked meaningful but compared the mode against one of its own old
    build outputs.
    """
    spec = registry.get("evolution_alpha", repo)
    assert spec.reference is None
    assert spec.base is None
    assert not (repo.modes / "evolution_alpha" / "base.aoe2scenario").exists()


def test_trigger_variables_round_trip(tmp_path, repo):
    """Variables are addressed by id, so dropping one silently rewires trigger logic.

    An earlier decompiler emitted variables nowhere and verification did not notice.
    No mode reference in the repo declares variables any more, so this builds a
    scenario that does — sparse, non-contiguous ids, and a condition that addresses
    one by id — and proves ids and names both survive a decompile/rebuild cycle.
    """
    source = AoE2DEScenario.from_default("1.58")
    tm = source.trigger_manager
    for variable_id, name in [(0, "alpha"), (7, "bravo"), (42, "charlie")]:
        tm.add_variable(name, variable_id)
    probe = tm.add_trigger("Probe")
    probe.new_condition.variable_value(quantity=3, variable=42, comparison=0)
    probe.new_effect.change_variable(quantity=1, operation=1, variable=7)

    out = tmp_path / "generated"
    decompile(source, out, source_label="synthetic")

    rebuilt_scenario = AoE2DEScenario.from_default("1.58")
    ctx = BuildContext(
        spec=registry.get(DECOMPILE_ROUND_TRIP_MODE, repo),
        scenario=rebuilt_scenario,
        repo=repo,
    )
    module_name = "aoe2modes._test_generated.variables_probe"
    loader_spec = importlib.util.spec_from_file_location(
        module_name, out / "__init__.py", submodule_search_locations=[str(out)]
    )
    assert loader_spec is not None and loader_spec.loader is not None
    module = importlib.util.module_from_spec(loader_spec)
    sys.modules[module_name] = module
    loader_spec.loader.exec_module(module)
    module.apply(ctx)

    original_snapshot = snapshot(source)
    rebuilt_snapshot = snapshot(rebuilt_scenario)
    assert original_snapshot["variables"], "the probe scenario declares variables"
    assert rebuilt_snapshot["variables"] == original_snapshot["variables"]
    # The id a condition points at must survive, not just the declaration table.
    assert compare(original_snapshot, rebuilt_snapshot).ok
