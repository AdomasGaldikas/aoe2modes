# Ascendants data tables and runbooks

The tunable data behind the mode, and the procedures for changing it safely. All of it
lives in `modes/evolution_alpha/build.py`; none of it is in `mode.toml`, because each
table also drives generated XS and is therefore logic-adjacent rather than "just
settings".

Related: [`ascendants-xs-runtime.md`](ascendants-xs-runtime.md) (how these tables reach
the engine), [`ascendants-architecture.md`](ascendants-architecture.md) (where the passes
that consume them sit).

## Trigger-variable registry

145 variables, ids **0–144**, contiguous with no holes. Every block is declared once as a
`*_VARIABLE_BASE` constant and read by both the Python trigger code and the generated XS,
so the two sides cannot drift apart.

| Ids | Constant | Count | Meaning | Written by |
| --- | --- | ---: | --- | --- |
| 0–7 | `PENDING_BUILDER_VARIABLE_BASE` | 8 | Unclaimed builder pairs for this color | XS |
| 8–31 | `COMBAT_ROW_VARIABLE_BASE` (stride 3) | 24 | Kills / Deaths / Razings per color | XS |
| 32–39 | `COLOR_ACTIVE_VARIABLE_BASE` | 8 | Color is occupied and not eliminated | **XS only** |
| 40–47 | `COLOR_WORLD_VARIABLE_BASE` | 8 | Trigger-side owner resolved from the Castle row | Triggers |
| 48–55 | `COLOR_ELIMINATED_VARIABLE_BASE` | 8 | Color has been eliminated | Triggers (XS latches) |
| 56 | `MATCH_READY_VARIABLE_ID` | 1 | Lobby has settled; systems may resolve | Triggers |
| 57–80 | `VOTE_MARKER_VARIABLE_BASE` | 24 | One per (target, voter) pair, 2 sides × 4 targets × 3 voters | Triggers |
| 81–88 | `ARMY_MOVE_PENDING_VARIABLE_BASE` | 8 | One-shot new-Castle-wave pulse | XS arms, triggers consume |
| 89–96 | `ARMY_RANGE_VARIABLE_BASE` | 8 | Sheep-selected Castle-army level, 0–5 | Triggers |
| 97–104 | `HERO_MOVE_PENDING_VARIABLE_BASE` | 8 | One-shot new-Hero pulse | Triggers |
| 105–112 | `BUILDER_MOVE_PENDING_VARIABLE_BASE` | 8 | One-shot new-builder-pair pulse | Triggers |
| 113–120 | `HERO_RANGE_VARIABLE_BASE` | 8 | Penguin-selected Hero level, 0–5 | Triggers |
| 121–128 | `COLOR_OCCUPIED_VARIABLE_BASE` | 8 | Color has participated; survives elimination | Native Castle-owner detector, latched |
| 129–136 | `COLOR_CLEANED_VARIABLE_BASE` | 8 | Empty slot or confirmed removal of all defeated owner's objects | XS initializes; owner detector resets; cleanup confirms |
| 137–144 | `COLOR_XS_VARIABLE_BASE` | 8 | XS API index plus 1000, copied from reserved resource 10 | Native owner-resolved identity bridge |

Colour-indexed blocks are addressed as `BASE + scenario_color - 1`. The combat block is
`BASE + (color - 1) * COMBAT_ROW_VARIABLE_STRIDE`, then `+0` kills, `+1` deaths,
`+2` razings.

Both range blocks initialize to `DEFAULT_RANGE_LEVEL = 3` for every occupied color.

> **Why this matters.** A condition or effect addresses a variable **by id, not by name**.
> A collision therefore rewires trigger logic without changing a single visible field, and
> a hole means a block silently moved. `_assert_variable_ids_are_contiguous` checks the
> whole allocation after the build and raises on a hole, a duplicate or a collision.
> Do not assume `lib/variables.SHARED` or a generated table owns the full range — inspect
> the complete build before allocating.

## Civilization table

Two Python dicts keyed by DE civilization id, which **must cover exactly the same ids** —
the XS renderer raises on a symmetric difference.

- `CIV_SPAWN_RULES[id] = (unit_id, military_population_cap, interval_seconds)`
- `CIV_BUILDER_RULES[id] = (public_name, razings_for_first_builder_pair)`

