"""Structural diff between two ``.aoe2scenario`` files.

The intended use is reverse-engineering an evolving CBA Hero variant: load a
baseline and a successor, then see which triggers were added, removed or
reshaped. The comparison is deliberately structural rather than byte-exact —
two triggers with the same name and effect signature count as "the same"
even if their internal IDs shifted.

Loading order matters. The parser leaks version-scoped global state between
scenarios; ``load_pair`` peeks each file's version and loads newest-first so a
v1.51 file never poisons a subsequent v1.58 load in the same process.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


def peek_scenario_version(path: Path) -> tuple[int, int]:
    """Read the 4-byte ASCII version stamp at the start of a scenario file."""
    with path.open("rb") as handle:
        raw = handle.read(4).decode("ascii")
    major, _, minor = raw.partition(".")
    return (int(major), int(minor or 0))


def load_pair(a: Path, b: Path) -> tuple[AoE2DEScenario, AoE2DEScenario]:
    """Load two scenarios newest-first, then return them in the original order.

    Loading v1.51 before v1.58 crashes the parser (see toolchain.py). We always
    load whichever is newer first, but keep the caller's semantic ``(a, b)``
    ordering by swapping back.
    """
    if peek_scenario_version(a) >= peek_scenario_version(b):
        return AoE2DEScenario.from_file(str(a)), AoE2DEScenario.from_file(str(b))
    scenario_b = AoE2DEScenario.from_file(str(b))
    scenario_a = AoE2DEScenario.from_file(str(a))
    return scenario_a, scenario_b


@dataclass(frozen=True)
class TriggerSignature:
    """What we treat as "the same trigger" across two files.

    Name plus the sorted tuple of condition and effect type ids. That is enough
    to spot renames (name differs) and re-shaping (types differ) while being
    robust to trivial reordering of effects within a trigger.
    """

    name: str
    condition_types: tuple[int, ...]
    effect_types: tuple[int, ...]

    @classmethod
    def of(cls, trigger) -> TriggerSignature:
        return cls(
            name=trigger.name,
            condition_types=tuple(sorted(int(c.condition_type) for c in trigger.conditions)),
            effect_types=tuple(sorted(int(e.effect_type) for e in trigger.effects)),
        )


@dataclass(frozen=True)
class DiffReport:
    added_signatures: Counter
    removed_signatures: Counter
    renamed_or_reshaped_by_name: dict[str, tuple[int, int]]  # name -> (in_a, in_b)
    same_signatures: Counter
    a_total: int
    b_total: int


def diff_triggers(a: AoE2DEScenario, b: AoE2DEScenario) -> DiffReport:
    """Compare the trigger sets of two scenarios by structural signature."""
    sigs_a = Counter(TriggerSignature.of(t) for t in a.trigger_manager.triggers)
    sigs_b = Counter(TriggerSignature.of(t) for t in b.trigger_manager.triggers)

    added = Counter({sig: n for sig, n in (sigs_b - sigs_a).items()})
    removed = Counter({sig: n for sig, n in (sigs_a - sigs_b).items()})
    same = sigs_a & sigs_b

    # A trigger whose signature moved but whose name still exists on both sides
    # is almost always a reshape rather than an add+remove — surface those.
    names_a = Counter(t.name for t in a.trigger_manager.triggers)
    names_b = Counter(t.name for t in b.trigger_manager.triggers)
    shared_names = set(names_a) & set(names_b)
    reshaped = {
        name: (names_a[name], names_b[name])
        for name in shared_names
        if names_a[name] != names_b[name]
    }

    return DiffReport(
        added_signatures=added,
        removed_signatures=removed,
        renamed_or_reshaped_by_name=reshaped,
        same_signatures=same,
        a_total=len(a.trigger_manager.triggers),
        b_total=len(b.trigger_manager.triggers),
    )


def format_report(report: DiffReport, a_label: str, b_label: str) -> str:
    """Render a DiffReport as human-readable text."""
    lines: list[str] = []
    lines.append(f"triggers        {a_label}: {report.a_total}   {b_label}: {report.b_total}")
    lines.append(f"unchanged sigs  {sum(report.same_signatures.values())}")
    lines.append(f"removed sigs    {sum(report.removed_signatures.values())}")
    lines.append(f"added sigs      {sum(report.added_signatures.values())}")
    lines.append("")

    def render_top(counter: Counter, header: str, limit: int) -> None:
        if not counter:
            return
        lines.append(header)
        for sig, count in counter.most_common(limit):
            sig: TriggerSignature
            lines.append(
                f"  x{count:<3} {sig.name!r:<40} "
                f"c={len(sig.condition_types):<2} e={len(sig.effect_types):<2}"
            )
        remaining = len(counter) - min(limit, len(counter))
        if remaining > 0:
            lines.append(f"  ... {remaining} more distinct signatures")
        lines.append("")

    render_top(report.removed_signatures, f"REMOVED (in {a_label} only)", limit=25)
    render_top(report.added_signatures, f"ADDED   (in {b_label} only)", limit=25)

    if report.renamed_or_reshaped_by_name:
        lines.append("RESHAPED (same name, different count per name)")
        for name, (in_a, in_b) in sorted(report.renamed_or_reshaped_by_name.items())[:25]:
            lines.append(f"  {name!r:<40} {a_label}: {in_a}   {b_label}: {in_b}")
        remaining = len(report.renamed_or_reshaped_by_name) - 25
        if remaining > 0:
            lines.append(f"  ... {remaining} more reshaped names")

    return "\n".join(lines)
