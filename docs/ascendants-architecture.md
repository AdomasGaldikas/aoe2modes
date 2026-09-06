# Ascendants build architecture

How `modes/evolution_alpha` turns Python into an `.aoe2scenario`. Read this before
changing anything in `build.py`.

Companion documents: [`ascendants-development.md`](ascendants-development.md) (why the
mode is code-defined and what the release loop is), [`ascendants-xs-runtime.md`](ascendants-xs-runtime.md)
(the scripting half), [`ascendants-map.md`](ascendants-map.md) (geometry) and
[`ascendants-testing.md`](ascendants-testing.md) (what is proven).

## The mode flavour

Ascendants is the repo's only **code-defined** mode. It has no `scenario.base` and no
`scenario.reference`:

- there is no binary input, so `aoe2modes decompile --mode evolution_alpha` refuses to
  run — and running it against the built file would overwrite the source with a dump of
  its own output;
- there is nothing to compare back against, so `aoe2modes verify` does not apply;
- `dist/CBA Hero Ascendants v<version>.aoe2scenario` is purely a build product.

The structural check is `aoe2modes audit` on the built file, plus the test suite.

## Two source layers

```
aoe2modes build evolution_alpha
  └─ builder.build_mode
       ├─ registry / config      mode.toml
       ├─ toolchain.configure    parser settings, xs-check
       ├─ from_default()         blank v1.58 scenario
       ├─ declarative phase      map + players from mode.toml
       └─ build(ctx)             modes/evolution_alpha/build.py
            ├─ scenario.apply(ctx)      ← layer 1: the arena
            └─ ~40 Ascendants passes    ← layer 2: the mode
                 └─ apply_v2_map(ctx)   ← the map transformation
```

**Layer 1 — `scenario/`** lays down the arena: map size, terrain, units, players, lobby
options, and the legacy CBA Hero trigger graph. It began as `aoe2modes decompile` output
and is now ordinary hand-maintained source. Its stages run in a fixed order
(`setup → terrain → units → triggers`) because the map must be sized before terrain is
painted, units placed before triggers reference them, and triggers created in a stable
order because `activate_trigger` addresses them **positionally**.

| File | Lines | Contents |
| --- | ---: | --- |
| `scenario/setup.py` | 268 | Map size, eight players, ages, colors, diplomacy, ban lists |
| `scenario/terrain.py` | 2,603 | Every terrain cell of the inherited arena |
| `scenario/units.py` | 1,214 | Preplaced objects with their reference ids |
| `scenario/triggers/part_000…007.py` | ~35,800 | The inherited CBA Hero trigger graph |

**Layer 2 — `build.py` + `v2_map.py`** runs after `scenario.apply(ctx)` and applies the
Ascendants map and gameplay layer. **It runs last and it wins.**

The split rule: *structural arena changes go in `scenario/`; Ascendants behavior goes in
`build.py`.*

## How layer 2 works on layer 1

Ascendants rarely deletes an inherited trigger and writes a new one. The dominant pattern
is **claim, reset, rebuild, fan out**:

```python
original = _unique_trigger(ctx, f"feudal ups (p{n})")   # claim it by name
_reset_trigger(original)                                 # strip conditions/effects
original.name = f"Sparse Feudal S{n} W{n}"               # rename to the new scheme
...                                                      # rebuild the behavior
for world_player in _possible_world_players():           # fan out to 8 owners
    ...
```

Three helpers underpin it:

- `_unique_trigger(ctx, name)` — fetch exactly one trigger by name, or raise. A rename
  upstream fails the build instead of silently skipping a patch.
- `_reset_trigger(trigger)` — clear conditions and effects for reuse.
- `_strip_trigger_references(ctx, ids)` — remove graph edges pointing at triggers you are
  about to repurpose.

The fan-out is the sparse-lobby pattern. Because DE may seat any lobby slot in any Castle
row, most systems exist as **8 colors × 8 possible runtime owners = 64 mappings**, each
gated on "this color is active" and "this color's resolved owner is W#". Where a slider
level is also involved the count grows accordingly — 384 Castle-army route mappings
(6 levels × 8 × 8) and 320 Hero route mappings (5 active levels × 8 × 8).

## Trigger naming

Names are the addressing scheme, so they follow a strict convention:

| Form | Meaning |
| --- | --- |
| `Center Kills S3 W5` | Scenario color 3, resolved runtime owner 5 |
| `Color Defeat Resolve S3 W5` | Same, for the defeat resolver family |
| `Color Castle Row Empty S3` | Owner-independent fallback |
| `Legacy Late Hero Boost Disabled #1234` | An inherited trigger neutralized on purpose |

`S#` is always the fixed scenario color; `W#` is always the trigger-side resolved owner.
Keeping the pair in the name is what makes a 3,600-trigger scenario navigable in the
in-game editor.

## The build pass order

`build(ctx)` is a flat list of passes. It is grouped below by intent; the order inside
`build.py` is the order shown.

### 1. Arena

`apply_scenario_source(ctx)` — runs layer 1.

### 2. Neutralize inherited behavior

| Pass | Removes |
| --- | --- |
| `_reset_unsafe_vote_kick` | The legacy vote path, which could defeat a real player at tick zero in a sparse lobby |
| `_remove_legacy_edge_deletion_strips` | Invisible map-edge strips that deleted every owned object |
| `_disable_legacy_no_wall_cleanup` | Startup deletion of the symmetric side walls |
| `_optimize_legacy_polling` | Throttles persistent checks; makes one-shot events truly one-shot |
| `_mirror_legacy_anti_treb_zones` | Rebuilds the eight anti-Trebuchet zones from one canonical rectangle |
| `_clear_legacy_resource_score_triggers` | Old 100k tribute loops that inflated score |

### 3. Economy and roster

`_zero_starting_resources`, `_normalize_player_restrictions`, `_disable_castle_trebuchets`,
`_ban_auto_spawned_unique_units`, `_ban_castle_class_buildings`.

`_normalize_player_restrictions` takes the **union** of the inherited per-color ban lists,
because a lobby color must not decide whether a civilization can train an otherwise banned
unit. The two `_ban_*` passes then close gaps that the union cannot: unique units are
derived from `CIV_SPAWN_RULES` so the ban is self-maintaining, and Krepost and Donjon join
the Castle ban so no civilization can raise a fifth castle-class fortification with free
stone.

### 4. Runtime identity — the foundation

```python
(active_variables, world_variables,
 eliminated_variables, match_ready_variable) = _add_color_runtime_variables(ctx)
_add_color_owner_detection(ctx, world_variables)
```

Everything sparse-safe downstream takes these four handles. `_add_color_owner_detection`
latches which trigger-side player selector owns each Castle row. It deliberately does
**not** write `p#coloractive` — that has exactly one writer, in XS. See
[`ascendants-xs-runtime.md`](ascendants-xs-runtime.md).

### 5. Match resolution

`_configure_custom_team_victory` builds defeat and victory on three properties:

1. **Defeat is a map state, not an event.** Each resolver ships enabled and fires from its
   own "no Castle of this owner in this color's row" condition. It used to ship disabled
   and depend on a one-shot `Destroy Object` chain, which can never become true if the
   Castles leave the map any other way — a `Remove Object`, a purge, an engine-cleaned
   closed slot.
2. **A row-empty fallback is independent of both identity domains.** `Color Castle Row
   Empty S#` asks only whether *any* candidate owner still holds a Castle there, so it
   needs neither the trigger-side latch nor the lobby-slot bit. If those two disagree, all
   eight owner-resolved resolvers for a color are unsatisfiable while the color still
   reads alive — the fallback is what stops that hanging a match.
3. **Victory ships disabled** and is armed by the one owner detector whose latch it can
   match, so seven of every eight candidates leave the tick loop at start-up.

v1.0.18 additionally separates persistent occupancy (`coloroccupied`) from active
state. The defeat resolver requires occupancy, not active=1. All elimination paths
share an unrestricted owner-only purge, preceded by enabling deletion. There are
64 one-second `Color Elimination Cleanup` retries and 64 `Color Cleanup Complete`
confirmations. Confirmation requires fewer than one owned object; each team-victory
candidate checks every opposing color's clean flag. Unused colors initialize clean;
the first XS in-game observation resets an occupied color's flag.

`_stop_eliminated_color_production` runs after gameplay generation and adds
eliminated=0 to color-gated object producers. XS waves and builder queuing have the
same early exit. The cached trigger owner remains separate from XS player IDs.

### 6. Spawning and the XS handoff

`_replace_legacy_army_spawns` replaces the legacy per-color spawn loops, allocates the
army and Hero range variables, and calls `ctx.add_xs(_render_color_spawn_xs(), ...)` —
this is where the generated XS enters the build.