| id | Civilization | Spawned unit | Cap | Interval | Builder threshold |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | Britons | Elite Longbowman (530) | 72 | 9 | 1 |
| 2 | Franks | Elite Throwing Axeman (531) | 76 | 8 | 3 |
| 3 | Goths | Elite Huskarl (Barracks) (761) | 92 | 10 | 2 |
| 4 | Teutons | Elite Teutonic Knight (554) | 76 | 8 | 3 |
| 5 | Japanese | Elite Samurai (560) | 80 | 9 | 3 |
| 6 | Chinese | Elite Chu Ko Nu (559) | 76 | 8 | 2 |
| 7 | Byzantines | Elite Cataphract (553) | 56 | 10 | 2 |
| 8 | Persians | War Elephant (239) | 40 | 13 | 4 |
| 9 | Saracens | Elite Mameluke (556) | 68 | 12 | 2 |
| 10 | Turks | Janissary (46) | 50 | 9 | 3 |
| 11 | Vikings | Elite Berserk (694) | 86 | 9 | 2 |
| 12 | Mongols | Elite Mangudai (561) | 56 | 9 | 2 |
| 13 | Celts | Elite Woad Raider (534) | 80 | 9 | 2 |
| 14 | Spanish | Conquistador (771) | 60 | 10 | 3 |
| 15 | Aztecs | Elite Jaguar Warrior (726) | 92 | 8 | 2 |
| 16 | Mayans | Elite Plumed Archer (765) | 70 | 8 | 1 |
| 17 | Huns | Elite Tarkan (757) | 80 | 13 | 4 |
| 18 | Koreans | Elite War Wagon (829) | 60 | 12 | 3 |
| 19 | Italians | Elite Genoese Crossbowman (868) | 72 | 9 | 1 |
| 20 | Hindustanis | Elite Ghulam (1749) | 60 | 12 | 3 |
| 21 | Incas | Elite Kamayuk (881) | 77 | 8 | 2 |
| 22 | Magyars | Elite Magyar Huszar (871) | 80 | 13 | 1 |
| 23 | Slavs | Elite Boyar (878) | 56 | 10 | 2 |
| 24 | Portuguese | Organ Gun (1001) | 34 | 12 | 3 |
| 25 | Ethiopians | Elite Shotel Warrior (1018) | 80 | 8 | 2 |
| 26 | Malians | Elite Gbeto (1015) | 81 | 10 | 3 |
| 27 | Berbers | Elite Camel Archer (1009) | 61 | 10 | 1 |
| 28 | Khmer | Elite Ballista Elephant (1122) | 31 | 14 | 4 |
| 29 | Malay | Elite Karambit Warrior (1125) | 80 | 6 | 1 |
| 30 | Burmese | Elite Arambai (1128) | 61 | 10 | 3 |
| 31 | Vietnamese | Elite Rattan Archer (1131) | 81 | 10 | 1 |
| 32 | Bulgarians | Elite Konnik (1227) | 41 | 12 | 2 |
| 33 | Tatars | Elite Keshik (1230) | 61 | 12 | 2 |
| 34 | Cumans | Elite Kipchak (1233) | 61 | 12 | 2 |
| 35 | Lithuanians | Elite Leitis (1236) | 60 | 10 | 2 |
| 36 | Burgundians | Elite Coustillier (1657) | 60 | 8 | 2 |
| 37 | Sicilians | Elite Serjeant (1659) | 92 | 8 | 2 |
| 38 | Poles | Elite Obuch (1703) | 60 | 8 | 2 |
| 39 | Bohemians | Elite Hussite Wagon (1706) | 35 | 15 | 2 |
| 40 | Dravidians | Elite Urumi Swordsman (1737) | 60 | 8 | 2 |
| 41 | Bengalis | Elite Ratha, ranged (1761) | 40 | 8 | 2 |
| 42 | Gurjaras | Elite Chakram Thrower (1743) | 41 | 11 | 3 |
| 43 | Romans | Elite Centurion (1792) | 60 | 8 | 2 |
| 44 | Armenians | Elite Composite Bowman (1802) | 80 | 8 | 2 |
| 45 | Georgians | Elite Monaspa (1805) | 80 | 8 | 1 |
| 46 | Achaemenids | Elite Immortal, ranged (2175) | 70 | 10 | 1 |
| 47 | Athenians | Elite Strategos (2105) | 80 | 10 | 1 |
| 48 | Spartans | Elite Hippeus (2108) | 80 | 8 | 1 |
| 49 | Shu | Elite White Feather Guard (1961) | 60 | 10 | 2 |
| 50 | Wu | Elite Fire Archer (1970) | 60 | 10 | 2 |
| 51 | Wei | Elite Tiger Cavalry (1951) | 60 | 10 | 2 |
| 52 | Jurchens | Elite Iron Pagoda (1910) | 80 | 10 | 2 |
| 53 | Khitans | Elite Liao Dao (1922) | 80 | 10 | 2 |
| 54 | Macedonians | Elite Companion Cavalry (2383) | 70 | 10 | 1 |
| 55 | Thracians | Elite Rhomphaia Warrior (2387) | 92 | 8 | 1 |
| 56 | Puru | Elite Pattiyodha (2389) | 72 | 9 | 1 |
| 57 | Muisca | Elite Temple Guard (2587) | 80 | 8 | 1 |
| 58 | Mapuche | Elite Bolas Rider (2571) | 80 | 10 | 1 |
| 59 | Tupi | Elite Ibirapema Warrior (2584) | 80 | 8 | 1 |

