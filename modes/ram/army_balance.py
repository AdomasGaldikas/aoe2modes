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
    result.setdefault("population_per_body", 1.0)
    # Bit 1 is native armour bypass on Leitis and Composite Bowmen. Explicit
    # IDs retain correct screening when older measured inputs lack this byte.
    result.setdefault(
        "ignore_base_armour",
        bool(result.get("ignore_armour"))
        or bool(result.get("break_off_combat", 0) & 1)
        or result.get("unit_id") in (1236, 1802),
    )
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
        if kind in (3, 4) and (
            attacker.get("ignore_base_armour")
            or attacker.get("ignore_armour")
            or bool(attacker.get("break_off_combat", 0) & 1)
            or attacker.get("unit_id") in (1236, 1802)
        ):
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


def unit_limit(unit, cap_basis="bodies"):
    """Convert the configured cap for an explicitly chosen sensitivity scenario.

    Native MilitaryPopulation/resource-40 accounting is not inferred from DAT
    population storage. The default is body-count caps; population weighting is
    a separate sensitivity calculation, never a runtime rule or asserted fact.
    """
    if cap_basis not in {"bodies", "population"}:
        raise ValueError("cap_basis must be bodies or population")
    population = unit.get("population_per_body", 1.0)
    if not isinstance(population, (int, float)) or not math.isfinite(population) or population <= 0:
        raise ValueError("population_per_body must be finite and positive")
    return float(unit["cap"]) / (population if cap_basis == "population" else 1.0)


def simulate_teams(
    left,
    right,
    seconds=180,
    step=0.5,
    full_start=False,
    frontage=24,
    cap_basis="bodies",
    contact_mode="frontal",
):
    """Simultaneous cohort attrition, explicit frontage and kill-feed accounting.

    Fresh build-up starts with zero ordinary units; full-field starts at each
    configured body limit. Replacements approximate four surviving Castles as a
    continuous stream, rather than native four-body batches. Contact mode and cap
    basis are independent scenario choices, not claims about engine geometry.
    """
    if not left or not right or step <= 0 or seconds <= 0 or frontage <= 0:
        raise ValueError("Two nonempty teams and positive simulation timing/frontage required")
    if contact_mode not in {"frontal", "wide"}:
        raise ValueError("contact_mode must be frontal or wide")
    teams = [list(left), list(right)]
    limits = [[unit_limit(u, cap_basis) for u in team] for team in teams]
    populations = [[limit if full_start else 0.0 for limit in side] for side in limits]
    budgets = [
        sum(limit * u["hp"] for limit, u in zip(side, team, strict=True))
        for side, team in zip(limits, teams, strict=True)
    ]
    dps = [
        [
            [
                tuple(damage_per_second(attacker, defender, screened) for screened in (False, True))
                for defender in teams[1 - side]
            ]
            for attacker in team
        ]
        for side, team in enumerate(teams)
    ]
    kills, destroyed_hp, births = [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]
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
            contacts = (
                frontage
                * (2 if contact_mode == "wide" else 1)
                * max(1, len(teams[side]) ** 0.5)
                * min(1.8, 1 + t / 90)
            )
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
                total = sum(n for _, _, n in target_pool)
                screened = int(ranged and melee_total > 1)
                for j, defender, amount in target_pool:
                    dealt = active * dps[side][i][j][screened] * amount / total * step
                    losses[enemy][j] += dealt / defender["hp"]
        for side in (0, 1):
            for i, unit in enumerate(teams[side]):
                died = min(populations[side][i], losses[side][i])
                kills[1 - side] += died
                destroyed_hp[1 - side] += died * unit["hp"]
                survivors = max(0.0, populations[side][i] - died)
                born = min(max(0.0, limits[side][i] - survivors), 4 / unit["seconds"] * step)
                births[side] += born
                populations[side][i] = survivors + born
    remaining = [
        sum(n * u["hp"] for n, u in zip(side, team, strict=True))
        for side, team in zip(populations, teams, strict=True)
    ]
    fractions = [hp / max(1.0, budget) for hp, budget in zip(remaining, budgets, strict=True)]
    kill_sum = sum(kills)
    return {
        "advantage": (remaining[0] - remaining[1]) / max(1.0, max(budgets)),
        "normalized_hp_advantage": fractions[0] - fractions[1],
        "remaining_hp": remaining,
        "remaining_hp_fraction": fractions,
        "full_field_hp_budget": budgets,
        "kills": kills,
        # Every ordinary death gives one native kill regardless of body HP.
        "killfeed_advantage": (kills[0] - kills[1]) / max(1.0, kill_sum),
        "enemy_hero_kills_fed": kills[::-1],
        "hp_destroyed": destroyed_hp,
        "hp_per_kill": [hp / n if n > 0 else 0.0 for hp, n in zip(destroyed_hp, kills, strict=True)],
        "hp_trade_ratio": (destroyed_hp[0] + 1) / (destroyed_hp[1] + 1),
        "kill_trade_ratio": (kills[0] + 1) / (kills[1] + 1),
        "births": births,
        "remaining_units": populations,
        "body_limits": limits,
        "seconds": seconds,
        "cap_basis": cap_basis,
        "contact_mode": contact_mode,
        "full_start": full_start,
    }


