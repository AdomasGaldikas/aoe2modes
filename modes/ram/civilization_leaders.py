"""Append isolated, civilization-specific starting leaders to RAM's Data Mod.

The existing unit tables, sounds, graphics and legacy unit headers are immutable.
Each civilization supplies the same reserved object ID with its own native donor.
This preserves placed scenario references and leaves later hero armies untouched.
"""

from __future__ import annotations

import hashlib
import json
import math
import tomllib
import zlib
from collections import Counter
from copy import deepcopy
from importlib.metadata import version
from pathlib import Path

ROLES = {"infantry", "melee_cavalry", "ranged", "ranged_cavalry"}
GENGHIS_ID = 731
# Native donor combat/movement tasks; remove auras, conversion and special actions.
COMBAT_ACTIONS = {3, 7, 13, 109}


def _settings(mode_dir: Path) -> dict:
    return tomllib.loads((Path(mode_dir) / "mode.toml").read_text(encoding="utf-8")).get(
        "civilization_leaders", {},
    )


def leaders_enabled(mode_dir: Path) -> bool:
    value = _settings(mode_dir).get("enabled", False)
    if type(value) is not bool:
        raise ValueError("civilization_leaders.enabled must be boolean")
    return value


def leader_unit_id(mode_dir: Path) -> int:
    value = _settings(mode_dir).get("unit_id", 2750)
    if type(value) is not int or not 1 <= value <= 32767:
        raise ValueError("civilization_leaders.unit_id must be a positive signed 16-bit ID")
    return value


def load_leader_catalog(mode_dir: Path) -> list[dict]:
    path = Path(mode_dir) / "assets/leaders/catalog.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    rows = manifest.get("civilizations") if isinstance(manifest, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("Leader catalog requires a nonempty civilizations list")
    seen = set()
    result = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Leader catalog rows must be objects")
        civ = row.get("civilization")
        if type(civ) is not int or civ <= 0 or civ in seen:
            raise ValueError(f"Invalid or duplicate leader civilization: {civ!r}")
        seen.add(civ)
        for field in ("civilization_name", "leader_name", "source_unit_name", "note"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"Leader {civ} requires {field}")
        donor = row.get("source_unit_id")
        if type(donor) is not int or donor < 0:
            raise ValueError(f"Invalid leader donor for civilization {civ}")
        if row.get("role") not in ROLES or type(row.get("fallback")) is not bool:
            raise ValueError(f"Invalid leader role/fallback for civilization {civ}")
        result.append(dict(row))
    return sorted(result, key=lambda row: row["civilization"])


def _profiles(settings: dict) -> dict:
    profiles = settings.get("profiles", {})
    if set(profiles) != ROLES:
        raise ValueError(f"Leader combat profiles must cover exactly {sorted(ROLES)}")
    fields = {"hit_points", "attack", "reload_seconds", "melee_armour", "pierce_armour"}
    for role, profile in profiles.items():
        if not isinstance(profile, dict) or set(profile) != fields:
            raise ValueError(f"Invalid leader combat profile fields: {role}")
        for key, value in profile.items():
            if type(value) not in {int, float} or not math.isfinite(value):
                raise ValueError(f"Invalid leader combat profile: {role}/{key}")
            if value < (0 if key.endswith("armour") else 0.001):
                raise ValueError(f"Invalid leader combat profile value: {role}/{key}")
            if key != "reload_seconds" and (type(value) is not int or value > 32767):
                raise ValueError(f"Leader combat profile requires bounded integer: {role}/{key}")
    return profiles


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _leader_costs(original_leader_costs):
    """Remove economic prices while retaining the old leader's population slot."""
    costs = deepcopy(original_leader_costs)
    for cost in costs:
        if cost.type in {0, 1, 2, 3}:
            cost.amount = 0
    return costs


