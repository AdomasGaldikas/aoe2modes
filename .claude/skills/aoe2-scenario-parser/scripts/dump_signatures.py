"""Regenerate every generated reference file.

- ``references/effects.md`` / ``references/conditions.md`` — factory signatures
- ``references/values/*.md`` — every member of every dataset enum, with its value

These are the parts of AoE2ScenarioParser that change most between releases and whose names are
impossible to guess. Rather than transcribing the docs site (which runs ahead of the released
package), we dump them straight out of whatever version is installed.

Run after upgrading the parser:

    .venv/Scripts/python .claude/skills/aoe2-scenario-parser/scripts/dump_signatures.py
"""

from __future__ import annotations

import importlib.metadata as metadata
import inspect
from pathlib import Path

from AoE2ScenarioParser.datasets import trigger_lists
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.new_condition import NewConditionSupport
from AoE2ScenarioParser.objects.support.new_effect import NewEffectSupport

WIDTH = 114
REFERENCES = Path(__file__).resolve().parent.parent / "references"
VALUES = REFERENCES / "values"

VERSION = metadata.version("AoE2ScenarioParser")

#: (filename, enum, import path, one-line note)
DATASETS = [
    ("units.md", UnitInfo, "AoE2ScenarioParser.datasets.units", "Units, including heroes' base forms."),
    ("buildings.md", BuildingInfo, "AoE2ScenarioParser.datasets.buildings", "Buildings."),
    ("heroes.md", HeroInfo, "AoE2ScenarioParser.datasets.heroes", "Named heroes."),
    ("techs.md", TechInfo, "AoE2ScenarioParser.datasets.techs", "Technologies."),
    (
        "other.md",
        OtherInfo,
        "AoE2ScenarioParser.datasets.other",
        "Everything else placeable: relics, gold piles, trees, cliffs, eye candy.",
    ),
    (
        "projectiles.md",
        ProjectileInfo,
        "AoE2ScenarioParser.datasets.projectiles",
        "Projectiles, for `ObjectAttribute.PROJECTILE_UNIT`.",
    ),
    (
        "terrains.md",
        TerrainId,
        "AoE2ScenarioParser.datasets.terrains",
        "Terrain types. A plain `IntEnum` — no `.ID` suffix.",
    ),
]


def _wrap(prefix: str, name: str, params: list[str]) -> list[str]:
    single = f"{prefix}.{name}({', '.join(params)})"
    if len(single) <= WIDTH + 4:
        return [single]

    lines = [f"{prefix}.{name}("]
    current = "    "
    for param in params:
        piece = param + ", "
        if len(current) + len(piece) > WIDTH:
            lines.append(current.rstrip())
            current = "    "
        current += piece
    lines.append(current.rstrip().rstrip(","))
    lines.append(")")
    return lines


def dump(cls: type, kind: str, prefix: str, title: str) -> str:
    version = VERSION
    article = "an" if kind[0] in "AEIOU" else "a"

    lines = [
        f"# {title}",
        "",
        f"Generated from AoE2ScenarioParser {version} "
        f"(`{cls.__module__}.{cls.__name__}`) by `scripts/dump_signatures.py`.",
        "",
        f"Every factory returns {article} `{kind}` object whose attributes stay editable afterwards.",
        "All parameters default to `None` (leave at the game's default) — always pass them by name.",
        "",
        "```py",
    ]

    for name, obj in sorted(vars(cls).items()):
        if name.startswith("_") or not inspect.isfunction(obj):
            continue
        params = [p for p in inspect.signature(obj).parameters if p != "self"]
        lines.extend(_wrap(prefix, name, params))

    lines.append("```")
    return "\n".join(lines) + "\n"


def dump_dataset(enum: type, import_path: str, note: str) -> str:
    """One file per info dataset: every member name with the id you actually pass to the parser."""
    members = list(enum.__members__.items())
    sample = members[0][1]
    extras = [f for f in ("ICON_ID", "DEAD_ID", "HOTKEY_ID", "IS_GAIA_ONLY") if hasattr(sample, f)]
    plain = not hasattr(sample, "ID")

    lines = [
        f"# `{enum.__name__}` values",
        "",
        f"All {len(members)} members in AoE2ScenarioParser {VERSION}, dumped by"
        f" `scripts/dump_signatures.py`. {note}",
        "",
        f"```py\nfrom {import_path} import {enum.__name__}\n```",
        "",
    ]

    if plain:
        lines.append(f"Listed as `NAME = value`. Pass the member directly: `{enum.__name__}.<NAME>`.")
    else:
        lines.append(
            f"Listed as `NAME = ID`. Pass the id, never the member: `{enum.__name__}.<NAME>.ID`."
        )
        if extras:
            fields = ", ".join(f"`.{f}`" for f in extras)
            lines.append(f"The same member also carries {fields}.")
        if "IS_GAIA_ONLY" in extras:
            lines.append("Members marked `# gaia` are GAIA-only objects.")

    lines += ["", "```py"]
    for name, member in members:
        value = member.value if plain else member.ID
        suffix = "  # gaia" if "IS_GAIA_ONLY" in extras and member.IS_GAIA_ONLY else ""
        lines.append(f"{name} = {value}{suffix}")
    lines += ["```", ""]

    return "\n".join(lines)


def dump_trigger_lists() -> str:
    version = VERSION
    enums = sorted(
        (name, obj)
        for name, obj in vars(trigger_lists).items()
        if inspect.isclass(obj) and not name.startswith("_") and hasattr(obj, "__members__")
    )

    lines = [
        "# `trigger_lists` enum values",
        "",
        f"Every member of every dropdown enum in AoE2ScenarioParser {version}, dumped by "
        "`scripts/dump_signatures.py`.",
        "",
        "Import all of them from `AoE2ScenarioParser.datasets.trigger_lists`. For *which* effect or "
        "condition takes which enum, see `../datasets.md`.",
        "",
        "## Index",
        "",
        " · ".join(f"[{name}](#{name.lower()})" for name, _ in enums),
        "",
    ]

    for name, enum in enums:
        lines += [f"## {name}", "", "```py"]
        lines += [f"{member} = {value.value}" for member, value in enum.__members__.items()]
        lines += ["```", ""]

    return "\n".join(lines)


def main() -> None:
    REFERENCES.mkdir(parents=True, exist_ok=True)
    VALUES.mkdir(parents=True, exist_ok=True)

    path = VALUES / "trigger-lists.md"
    path.write_text(dump_trigger_lists(), encoding="utf-8")
    print(f"wrote {path}")

    for filename, enum, import_path, note in DATASETS:
        path = VALUES / filename
        path.write_text(dump_dataset(enum, import_path, note), encoding="utf-8")
        print(f"wrote {path}")

    targets = [
        (NewEffectSupport, "Effect", "trigger.new_effect", "Effect reference", "effects.md"),
        (NewConditionSupport, "Condition", "trigger.new_condition", "Condition reference", "conditions.md"),
    ]
    for cls, kind, prefix, title, filename in targets:
        path = REFERENCES / filename
        path.write_text(dump(cls, kind, prefix, title), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
