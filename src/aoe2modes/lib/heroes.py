"""Hero rosters and hero manipulation — the CBA Hero-specific half of the library.

A CBA *Hero* mode gives every player a single hero unit instead of an economy. The
hero grows over the course of the game, either by tier upgrades or by stat buffs.
This module models that as a set of named **hero lines**: an archetype (cavalry,
archer, monk...) with an ordered list of hero units, one per tier.

The lines below are a sensible, playable starting roster grouped by archetype — they
are *not* a reproduction of any specific published CBA Hero scenario's balance. Treat
:data:`CLASSIC_LINES` as a template to tune, and add your own lines per mode.
"""

from __future__ import annotations

from dataclasses import dataclass

from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import (
    DamageClass,
    HeroStatusFlag,
    ObjectAttribute,
    Operation,
)
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.tile import Tile


@dataclass(frozen=True)
class HeroLine:
    """One archetype and its tier ladder."""

    key: str
    label: str
    tiers: tuple[HeroInfo, ...]
    hint: str = ""

    def __post_init__(self) -> None:
        if not self.tiers:
            raise ValueError(f"hero line {self.key!r} has no tiers")

    @property
    def base(self) -> HeroInfo:
        return self.tiers[0]

    @property
    def top(self) -> HeroInfo:
        return self.tiers[-1]

    def tier(self, index: int) -> HeroInfo:
        """Tier by 1-based index, clamped to the top of the ladder."""
        return self.tiers[max(0, min(len(self.tiers) - 1, index - 1))]

    def upgrades(self) -> list[tuple[HeroInfo, HeroInfo]]:
        """Consecutive (from, to) pairs — one per upgrade step."""
        return list(zip(self.tiers, self.tiers[1:], strict=False))


class HeroPool:
    """An ordered, keyed collection of hero lines."""

    def __init__(self, lines: tuple[HeroLine, ...]):
        keys = [line.key for line in lines]
        duplicates = {key for key in keys if keys.count(key) > 1}
        if duplicates:
            raise ValueError(f"duplicate hero line keys: {sorted(duplicates)}")
        self._lines = lines
        self._by_key = {line.key: line for line in lines}

    def __iter__(self):
        return iter(self._lines)

    def __len__(self) -> int:
        return len(self._lines)

    def __getitem__(self, key: str | int) -> HeroLine:
        if isinstance(key, int):
            return self._lines[key]
        return self._by_key[key]

    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(self._by_key)

    def for_player(self, player: PlayerId) -> HeroLine:
        """Deterministic assignment — player N gets line N, wrapping around.

        Deterministic on purpose: it keeps builds reproducible. For an in-game random
        or player-chosen pick, drive the choice from XS instead.
        """
        return self._lines[(int(player) - 1) % len(self._lines)]

    def all_unit_ids(self) -> list[int]:
        return [hero.ID for line in self._lines for hero in line.tiers]


CLASSIC_LINES = HeroPool((
    HeroLine(
        key="paladin",
        label="Paladin",
        tiers=(HeroInfo.SIEUR_BERTRAND, HeroInfo.ROLAND, HeroInfo.FRANKISH_PALADIN),
        hint="Heavy cavalry. Fast, tanky, weak to camels and pikes.",
    ),
    HeroLine(
        key="huskarl",
        label="Huskarl",
        tiers=(HeroInfo.JARL, HeroInfo.SIEGFRIED, HeroInfo.WILLIAM_WALLACE),
        hint="Infantry that shrugs off archer fire.",
    ),
    HeroLine(
        key="archer",
        label="Archer",
        tiers=(HeroInfo.ARCHER_OF_THE_EYES, HeroInfo.LA_HIRE, HeroInfo.ROBIN_HOOD),
        hint="Ranged damage. Fragile in melee.",
    ),
    HeroLine(
        key="mangudai",
        label="Cavalry Archer",
        tiers=(HeroInfo.KUSHLUK, HeroInfo.SUBOTAI, HeroInfo.GENGHIS_KHAN),
        hint="Mobile ranged harassment. Rewards micro.",
    ),
    HeroLine(
        key="monk",
        label="Monk",
        tiers=(HeroInfo.FRIAR_TUCK, HeroInfo.IMAM, HeroInfo.POPE_LEO_I),
        hint="Converts and heals. Support pick, needs a front line.",
    ),
    HeroLine(
        key="siege",
        label="Siege",
        tiers=(HeroInfo.BAD_NEIGHBOR, HeroInfo.GODS_OWN_SLING, HeroInfo.WARWOLF_TREBUCHET),
        hint="Area damage against clumps and castles. Helpless alone.",
    ),
    HeroLine(
        key="elephant",
        label="War Elephant",
        tiers=(HeroInfo.PRITHVIRAJ, HeroInfo.GAJAH_MADA, HeroInfo.ABRAHA_ELEPHANT),
        hint="Slow, enormous health pool, trample damage.",
    ),
    HeroLine(
        key="samurai",
        label="Duelist",
        tiers=(HeroInfo.MINAMOTO, HeroInfo.NOBUNAGA, HeroInfo.KITABATAKE),
        hint="Anti-unique-unit specialist. Strong one-on-one.",
    ),
))
"""Eight archetypes, three tiers each — one line per player in a standard 8-player CBA."""


