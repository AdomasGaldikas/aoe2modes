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

ROLES = {"ranged", "ranged_cavalry"}
WEAPONS = {"bow", "crossbow", "firearm"}
ARROW_PROJECTILES = {363, 364, 373, 477, 478, 503, 507, 510, 511, 1781, 2608, 2609}
FIREARM_PROJECTILES = {380}
GENGHIS_ID = 731
# Native unit resource storages control population consumption and counters.
POPULATION_STORAGE_TYPES = frozenset({4, 11, 19})
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
        if row.get("weapon") not in WEAPONS:
            raise ValueError(f"Invalid leader bow/crossbow/firearm weapon: {civ}")
        for field in ("source_projectile_unit_id", "source_attack_graphic"):
            value = row.get(field)
            if type(value) is not int or value < 0:
                raise ValueError(f"Leader {civ} requires native {field}")
        allowed = FIREARM_PROJECTILES if row["weapon"] == "firearm" else ARROW_PROJECTILES
        if row["source_projectile_unit_id"] not in allowed:
            raise ValueError(f"Leader {civ} does not use a native arrow or firearm projectile")
        result.append(dict(row))
    return sorted(result, key=lambda row: row["civilization"])


def _profiles(settings: dict) -> dict:
    profiles = settings.get("profiles", {})
    if set(profiles) != ROLES:
        raise ValueError(f"Leader combat profiles must cover exactly {sorted(ROLES)}")
    integer_bounds = {"hit_points": (1, 32767), "attack": (1, 32767),
                      "melee_armour": (0, 32767), "pierce_armour": (0, 32767),
                      "accuracy_percent": (1, 100)}
    scalar_bounds = {"reload_seconds": (0.1, 60), "range": (1, 20), "speed": (0.1, 3)}
    fields = set(integer_bounds) | set(scalar_bounds)
    for role, profile in profiles.items():
        if not isinstance(profile, dict) or set(profile) != fields:
            raise ValueError(f"Invalid leader combat profile fields: {role}")
        for key, value in profile.items():
            if type(value) not in {int, float} or not math.isfinite(value):
                raise ValueError(f"Invalid leader combat profile: {role}/{key}")
            lower, upper = (integer_bounds | scalar_bounds)[key]
            if not lower <= value <= upper:
                raise ValueError(f"Leader combat profile out of bounds: {role}/{key}")
            if key in integer_bounds and type(value) is not int:
                raise ValueError(f"Leader combat profile requires integer: {role}/{key}")
    if profiles["ranged"] != profiles["ranged_cavalry"]:
        raise ValueError("Ranged leader profiles must share identical starting combat values")
    return profiles


def _validate_ranged_donor(donor, row: dict, civilization: int) -> None:
    """Check the actual input DAT against the reviewed native-actor snapshot."""
    if (donor.bird is None or donor.type_50 is None or donor.creatable is None
            or donor.dead_fish is None or donor.class_ not in {0, 23, 36, 44}):
        raise ValueError(f"Leader donor is not a mobile native ranged military actor: {civilization}")
    combat = donor.type_50
    expected_role = "ranged_cavalry" if donor.class_ in {23, 36} else "ranged"
    if row["role"] != expected_role:
        raise ValueError(f"Leader donor body role differs from catalog: {civilization}")
    if (combat.projectile_unit_id != row["source_projectile_unit_id"]
            or combat.attack_graphic != row["source_attack_graphic"]):
        raise ValueError(f"Leader native projectile/attack animation differs from catalog: {civilization}")
    allowed = FIREARM_PROJECTILES if row["weapon"] == "firearm" else ARROW_PROJECTILES
    if combat.projectile_unit_id not in allowed or combat.attack_graphic < 0 or combat.max_range <= 1:
        raise ValueError(f"Leader donor has no native bow/crossbow/firearm attack: {civilization}")
    if not any(attack.amount > 0 for attack in combat.attacks):
        raise ValueError(f"Leader donor has no positive native attack: {civilization}")
    if not any(task.action_type == 7 for task in donor.bird.tasks):
        raise ValueError(f"Leader donor has no ordinary native attack task: {civilization}")


def _native_visuals(unit) -> dict:
    return {"standing": list(unit.standing_graphic), "dying": unit.dying_graphic,
            "walking": unit.dead_fish.walking_graphic, "running": unit.dead_fish.running_graphic,
            "attack": unit.type_50.attack_graphic, "projectile": unit.type_50.projectile_unit_id}


