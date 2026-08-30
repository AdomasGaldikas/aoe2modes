"""Static integrity checks for an existing ``.aoe2scenario``.

AoE2ScenarioParser can prove that references and serialized geometry are coherent;
it cannot run Definitive Edition's trigger scheduler, XS runtime, pathfinder, or UI.
This module deliberately keeps that boundary explicit.  Errors are structural defects
that can make a scenario unsafe to test.  Warnings are editor/development debt that
may be intentional in a decompiled legacy scenario.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId

from aoe2modes.lib.decompile import (
    CONDITION_PARAMS,
    EFFECT_PARAMS,
    condition_factory_name,
    effect_factory_name,
    safe_get,
)

ERROR = "ERROR"
WARNING = "WARNING"


@dataclass(frozen=True)
class AuditFinding:
    severity: str
    code: str
    message: str


@dataclass
class AuditReport:
    map_size: int
    triggers: int
    units: int
    variables: int
    initially_enabled: int
    reachable: int
    findings: list[AuditFinding] = field(default_factory=list)

    @property
    def errors(self) -> list[AuditFinding]:
        return [finding for finding in self.findings if finding.severity == ERROR]

    @property
    def warnings(self) -> list[AuditFinding]:
        return [finding for finding in self.findings if finding.severity == WARNING]

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self, *, label: str | None = None) -> str:
        lines = []
        if label:
            lines.append(f"file        {label}")
        lines.extend(
            (
                f"map         {self.map_size}x{self.map_size}",
                f"units       {self.units}",
                f"triggers    {self.triggers} ({self.initially_enabled} initially enabled, "
                f"{self.reachable} conservatively reachable)",
                f"variables   {self.variables}",
            )
        )
        for finding in sorted(
            self.findings,
            key=lambda item: (item.severity != ERROR, item.code, item.message),
        ):
            lines.append(f"{finding.severity:<7} {finding.code}: {finding.message}")
        verdict = "PASS" if self.ok else "FAIL"
        lines.append(
            f"{verdict} — {len(self.errors)} error(s), {len(self.warnings)} warning(s)"
        )
        return "\n".join(lines)


def _duplicates(values: Iterable[Any]) -> dict[Any, int]:
    return {value: count for value, count in Counter(values).items() if count > 1}


def _finding(
    findings: list[AuditFinding],
    severity: str,
    code: str,
    message: str,
) -> None:
    findings.append(AuditFinding(severity, code, message))


def _component_params(component, *, condition: bool) -> tuple[str, list[str]]:
    if condition:
        factory = condition_factory_name(component)
        return factory, CONDITION_PARAMS.get(factory, [])
    factory = effect_factory_name(component)
    return factory, EFFECT_PARAMS.get(factory, [])


def _non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _audit_component_references(
    *,
    trigger,
    component,
    position: int,
    condition: bool,
    trigger_ids: set[int],
    unit_ids: set[int],
    variable_ids: set[int],
    enforce_variable_references: bool,
    map_size: int,
    findings: list[AuditFinding],
) -> None:
    kind = "condition" if condition else "effect"
    factory, params = _component_params(component, condition=condition)
    where = f"trigger {trigger.trigger_id} {trigger.name!r} {kind}[{position}] {factory}"

    if "trigger_id" in params:
        reference = safe_get(component, "trigger_id", -1)
        if _non_negative_int(reference) and reference not in trigger_ids:
            _finding(
                findings,
                ERROR,
                "dangling-trigger-reference",
                f"{where} points to missing trigger {reference}",
            )

    for name in ("variable", "variable2"):
        if name not in params:
            continue
        reference = safe_get(component, name, -1)
        if (
            enforce_variable_references
            and _non_negative_int(reference)
            and reference not in variable_ids
        ):
            _finding(
                findings,
                ERROR,
                "dangling-variable-reference",
                f"{where} points to missing variable {reference} via {name}",
            )

    for name in ("unit_object", "next_object", "location_object_reference"):
        if name not in params:
            continue
        reference = safe_get(component, name, -1)
        if _non_negative_int(reference) and reference not in unit_ids:
            _finding(
                findings,
                ERROR,
                "dangling-unit-reference",
                f"{where} points to missing object {reference} via {name}",
            )

    if "selected_object_ids" in params:
        for reference in safe_get(component, "selected_object_ids", ()) or ():
            if reference not in unit_ids:
                _finding(
                    findings,
                    ERROR,
                    "dangling-unit-reference",
                    f"{where} selects missing object {reference}",
                )

    for prefix in ("area", "wall"):
        names = tuple(f"{prefix}_{axis}{corner}" for axis in "xy" for corner in (1, 2))
        if not all(name in params for name in names):
            continue
        values = tuple(safe_get(component, name, -1) for name in names)
        used = tuple(_non_negative_int(value) for value in values)
        if not any(used):
            continue
        if not all(used):
            _finding(
                findings,
                ERROR,
                "partial-area",
                f"{where} has incomplete {prefix} coordinates {values}",
            )
            continue
        x1, x2, y1, y2 = values
        if x1 > x2 or y1 > y2:
            _finding(
                findings,
                ERROR,
                "inverted-area",
                f"{where} has inverted {prefix} coordinates {values}",
            )
        if any(value >= map_size for value in values):
            _finding(
                findings,
                ERROR,
                "out-of-bounds-area",
                f"{where} has {prefix} coordinates {values} outside 0..{map_size - 1}",
            )

    if "location_x" in params and "location_y" in params:
        x = safe_get(component, "location_x", -1)
        y = safe_get(component, "location_y", -1)
        used = (_non_negative_int(x), _non_negative_int(y))
        if any(used) and not all(used):
            _finding(
                findings,
                ERROR,
                "partial-location",
                f"{where} has incomplete location ({x}, {y})",
            )
        elif all(used) and (x >= map_size or y >= map_size):
            _finding(
                findings,
                ERROR,
                "out-of-bounds-location",
                f"{where} has location ({x}, {y}) outside 0..{map_size - 1}",
            )

    for name in ("source_player", "target_player"):
        if name not in params:
            continue
        player = safe_get(component, name, -1)
        if isinstance(player, int) and not -1 <= player <= 8:
            _finding(
                findings,
                ERROR,
                "invalid-player",
                f"{where} uses {name}={player}; valid scenario players are -1..8",
            )


def audit_scenario(scenario) -> AuditReport:
    """Return a conservative structural audit of a loaded scenario."""
    tm = scenario.trigger_manager
    um = scenario.unit_manager
    mm = scenario.map_manager
    triggers = list(tm.triggers)
    units_by_owner = list(um.units)
    units = [unit for owned in units_by_owner for unit in owned]
    variables = list(tm.variables)
    map_size = int(mm.map_size)
    findings: list[AuditFinding] = []

    trigger_ids_list = [trigger.trigger_id for trigger in triggers]
    duplicate_trigger_ids = _duplicates(trigger_ids_list)
    if duplicate_trigger_ids:
        _finding(
            findings,
            ERROR,
            "duplicate-trigger-id",
            f"{len(duplicate_trigger_ids)} trigger id(s) are reused: "
            f"{sorted(duplicate_trigger_ids)[:10]}",
        )
    trigger_ids = set(trigger_ids_list)

    display_order = list(tm.trigger_display_order)
    duplicate_display_ids = _duplicates(display_order)
    missing_from_order = sorted(trigger_ids - set(display_order))
    unknown_in_order = sorted(set(display_order) - trigger_ids)
    if duplicate_display_ids or missing_from_order or unknown_in_order:
        _finding(
            findings,
            ERROR,
            "invalid-trigger-display-order",
            f"duplicates={sorted(duplicate_display_ids)[:10]}, "
            f"missing={missing_from_order[:10]}, unknown={unknown_in_order[:10]}",
        )

    names: dict[str, list[int]] = defaultdict(list)
    for trigger in triggers:
        names[trigger.name].append(trigger.trigger_id)
    duplicate_names = {
        name: ids for name, ids in names.items() if name and len(ids) > 1
    }
    if duplicate_names:
        largest = sorted(
            duplicate_names.items(),
            key=lambda item: (-len(item[1]), item[0]),
        )[:5]
        examples = ", ".join(f"{name!r} x{len(ids)}" for name, ids in largest)
        _finding(
            findings,
            WARNING,
            "duplicate-trigger-names",
            f"{len(duplicate_names)} name(s) are reused; largest groups: {examples}",
        )

    unit_ids_list = [unit.reference_id for unit in units]
    duplicate_unit_ids = _duplicates(unit_ids_list)
    if duplicate_unit_ids:
        _finding(
            findings,
            ERROR,
            "duplicate-unit-reference",
            f"{len(duplicate_unit_ids)} object reference id(s) are reused: "
            f"{sorted(duplicate_unit_ids)[:10]}",
        )
    unit_ids = set(unit_ids_list)
    for owner, owned in enumerate(units_by_owner):
        for unit in owned:
            if int(unit.player) != owner:
                _finding(
                    findings,
                    ERROR,
                    "unit-owner-mismatch",
                    f"object {unit.reference_id} is in P{owner}'s list but records P{int(unit.player)}",
                )
            if not (0 <= unit.x < map_size and 0 <= unit.y < map_size):
                _finding(
                    findings,
                    ERROR,
                    "out-of-bounds-unit",
                    f"object {unit.reference_id} is at ({unit.x}, {unit.y}) on a {map_size} map",
                )
            garrison = safe_get(unit, "garrisoned_in_id", -1)
            if _non_negative_int(garrison) and garrison not in unit_ids:
                _finding(
                    findings,
                    ERROR,
                    "dangling-garrison-reference",
                    f"object {unit.reference_id} is garrisoned in missing object {garrison}",
                )

    variable_ids_list = [variable.variable_id for variable in variables]
    duplicate_variable_ids = _duplicates(variable_ids_list)
    if duplicate_variable_ids:
        _finding(
            findings,
            ERROR,
            "duplicate-variable-id",
            f"{len(duplicate_variable_ids)} variable id(s) are reused: "
            f"{sorted(duplicate_variable_ids)[:10]}",
        )
    variable_names = [variable.name for variable in variables if variable.name]
    duplicate_variable_names = _duplicates(variable_names)
    if duplicate_variable_names:
        _finding(
            findings,
            WARNING,
            "duplicate-variable-names",
            f"{len(duplicate_variable_names)} variable name(s) are reused: "
            f"{sorted(duplicate_variable_names)[:10]}",
        )
    variable_ids = set(variable_ids_list)

    activate = int(EffectId.ACTIVATE_TRIGGER)
    edges: dict[int, set[int]] = defaultdict(set)
    implicit_variable_references = 0
    for trigger in triggers:
        for position, condition in enumerate(trigger.conditions):
            _factory, params = _component_params(condition, condition=True)
            if not variables:
                implicit_variable_references += sum(
                    _non_negative_int(safe_get(condition, name, -1))
                    for name in ("variable", "variable2")
                    if name in params
                )
            _audit_component_references(
                trigger=trigger,
                component=condition,
                position=position,
                condition=True,
                trigger_ids=trigger_ids,
                unit_ids=unit_ids,
                variable_ids=variable_ids,
                enforce_variable_references=bool(variables),
                map_size=map_size,
                findings=findings,
            )
        for position, effect in enumerate(trigger.effects):
            _factory, params = _component_params(effect, condition=False)
            if not variables:
                implicit_variable_references += sum(
                    _non_negative_int(safe_get(effect, name, -1))
                    for name in ("variable", "variable2")
                    if name in params
                )
            _audit_component_references(
                trigger=trigger,
                component=effect,
                position=position,
                condition=False,
                trigger_ids=trigger_ids,
                unit_ids=unit_ids,
                variable_ids=variable_ids,
                enforce_variable_references=bool(variables),
                map_size=map_size,
                findings=findings,
            )
            if effect.effect_type == activate and effect.trigger_id in trigger_ids:
                edges[trigger.trigger_id].add(effect.trigger_id)

    if implicit_variable_references:
        _finding(
            findings,
            WARNING,
            "implicit-variable-references",
            f"{implicit_variable_references} trigger-variable reference(s) cannot be "
            "cross-checked because the scenario has no serialized variable table",
        )

    initially_enabled = {
        trigger.trigger_id for trigger in triggers if bool(trigger.enabled)
    }
    reachable = set(initially_enabled)
    queue = deque(initially_enabled)
    while queue:
        source = queue.popleft()
        for target in edges[source]:
            if target in reachable:
                continue
            reachable.add(target)
            queue.append(target)

    timer = int(ConditionId.TIMER)
    unpaced_loops = [
        trigger
        for trigger in triggers
        if trigger.trigger_id in reachable
        and bool(trigger.looping)
        and not any(condition.condition_type == timer for condition in trigger.conditions)
    ]
    if unpaced_loops:
        examples = ", ".join(
            f"{trigger.trigger_id}:{trigger.name!r}" for trigger in unpaced_loops[:10]
        )
        _finding(
            findings,
            WARNING,
            "unpaced-reachable-loop",
            f"{len(unpaced_loops)} reachable looping trigger(s) have no Timer condition: {examples}",
        )

    destructive = {
        int(EffectId.DECLARE_VICTORY),
        int(EffectId.KILL_OBJECT),
        int(EffectId.REMOVE_OBJECT),
    }
    immediate_declarations = [
        trigger
        for trigger in triggers
        if trigger.trigger_id in initially_enabled
        and not trigger.conditions
        and any(
            effect.effect_type == int(EffectId.DECLARE_VICTORY)
            for effect in trigger.effects
        )
    ]
    if immediate_declarations:
        examples = ", ".join(
            f"{trigger.trigger_id}:{trigger.name!r}"
            for trigger in immediate_declarations[:10]
        )
        _finding(
            findings,
            ERROR,
            "immediate-victory-or-defeat",
            f"{len(immediate_declarations)} initially enabled trigger(s) can declare "
            f"victory or defeat without a condition: {examples}",
        )

    unconditional_destructive = [
        trigger
        for trigger in triggers
        if trigger.trigger_id in reachable
        and not trigger.conditions
        and any(effect.effect_type in destructive for effect in trigger.effects)
    ]
    if unconditional_destructive:
        examples = ", ".join(
            f"{trigger.trigger_id}:{trigger.name!r}"
            for trigger in unconditional_destructive[:10]
        )
        _finding(
            findings,
            WARNING,
            "unconditional-destructive-trigger",
            f"{len(unconditional_destructive)} reachable trigger(s) can remove, kill, or "
            f"declare victory without a condition: {examples}",
        )

    empty = [
        trigger
        for trigger in triggers
        if not trigger.conditions and not trigger.effects
    ]
    enabled_empty = [
        trigger
        for trigger in empty
        if trigger.enabled
    ]
    if enabled_empty:
        examples = ", ".join(
            f"{trigger.trigger_id}:{trigger.name!r}" for trigger in enabled_empty[:5]
        )
        _finding(
            findings,
            WARNING,
            "enabled-empty-triggers",
            f"{len(enabled_empty)} of {len(empty)} empty trigger shell(s) are initially enabled; "
            f"examples: {examples}",
        )

    return AuditReport(
        map_size=map_size,
        triggers=len(triggers),
        units=len(units),
        variables=len(variables),
        initially_enabled=len(initially_enabled),
        reachable=len(reachable),
        findings=findings,
    )
