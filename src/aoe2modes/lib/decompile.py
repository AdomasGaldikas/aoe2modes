"""Turn an existing ``.aoe2scenario`` into regenerable Python source.

The point is to stop treating a downloaded mod as an opaque blob. ``decompile``
reads every piece of state the parser's managers expose and writes Python that
rebuilds it, so a mode can be edited as code and recompiled.

Two properties matter more than pretty output:

**Fidelity.** Field values are read back through the same typed API that writes
them, and only fields that differ from a freshly constructed effect/condition are
emitted. ``aoe2modes verify`` rebuilds the generated source and diffs it against
the original; the emitter is only useful if that diff is empty.

**Process isolation.** The parser leaks version-scoped global state, so a v1.51
scenario cannot be read in the same process that builds a v1.58 one. Decompiling
therefore *writes source* rather than handing back objects: the build runs later,
in its own process, from a blank scenario of the current version.

Older scenarios raise ``UnsupportedAttributeError`` for fields their version
predates, so every read here is defensive — see ``safe_get``.
"""

from __future__ import annotations

import inspect
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.new_condition import NewConditionSupport
from AoE2ScenarioParser.objects.support.new_effect import NewEffectSupport

# --------------------------------------------------------------------------------------
# Introspection: what a factory accepts is exactly what we need to read back.
# --------------------------------------------------------------------------------------

EFFECT_PARAMS: dict[str, list[str]] = {
    name: [p for p in inspect.signature(fn).parameters if p != "self"]
    for name, fn in vars(NewEffectSupport).items()
    if not name.startswith("_") and inspect.isfunction(fn)
}
CONDITION_PARAMS: dict[str, list[str]] = {
    name: [p for p in inspect.signature(fn).parameters if p != "self"]
    for name, fn in vars(NewConditionSupport).items()
    if not name.startswith("_") and inspect.isfunction(fn)
}

#: Trigger attributes ``add_trigger`` accepts, minus ``name`` which is positional.
TRIGGER_PARAMS = [
    "description",
    "description_stid",
    "display_as_objective",
    "short_description",
    "short_description_stid",
    "display_on_screen",
    "description_order",
    "enabled",
    "looping",
    "execute_on_load",
    "header",
    "mute_objectives",
]

#: ``add_unit`` keyword -> attribute name on a ``Unit``. They differ for one field.
UNIT_FIELDS = {
    "unit_const": "unit_const",
    "x": "x",
    "y": "y",
    "z": "z",
    "rotation": "rotation",
    "garrisoned_in_id": "garrisoned_in_id",
    "animation_frame": "initial_animation_frame",
    "status": "status",
    "reference_id": "reference_id",
    "caption_string_id": "caption_string_id",
    "caption_string": "caption_string",
}

PLAYER_FIELDS = [
    "starting_age",
    "lock_civ",
    "lock_personality",
    "population_cap",
    "food",
    "wood",
    "gold",
    "stone",
    "color",
    "human",
    "civilization",
    "architecture_set",
    "allied_victory",
    "base_priority",
    "tribe_name",
    "string_table_name_id",
    "initial_player_view_x",
    "initial_player_view_y",
]
PLAYER_LIST_FIELDS = ["disabled_techs", "disabled_buildings", "disabled_units", "diplomacy"]

OPTION_FIELDS = [
    "victory_condition",
    "victory_score",
    "victory_years",
    "victory_custom_conditions_required",
    "secondary_game_modes",
    "lock_teams",
    "lock_coop_alliances",
    "allow_players_choose_teams",
    "random_start_points",
    "collide_and_correct",
    "villager_force_drop",
    "legacy_execution_order",
]
MESSAGE_FIELDS = ["instructions", "hints", "history", "loss", "scouts", "victory"]

_UNSET = object()


def safe_get(obj: Any, name: str, default: Any = _UNSET) -> Any:
    """Read an attribute, tolerating fields the scenario's version does not support.

    A v1.51 file raises ``UnsupportedAttributeError`` for ``execute_on_load`` and
    ``caption_string``. Those fields simply do not exist in that file, so skipping
    them loses nothing.
    """
    try:
        value = getattr(obj, name)
    except Exception:  # noqa: BLE001 - any version/structure complaint means "absent"
        return default
    return tuple(value) if isinstance(value, list) else value


# --------------------------------------------------------------------------------------
# Rendering values as source
# --------------------------------------------------------------------------------------

