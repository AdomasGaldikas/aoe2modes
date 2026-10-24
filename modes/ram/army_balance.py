"""Deterministic RAM army balance screening, not a native DE combat simulator.

Inputs are measured DAT values plus explicit scenario startup technologies. The
screen retains attack/armour classes, projectile accuracy, multiple projectiles,
limited melee frontage, range lead-in, mobility, splash and Castle replacement.
It omits terrain/pathfinding, player micro, hero tiers, Castle fire, and manually
researched technologies. Its outputs are playtest priorities, never win-rate claims.
"""

from __future__ import annotations

import math
import random
from copy import deepcopy
from statistics import median


def _numeric_keys(unit):
    result = deepcopy(unit)
    for field in ("attack", "armour"):
        result[field] = {int(k): v for k, v in result[field].items()}
    return result


def apply_passive_technologies(snapshot, startup_techs=None, age="feudal"):
    """Apply automatically reachable native bonuses and explicit startup grants.

    Only combat-relevant set/add/multiply commands are interpreted. All unsupported
    relevant commands are exposed in the inventory rather than silently simulated.
    Global technology discovery requires native prerequisites; it does not grant
    blacksmith or unique technologies merely because RAM makes research free.
    """
    techs, effects = snapshot["techs"], snapshot["effects"]
    rows = {int(k): _numeric_keys(v) for k, v in snapshot["units"].items()}
    age_techs = {
        "dark": [104],
        "feudal": [104, 101],
        "castle": [104, 101, 102],
        "imperial": [104, 101, 102, 103],
    }[age]
    for civ, unit in rows.items():
        active = set(age_techs) | set((startup_techs or {}).get(civ, []))
        applied = set()
        candidates = unit.get("automatic_tech_candidates", [])
        changed = True
        while changed:
            changed = False
            for candidate in candidates:
                needed = candidate["required_count"]
                satisfied = sum(t in active for t in candidate["requirements"] if t >= 0)
                if candidate["id"] not in active and satisfied >= needed:
                    active.add(candidate["id"])
                    changed = True
        unsupported = []
        for tech_id in sorted(active):
            tech = techs[tech_id]
            if tech["civ"] not in (-1, civ) or tech["effect_id"] < 0:
                continue
            did_apply = False
            for command in effects[tech["effect_id"]]["commands"]:
                if command["a"] != unit["unit_id"] and not (
                    command["a"] == -1 and command["b"] == unit["class"]
                ):
                    continue
                kind, attr, value = command["type"], command["c"], command["d"]
                if kind not in (0, 4, 5):
                    unsupported.append({"technology": tech_id, **command})
                    continue
                if attr in (8, 9):
                    cls = int(value) // 256
                    amount = value - cls * 256
                    field = "armour" if attr == 8 else "attack"
                    old = unit[field].get(cls, 0)
                    unit[field][cls] = amount if kind == 0 else (old + amount if kind == 4 else old * amount)
                else:
                    field = {
                        0: "hp",
                        5: "speed",
                        10: "reload",
                        11: "accuracy",
                        12: "range",
                        16: "projectile",
                        22: "splash",
                    }.get(attr)
                    if field is None:
                        # Noncombat attributes/costs are not part of the screen.
                        if attr in (24, 59, 60, 61, 63, 100, 101, 102, 103, 104, 105, 106):
                            unsupported.append({"technology": tech_id, **command})
                        continue
                    if field == "accuracy" and kind != 5:
                        value /= 100
                    old = unit[field]
                    unit[field] = value if kind == 0 else (old + value if kind == 4 else old * value)
                did_apply = True
            if did_apply:
                applied.add(tech_id)
        unit["applied_technology_ids"] = sorted(applied)
        unit["unsupported_combat_effects"] = unsupported
    return rows


def hit_damage(attacker, defender):
    """Native matching armour classes; absent bonus classes do not take damage."""
    damage = 0.0
    for kind, attack in attacker["attack"].items():
        if kind not in defender["armour"]:
            continue
        armour = defender["armour"][kind]
        if attacker.get("ignore_armour") and kind == 4:
            armour = 0
        damage += max(0.0, attack - armour)
    return max(1.0, damage)


def damage_per_second(attacker, defender, screened=False):
    damage = hit_damage(attacker, defender)
    shots = max(1.0, attacker.get("projectiles", 1.0))
    # Secondary arrows usually carry reduced native projectile damage. Avoid
    # treating all Chu Ko Nu/Organ Gun arrows as full-strength primary attacks.
    damage += max(0, shots - 1) * 1.0
    if attacker.get("splash", 0) > 0:
        # At most one extra average target; actual density/terrain remain a limit.
        damage *= 1 + min(1.0, attacker["splash"] * 0.8) * max(
            0.0, min(1.0, attacker.get("splash_damage", 1.0))
        )
    accuracy = max(0.05, min(1.0, attacker.get("accuracy", 1)))
    # In packed team fights missed primary shots can still hit another enemy.
    if screened and attacker.get("range", 0) >= 2:
        accuracy += (1 - accuracy) * 0.35
    reload = max(0.1, attacker["reload"])
    base = damage * accuracy / reload
    # Damage-charge types 1/3 have measurable capped opening and sustained charge.
    # Other native charge types are deliberately inventoried, not misread as damage.
    charge = 0.0
    if attacker.get("charge_type") in (1, 3) and 0 < attacker.get("charge", 0) <= 100:
        charge = min(3.0, attacker.get("recharge", 0) + attacker["charge"] / 40)
    return base + charge


