"""Prove that a code-built mode still matches the scenario it was decompiled from.

Decompiling is only trustworthy if the rebuild is checkable, and a byte compare is
useless here: the rebuild targets the newest scenario version, so its file layout
differs from a v1.51 original by construction. What has to match is the *content* —
every trigger, condition, effect field, every unit, every terrain tile.

So both sides are reduced to plain Python data (``snapshot``) and compared field by
field. Snapshots are plain data for a second reason: the parser leaks version-scoped
state between scenarios, so the newer file must be fully read *before* the older one
is loaded. Holding onto live objects across that boundary raises
``UnsupportedAttributeError`` on fields the older version predates.

Fields that exist on only one side are counted as ``version_only`` rather than
reported as differences — a v1.58 rebuild genuinely has fields a v1.51 file never had.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from aoe2modes.lib.decompile import (
    CONDITION_PARAMS,
    EFFECT_PARAMS,
    MESSAGE_FIELDS,
    OPTION_FIELDS,
    PLAYER_FIELDS,
    PLAYER_LIST_FIELDS,
    TRIGGER_PARAMS,
    UNIT_FIELDS,
    condition_factory_name,
    effect_factory_name,
    safe_get,
)

ABSENT = "<absent>"

_INDEXED = re.compile(r"^\w+\[\d+\][^.]*\.")


def _field_name(path: str) -> str:
    """``trigger[7] 'x'.attrs.execute_on_load`` -> ``attrs.execute_on_load``."""
    return _INDEXED.sub("", path)


def _read(obj, names) -> dict[str, Any]:
    return {name: safe_get(obj, name, ABSENT) for name in names}


def snapshot(scenario) -> dict[str, Any]:
    """Reduce a scenario to comparable plain data. Must be called before loading an older file."""
    tm, um, mm, pm = (
        scenario.trigger_manager,
        scenario.unit_manager,
        scenario.map_manager,
        scenario.player_manager,
    )

    terrain: list[tuple[int, int, int, int]] = []
    for tile in mm.terrain:
        key = (tile.terrain_id, tile.elevation, safe_get(tile, "layer", -1))
        if terrain and terrain[-1][1:] == key:
            terrain[-1] = (terrain[-1][0] + 1, *key)
        else:
            terrain.append((1, *key))

    triggers = []
    for trigger in tm.triggers:
        triggers.append(
            {
                "name": trigger.name,
                "attrs": _read(trigger, TRIGGER_PARAMS),
                "conditions": [
                    (factory, _read(condition, CONDITION_PARAMS.get(factory, [])))
                    for condition in trigger.conditions
                    for factory in [condition_factory_name(condition)]
                ],
                "effects": [
                    (factory, _read(effect, EFFECT_PARAMS.get(factory, [])))
                    for effect in trigger.effects
                    for factory in [effect_factory_name(effect)]
                ],
            }
        )

    units = []
    for player_index, player_units in enumerate(um.units):
        for unit in player_units:
            row = {"player": player_index}
            row.update({kwarg: safe_get(unit, attr, ABSENT) for kwarg, attr in UNIT_FIELDS.items()})
            units.append(row)

    return {
        "map_size": mm.map_size,
        "active_players": pm.active_players,
        "terrain": terrain,
        "terrain_tiles": sum(run[0] for run in terrain),
        "players": [_read(p, PLAYER_FIELDS + PLAYER_LIST_FIELDS) for p in pm.players],
        "options": _read(scenario.option_manager, OPTION_FIELDS),
        "messages": _read(scenario.message_manager, MESSAGE_FIELDS),
        "units": units,
        "triggers": triggers,
        "display_order": list(tm.trigger_display_order),
    }


@dataclass
class VerifyReport:
    differences: list[str] = field(default_factory=list)
    version_only: Counter = field(default_factory=Counter)
    checked: int = 0

    @property
    def ok(self) -> bool:
        return not self.differences

    @property
    def version_only_total(self) -> int:
        return sum(self.version_only.values())

    def summary(self, limit: int = 40) -> str:
        lines = [f"compared {self.checked} fields"]
        if self.version_only:
            # Naming the fields matters: "ignored 9392 fields" is only reassuring once
            # you can see they are all fields the older format never had.
            lines.append(
                f"{self.version_only_total} field slots exist on only one side "
                "(version gap, not a content difference):"
            )
            lines += [f"  {count:6}x {name}" for name, count in self.version_only.most_common(10)]
            if len(self.version_only) > 10:
                lines.append(f"  ... {len(self.version_only) - 10} more field names")
        if self.ok:
            lines.append("MATCH — the rebuild is content-identical to the original.")
            return "\n".join(lines)
        lines.append(f"{len(self.differences)} DIFFERENCES:")
        lines += [f"  {d}" for d in self.differences[:limit]]
        if len(self.differences) > limit:
            lines.append(f"  ... {len(self.differences) - limit} more")
        return "\n".join(lines)


class _Comparer:
    def __init__(self) -> None:
        self.report = VerifyReport()

    def field(self, path: str, a: Any, b: Any) -> None:
        if a is ABSENT or b is ABSENT:
            if a is not b:
                # Collapse the index out of "trigger[1234] 'name'.attrs.execute_on_load"
                # so the report names each field once rather than 2993 times.
                self.report.version_only[_field_name(path)] += 1
            return
        self.report.checked += 1
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            a, b = tuple(a), tuple(b)
        if a != b:
            self.report.differences.append(f"{path}: original={a!r} rebuilt={b!r}")

    def mapping(self, path: str, a: dict, b: dict) -> None:
        for key in a.keys() | b.keys():
            self.field(f"{path}.{key}", a.get(key, ABSENT), b.get(key, ABSENT))


def compare(original: dict[str, Any], rebuilt: dict[str, Any]) -> VerifyReport:
    """Field-by-field comparison of two snapshots, original first."""
    cmp = _Comparer()

    for key in ("map_size", "active_players", "terrain_tiles", "display_order"):
        cmp.field(key, original[key], rebuilt[key])

    if original["terrain"] != rebuilt["terrain"]:
        differing = sum(1 for a, b in zip(original["terrain"], rebuilt["terrain"], strict=False) if a != b)
        cmp.report.differences.append(
            f"terrain: {len(original['terrain'])} runs vs {len(rebuilt['terrain'])}, "
            f"{differing} differing in the overlap"
        )
    cmp.report.checked += 1

    cmp.mapping("options", original["options"], rebuilt["options"])
    cmp.mapping("messages", original["messages"], rebuilt["messages"])
    for index, (a, b) in enumerate(zip(original["players"], rebuilt["players"], strict=False)):
        cmp.mapping(f"player[{index}]", a, b)

    if len(original["units"]) != len(rebuilt["units"]):
        cmp.report.differences.append(
            f"units: {len(original['units'])} vs {len(rebuilt['units'])}"
        )
    for index, (a, b) in enumerate(zip(original["units"], rebuilt["units"], strict=False)):
        cmp.mapping(f"unit[{index}]", a, b)

    if len(original["triggers"]) != len(rebuilt["triggers"]):
        cmp.report.differences.append(
            f"triggers: {len(original['triggers'])} vs {len(rebuilt['triggers'])}"
        )
    for index, (a, b) in enumerate(zip(original["triggers"], rebuilt["triggers"], strict=False)):
        label = f"trigger[{index}] {a['name']!r}"
        cmp.field(f"{label}.name", a["name"], b["name"])
        cmp.mapping(f"{label}.attrs", a["attrs"], b["attrs"])
        for kind in ("conditions", "effects"):
            if len(a[kind]) != len(b[kind]):
                cmp.report.differences.append(
                    f"{label}.{kind}: {len(a[kind])} vs {len(b[kind])}"
                )
                continue
            for position, (one, two) in enumerate(zip(a[kind], b[kind], strict=True)):
                if one[0] != two[0]:
                    cmp.report.differences.append(
                        f"{label}.{kind}[{position}]: {one[0]} vs {two[0]}"
                    )
                    continue
                cmp.mapping(f"{label}.{kind}[{position}] {one[0]}", one[1], two[1])

    return cmp.report