#: Field name -> the ``trigger_lists`` enum that field's dropdown draws from.
#: Only unambiguous mappings live here; anything else is emitted as a plain int.
ENUM_FIELDS = {
    "action_type": "ActionType",
    "armour_attack_class": "DamageClass",
    "attack_stance": "AttackStance",
    "attribute": "Attribute",
    "button_location": "ButtonLocation",
    "color_mood": "ColorMood",
    "comparison": "Comparison",
    "diplomacy": "DiplomacyState",
    "difficulty_level": "DifficultyLevel",
    "instruction_panel_position": "PanelLocation",
    "object_group": "ObjectClass",
    "object_state": "ObjectState",
    "object_type": "ObjectType",
    "operation": "Operation",
    "quantity_type": "Attribute",
    "technology_state": "TechnologyState",
    "time_unit": "TimeUnit",
    "timer_type": "VictoryTimerType",
    "visibility_state": "VisibilityState",
}

#: Fields naming a player slot.
PLAYER_ID_FIELDS = {"source_player", "target_player", "player_source", "player_target"}

#: Fields naming a placeable object id, resolved against the info datasets in order.
OBJECT_ID_FIELDS = {"object_list_unit_id", "object_list_unit_id_2", "unit_const"}

_OBJECT_DATASETS = (
    ("UnitInfo", UnitInfo),
    ("BuildingInfo", BuildingInfo),
    ("HeroInfo", HeroInfo),
    ("OtherInfo", OtherInfo),
)


def _object_const(value: int) -> str | None:
    """``4`` -> ``"UnitInfo.ARCHER.ID"``. Ids are shared across datasets; first hit wins.

    Ambiguity is harmless: every candidate resolves to the same integer, so the
    rebuilt scenario is identical either way. Only the comment value differs.
    """
    for label, dataset in _OBJECT_DATASETS:
        try:
            member = dataset.from_id(value)
        except Exception:  # noqa: BLE001 - "not in this dataset"
            continue
        if member is not None:
            return f"{label}.{member.name}.ID"
    return None


def _enum_const(field_name: str, value: int) -> str | None:
    from AoE2ScenarioParser.datasets import trigger_lists

    enum_name = ENUM_FIELDS.get(field_name)
    if enum_name is None:
        return None
    enum_cls = getattr(trigger_lists, enum_name, None)
    if enum_cls is None:
        return None
    try:
        return f"{enum_name}.{enum_cls(value).name}"
    except ValueError:
        return None


#: Enum classes the generated modules import by name, so their members can be rendered
#: as ``StartingAge.IMPERIAL_AGE`` rather than a bare ``4``. Anything not listed here
#: degrades to its underlying value, which is still correct — just less readable.
RENDER_ENUMS = {
    "Civilization": "AoE2ScenarioParser.datasets.object_support",
    "ColorId": "AoE2ScenarioParser.datasets.players",
    "ColorMood": "AoE2ScenarioParser.datasets.trigger_lists",
    "SecondaryGameMode": "AoE2ScenarioParser.datasets.trigger_lists",
    "StartingAge": "AoE2ScenarioParser.datasets.object_support",
    "VictoryCondition": "AoE2ScenarioParser.datasets.trigger_lists",
}

#: Every generated module gets the same imports. The renderer picks constant names from
#: several datasets at once, and tracking which file happens to need which one is exactly
#: the kind of bookkeeping that silently breaks a regenerated build.
GENERATED_IMPORTS = """
from AoE2ScenarioParser.datasets.buildings import BuildingInfo  # noqa: F401
from AoE2ScenarioParser.datasets.heroes import HeroInfo  # noqa: F401
from AoE2ScenarioParser.datasets.object_support import Civilization, StartingAge  # noqa: F401
from AoE2ScenarioParser.datasets.other import OtherInfo  # noqa: F401
from AoE2ScenarioParser.datasets.players import ColorId, PlayerId  # noqa: F401
from AoE2ScenarioParser.datasets.techs import TechInfo  # noqa: F401
from AoE2ScenarioParser.datasets.terrains import TerrainId  # noqa: F401
from AoE2ScenarioParser.datasets.trigger_lists import *  # noqa: F401,F403
from AoE2ScenarioParser.datasets.units import UnitInfo  # noqa: F401
"""


