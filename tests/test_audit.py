from __future__ import annotations

from types import SimpleNamespace

from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId

from aoe2modes.lib.audit import audit_scenario


def _scenario(*, triggers, units=None, variables=None, display_order=None, map_size=10):
    units = [[]] if units is None else units
    variables = [] if variables is None else variables
    if display_order is None:
        display_order = [trigger.trigger_id for trigger in triggers]
    return SimpleNamespace(
        trigger_manager=SimpleNamespace(
            triggers=triggers,
            variables=variables,
            trigger_display_order=display_order,
        ),
        unit_manager=SimpleNamespace(units=units),
        map_manager=SimpleNamespace(map_size=map_size),
    )


def _trigger(
    trigger_id,
    name,
    *,
    enabled=0,
    looping=0,
    conditions=None,
    effects=None,
):
    return SimpleNamespace(
        trigger_id=trigger_id,
        name=name,
        enabled=enabled,
        looping=looping,
        conditions=[] if conditions is None else conditions,
        effects=[] if effects is None else effects,
    )


def test_audit_accepts_a_small_coherent_scenario():
    timer = SimpleNamespace(condition_type=int(ConditionId.TIMER), timer=1)
    trigger = _trigger(0, "paced", enabled=1, looping=1, conditions=[timer])

    report = audit_scenario(_scenario(triggers=[trigger]))

    assert report.ok
    assert report.findings == []
    assert report.initially_enabled == 1
    assert report.reachable == 1
    assert report.summary().endswith("PASS - 0 error(s), 0 warning(s)")


def test_audit_reports_broken_references_geometry_and_scheduling():
    remove = SimpleNamespace(
        effect_type=int(EffectId.REMOVE_OBJECT),
        source_player=9,
        selected_object_ids=[999],
        area_x1=5,
        area_x2=4,
        area_y1=0,
        area_y2=11,
    )
    activate = SimpleNamespace(
        effect_type=int(EffectId.ACTIVATE_TRIGGER),
        trigger_id=99,
    )
    change_variable = SimpleNamespace(
        effect_type=int(EffectId.CHANGE_VARIABLE),
        variable=7,
    )
    declare_defeat = SimpleNamespace(
        effect_type=int(EffectId.DECLARE_VICTORY),
        source_player=1,
        enabled=0,
    )
    trigger = _trigger(
        0,
        "unsafe",
        enabled=1,
        looping=1,
        effects=[remove, activate, change_variable, declare_defeat],
    )
    unit = SimpleNamespace(
        reference_id=1,
        player=0,
        x=10.5,
        y=2.5,
        garrisoned_in_id=404,
    )

    variables = [SimpleNamespace(variable_id=1, name="declared")]
    report = audit_scenario(
        _scenario(triggers=[trigger], units=[[unit]], variables=variables)
    )
    codes = {finding.code for finding in report.errors}

    assert not report.ok
    assert {
        "dangling-trigger-reference",
        "dangling-unit-reference",
        "dangling-variable-reference",
        "dangling-garrison-reference",
        "invalid-player",
        "inverted-area",
        "immediate-victory-or-defeat",
        "out-of-bounds-area",
        "out-of-bounds-unit",
    } <= codes
    assert {
        "unconditional-destructive-trigger",
        "unpaced-reachable-loop",
    } <= {finding.code for finding in report.warnings}


def test_audit_keeps_legacy_editor_debt_as_warnings():
    triggers = [
        _trigger(0, "legacy header", enabled=1),
        _trigger(1, "legacy header"),
    ]

    report = audit_scenario(_scenario(triggers=triggers))

    assert report.ok
    assert {finding.code for finding in report.warnings} == {
        "duplicate-trigger-names",
        "enabled-empty-triggers",
    }


def test_audit_marks_unnamed_variable_slots_as_unverifiable():
    effect = SimpleNamespace(
        effect_type=int(EffectId.CHANGE_VARIABLE),
        variable=7,
    )
    trigger = _trigger(0, "implicit variable", effects=[effect])

    report = audit_scenario(_scenario(triggers=[trigger]))

    assert report.ok
    assert {finding.code for finding in report.warnings} == {
        "implicit-variable-references"
    }