def unit_power(unit, opponents):
    """Geometric matchup summary, retaining counters in the underlying matrix."""
    values = []
    for opponent in opponents:
        dealt = damage_per_second(unit, opponent, screened=True)
        received = damage_per_second(opponent, unit, screened=True)
        own_contact = 1.0 if unit["range"] >= 2 else min(1.0, 36 / unit["cap"])
        opposing_contact = 1.0 if opponent["range"] >= 2 else min(1.0, 36 / opponent["cap"])
        effective = unit["hp"] * dealt * own_contact / max(0.05, received * opposing_contact)
        # First-shot reach and modest tactical mobility; no perpetual perfect kite.
        reach = 1 + min(0.45, max(0, unit["range"] - opponent["range"]) * 0.075)
        mobility = 1 + max(-0.12, min(0.12, (unit["speed"] - opponent["speed"]) * 0.12))
        values.append(math.sqrt(max(0.01, effective)) * reach * mobility)
    return math.exp(sum(math.log(v) for v in values) / len(values))


def propose_rules(units, overrides=None):
    """Bounded all-civilization pacing review, not a stat/counter rewrite."""
    pool = list(units.values())
    powers = {civ: unit_power(unit, pool) for civ, unit in units.items()}
    masses = {c: u["cap"] * powers[c] for c, u in units.items()}
    rates = {c: 4 / u["seconds"] * powers[c] for c, u in units.items()}
    mass_target, rate_target = median(masses.values()), median(rates.values())
    result = {}
    for civ, unit in units.items():
        # Partial correction avoids erasing unit identity/counter specialization.
        cap_scale = max(0.75, min(1.25, (mass_target / masses[civ]) ** 0.35))
        interval_scale = max(0.75, min(1.25, (rates[civ] / rate_target) ** 0.35))
        low, high = math.ceil(unit["cap"] * 0.75), math.floor(unit["cap"] * 1.25)
        cap = max(low, min(high, int(round(unit["cap"] * cap_scale / 4) * 4)))
        interval = max(
            math.ceil(unit["seconds"] * 0.75),
            min(math.floor(unit["seconds"] * 1.25), round(unit["seconds"] * interval_scale)),
        )
        result[civ] = {
            "civilization": civ,
            "army_cap": cap,
            "spawn_seconds": interval,
            "hit_points_bonus": 0,
            "reason": "Partial matchup-based pacing correction; native unit and counters retained.",
            "screen_unit_power": powers[civ],
        }
    for civ, values in (overrides or {}).items():
        if civ not in result:
            raise ValueError(f"Unknown override civilization {civ}")
        result[civ].update(values)
    return result


def with_rules(units, rules):
    result = deepcopy(units)
    if set(result) != set(rules):
        raise ValueError("Balance rules must cover every civilization exactly")
    for civ, row in rules.items():
        cap, seconds = row["army_cap"], row["spawn_seconds"]
        if type(cap) is not int or type(seconds) is not int or cap <= 0 or seconds <= 0:
            raise ValueError("Army caps and spawn intervals must be positive integers")
        result[civ]["cap"], result[civ]["seconds"] = cap, seconds
        result[civ]["hp"] += row.get("hit_points_bonus", 0)
    return result


