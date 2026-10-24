"""Explicit all-civilization pacing review, preserving native units and counters."""

import tomllib

from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute


def _adjustments(ctx, baseline):
    settings = tomllib.loads((ctx.mode_dir / "mode.toml").read_text()).get("civilization_balance", {})
    enabled = settings.get("enabled", False)
    if type(enabled) is not bool:
        raise ValueError("civilization_balance.enabled must be boolean")
    if not enabled:
        return []
    rows = settings.get("adjustments", [])
    if not isinstance(rows, list):
        raise ValueError("Balance adjustments must be a list")
    seen = set()
    allowed = {"civilization", "army_cap", "spawn_seconds", "hit_points_bonus", "reason"}
    for row in rows:
        if not isinstance(row, dict) or set(row) - allowed:
            raise ValueError("Balance rows contain invalid fields")
        civilization = row.get("civilization")
        if type(civilization) is not int or civilization not in baseline or civilization in seen:
            raise ValueError("Balance civilization IDs must be known and unique")
        seen.add(civilization)
        _, old_cap, old_interval = baseline[civilization]
        for field, old in (("army_cap", old_cap), ("spawn_seconds", old_interval)):
            value = row.get(field, old)
            if type(value) is not int or value < 1 or not 0.75 <= value / old <= 1.25:
                raise ValueError(f"Balance {field} must be a positive integer within 25% of baseline")
        bonus = row.get("hit_points_bonus", 0)
        if type(bonus) is not int or not 0 <= bonus <= 20:
            raise ValueError("Balance HP bonus must be an integer from 0 to 20")
        reason = row.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Every balance adjustment needs a reason")
    if seen != set(baseline):
        missing = sorted(set(baseline) - seen)
        raise ValueError(f"Enabled balance table must review every civilization; missing={missing}")
    return rows


def balanced_spawn_rules(ctx, baseline):
    rules = baseline.copy()
    for row in _adjustments(ctx, baseline):
        civilization = row["civilization"]
        unit, cap, interval = baseline[civilization]
        rules[civilization] = (unit, row.get("army_cap", cap), row.get("spawn_seconds", interval))
    return rules


def render_civilization_balance(ctx, baseline):
    lines = []
    for row in _adjustments(ctx, baseline):
        bonus = row.get("hit_points_bonus", 0)
        if bonus:
            unit = baseline[row["civilization"]][0]
            # main() executes once, before births, using the actual XS owner/civ.
            lines.extend(
                [
                    f"        if (xsGetPlayerCivilization(worldPlayer) == {row['civilization']}) {{",
                    f"            xsEffectAmount(cAddAttribute, {unit}, "
                    f"{int(ObjectAttribute.HIT_POINTS)}, {bonus}, worldPlayer);",
                    "        }",
                ]
            )
    return "\n".join(lines) + ("\n" if lines else "")
