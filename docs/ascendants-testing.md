# What Ascendants actually proves

Ascendants is a code-defined mode with no binary reference, so there is no
`aoe2modes verify` round trip to lean on. Confidence comes from three independent
layers, and each has a hard limit. This document says what each one covers, and — just as
importantly — what none of them can cover.

## The three layers

| Layer | Runs when | Catches |
| --- | --- | --- |
| **Build assertions** | Every build, inline | Assumption drift: renamed triggers, changed family counts, variable id collisions, mismatched civ tables |
| **Test suite** | `pytest tests/test_evolution_alpha.py` | Behavior of the serialized graph: ownership matrices, geometry, bands, pulses, bans |
| **Structural audit** | `aoe2modes audit <file> --strict` | Defects in the *serialized artifact*: dangling references, invalid coordinates, unpaced loops, immediate victory |

They fail in that order, and earlier is cheaper. A build assertion fires in seconds and
names the assumption; an audit finding arrives after a full build and describes a symptom.

## Running it

```bash
.venv/Scripts/python -m pytest -q tests/test_evolution_alpha.py
.venv/Scripts/python -m pytest -q --ignore=tests/test_evolution_alpha.py
.venv/Scripts/python -m aoe2modes build evolution_alpha
.venv/Scripts/python -m aoe2modes audit \
  "dist/CBA Hero Ascendants v<version>.aoe2scenario" --strict
.venv/Scripts/python -m aoe2modes map evolution_alpha --html dist/ascendants-map.html
```

Where `make` is available, `make check-ascendants` runs the focused tests, the build, the
audit and the map report in one go. It derives the audited filename from `mode.toml`, so a
version bump needs no edit.

The two pytest invocations are split deliberately: the Ascendants file is large and slow,
and running it separately from the rest of the suite keeps a failure in one from masking
the other. Together they are the full repository suite.

`pytest` runs with `filterwarnings = ["error", ...]`, so warnings fail tests.

## Layer 1 — build assertions

The build refuses to emit a quietly wrong scenario. Each of these raises rather than
warns; when one fires, an assumption moved and the fix belongs at the cause.

| Assertion | What moved if it fires |
| --- | --- |
| `_assert_variable_ids_are_contiguous` | A variable block collided, duplicated or left a hole in ids 0–136 |
| `_validate_army_spawn_geometry` | A color's four wave pads are unsafe, duplicated, or nearest the wrong Castle |
| `_unique_trigger(ctx, name)` | An inherited trigger was renamed, duplicated or removed upstream |
| Exact family counts | e.g. exactly 40 legacy late-hero triggers, exactly two legacy rename triggers, one Blacksmith condition per color |
| `V2MapReport` expected totals | Source object count, canonical sector size, terrain changes, object moves, or new-wall count changed |
| Civ table symmetry | `CIV_SPAWN_RULES` and `CIV_BUILDER_RULES` stopped covering the same ids |
| XS array sizing | Implicit — arrays are sized from the tables, so a new civ cannot overrun them |
| `xs-check` | The generated XS does not lint |

The variable-id assertion deserves its own note: conditions and effects address a variable
**by id, not by name**, so a collision rewires trigger logic without changing a single
visible field. It is cheap to assert and expensive to debug in a lobby.

## Layer 2 — the test suite

`tests/test_evolution_alpha.py` holds 78 test functions (count them with
`pytest --collect-only -q tests/test_evolution_alpha.py`). They build the scenario once
and interrogate the resulting graph. Grouped by what they pin:

### Identity and ownership

The most load-bearing group. DE may seat any lobby slot in any Castle row.

- `keeps_xs_spawn_and_trigger_routes_in_separate_identity_domains` — asserts the engine
  conversion boundary itself. Enumerating Python permutations does not simulate the DE
  engine and proves nothing here.
- `detects_every_color_owner_from_its_castles` — all 64 color/owner detectors.
- `color_active_has_exactly_one_writer` — `p#coloractive` is written only by XS.
- `xs_addresses_trigger_variables_through_named_bases` — no bare variable literals in the
  generated XS.