def simulate_teams(left, right, seconds=180, step=0.5, full_start=False, frontage=24):
    """Fractional-cohort attrition with simultaneous damage and replacements.

    Both armies approach from 12 tiles. Melee has finite frontage; ranged units
    behind surviving allied melee retain firing opportunities. This is deliberately
    a screening proxy with no native pathfinding or perfect target micro.
    """
    if not left or not right or step <= 0 or seconds <= 0:
        raise ValueError("Two nonempty teams and positive simulation timing required")
    teams = [list(left), list(right)]
    populations = [[float(u["cap"] if full_start else min(u["cap"], 12)) for u in team] for team in teams]
    initial = [
        sum(n * u["hp"] for n, u in zip(nums, team, strict=True))
        for nums, team in zip(populations, teams, strict=True)
    ]
    kills = [0.0, 0.0]
    for tick in range(math.ceil(seconds / step)):
        t = tick * step
        losses = [[0.0 for _ in team] for team in teams]
        for side in (0, 1):
            enemy = 1 - side
            targets = [
                (i, u, populations[enemy][i])
                for i, u in enumerate(teams[enemy])
                if populations[enemy][i] > 0.001
            ]
            if not targets:
                continue
            enemy_speed = sum(u["speed"] * n for _, u, n in targets) / sum(n for _, _, n in targets)
            melee_total = sum(populations[side][i] for i, u in enumerate(teams[side]) if u["range"] < 2)
            # Wider engagements emerge as combat unfolds, bounded by the map's routes.
            contacts = frontage * max(1, len(teams[side]) ** 0.5) * min(1.8, 1 + t / 90)
            for i, unit in enumerate(teams[side]):
                count = populations[side][i]
                if count <= 0.001:
                    continue
                ranged = unit["range"] >= 2
                approach = max(0.0, (12 - unit["range"]) / max(0.1, unit["speed"] + enemy_speed))
                if t < approach:
                    continue
                active = count if ranged else count * min(1.0, contacts / max(1, melee_total))
                target_pool = targets
                if not ranged:
                    front = [(j, u, n) for j, u, n in targets if u["range"] < 2]
                    if front:
                        target_pool = front
                # Attack the enemy frontage, distributed by presence, not an
                # omniscient selection of the most profitable counter target.
                total = sum(n for _, _, n in target_pool)
                screened = ranged and melee_total > 1
                for j, defender, amount in target_pool:
                    dealt = active * damage_per_second(unit, defender, screened) * amount / total * step
                    losses[enemy][j] += dealt / defender["hp"]
        for side in (0, 1):
            for i, unit in enumerate(teams[side]):
                died = min(populations[side][i], losses[side][i])
                kills[1 - side] += died
                populations[side][i] = min(
                    unit["cap"], max(0.0, populations[side][i] - died) + 4 / unit["seconds"] * step
                )
    remaining = [
        sum(n * u["hp"] for n, u in zip(nums, team, strict=True))
        for nums, team in zip(populations, teams, strict=True)
    ]
    # Signed health advantage normalized by the larger initial team budget.
    advantage = (remaining[0] - remaining[1]) / max(1.0, max(initial))
    return {
        "advantage": advantage,
        "remaining_hp": remaining,
        "kills": kills,
        "remaining_units": populations,
        "seconds": seconds,
    }


def mixed_team_screen(units, draws=128, seed=816, team_sizes=(1, 2, 4)):
    """Reproducible distinct-lineup trials including mixed ranged/melee teams."""
    rng = random.Random(seed)
    civs = sorted(units)
    trials = []
    contributions = {civ: [] for civ in civs}
    for size in team_sizes:
        for _ in range(draws):
            selected = rng.sample(civs, min(len(civs), size * 2))
            if len(selected) < size * 2:
                continue
            a, b = selected[:size], selected[size:]
            outcome = simulate_teams([units[c] for c in a], [units[c] for c in b], seconds=90)
            value = max(-1.0, min(1.0, outcome["advantage"]))
            for c in a:
                contributions[c].append(value)
            for c in b:
                contributions[c].append(-value)
            trials.append({"left": a, "right": b, "advantage": value})
    return {
        "seed": seed,
        "trials": trials,
        "mean_contribution": {c: sum(v) / len(v) if v else 0 for c, v in contributions.items()},
        "sample_count": {c: len(v) for c, v in contributions.items()},
    }


def review_saved_inputs(inputs, review, draws=64, seed=816):
    """Reproduce mixed-team screens from compact checked-in measured inputs."""
    if inputs.get("schema_version") != 1 or review.get("schema_version") != 1:
        raise ValueError("Unsupported saved balance review schema")
    units = {int(cid): _numeric_keys(row) for cid, row in inputs["units"].items()}
    rules = {row["civilization"]: row for row in review["rules"]}
    previous = {row["civilization"]: row["previous"] for row in review["rules"]}
    return {
        "schema_version": 1,
        "purpose": "Reproducible screening only; native balance and win rates remain unverified.",
        "native_dataset_sha256": inputs["native_dataset_sha256"],
        "civilization_count": len(units),
        "assumptions": review["screen_assumptions"],
        "before": mixed_team_screen(with_rules(units, previous), draws=draws, seed=seed),
        "after": mixed_team_screen(with_rules(units, rules), draws=draws, seed=seed),
    }


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--draws", type=int, default=64)
    args = parser.parse_args()
    if args.draws < 1:
        parser.error("--draws must be positive")
    report = review_saved_inputs(
        json.loads(args.inputs.read_text()), json.loads(args.review.read_text()), draws=args.draws
    )
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"Reviewed {report['civilization_count']} civilizations; "
        f"{len(report['before']['trials'])} distinct-lineup trials per version. "
        "Native gameplay acceptance remains open."
    )


if __name__ == "__main__":
    main()