def render(value: Any, *, field_name: str = "") -> str:
    """Render one field value as a Python expression.

    Named constants are preferred over magic numbers wherever the value resolves,
    because the generated source is meant to be *edited*. Every substitution is
    value-preserving, and ``verify`` proves it.
    """
    if isinstance(value, Enum):
        # Not every parser enum subclasses int (``Civilization`` does not), so repr()
        # would emit ``<Civilization.BYZANTINES: 11>`` — valid output, invalid Python.
        name = type(value).__name__
        if name in RENDER_ENUMS:
            return f"{name}.{value.name}"
        value = value.value
    if isinstance(value, bool):
        return repr(value)
    if isinstance(value, int):
        if field_name in PLAYER_ID_FIELDS and 0 <= value <= 8:
            from AoE2ScenarioParser.datasets.players import PlayerId

            return f"PlayerId.{PlayerId(value).name}"
        if value >= 0:
            if field_name in OBJECT_ID_FIELDS and (const := _object_const(value)):
                return const
            if field_name == "technology":
                try:
                    member = TechInfo.from_id(value)
                except Exception:  # noqa: BLE001
                    member = None
                if member is not None:
                    return f"TechInfo.{member.name}.ID"
            if field_name == "terrain_id":
                try:
                    return f"TerrainId.{TerrainId(value).name}"
                except ValueError:
                    pass
            if (const := _enum_const(field_name, value)) is not None:
                return const
        return repr(value)
    if isinstance(value, float):
        return repr(int(value)) if value.is_integer() else repr(value)
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, (tuple, list)):
        return "[" + ", ".join(render(v, field_name=field_name) for v in value) + "]"
    return repr(value)


def render_kwargs(pairs: dict[str, Any], indent: str = "    ") -> str:
    """Render kwargs inline when short, one-per-line when not."""
    if not pairs:
        return ""
    inline = ", ".join(f"{k}={render(v, field_name=k)}" for k, v in pairs.items())
    if len(inline) <= 92:
        return inline
    lines = [f"\n{indent}    {k}={render(v, field_name=k)}," for k, v in pairs.items()]
    return "".join(lines) + f"\n{indent}"


# --------------------------------------------------------------------------------------
# Baselines: which fields actually carry information
# --------------------------------------------------------------------------------------


@dataclass
class Baselines:
    """What each factory produces when called with no arguments.

    Emitting only the fields that differ keeps the generated source readable — most
    effects set three or four of their sixty-odd fields.
    """

    effects: dict[str, dict[str, Any]] = field(default_factory=dict)
    conditions: dict[str, dict[str, Any]] = field(default_factory=dict)
    trigger: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def probe(cls, scenario) -> Baselines:
        """Build baselines from a throwaway trigger in *this* scenario.

        Using the scenario itself rather than a blank one keeps everything on the
        same structure version, which is what makes older files decompilable.
        """
        self = cls()
        tm = scenario.trigger_manager
        probe = tm.add_trigger("__aoe2modes_probe__")
        try:
            self.trigger = {name: safe_get(probe, name, None) for name in TRIGGER_PARAMS}
            for name, params in EFFECT_PARAMS.items():
                if name.upper() not in EffectId.__members__:
                    continue  # deprecated alias, never emitted
                effect = self._construct(probe.new_effect, name)
                if effect is not None:
                    self.effects[name] = {p: safe_get(effect, p, None) for p in params}
            for name, params in CONDITION_PARAMS.items():
                if _condition_id_name(name) not in ConditionId.__members__:
                    continue
                condition = self._construct(probe.new_condition, name)
                if condition is not None:
                    self.conditions[name] = {p: safe_get(condition, p, None) for p in params}
        finally:
            tm.remove_trigger(probe.trigger_id)
        return self

    @staticmethod
    def _construct(factory_holder, name: str):
        """Build a pristine effect/condition, or ``None`` if this version lacks it.

        An older scenario rejects effects added to the game later (``SET_OBJECT_COST``
        did not exist in v1.51). Missing a baseline is harmless: a file that cannot
        hold such an effect cannot contain one to decompile either, and if one somehow
        appears, ``changed_fields`` falls back to emitting every readable field.
        """
        try:
            return getattr(factory_holder, name)()
        except Exception:  # noqa: BLE001 - "this version does not have that one"
            return None


def _condition_id_name(factory_name: str) -> str:
    """``or_`` -> ``OR``. Only ``and``/``or`` need the trailing underscore."""
    return factory_name.rstrip("_").upper()


def effect_factory_name(effect) -> str:
    return EffectId(effect.effect_type).name.lower()