- `spawns_for_compacted_color_slots`, `spawns_sparse_raze_builders_in_their_color_base`,
  `hero_milestones_work_for_every_color_and_runtime_owner`,
  `remaps_sparse_feudal_upgrades`, `maps_center_rewards_to_runtime_players`.

### Victory and liveness

- `victory_resolves_for_every_lobby_shape` and `victory_survives_split_player_identity`
  walk the serialized victory subsystem **as a state machine** across six lobby shapes,
  closed slots both cleaned and left in place, and a deliberately split player identity,
  and prove that a side which has lost its Castles always ends the match.
- `uses_color_side_custom_victory`, `keeps_fixed_slot_teams`.

The v1.0.18 model also evaluates elimination removals and inspects every victory
snapshot. `elimination_purges_objects_before_any_winner` fails on the pulled v1.0.17
artifact. It tests elimination before cleanup, residual placed objects/foundations,
already-spent one-shot resolvers, six lobby shapes, both losing sides, and preservation
of other owners and Gaia. `cleanup_is_owner_wide_and_inactive_safe` pins all 64
owner mappings and unrestricted filters. `cannot_produce_after_elimination` covers
trigger producers and the XS birth/queue early exits. This remains a state model,
not a DE garrison or scheduler simulation.

### Controllers and movement

- `builds_clear_two_lane_range_islands` — every lane cell, both tracks, the water gap.
- `controllers_cannot_leave_their_trigger_tracks` — connectivity from each controller
  start reaches every level of its own track and nothing outside it.
- `uses_independent_sheep_and_penguin_range_sliders` — all 96 slider selectors and the
  704 army/Hero movement mappings.
- `all_looping_move_orders_consume_one_spawn_pulse` — the one-shot invariant: no looping
  move order exists that is not gated on a creation pulse it then resets.
- `closest_heroes_share_the_castle_front_line`, `hero_off_discards_a_pending_route`,
  `late_heroes_arm_one_shot_route_orders`,
  `returned_units_are_not_deleted_or_rebuffed_by_rewards`.

### Geometry and symmetry

- `uses_v2_terrain_with_protected_team_routes`, `trims_all_four_corner_team_routes`,
  `keeps_v2_objects_and_playable_gate_holes`,
  `orients_every_v2_wall_and_gate_by_map_axis`.
- `keeps_allied_routes_open_and_enemy_sides_water`,
  `all_six_allied_links_have_clear_dry_centerlines`,
  `keeps_all_rear_technology_paths_dry` — bounded flood fills, treating water, walls,
  towers, Castles and cliffs as blocked.
- `uses_complete_rear_walls_without_cliffs`,
  `anti_treb_zones_are_mirrored_and_cover_their_castles`,
  `pins_king_and_relic_selector_roles`, `kings_use_symmetric_island_destinations`,
  `king_cannons_use_symmetric_ground_positions`.

Symmetry tests re-derive the eight-way transform independently and compare against all
eight serialized results, rather than trusting the build's own transform helper.

### Walls

- `wall_breach_removes_side_walls_but_keeps_front_and_uni` — all 64 exact-reference
  breaches.
- `gate_breach_keeps_front_and_university_enclosures_sealed` — closed-gate reachability
  after side-wall removal, in all eight orientations.
- `wall_cap_warns_then_wipes_for_every_resolved_owner`,
  `wall_cap_clears_every_nonstructural_cell_once` — the 49-rectangle wipe complement and
  its protected-footprint exclusion.
- `has_no_unauthorized_wall_or_gate_destruction`, `protects_all_added_v2_walls`,
  `removes_legacy_no_wall_cleanup`.

### Economy and roster

- `has_zero_resources_and_free_purchases`, `keeps_all_research_free_at_runtime`,
  `keeps_every_object_free_at_runtime`, `free_costs_are_activated_only_for_occupied_slots`,
  `equalizes_only_confirmed_occupied_slots`.
- `bans_every_auto_spawned_unique_unit`, `bans_every_castle_class_building`,
  `training_rules_do_not_depend_on_color`, `disables_castle_trebuchet_training`,
  `forces_the_original_bombard_tower_unlock`.
- `removes_palisade_bonus_and_maps_other_goth_rules`,
  `imperial_goths_cannot_lose_barracks_to_trigger_order`.