def _copy_counter_template(clone, original_khan) -> None:
    clone.class_ = original_khan.class_
    clone.type_50.armours = deepcopy(original_khan.type_50.armours)
    clone.type_50.base_armor = original_khan.type_50.base_armor


def _normalise_ranged_stats(clone, profile: dict) -> None:
    """Equal powers for every national actor; preserve the actual weapon animation."""
    combat = clone.type_50
    clone.hit_points = profile["hit_points"]
    clone.speed = float(profile["speed"])
    clone.line_of_sight = max(clone.line_of_sight, float(profile["range"]) + 2.0, 7.0)
    attack_type = type(combat.attacks[0])
    combat.attacks = [attack_type(class_=3, amount=profile["attack"])]
    combat.reload_time = combat.displayed_reload_time = float(profile["reload_seconds"])
    combat.displayed_attack = profile["attack"]
    combat.max_range = combat.displayed_range = float(profile["range"])
    combat.min_range = 0.0
    combat.accuracy_percent = profile["accuracy_percent"]
    combat.accuracy_dispersion = 0.0
    for armour_class, key in ((4, "melee_armour"), (3, "pierce_armour")):
        entries = [armour for armour in combat.armours if armour.class_ == armour_class]
        if entries:
            for armour in entries:
                armour.amount = profile[key]
        else:
            combat.armours.append(attack_type(class_=armour_class, amount=profile[key]))
    combat.displayed_melee_armour = profile["melee_armour"]
    clone.creatable.displayed_pierce_armour = profile["pierce_armour"]


def _acknowledgement_groups(unit) -> dict:
    return {"selection": unit.selection_sound, "move": unit.bird.move_sound,
            "attack": unit.bird.attack_sound}


def _wwise_fallbacks(unit) -> dict:
    return {"selection": unit.wwise_selection_sound_id, "move": unit.bird.wwise_move_sound_id,
            "attack": unit.bird.wwise_attack_sound_id}


def _copy_acknowledgements(clone, voice_source) -> None:
    """Use accepted national replies but retain each donor's native Wwise fallback."""
    fallback = _wwise_fallbacks(clone)
    clone.selection_sound = voice_source.selection_sound
    clone.bird.move_sound = voice_source.bird.move_sound
    clone.bird.attack_sound = voice_source.bird.attack_sound
    if _wwise_fallbacks(clone) != fallback:
        raise ValueError("Copying leader acknowledgements changed native Wwise fallbacks")


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _leader_costs(original_leader_costs):
    """Remove economic prices while retaining the old leader's population slot."""
    costs = deepcopy(original_leader_costs)
    for cost in costs:
        if cost.type in {0, 1, 2, 3}:
            cost.amount = 0
    return costs


def _population_storage_snapshot(storages) -> dict[int, tuple[float, int]]:
    """Capture the three native population storages without hiding duplicates."""
    result = {}
    for storage in storages:
        if storage.type not in POPULATION_STORAGE_TYPES:
            continue
        if storage.type in result:
            raise ValueError(f"Duplicate leader population storage type {storage.type}")
        result[storage.type] = (storage.amount, storage.flag)
    if set(result) != POPULATION_STORAGE_TYPES:
        missing = sorted(POPULATION_STORAGE_TYPES - result.keys())
        raise ValueError(f"Missing leader population storage types: {missing}")
    return result


def _leader_population_storages(donor_storages, original_leader_storages):
    """Copy the original leader's population accounting, preserving other fields.

    DE's unit table has a fixed-size resource storage array. Reject missing or
    duplicate types instead of silently replacing a potentially unrelated entry.
    """
    _population_storage_snapshot(donor_storages)
    _population_storage_snapshot(original_leader_storages)
    original = {entry.type: entry for entry in original_leader_storages
                if entry.type in POPULATION_STORAGE_TYPES}
    return tuple(deepcopy(original[entry.type] if entry.type in original else entry)
                 for entry in donor_storages)