### 7. Gameplay systems on the pre-V2 map

`_add_sparse_feudal_upgrades`, `_add_rear_enclosures`, `_open_rear_technology_paths`,
`_finish_rear_perimeters`, `_rewrite_public_messages`, `_add_sparse_lobby_scoreboard`,
`_force_bombard_tower_unlock`, `_add_live_white_king_kill_counters`,
`_disable_fixed_color_kill_announcements`, `_configure_sparse_center_views`.

### 8. The V2 map transformation — the ordering hinge

```python
v2_report = apply_v2_map(ctx)
_remap_v2_trigger_geometry(ctx)
```

`apply_v2_map` rewrites terrain and moves objects into eight-way symmetry. **Everything
that depends on final coordinates must run after it**, and `_remap_v2_trigger_geometry`
immediately repairs trigger geometry the move invalidated. This is the single most
important ordering constraint in the file. See [`ascendants-map.md`](ascendants-map.md).

### 9. Geometry-dependent systems

`_configure_range_sliders`, `_configure_sparse_center_rewards`,
`_configure_sparse_wall_breaches`, `_configure_sparse_king_islands`,
`_relocate_builder_spawn_flags`, `_remove_remaining_ice_decorations`,
`_remove_corner_staging_objects`, `_remap_raze_villagers`,
`_configure_sparse_hero_milestones`, `_configure_sparse_late_hero_boosts`,
`_configure_sparse_vote_kick`.

### 10. Finalize

`_finalize_occupied_slot_gates`, `_retire_obsolete_public_loops`,
`_neutralize_fixed_color_tags`, `_sanitize_serialized_labels` — the last of these runs
**after every name-based patch**, because it removes the identity and attribution text
those patches match on.

### 11. Validate and compact

```python
_validate_army_spawn_geometry(ctx)
# fold V2's new wall references into each color's Antidelete protection
_compact_legacy_trigger_graph(ctx)
_assert_variable_ids_are_contiguous(ctx)
```

`_compact_legacy_trigger_graph` removes proven no-op shells and merges byte-identical
legacy age-up logic. It must run **after every name- and id-based patch**, because it
rewires references and then lets `TriggerManager.remove_triggers` remap ids and display
order. Exact baseline counts make a future upstream change fail closed rather than delete
a newly meaningful trigger by accident.

## Fail-closed assertions

The build raises rather than emitting a quietly wrong scenario. When one of these fires,
it is telling you an assumption moved — fix the cause, do not relax the assertion.

| Assertion | Catches |
| --- | --- |
| `_assert_variable_ids_are_contiguous` | A hole, duplicate or collision in the 0–136 id space. Ids are handed out by independent passes from separate bases, and a condition addresses a variable **by id, not by name** — so a collision rewires trigger logic without changing a single visible field |
| `_validate_army_spawn_geometry` | A color's four wave pads being unsafe, duplicated or assigned to the wrong Castle |
| `_unique_trigger` | An inherited trigger renamed or duplicated upstream |
| Exact family counts | e.g. exactly 40 legacy late-hero triggers, exactly two legacy rename triggers, exactly one Blacksmith condition per color |
| `V2MapReport` expected totals | Source unit count, canonical sector size, terrain changes, object moves, new walls |
| Civ table symmetry (in the XS renderer) | `CIV_SPAWN_RULES` and `CIV_BUILDER_RULES` covering different id sets |

## Working on `build.py`

- **Adding a gameplay system?** Write it as a fan-out over
  `for color in PLAYERS: for world_player in _possible_world_players():`, gated on the
  active and world variables. A fixed `PlayerId.FIVE` in an effect is almost always a bug
  in a sparse lobby.
- **Does it need final coordinates?** Then it belongs after `apply_v2_map`.
- **Does it match trigger names?** Then it belongs before `_sanitize_serialized_labels`
  and `_compact_legacy_trigger_graph`.
- **Needs a new variable?** Add a `*_VARIABLE_BASE` constant next to the others, allocate
  contiguously, and let the contiguity assertion check you. Never inline a literal id.
- **Touching player identity?** Read the identity rule in
  [`ascendants-xs-runtime.md`](ascendants-xs-runtime.md) first.
- **Then run** the commands in [`ascendants-testing.md`](ascendants-testing.md).