### Vote kick

`uses_sparse_safe_two_teammate_vote_kick`, `places_vote_flags_beside_their_markers`,
`vote_markers_allow_delete_but_not_combat_votes`.

### HUD, text and hygiene

- `uses_ordered_right_side_combat_hud`, `shows_live_kills_on_every_white_king`,
  `publishes_combat_only_score_values`, `preserves_player_names`.
- `messages_are_public_facing` rejects development and AI references in serialized text;
  `has_no_imported_language_dependencies` rejects dependence on the source scenario's
  display language.
- `keeps_compact_trigger_count`, `has_valid_runtime_references_and_throttled_loops`,
  `has_no_unconditional_all_slot_resource_loop`,
  `removes_invisible_edge_deletion_strips`,
  `removes_corner_staging_objects_and_submerged_clutter`,
  `static_corner_clutter_is_not_referenced`, `has_no_transport_ship_spawn_markers`,
  `removes_fixed_player_closed_slot_cleanup`, `has_no_retired_cleanup_references`.
- `readme_tracks_the_built_version` keeps `modes/evolution_alpha/README.md` in step with
  `mode.toml`.
- `passes_parser_structural_audit` runs layer 3 from inside the suite.

## Layer 3 — the structural audit

`aoe2modes audit` (implemented in `src/aoe2modes/lib/audit.py`) loads the serialized file
and reports **errors** — structural defects that make a scenario unsafe to test — and
**warnings** — editor debt that may be intentional in a decompiled legacy scenario.
`--strict` treats warnings as failures. Ascendants is expected to report **0 errors and 0
warnings**.

| Class | Findings |
| --- | --- |
| Reference integrity | `dangling-trigger-reference`, `dangling-unit-reference`, `dangling-variable-reference`, `dangling-garrison-reference`, `implicit-variable-references` |
| Identity integrity | `duplicate-trigger-id`, `duplicate-unit-reference`, `duplicate-variable-id`, `invalid-trigger-display-order`, `unit-owner-mismatch`, `invalid-player` |
| Geometry | `out-of-bounds-area`, `out-of-bounds-location`, `out-of-bounds-unit`, `inverted-area`, `partial-area`, `partial-location` |
| Runtime safety | `unpaced-reachable-loop`, `unconditional-destructive-trigger`, `immediate-victory-or-defeat`, `enabled-empty-triggers` |
| Hygiene | `duplicate-trigger-names`, `duplicate-variable-names` |

`immediate-victory-or-defeat` and `unpaced-reachable-loop` are the two that most directly
protect the mode: the first is the class of defect behind ASC-004 (a lobby declaring
defeat at launch), and the second catches a looping trigger with no timer, which in DE
means an every-tick loop.

## The map report

`aoe2modes map evolution_alpha --html dist/ascendants-map.html` covers the half of the
scenario the trigger checks cannot see. It renders terrain and zone views, walkable
regions with gates open and shut, symmetry against all eight transforms, per-player parity
and a distance matrix.

**It is not a pass/fail gate.** Read it and confirm the arena still holds its shape. A map
metric that moves without a matching geometry change is a signal to investigate — for
example the land/water cell counts and the walkable-region counts with gates open versus
closed should only change when you meant to change them.

## The boundary

AoE2ScenarioParser cannot execute Definitive Edition's trigger scheduler, XS runtime,
pathfinder, lobby compaction, multiplayer scheduling, or UI. Everything above reasons about
a serialized data structure.

That means a green suite proves the scenario is **internally coherent and structurally
correct**, not that it plays correctly. In particular these can only be settled in-game:

- whether DE's pathfinder actually walks a route the flood fill says is connected;
- whether lobby compaction seats players the way the identity model assumes;
- whether a trigger fires within the expected number of seconds under multiplayer
  scheduling;
- anything about how the UI renders.

Those cases live in [`ascendants-issue-register.md`](ascendants-issue-register.md), whose
"Required game check" column is the acceptance checklist. In that register, **"Guarded"
means the serialized scenario and tests contain the intended correction — not that the
engine has been observed running it successfully.** Keep that distinction when writing
release notes.
