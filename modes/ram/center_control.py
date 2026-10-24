"""RAM-only center controller. Center rewards add directly to the existing kill counter."""

import re
import tomllib
from math import lcm

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.trigger_lists import (
    AttackStance,
    Attribute,
    Comparison,
    HeroStatusFlag,
    ObjectAttribute,
    ObjectClass,
    ObstructionType,
    Operation,
)
from AoE2ScenarioParser.datasets.units import UnitInfo

from aoe2modes.lib.xs import substitute

from .center_audio import declare_center_audio

CREDIT_BASE = 153
PRESENT_BASE = 161
TEAM2_SHARE = 169
COUNTDOWN = 170
TEAM1_RATE = 171
TEAM2_RATE = 172
TEAM1_PRESENT = 173
TEAM2_PRESENT = 174
TEAM1_LAST = 175
TEAM2_LAST = 176
STATE = 177
METER = 178
BONUS = 179
KILL_PENDING_BASE = 180


def configure_center_control(ctx, *, spawn_positions):
    settings = tomllib.loads((ctx.mode_dir / "mode.toml").read_text())["center"]
    if not settings["enabled"]:
        return
    for name, value in settings.items():
        if name != "enabled" and (type(value) is not int or value <= 0):
            raise ValueError(f"center.{name} must be a positive integer")
    if settings["equalize_seconds"] < settings["capture_seconds"]:
        raise ValueError("Contested equalization must be at least as slow as capturing")
    control_scale = lcm(settings["capture_seconds"], settings["equalize_seconds"],
                        settings["empty_reset_seconds"])
    if control_scale * max(100, settings["credit_cap"]) > 2_000_000_000:
        raise ValueError("Center timings exceed the fixed-point control range")
    if not 0 < settings["x1"] < settings["x2"] < ctx.map_size:
        raise ValueError("invalid center X bounds")
    if not 0 < settings["y1"] < settings["y2"] < ctx.map_size:
        raise ValueError("invalid center Y bounds")
    old = [t for t in ctx.tm.triggers if re.fullmatch(r"Center (Kills|Trebuchet) S[1-8] W[1-8]", t.name)]
    if len(old) != 128:
        raise RuntimeError(f"center trigger migration drift: {len(old)}")
    for trigger in old:
        trigger.enabled = 0
        trigger.looping = 0
        trigger.conditions = []
        trigger.condition_order = []
        trigger.effects = []
        trigger.effect_order = []

    expected = list(range(CREDIT_BASE))
    if sorted(v.variable_id for v in ctx.tm.variables) != expected:
        raise RuntimeError("RAM center variable allocation must follow the complete normal RA allocation")
    for base, suffix in ((CREDIT_BASE, "center"), (PRESENT_BASE, "cp")):
        for color in range(1, 9):
            ctx.tm.add_variable(f"p{color}{suffix}", variable_id=base + color - 1)
    for name, identifier in (
        ("ramteam2share", TEAM2_SHARE), ("ramcenterleft", COUNTDOWN),
        ("ramteam1rate", TEAM1_RATE), ("ramteam2rate", TEAM2_RATE),
        ("ramteam1present", TEAM1_PRESENT), ("ramteam2present", TEAM2_PRESENT),
        ("ramteam1last", TEAM1_LAST), ("ramteam2last", TEAM2_LAST),
        ("ramstate", STATE), ("rammeter", METER), ("rambonus", BONUS),
    ):
        ctx.tm.add_variable(name, variable_id=identifier)
    # Deliver the computed award through the same native kill resource used by
    # RA's old middle reward. Owner selectors stay native; XS only sets an amount.
    for color in range(1, 9):
        pending = KILL_PENDING_BASE + color - 1
        ctx.tm.add_variable(f"p{color}centerpending", variable_id=pending)
        for owner in range(1, 9):
            payout = ctx.tm.add_trigger(f"RAM Center kills — P{color} W{owner}", looping=1)
            payout.new_condition.timer(timer=1)
            payout.new_condition.variable_value(variable=40 + color - 1,
                                                quantity=owner, comparison=Comparison.EQUAL)
            payout.new_condition.variable_value(variable=32 + color - 1,
                                                quantity=1, comparison=Comparison.EQUAL)
            payout.new_condition.variable_value(variable=pending, quantity=1,
                                                comparison=Comparison.LARGER_OR_EQUAL)
            payout.new_effect.modify_resource_by_variable(
                tribute_list=Attribute.UNITS_KILLED, source_player=owner,
                operation=Operation.ADD, variable=pending,
            )
            # Read the actual delivered amount before acknowledging the queue.
            # The helper only renders a local message; it cannot change state.
            payout.new_effect.script_call(message=f"ramCenterNoticeP{color}")
            payout.new_effect.change_variable(variable=pending, quantity=0, operation=Operation.SET)

    left, top, right, bottom = (settings[name] for name in ("x1", "y1", "x2", "y2"))
    flags = {member.ID for member in OtherInfo if member.name.startswith("FLAG_")}
    fire = {OtherInfo.TORCH_A.ID, OtherInfo.TORCH_B.ID, OtherInfo.BONFIRE.ID}
    retired = {u.reference_id for group in ctx.um.units for u in group
               if left - 3 <= u.x <= right + 3 and top - 3 <= u.y <= bottom + 3
               and u.unit_const in flags | fire}
    # Retire only explicitly selected old indicators, never broaden an empty
    # selection into an owner-wide effect after removing its last reference.
    for trigger in ctx.tm.triggers:
        effects = []
        for effect in trigger.effects:
            selected = set(effect.selected_object_ids or ())
            if selected & retired:
                retained = [ref for ref in effect.selected_object_ids if ref not in retired]
                if not retained:
                    continue
                effect.selected_object_ids = retained
            effects.append(effect)
        trigger.effects = effects
        trigger.effect_order = list(range(len(effects)))
    for reference in retired:
        ctx.um.remove_unit(reference_id=reference)
    protect = ctx.tm.add_trigger("RAM — protect team center flags")
    team_flags = []
    for team, x in ((1, left + 0.5), (2, right - 0.5)):
        reference = ctx.um.add_unit(player=0, unit_const=OtherInfo.FLAG_A.ID,
                                     x=x, y=(top + bottom) / 2).reference_id
        team_flags.append(reference)
        protect.new_effect.disable_unit_attackable(source_player=0, selected_object_ids=[reference])
        protect.new_effect.disable_object_deletion(source_player=0, selected_object_ids=[reference])
        protect.new_effect.change_object_name(source_player=0, selected_object_ids=[reference],
                                              message=f"Team {team} center control")
    # One neutral physical meter, kept outside every player lifecycle. Exact-ref
    # attributes clone its master instead of changing other Gaia/player rams.
    indicator = ctx.um.add_unit(
        player=0, unit_const=UnitInfo.BATTERING_RAM.ID,
        x=(left + right) / 2, y=(top + bottom) / 2,
    ).reference_id
    meter = ctx.tm.add_trigger("RAM — protect center control ram")
    for factory in (meter.new_effect.disable_unit_attackable,
                    meter.new_effect.disable_unit_targeting,
                    meter.new_effect.disable_object_deletion,
                    meter.new_effect.disable_object_selection):
        factory(source_player=0, selected_object_ids=[indicator])
    for attribute, value in (
        (ObjectAttribute.HERO_STATUS, int(HeroStatusFlag.CANNOT_BE_CONVERTED)),
        (ObjectAttribute.FRIENDLY_FIRE_DAMAGE, 0),
        (ObjectAttribute.MOVEMENT_SPEED, 0), (ObjectAttribute.SEARCH_RADIUS, 0),
        (ObjectAttribute.GARRISON_CAPACITY, 0), (ObjectAttribute.GARRISON_TYPE, 0),
        (ObjectAttribute.UNIT_SIZE_X, 0), (ObjectAttribute.UNIT_SIZE_Y, 0),
        (ObjectAttribute.OBSTRUCTION_TYPE, int(ObstructionType.NO_OUTLINE_PASSABLE)),
    ):
        meter.new_effect.modify_object_attribute(
            source_player=0, selected_object_ids=[indicator], object_attributes=attribute,
            operation=Operation.SET, quantity=value,
        )
    meter.new_effect.change_object_stance(
        source_player=0, selected_object_ids=[indicator], attack_stance=AttackStance.NO_ATTACK_STANCE,
    )
    meter.new_effect.change_object_name(
        source_player=0, selected_object_ids=[indicator], message="Center control — physical team meter",
    )
    # Disable Gaia proximity capture as well as monk conversion. The same helper
    # reasserts these native instance flags during synchronized meter updates.
    meter.new_effect.script_call(message="ramProtectCenterRam")
    rows = []
    for state, label in enumerate(("Empty", "T1 present", "T2 present", "CONTESTED")):
        row = ctx.tm.add_trigger(
            f"RAM Center HUD {label}", enabled=int(state == 0), display_on_screen=1,
            short_description="Center T1 <rammeter>% / T2 <ramteam2share>%\n"
                              f"{label} | +<ramteam1rate>/+<ramteam2rate> kills | <ramcenterleft>s",
            description_order=21, mute_objectives=1,
        )
        row.new_condition.player_defeated(source_player=0)
        rows.append(row)
    for state, row in enumerate(rows):
        sync = ctx.tm.add_trigger(f"RAM Center HUD sync {state}", looping=1)
        sync.new_condition.timer(timer=1)
        sync.new_condition.variable_value(variable=STATE, quantity=state, comparison=Comparison.EQUAL)
        for other in rows:
            if other == row:
                sync.new_effect.activate_trigger(trigger_id=other.trigger_id)
            else:
                sync.new_effect.deactivate_trigger(trigger_id=other.trigger_id)

    births = []
    for color, points in spawn_positions.items():
        castles = [u for u in ctx.um.units[color] if u.unit_const == BuildingInfo.CASTLE.ID]
        births.append(f"if (color == {int(color)}) {{")
        for slot, (x, y) in enumerate(points):
            castle = min(castles, key=lambda u: (u.x - x) ** 2 + (u.y - y) ** 2).reference_id
            births.append(
                f"if (xsDoesUnitExist({castle}) && xsGetUnitHitpoints({castle}) > 0 "
                f"&& xsGetUnitOwner({castle}) == owner) {{ "
                f"reference = xsCreateUnit(unit, owner, vector({x}, {y}, -1), false, false, true); "
                f"if (reference >= 0) {{ cbaOrderArmyBirth(color, {slot}, reference); return(true); }} }}"
            )
        births.append("}")
    classes = ("ARCHER", "INFANTRY", "CAVALRY", "SIEGE_WEAPON", "MONK", "WARSHIP", "CONQUISTADOR",
               "WAR_ELEPHANT", "HERO", "ELEPHANT_ARCHER", "PHALANX", "PETARD", "CAVALRY_ARCHER",
               "MONKWITH_RELIC", "HAND_CANNONEER", "TWO_HANDED_SWORDSMAN", "PIKEMAN", "SCOUT",
               "SPEARMAN", "PACKED_UNIT", "BOARDING_BOAT", "UNPACKED_SIEGE_UNIT", "BALLISTA",
               "RAIDER", "CAVALRY_RAIDER")
    allowed = " || ".join(f"kind == {900 + int(ObjectClass[name])}" for name in classes)
    substitutions = {name.upper(): value for name, value in settings.items() if name != "enabled"}
    substitutions.update(declare_center_audio(ctx))
    substitutions.update(CREDIT_BASE=CREDIT_BASE, PRESENT_BASE=PRESENT_BASE,
                         TEAM2_SHARE=TEAM2_SHARE, COUNTDOWN=COUNTDOWN,
                         TEAM1_RATE=TEAM1_RATE, TEAM2_RATE=TEAM2_RATE,
                         TEAM1_PRESENT=TEAM1_PRESENT, TEAM2_PRESENT=TEAM2_PRESENT,
                         TEAM1_LAST=TEAM1_LAST, TEAM2_LAST=TEAM2_LAST,
                         CONTROL_SCALE=control_scale, CONTROL_MINIMUM=-control_scale,
                         STATE=STATE, METER=METER, BONUS=BONUS,
                         TEAM1_FLAG=team_flags[0], TEAM2_FLAG=team_flags[1],
                         CENTER_RAM=indicator, CENTER_RAM_MID_X=(left + right) / 2,
                         CENTER_RAM_Y=(top + bottom) / 2,
                         CENTER_RAM_HALF_TRAVEL=(right - left - 1) / 2,
                         KILL_PENDING_BASE=KILL_PENDING_BASE, BIRTHS="\n".join(births), CLASSES=allowed,
                         PENGUIN=UnitInfo.WAR_PENGUIN.ID)
    source = substitute((ctx.mode_dir / "center_control.xs").read_text(), substitutions)
    source += "\n" + "\n".join(
        f"void ramCenterNoticeP{color}() {{ ramAnnounceCenterKills({color}); }}"
        for color in range(1, 9)
    )
    ctx.add_xs(source, label="RAM center control")
    ctx.message_manager.instructions += (
        f"\nRAM CENTER: one team's combat units push control toward 100/0. Neutral to full control "
        f"takes {settings['capture_seconds']}s; reversing full enemy control takes twice as long. "
        f"Both teams present always equalize slowly toward 50/50, regardless of numbers or power "
        f"({settings['equalize_seconds']}s from full to neutral). Every {settings['payout_seconds']}s, "
        f"the control percentage at that instant awards kills to EVERY active teammate of the "
        f"leading team, provided that team has combat units in the center. At 55/45: +2, "
        f"60/40: +5, 75/25: +12, and 100/0: +{settings['credit_cap']} per teammate. "
        f"50/50 pays nobody. Empty center pays nothing and returns toward 50/50 over "
        f"{settings['empty_reset_seconds']}s. The HUD shows both shares, current payout and countdown. "
        f"Present players still receive {settings['reinforcement_units']} civ army units at surviving "
        f"Castles per {settings['reinforcement_seconds']} full, uncontested held seconds, "
        "subject to population/space. "
        "Center rewards increase k and all kill-based Hero progression; each payout shows "
        "its exact kill amount in the recipient's chat. No separate points column. "
        "Two fixed team flags replace the old center flags; there are no center fire effects. "
        "An indestructible neutral ram marks control physically: midway at 50/50, "
        "at Team 1's flag for 100/0 and Team 2's flag for 0/100. It never blocks troops."
    )
    ctx.log(f"RAM center: team-wide snapshot kills, 50/50 neutral; removed {len(retired)} old indicators")