Ranges: caps 31–92, intervals 6–15 seconds, builder thresholds 1–4. Unit names come from
the pinned dataset; the id in brackets is authoritative.

Two deliberate irregularities, both maintainer balance calls rather than defects:

- **Four civilizations spawn the non-Elite form** — Persians (War Elephant), Turks
  (Janissary), Spanish (Conquistador) and Portuguese (Organ Gun).
- **The cap is a military population cap, not a unit count.** A 0.5-population Karambit
  Warrior therefore buys the Malay roughly twice as many units as the number suggests.

Goths spawn the **Barracks** Elite Huskarl (761), which is why
`_configure_sparse_goth_barracks_restriction` exists: the Anarchy Barracks rule has to
stay correct in a compacted lobby, and the Imperial transition needs guarding against
trigger order.

## Hero milestones

`HERO_MILESTONES` pairs a kill threshold with a hero unit;
`HERO_MILESTONE_UPPER_BOUNDS` closes each band so exactly one tier is ever live.

| Kills | Hero | Band upper bound |
| ---: | --- | ---: |
| 200 | Robin Hood | 400 |
| 400 | Theodoric the Goth | 600 |
| 600 | Charles Martel | 800 |
| 800 | Subotai | 1,000 |
| 1,000 | Genghis Khan | 2,000 |
| 2,000 | Genghis Khan (Super) | 3,500 |

Above 3,500 the late-hero boost loops take over (`_configure_sparse_late_hero_boosts`):
one boosted Genghis loop in the 3,500–4,999 band, two from 5,000. Those loops are also
gated on Penguin level ≥ 1 and on an object ceiling that excludes the controller Penguin.

Milestone Heroes are created at `HERO_MILESTONE_SPAWN_TILES` — canonical `(16, 38)`,
transformed per color — with the two late-Genghis pads at `(15, 38)` and `(17, 38)`.

## Slider geometry

Declared once in the P3 source frame and transformed eight ways. Exact per-color values
are in [`ascendants-control-map.md`](ascendants-control-map.md); the source constants are:

| Constant | Value |
| --- | --- |
| `SOURCE_RANGE_ISLAND` | `(1, 60, 9, 66)` |
| `SOURCE_ARMY_RANGE_LANE` | `(1, 60, 9, 61)` |
| `SOURCE_HERO_RANGE_LANE` | `(1, 65, 9, 66)` |
| `SOURCE_RANGE_LEVEL_SPANS` | `((1,3), (4,4), (5,5), (6,6), (7,7), (8,9))` |
| `SOURCE_ARMY_CONTROLLER_POSITION` | `(6.5, 61.5)` |
| `SOURCE_HERO_CONTROLLER_POSITION` | `(6.5, 65.5)` |
| `RANGE_LEVELS` / `DEFAULT_RANGE_LEVEL` | `0–5` / `3` |
| `ARMY_CONTROLLER_LABEL` | `Army range - snow = HOLD` |
| `HERO_CONTROLLER_LABEL` | `Hero range - snow = OFF` |

Level 0 spans three cells (the whole snowy pad) and level 5 spans two; levels 1–4 are one
cell each. The snow/road boundary is exactly the level 0/1 trigger boundary — not a
decorative approximation.

## Other constants worth knowing

| Constant | Value | Purpose |
| --- | --- | --- |
| `SOURCE_ARMY_SPAWN_POINTS` | `(22,48) (22,52) (22,55) (22,59)` | The four Castle-wave pads, canonical frame |
| `ANTI_TREB_SOURCE_AREA` | `(18, 38, 25, 64)` | One rectangle, mirrored eight ways |
| `LOBBY_SETTLE_SECONDS` | 3 | Delay before systems may resolve owners |
| `VICTORY_RESOLVE_SECONDS` | 5 | Victory tick cadence |
| `SOURCE_FRONT_WIPE_END_POSTS` | `(39.5,45.5) (39.5,62.5)` | Two posts per color closing the front row |
| `WHITE_KING_KILL_COUNTERS` | 8 reference ids | Kings that publish live kill totals |
| `MIDDLE_TREBUCHET_MARKERS` | 8 reference ids | Center-reward delivery pads |

