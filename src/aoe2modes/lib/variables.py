"""The trigger variables that XS and the trigger layer share.

XS writes with ``xsSetTriggerVariable(id, value)``; triggers read with a
"Variable Value" condition. The ids have to match on both sides, so they are declared
once here and mirrored by the ``const int VAR_*`` block in ``xs/lib/util.xs``.
"""

from __future__ import annotations

from dataclasses import dataclass

from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager

WAVE = 0
WAVE_SIZE = 1
MATCH_SECONDS = 2

#: id -> name, in the order the game should allocate them.
SHARED: dict[int, str] = {
    WAVE: "wave",
    WAVE_SIZE: "wave_size",
    MATCH_SECONDS: "match_seconds",
}


@dataclass(frozen=True)
class VariableSet:
    """The ids handed back after declaring a mode's variables."""

    shared: dict[str, int]
    per_player: dict[str, dict[int, int]]

    def player(self, prefix: str, player: int) -> int:
        return self.per_player[prefix][int(player)]


def declare(
    tm: TriggerManager,
    *,
    per_player: dict[str, list[int]] | None = None,
) -> VariableSet:
    """Create the shared variables, plus one variable per (prefix, player) pair.

    ``per_player={"hero_tier": [1, 2, 3]}`` creates ``hero_tier_p1`` … ``hero_tier_p3``.
    """
    for variable_id, name in SHARED.items():
        tm.add_variable(name, variable_id)

    resolved: dict[str, dict[int, int]] = {}
    for prefix, players in (per_player or {}).items():
        resolved[prefix] = {}
        for player in players:
            variable = tm.add_variable(f"{prefix}_p{int(player)}")
            resolved[prefix][int(player)] = variable.variable_id

    return VariableSet(shared=dict(zip(SHARED.values(), SHARED.keys(), strict=True)), per_player=resolved)