# --- effect helpers ----------------------------------------------------------------

def spawn_hero(trigger: Trigger, player: PlayerId, hero: HeroInfo, tile: Tile) -> Trigger:
    trigger.new_effect.create_object(
        object_list_unit_id=hero.ID,
        source_player=player,
        location_x=tile.x,
        location_y=tile.y,
    )
    return trigger


def upgrade_hero(trigger: Trigger, player: PlayerId, old: HeroInfo, new: HeroInfo) -> Trigger:
    """Swap every instance of one hero for the next tier, in place."""
    trigger.new_effect.replace_object(
        object_list_unit_id=old.ID,
        source_player=player,
        target_player=player,
        object_list_unit_id_2=new.ID,
    )
    return trigger


#: Attributes the game stores per damage class rather than as a single number.
ARMOUR_ATTACK_ATTRIBUTES = frozenset({
    ObjectAttribute.ATTACK,
    ObjectAttribute.ARMOR,
})


def buff(
    trigger: Trigger,
    player: PlayerId,
    hero: HeroInfo,
    attribute: ObjectAttribute,
    quantity: int,
    *,
    operation: Operation = Operation.ADD,
) -> Trigger:
    """Adjust a hero's stats for one player.

    Attribute changes apply to the unit *type* for that player, so they also affect
    units created later — which is how CBA-style permanent upgrades are built.

    Attack and armour are stored per damage class, so they go through
    :func:`buff_attack` / :func:`buff_armour` instead of this function.
    """
    if attribute in ARMOUR_ATTACK_ATTRIBUTES:
        raise ValueError(
            f"{attribute.name} is per-damage-class; use buff_attack()/buff_armour() "
            "so the damage class is set alongside the amount."
        )
    trigger.new_effect.modify_attribute(
        quantity=quantity,
        object_list_unit_id=hero.ID,
        source_player=player,
        operation=operation,
        object_attributes=attribute,
    )
    return trigger


def _buff_armour_attack(
    trigger: Trigger,
    player: PlayerId,
    hero: HeroInfo,
    attribute: ObjectAttribute,
    amount: int,
    damage_class: DamageClass,
    operation: Operation,
) -> Trigger:
    # Amount and damage class pack into the effect's quantity slot. Passing them as
    # `armour_attack_*` lets the parser do the packing; setting `quantity` directly
    # would clobber the class.
    trigger.new_effect.modify_attribute(
        object_list_unit_id=hero.ID,
        source_player=player,
        operation=operation,
        object_attributes=attribute,
        armour_attack_quantity=amount,
        armour_attack_class=damage_class,
    )
    return trigger


def buff_attack(
    trigger: Trigger,
    player: PlayerId,
    hero: HeroInfo,
    amount: int,
    *,
    damage_class: DamageClass = DamageClass.BASE_MELEE,
    operation: Operation = Operation.ADD,
) -> Trigger:
    """Add attack of one damage class. Use ``BASE_PIERCE`` for ranged heroes."""
    return _buff_armour_attack(
        trigger, player, hero, ObjectAttribute.ATTACK, amount, damage_class, operation
    )


def buff_armour(
    trigger: Trigger,
    player: PlayerId,
    hero: HeroInfo,
    amount: int,
    *,
    damage_class: DamageClass = DamageClass.BASE_MELEE,
    operation: Operation = Operation.ADD,
) -> Trigger:
    """Add armour of one damage class."""
    return _buff_armour_attack(
        trigger, player, hero, ObjectAttribute.ARMOR, amount, damage_class, operation
    )


def make_heroic(trigger: Trigger, player: PlayerId, hero: HeroInfo) -> Trigger:
    """Give a unit full hero status: no conversion, auto-heal, hero glyph on the minimap."""
    trigger.new_effect.modify_attribute(
        quantity=HeroStatusFlag.combine(
            full_hero_status=True,
            cannot_be_converted=True,
            hero_regeneration=True,
            hero_glow=True,
        ),
        object_list_unit_id=hero.ID,
        source_player=player,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.HERO_STATUS,
    )
    return trigger