---

# Runbooks

## Adding a civilization

DE ships a new civilization with id 60. Without these steps it produces **no army and no
builder pairs**, and the player is told so by chat at four seconds.

1. Add a row to **both** tables in `build.py`:

   ```python
   CIV_SPAWN_RULES[60]   = (unit_id, military_pop_cap, interval_seconds)
   CIV_BUILDER_RULES[60] = ("Public Name", razings_for_first_pair)
   ```

   Missing one raises at build time — the renderer reports the symmetric difference.

2. **Nothing else is required for the ban.** `_ban_auto_spawned_unique_units` derives the
   training ban from `CIV_SPAWN_RULES`, and `_unit_family` expands your unit id to every
   trainable form — Elite and non-Elite, ranged and melee siblings (Ratha, Immortal). Add
   the row and the civilization can no longer hand-train what its Castles give it free.

3. XS array sizing follows automatically: the arrays are sized `max(ids) + 1`.

4. Rebuild and run the suite. Sanity-check the new row in-game: army appears on schedule,
   the unit cannot be queued from a Castle, the builder chat line names the right
   threshold, and the first pair arrives at that razing count.

**Do not** raise a hardcoded array size in the XS — there is none. **Do not** add the unit
to `disabled_units` in `scenario/setup.py`; that list is the inherited baseline and the
derived ban is what keeps itself current.

## Allocating a new variable id

1. Pick the next free id after the highest current block (today: 121) and add a constant
   beside the others in `build.py`:

   ```python
   MY_FEATURE_VARIABLE_BASE = 121
   ```

2. Allocate contiguously — one per color if the block is color-indexed. Leave no gap.

3. Reference the constant everywhere. In Python, `MY_FEATURE_VARIABLE_BASE + n - 1`. In
   the XS f-string, `{MY_FEATURE_VARIABLE_BASE} + scenarioPlayer - 1`. Never a literal;
   `test_evolution_alpha_xs_addresses_trigger_variables_through_named_bases` enforces the
   XS side.

4. Declare the variables in `_add_color_runtime_variables` (or wherever the owning pass
   lives) so they exist in the serialized table.

5. Build. `_assert_variable_ids_are_contiguous` will tell you immediately if you left a
   hole or collided with an existing block.

## Adding or changing a hero tier

1. Add the `(kills, hero_id)` pair to `HERO_MILESTONES` and the closing bound to
   `HERO_MILESTONE_UPPER_BOUNDS`. **Bands must stay mutually exclusive and contiguous** —
   overlapping bands let a lower tier burst-spawn when the Penguin returns from OFF, which
   is the exact bug the band structure exists to prevent.
2. If the new tier sits above 3,500, it belongs in `_configure_sparse_late_hero_boosts`
   instead, and needs the Penguin-level gate and the object ceiling that excludes the
   controller.
3. The tier must arm the Hero pulse after creating its unit, or the new Hero receives no
   route order at all.
4. Update the table in [`ascendants-gameplay.md`](ascendants-gameplay.md) and the public
   `PUBLIC_INSTRUCTIONS` string, which lists the milestones to players.

## Changing a slider level

1. Edit `SOURCE_ARMY_RANGE_DESTINATIONS` or `SOURCE_HERO_RANGE_DESTINATIONS` in the
   canonical P3 frame only. Never write per-color coordinates.
2. Destinations must stay on grounded arena cells and must remain **monotonic** toward the
   center; a destination behind the previous level makes the slider read as broken.
3. Changing the *number* of levels means changing `SOURCE_RANGE_LEVEL_SPANS` too, and the
   spans must still partition the whole dry track with no gap and no overlap.
4. Rebuild and re-read `aoe2modes map --html`; then walk the change in-game, because the
   parser cannot execute DE pathfinding.

## Changing a ban

Bans are cumulative and conservative. `_normalize_player_restrictions` takes the **union**
of the inherited per-color lists so a lobby color never decides what a civilization may
train.

The inherited `disabled_buildings` list carries id 621, which resolves to no building in
the pinned dataset. It is kept deliberately: removing an entry from a ban list is a live
gameplay change, and a ban on an id the game does not have is inert.