def mixed_team_screen(
    units,
    draws=128,
    seed=816,
    team_sizes=(1, 2, 4),
    *,
    cap_basis="bodies",
    contact_mode="frontal",
    full_start=False,
    seconds=90,
):
    """Equal-exposure paired rounds with separate 1v1, 2v2 and 4v4 reports.

    Each shuffled cyclic round uses every civilization in every lineup position;
    every trial has its side-swapped partner. A full round can exceed requested
    draws, rather than silently dropping civilizations or giving uneven samples.
    These are lineup results, not isolated causal effects of individual civs.
    """
    if type(draws) is not int or draws < 1:
        raise ValueError("draws must be a positive integer")
    rng = random.Random(seed)
    units = {civ: _numeric_keys(unit) for civ, unit in units.items()}
    civs = sorted(units)
    trials, by_size = [], {}
    all_scores = {civ: [] for civ in civs}
    all_feed = {civ: [] for civ in civs}
    for size in team_sizes:
        if type(size) is not int or size < 1:
            raise ValueError("Team sizes must be positive integers")
        if len(civs) < size * 2:
            continue
        rounds = math.ceil(draws / (2 * len(civs)))
        scores = {civ: [] for civ in civs}
        feeds = {civ: [] for civ in civs}
        positions = {civ: [0] * (size * 2) for civ in civs}
        size_trials = []
        for _ in range(rounds):
            order = rng.sample(civs, len(civs))
            ring = order + order
            for start in range(len(civs)):
                selected = ring[start : start + size * 2]
                for swapped in (False, True):
                    a, b = selected[:size], selected[size:]
                    if swapped:
                        a, b = b, a
                    outcome = simulate_teams(
                        [units[c] for c in a],
                        [units[c] for c in b],
                        seconds=seconds,
                        cap_basis=cap_basis,
                        contact_mode=contact_mode,
                        full_start=full_start,
                    )
                    value = outcome["normalized_hp_advantage"]
                    feed = outcome["killfeed_advantage"]
                    for position, civ in enumerate(a + b):
                        sign = 1 if position < size else -1
                        scores[civ].append(sign * value)
                        feeds[civ].append(sign * feed)
                        all_scores[civ].append(sign * value)
                        all_feed[civ].append(sign * feed)
                        positions[civ][position] += 1
                    trial = {
                        "left": a,
                        "right": b,
                        "advantage": outcome["advantage"],
                        "normalized_hp_advantage": value,
                        "killfeed_advantage": feed,
                        "hp_trade_ratio": outcome["hp_trade_ratio"],
                        "kill_trade_ratio": outcome["kill_trade_ratio"],
                        "kills": outcome["kills"],
                        "hp_destroyed": outcome["hp_destroyed"],
                    }
                    size_trials.append(trial)
                    trials.append(trial)
        counts = {c: len(v) for c, v in scores.items()}
        if len(set(counts.values())) != 1 or any(len(set(v)) != 1 for v in positions.values()):
            raise RuntimeError("Unbalanced paired-round civilization exposure")
        by_size[str(size)] = {
            "paired_rounds": rounds,
            "trial_count": len(size_trials),
            "sample_count": counts,
            "lineup_position_counts": positions,
            "mean_contribution": {c: sum(v) / len(v) for c, v in scores.items()},
            "mean_killfeed_advantage": {c: sum(v) / len(v) for c, v in feeds.items()},
            "trials": size_trials,
        }
    return {
        "seed": seed,
        "requested_draws_per_team_size": draws,
        "trials": trials,
        "by_team_size": by_size,
        "score_definition": "Own-field HP fraction; paired lineup effect, not native win rate.",
        "cap_basis": cap_basis,
        "contact_mode": contact_mode,
        "full_start": full_start,
        "mean_contribution": {c: sum(v) / len(v) if v else 0 for c, v in all_scores.items()},
        "mean_killfeed_advantage": {c: sum(v) / len(v) if v else 0 for c, v in all_feed.items()},
        "sample_count": {c: len(v) for c, v in all_scores.items()},
    }