def package_civilization_leaders(dataset_bytes: bytes, mode_dir: Path) -> tuple[bytes, dict, dict]:
    """Append one isolated unit to every table and prove all original bytes survive."""
    if not leaders_enabled(mode_dir):
        return dataset_bytes, {}, {"enabled": False}
    from genieutils.common import ByteHandler
    from genieutils.datfile import DatFile
    from genieutils.unit import AttackOrArmor

    if version("genieutils-py") != "0.1.2":
        raise RuntimeError("RAM leader DAT patching requires genieutils-py==0.1.2")
    raw = zlib.decompress(dataset_bytes, wbits=-15)
    data = DatFile.from_bytes(ByteHandler(memoryview(raw)))
    if data.to_bytes() != raw:
        raise ValueError("Leader DAT parser does not preserve all input bytes")
    reserved = leader_unit_id(mode_dir)
    if any(len(civ.units) != reserved for civ in data.civs):
        raise ValueError(f"Leader reserved ID {reserved} must equal every input table's length")
    catalog_rows = load_leader_catalog(mode_dir)
    catalog = {row["civilization"]: row for row in catalog_rows}
    actual = {civ_id: civ.name for civ_id, civ in enumerate(data.civs) if civ_id > 0}
    if set(catalog) != set(actual):
        raise ValueError("Leader catalog must cover every non-Gaia DAT civilization exactly")
    if any(catalog[civ_id]["civilization_name"] != name for civ_id, name in actual.items()):
        raise ValueError("Leader catalog civilization names differ from input DAT")
    profiles = _profiles(_settings(mode_dir))
    selection_path = Path(mode_dir) / "assets/selection_audio/manifest.json"
    generated = set()
    if selection_path.is_file():
        generated = {row["id"] for row in json.loads(selection_path.read_text())["civilizations"]
                     if row["mode"] == "generated"}
    original_header_count = len(data.unit_headers)
    source_rows = []
    clones = []
    for civ_id, civ in enumerate(data.civs):
        row = catalog.get(civ_id)
        donor_id = row["source_unit_id"] if row else GENGHIS_ID
        if not 0 <= donor_id < reserved or civ.units[donor_id] is None:
            raise ValueError(f"Missing native leader donor {donor_id} for civilization {civ_id}")
        donor = civ.units[donor_id]
        if donor.bird is None or donor.type_50 is None or donor.creatable is None:
            raise ValueError(f"Leader donor is not a native military unit: {civ_id}/{donor_id}")
        clone = deepcopy(donor)
        clone.id = clone.copy_id = clone.base_id = reserved
        clone.enabled, clone.disabled = 1, 0
        clone.name = f"RAM LEADER {civ_id}"
        clone.bird.run_pattern = 3
        removed_tasks = Counter(t.action_type for t in clone.bird.tasks
                                if t.action_type not in COMBAT_ACTIONS)
        clone.bird.tasks = [t for t in clone.bird.tasks if t.action_type in COMBAT_ACTIONS]
        if not any(t.action_type == 7 for t in clone.bird.tasks):
            raise ValueError(f"Leader donor has no ordinary attack task: {civ_id}/{donor_id}")
        # In particular, Ratha's trait bit 8 exposes weapon switching to an
        # ordinary native ID; a starting leader must never leave its reserved ID.
        clone.trait = 0
        c, combat = clone.creatable, clone.type_50
        c.hero_mode = civ.units[GENGHIS_ID].creatable.hero_mode
        c.train_locations = []
        c.resource_costs = _leader_costs(civ.units[GENGHIS_ID].creatable.resource_costs)
        c.max_charge = c.recharge_rate = 0.0
        c.charge_event = c.charge_type = c.charge_target = 0
        c.charge_projectile_unit = -1
        c.invulnerability_level = 0.0
        c.special_ability = 0
        c.total_projectiles, c.max_total_projectiles = 1.0, 1
        c.secondary_projectile_unit = -1
        c.rear_attack_modifier = c.flank_attack_modifier = 1.0
        combat.blast_width = 0.0
        combat.blast_attack_level = 0
        combat.blast_damage = 1.0
        combat.damage_reflection = combat.friendly_fire_damage = 0.0
        combat.bonus_damage_resistance = 0.0
        role = row["role"] if row else "ranged_cavalry"
        profile = profiles[role]
        main_attacks = {kind: max((a.amount for a in combat.attacks if a.class_ == kind), default=0)
                        for kind in (3, 4)}
        main_class = max((3, 4), key=lambda kind: main_attacks[kind])
        if main_attacks[main_class] <= 0:
            raise ValueError(f"Leader donor has no positive main attack: {civ_id}/{donor_id}")
        clone.hit_points = profile["hit_points"]
        combat.attacks = [AttackOrArmor(class_=main_class, amount=profile["attack"])]
        combat.reload_time = combat.displayed_reload_time = float(profile["reload_seconds"])
        combat.displayed_attack = profile["attack"]
        for armour_class, key in ((4, "melee_armour"), (3, "pierce_armour")):
            entries = [a for a in combat.armours if a.class_ == armour_class]
            if entries:
                for armour in entries:
                    armour.amount = profile[key]
            else:
                combat.armours.append(AttackOrArmor(class_=armour_class, amount=profile[key]))
        combat.displayed_melee_armour = profile["melee_armour"]
        c.displayed_pierce_armour = profile["pierce_armour"]
        if civ_id in generated:
            clone.selection_sound = civ.units[GENGHIS_ID].selection_sound
            clone.wwise_selection_sound_id = civ.units[GENGHIS_ID].wwise_selection_sound_id
        clones.append(clone)
        source_rows.append({
            **(row or {"civilization": 0, "civilization_name": civ.name,
                       "leader_name": "Gaia fallback", "role": role, "fallback": True}),
            "native_donor_id": donor_id, "native_donor_name": donor.name,
            "unit_id": reserved, "main_attack_class": main_class,
            "combat_profile": dict(profile), "speed": clone.speed, "class": clone.class_,
            "range": combat.max_range, "projectile": combat.projectile_unit_id,
            "selection_sound": clone.selection_sound,
            "population_cost": sum(cost.amount for cost in c.resource_costs if cost.type == 4),
            "removed_special_task_actions": dict(sorted(removed_tasks.items())),
            "retained_native_tasks": len(clone.bird.tasks),
            "disabled_native_trait": donor.trait,
        })
    for civ, clone in zip(data.civs, clones, strict=True):
        civ.units.append(clone)
    patched_raw = data.to_bytes()
    reloaded = DatFile.from_bytes(ByteHandler(memoryview(patched_raw)))
    if reloaded.to_bytes() != patched_raw:
        raise ValueError("Appended leader DAT is not stable across reload")
    if len(reloaded.unit_headers) != original_header_count:
        raise ValueError("Leader patch unexpectedly changed legacy unit headers")
    for civ in reloaded.civs:
        if len(civ.units) != reserved + 1 or civ.units[-1].id != reserved:
            raise ValueError("Leader clone table append was not serialized correctly")
        civ.units.pop()
    if reloaded.to_bytes() != raw:
        raise ValueError("Removing appended leaders did not restore every original DAT byte")
    patched = zlib.compress(patched_raw, level=-1, wbits=-15)
    report = {
        "enabled": True, "unit_id": reserved, "civilizations": source_rows,
        "catalogued_non_gaia": len(catalog), "appended_unit_definitions": len(clones),
        "legacy_unit_headers_unchanged": original_header_count,
        "previous_native_genghis": {
            "hit_points": data.civs[0].units[GENGHIS_ID].hit_points,
            "attacks": [{"class": attack.class_, "amount": attack.amount}
                        for attack in data.civs[0].units[GENGHIS_ID].type_50.attacks],
            "reload_seconds": data.civs[0].units[GENGHIS_ID].type_50.reload_time,
            "range": data.civs[0].units[GENGHIS_ID].type_50.max_range,
            "speed": data.civs[0].units[GENGHIS_ID].speed,
        },
        "source_sha256": hashlib.sha256(dataset_bytes).hexdigest(),
        "output_sha256": hashlib.sha256(patched).hexdigest(),
        "restored_original_bytes_exactly": True, "modified_reload_stable": True,
        "native_graphics_movement_class_range_and_projectile_preserved": True,
        "special_auras_charge_splash_conversion_and_weapon_switching_disabled": True,
        "live_match_verified": False,
    }
    text = ["RAM CIVILIZATION LEADERS", "", f"Reserved leader object ID: {reserved}",
            "Native appearances and weapons; normalized starting combat profiles.",
            "Original game unit definitions and global legacy task headers are unchanged.",
            "Special auras, charge, splash, conversion and weapon switching are disabled.", ""]
    text.extend(f"{row['civilization_name']}: {row['leader_name']} ({row['role']})"
                for row in source_rows if row["civilization"])
    extras = {"RAM_CIVILIZATION_LEADERS.json": _json_bytes(report),
              "RAM_CIVILIZATION_LEADERS.txt": ("\n".join(text) + "\n").encode("utf-8")}
    return patched, extras, report