def condition_factory_name(condition) -> str:
    name = ConditionId(condition.condition_type).name.lower()
    return f"{name}_" if name in ("and", "or") else name


def changed_fields(obj, params: list[str], baseline: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for param in params:
        value = safe_get(obj, param, _UNSET)
        if value is _UNSET or value == baseline.get(param):
            continue
        out[param] = value
    return out


# --------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------


@dataclass
class DecompileReport:
    out_dir: Path
    triggers: int
    conditions: int
    effects: int
    units: int
    terrain_runs: int
    terrain_tiles: int
    parts: int
    files: list[Path] = field(default_factory=list)
    skipped: Counter = field(default_factory=Counter)

    def summary(self) -> str:
        lines = [
            f"decompiled into {self.out_dir}",
            f"  triggers    {self.triggers} "
            f"({self.conditions} conditions, {self.effects} effects) in {self.parts} parts",
            f"  units       {self.units}",
            f"  terrain     {self.terrain_tiles} tiles -> {self.terrain_runs} runs",
            f"  files       {len(self.files)}",
        ]
        if self.skipped:
            lines.append(f"  skipped     {dict(self.skipped)}")
        return "\n".join(lines)


# --------------------------------------------------------------------------------------
# Emitters
# --------------------------------------------------------------------------------------

HEADER = '''"""Generated by `aoe2modes decompile` — do not hand-edit unless you mean it.

Regenerating overwrites this file. To keep a change, either move it into the
mode's build.py (which runs after this code and can override anything) or accept
that this file is now hand-maintained and stop regenerating it.
"""

from __future__ import annotations
'''


def _emit_setup(scenario, spec_name: str) -> str:
    mm, pm, om, msg = (
        scenario.map_manager,
        scenario.player_manager,
        scenario.option_manager,
        scenario.message_manager,
    )

    lines = [HEADER, GENERATED_IMPORTS, "", "def apply(ctx) -> None:"]
    lines.append(f'    """Map, player and lobby settings recovered from {spec_name}."""')
    lines.append("    mm, pm, om, msg = ctx.mm, ctx.pm, ctx.scenario.option_manager, ctx.message_manager")
    lines.append("")
    lines.append("    # Map size first: resizing rebuilds the terrain array.")
    lines.append(f"    mm.map_size = {mm.map_size}")
    color_mood = safe_get(mm, "map_color_mood", None)
    if color_mood is not None:
        lines.append(f"    mm.map_color_mood = {render(color_mood, field_name='color_mood')}")
    lines.append("")

    lines.append(f"    pm.active_players = {pm.active_players}")
    for index, player in enumerate(pm.players):
        # GAIA reports None for the fields it has no concept of (diplomacy, tribe
        # name, population cap); writing those back would be meaningless at best.
        present = {}
        for name in PLAYER_FIELDS:
            value = safe_get(player, name, _UNSET)
            if value is not _UNSET and value is not None:
                present[name] = value
        for name in PLAYER_LIST_FIELDS:
            value = safe_get(player, name, _UNSET)
            if value is not _UNSET and value:
                present[name] = value
        if not present:
            continue
        label = "GAIA" if index == 0 else f"P{index}"
        lines.append(f"    # --- {label}")
        lines.append(f"    p = pm.players[{index}]")
        for name, value in present.items():
            if name in PLAYER_LIST_FIELDS:
                lines.append(f"    p.{name} = {render(value, field_name=name)}")
            else:
                lines.append(f"    p.{name} = {render(value, field_name=name)}")
    lines.append("")

    lines.append("    # --- lobby options")
    for name in OPTION_FIELDS:
        value = safe_get(om, name, _UNSET)
        if value is not _UNSET and value is not None:
            lines.append(f"    om.{name} = {render(value, field_name=name)}")
    lines.append("")

    lines.append("    # --- Messages tab")
    for name in MESSAGE_FIELDS:
        value = safe_get(msg, name, _UNSET)
        if value is not _UNSET and value is not None:
            lines.append(f"    msg.{name} = {render(value)}")
    lines.append("")
    return "\n".join(lines)


def _emit_terrain(scenario) -> tuple[str, int, int]:
    """Terrain as run-length pairs; a 144x144 arena is ~2000 runs rather than 20736 tiles."""
    tiles = scenario.map_manager.terrain
    runs: list[tuple[int, int, int, int]] = []
    for tile in tiles:
        key = (tile.terrain_id, tile.elevation, safe_get(tile, "layer", -1))
        if runs and runs[-1][1:] == key:
            runs[-1] = (runs[-1][0] + 1, *key)
        else:
            runs.append((1, *key))

    lines = [HEADER, ""]
    lines.append("# (count, terrain_id, elevation, layer), walking the flat terrain list.")
    lines.append("RUNS: list[tuple[int, int, int, int]] = [")
    for count, terrain_id, elevation, layer in runs:
        lines.append(f"    ({count}, {terrain_id}, {elevation}, {layer}),")
    lines.append("]")
    lines.append("")
    lines.append("")
    lines.append("def apply(ctx) -> None:")
    lines.append('    """Paint the terrain array from the run-length table."""')
    lines.append("    terrain = ctx.mm.terrain")
    lines.append("    index = 0")
    lines.append("    for count, terrain_id, elevation, layer in RUNS:")
    lines.append("        for _ in range(count):")
    lines.append("            tile = terrain[index]")
    lines.append("            tile.terrain_id = terrain_id")
    lines.append("            tile.elevation = elevation")
    lines.append("            tile.layer = layer")
    lines.append("            index += 1")
    lines.append("")
    return "\n".join(lines), len(runs), len(tiles)


def _emit_units(scenario) -> tuple[str, int]:
    um = scenario.unit_manager
    lines = [HEADER, GENERATED_IMPORTS, "", "def apply(ctx) -> None:"]
    lines.append('    """Place every unit, preserving reference ids so triggers keep pointing at them."""')
    lines.append("    um = ctx.um")

    total = 0
    for player_index, units in enumerate(um.units):
        if not units:
            continue
        label = "GAIA" if player_index == 0 else f"Player {player_index}"
        lines.append("")
        lines.append(f"    # --- {label} ({len(units)} units)")
        for unit in units:
            pairs: dict[str, Any] = {"player": player_index}
            for kwarg, attr in UNIT_FIELDS.items():
                value = safe_get(unit, attr, _UNSET)
                if value is _UNSET:
                    continue
                pairs[kwarg] = value
            body = ", ".join(f"{k}={render(v, field_name=k)}" for k, v in pairs.items())
            lines.append(f"    um.add_unit({body})")
            total += 1
    lines.append("")
    return "\n".join(lines), total


def comment_safe(text: str, limit: int = 70) -> str:
    """Make arbitrary scenario text safe to drop into a ``#`` comment.

    Trigger names come from the in-game editor and can contain anything, including
    a bare carriage return — which Python treats as a line terminator *inside the
    source file*, silently ending the comment and corrupting the indentation of
    whatever follows. Control characters are escaped rather than stripped so the
    comment still describes the real name.
    """
    escaped = "".join(char if char.isprintable() else repr(char)[1:-1] for char in str(text))
    return escaped[: limit - 1] + "…" if len(escaped) > limit else escaped


def _emit_trigger(trigger, baselines: Baselines, index: int, display: int) -> list[str]:
    lines: list[str] = []
    lines.append(f"    # --- #{index}  {comment_safe(trigger.name)}   [display {display}]")

    attrs = {}
    for name in TRIGGER_PARAMS:
        value = safe_get(trigger, name, _UNSET)
        if value is _UNSET or value == baselines.trigger.get(name):
            continue
        attrs[name] = value
    head = render_kwargs(attrs)
    prefix = f"    t = tm.add_trigger({render(trigger.name)}"
    lines.append(f"{prefix}, {head})" if head else f"{prefix})")

    for condition in trigger.conditions:
        factory = condition_factory_name(condition)
        params = CONDITION_PARAMS.get(factory, [])
        pairs = changed_fields(condition, params, baselines.conditions.get(factory, {}))
        lines.append(f"    t.new_condition.{factory}({render_kwargs(pairs)})")
    for effect in trigger.effects:
        factory = effect_factory_name(effect)
        params = EFFECT_PARAMS.get(factory, [])
        pairs = changed_fields(effect, params, baselines.effects.get(factory, {}))
        lines.append(f"    t.new_effect.{factory}({render_kwargs(pairs)})")
    lines.append("")
    return lines


def _emit_triggers(scenario, baselines: Baselines, chunk_size: int) -> tuple[list[str], str, int, int]:
    """Return (part sources, package __init__ source, condition count, effect count).

    Triggers are emitted in creation order because ``activate_trigger`` effects
    address triggers by that index. Display order is restored separately.
    """
    tm = scenario.trigger_manager
    triggers = tm.triggers
    display_of = {tid: pos for pos, tid in enumerate(tm.trigger_display_order)}

    parts: list[str] = []
    conditions = effects = 0
    for start in range(0, len(triggers), chunk_size):
        chunk = triggers[start : start + chunk_size]
        body: list[str] = [HEADER, GENERATED_IMPORTS, "", "def emit(tm) -> None:"]
        names = Counter()
        for offset, trigger in enumerate(chunk):
            index = start + offset
            body.extend(_emit_trigger(trigger, baselines, index, display_of.get(index, index)))
            conditions += len(trigger.conditions)
            effects += len(trigger.effects)
            names[trigger.name] += 1
        docline = ", ".join(f"{n}x {comment_safe(name, 30)!r}" for name, n in names.most_common(3))
        body.insert(4, f'    """Triggers {start}..{start + len(chunk) - 1}. Mostly: {docline}."""')
        parts.append("\n".join(body))

    module_names = [f"part_{i:03d}" for i in range(len(parts))]
    init = [HEADER, ""]
    for name in module_names:
        init.append(f"from . import {name}")
    init.append("")
    init.append("#: Parts run in order — trigger ids are positional, so order is load-bearing.")
    init.append("PARTS = [" + ", ".join(module_names) + "]")
    init.append("")
    init.append("#: In-editor display order, when it differs from creation order.")
    init.append(f"DISPLAY_ORDER = {list(tm.trigger_display_order)!r}")
    init.append("")
    init.append("")
    init.append("def apply(ctx) -> None:")
    init.append('    """Recreate every trigger, then restore the in-editor display order."""')
    init.append("    tm = ctx.tm")
    init.append("    for part in PARTS:")
    init.append("        part.emit(tm)")
    init.append("    if DISPLAY_ORDER != list(range(len(DISPLAY_ORDER))):")
    init.append("        tm.trigger_display_order = list(DISPLAY_ORDER)")
    init.append("")
    return parts, "\n".join(init), conditions, effects


PACKAGE_INIT = '''"""Generated by `aoe2modes decompile`.

``apply(ctx)`` rebuilds the whole scenario. The mode's build.py calls it and can
then patch anything it wants — build.py runs after this and wins.

Stage order matters: the map is sized before terrain is painted, units are placed
before triggers reference them, and triggers are created in their original order
because ``activate_trigger`` addresses them positionally.
"""

from __future__ import annotations

from . import setup, terrain, triggers, units

STAGES = (setup, terrain, units, triggers)


def apply(ctx) -> None:
    """Run every generated stage in order."""
    for stage in STAGES:
        ctx.log(f"generated: {stage.__name__.rsplit('.', 1)[-1]}")
        stage.apply(ctx)
'''


def decompile(scenario, out_dir: Path, *, source_label: str = "", chunk_size: int = 250) -> DecompileReport:
    """Write Python that rebuilds *scenario* into ``out_dir`` (a ``generated/`` folder)."""
    out_dir = Path(out_dir)
    triggers_dir = out_dir / "triggers"
    out_dir.mkdir(parents=True, exist_ok=True)
    triggers_dir.mkdir(parents=True, exist_ok=True)

    baselines = Baselines.probe(scenario)
    label = source_label or "the source scenario"

    written: list[Path] = []

    def write(path: Path, text: str) -> None:
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        written.append(path)

    write(out_dir / "__init__.py", PACKAGE_INIT)
    write(out_dir / "setup.py", _emit_setup(scenario, label))

    terrain_src, runs, tiles = _emit_terrain(scenario)
    write(out_dir / "terrain.py", terrain_src)

    units_src, unit_count = _emit_units(scenario)
    write(out_dir / "units.py", units_src)

    parts, init_src, conditions, effects = _emit_triggers(scenario, baselines, chunk_size)
    for index, part in enumerate(parts):
        write(triggers_dir / f"part_{index:03d}.py", part)
    write(triggers_dir / "__init__.py", init_src)

    # Stale parts from a previous, larger decompile would still be imported.
    for leftover in sorted(triggers_dir.glob("part_*.py")):
        if leftover not in written:
            leftover.unlink()

    return DecompileReport(
        out_dir=out_dir,
        triggers=len(scenario.trigger_manager.triggers),
        conditions=conditions,
        effects=effects,
        units=unit_count,
        terrain_runs=runs,
        terrain_tiles=tiles,
        parts=len(parts),
        files=written,
    )