def review_saved_inputs(
    inputs, review, draws=64, seed=816, *, cap_basis="bodies", contact_mode="frontal", full_start=False
):
    """Reproduce explicit combat/kill-feed sensitivity scenarios from saved inputs."""
    if inputs.get("schema_version") != 1 or review.get("schema_version") != 1:
        raise ValueError("Unsupported saved balance review schema")
    units = {int(cid): _numeric_keys(row) for cid, row in inputs["units"].items()}
    rules = {row["civilization"]: row for row in review["rules"]}
    previous = {row["civilization"]: row["previous"] for row in review["rules"]}
    options = {
        "draws": draws,
        "seed": seed,
        "cap_basis": cap_basis,
        "contact_mode": contact_mode,
        "full_start": full_start,
    }
    return {
        "schema_version": 1,
        "purpose": "Combat and kill-feed screening only; native balance/win rates remain unverified.",
        "native_dataset_sha256": inputs["native_dataset_sha256"],
        "civilization_count": len(units),
        "assumptions": review["screen_assumptions"]
        + [
            "Native military-cap accounting is unverified; body/population bases are separate sensitivities.",
            "Fresh starts contain no ordinary units; replacements approximate four-Castle waves.",
            "Paired rounds equalize lineup positions; opponent coverage and human micro are not exhaustive.",
            "Deaths feed equal native kills; the screen does not change progression or add a kill ledger.",
        ],
        "before": mixed_team_screen(with_rules(units, previous), **options),
        "after": mixed_team_screen(with_rules(units, rules), **options),
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
    parser.add_argument("--cap-basis", choices=("bodies", "population"), default="bodies")
    parser.add_argument("--contacts", choices=("frontal", "wide"), default="frontal")
    parser.add_argument("--start", choices=("fresh", "full"), default="fresh")
    args = parser.parse_args()
    if args.draws < 1:
        parser.error("--draws must be positive")
    report = review_saved_inputs(
        json.loads(args.inputs.read_text()),
        json.loads(args.review.read_text()),
        draws=args.draws,
        cap_basis=args.cap_basis,
        contact_mode=args.contacts,
        full_start=args.start == "full",
    )
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"Reviewed {report['civilization_count']} civilizations; "
        f"{len(report['before']['trials'])} paired-lineup trials per version. "
        "Native gameplay acceptance remains open."
    )


if __name__ == "__main__":
    main()