def package_civilization_leaders(dataset_bytes: bytes, mode_dir: Path) -> tuple[bytes, dict, dict]:
    """Append one isolated unit to every table and prove all original bytes survive."""
    if not leaders_enabled(mode_dir):
        return dataset_bytes, {}, {"enabled": False}
    from genieutils.common import ByteHandler
    from genieutils.datfile import DatFile

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
        donor_row = row or {"role": "ranged_cavalry", "weapon": "bow",
                            "source_projectile_unit_id": donor.type_50.projectile_unit_id,
                            "source_attack_graphic": donor.type_50.attack_graphic}
        _validate_ranged_donor(donor, donor_row, civ_id)
        native_visuals = _native_visuals(donor)
        native_fallbacks = _wwise_fallbacks(donor)
        clone = deepcopy(donor)
        # Every national actor keeps the old Khan's counter/bonus envelope.
        # Native cavalry, foot, elephant and wagon visuals must not grant
        # different anti-unit armour classes or class-based civilization bonuses.
        original_khan = civ.units[GENGHIS_ID]
        _copy_counter_template(clone, original_khan)
        clone.resource_storages = _leader_population_storages(
            clone.resource_storages, original_khan.resource_storages,
        )
        if (_population_storage_snapshot(clone.resource_storages)
                != _population_storage_snapshot(original_khan.resource_storages)):
            raise ValueError(f"Leader population storage differs from original: {civ_id}")
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
        main_class = 3
        _normalise_ranged_stats(clone, profile)
        if civ_id in generated:
            _copy_acknowledgements(clone, civ.units[GENGHIS_ID])
        if _native_visuals(clone) != native_visuals or _wwise_fallbacks(clone) != native_fallbacks:
            raise ValueError(f"Leader normalization changed native visuals or Wwise fallback: {civ_id}")
        clones.append(clone)
        source_rows.append({
            **(row or {"civilization": 0, "civilization_name": civ.name,
                       "leader_name": "Gaia fallback", "role": role, "fallback": True}),
            "native_donor_id": donor_id, "native_donor_name": donor.name,
            "unit_id": reserved, "main_attack_class": main_class,
            "combat_profile": dict(profile), "speed": clone.speed, "class": clone.class_,
            "native_donor_class": donor.class_, "shared_class": original_khan.class_,
            "shared_counter_armour_classes": [{"class": armour.class_, "amount": armour.amount}
                                             for armour in combat.armours],
            "range": combat.max_range, "projectile": combat.projectile_unit_id,
            "selection_sound": clone.selection_sound,
            "acknowledgement_sound_groups": _acknowledgement_groups(clone),
            "native_wwise_fallbacks": native_fallbacks,
            "acknowledgements_copied_from_generated_genghis": civ_id in generated,
            "native_visuals": native_visuals,
            "native_visuals_and_wwise_fallbacks_preserved": True,
            "minimum_range": combat.min_range, "accuracy_percent": combat.accuracy_percent,
            "line_of_sight": clone.line_of_sight,
            "population_cost": sum(cost.amount for cost in c.resource_costs if cost.type == 4),
            "population_storages": [
                {"type": storage.type, "amount": storage.amount, "flag": storage.flag}
                for storage in clone.resource_storages if storage.type in POPULATION_STORAGE_TYPES
            ],
            "population_storages_match_original_khan": True,
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
        if (_population_storage_snapshot(civ.units[-1].resource_storages)
                != _population_storage_snapshot(civ.units[GENGHIS_ID].resource_storages)):
            raise ValueError("Serialized leader population storage differs from original Khan")
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
        "native_graphics_movement_animations_and_projectile_preserved": True,
        "shared_genghis_class_and_counter_armour_template": True,
        "all_serialized_population_storages_match_original_khan": True,
        "all_native_bow_crossbow_or_firearm_donors_validated": True,
        "equal_starting_stats_range_accuracy_and_movement_speed": True,
        "main_pierce_attack_class": 3,
        "native_wwise_acknowledgement_fallbacks_preserved": True,
        "three_custom_acknowledgement_groups_copied_for_generated_civilizations": True,
        "special_auras_charge_splash_conversion_and_weapon_switching_disabled": True,
        "live_match_verified": False,
    }
    text = ["RAM CIVILIZATION LEADERS", "", f"Reserved leader object ID: {reserved}",
            "Native bow/crossbow/firearm appearances and weapons; identical starting combat profiles.",
            "Range, accuracy and movement speed are equal; original movement/weapon animations survive.",
            "Generated national selection, move and attack replies share accepted role groups.",
            "Native donor Wwise sound fallbacks are preserved.",
            "Original game unit definitions and global legacy task headers are unchanged.",
            "Special auras, charge, splash, conversion and weapon switching are disabled.", ""]
    text.extend(f"{row['civilization_name']}: {row['leader_name']} ({row['role']})"
                for row in source_rows if row["civilization"])
    extras = {"RAM_CIVILIZATION_LEADERS.json": _json_bytes(report),
              "RAM_CIVILIZATION_LEADERS.txt": ("\n".join(text) + "\n").encode("utf-8")}
    return patched, extras, report
