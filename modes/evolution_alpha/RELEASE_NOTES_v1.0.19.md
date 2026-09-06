# CBA Hero: Ascendants v1.0.19 candidate

## ASC-049 — closed-slot player identity

The user reproduced the failure in v1.0.18: Blue and Green versus Teal, Purple,
Gray and Orange, with **two slots explicitly closed before starting**, not left
open. Gray and Orange were missing from the custom K/D/R display and retained
buildings after losing their Castles. This invalidates the claim that v1.0.18's
cleanup changes alone handled the live report.

The available recording's initial header confirms six players, scenario v1.0.18,
DE build 180059 and save format 68.0. The replay reader cannot parse the full player
table for that format; it does not establish exact runtime ids or XS values.

All four color-runtime consumers used `xsGetWorldPlayerId(color)` and stopped if
that result was not in-game. The active/occupied state then controlled HUD setup,
cleanup and victory. Existing assertions only proved the converter was called;
the cleanup model supplied already-correct occupancy. Neither could detect this
shared missing-player path. The exact engine-level converter behavior remains
unconfirmed, so this release is a **candidate**, not a live-verified resolution.

## Changed

- Build the XS identity table from all 32 final placed Castle reference ids.
  Reject missing, negative or duplicate reference ids during generation.
- Read the actual Castles' owners with `xsGetUnitOwner`, independently of the
  trigger-side selector. Reject Gaia, invalid/non-playing owners, mixed Castle
  ownership and duplicate territory bindings. Retry unresolved colors.
- Cache the first valid XS owner per color. Retain it after Castle loss or
  resignation; never remap eliminated colors from surviving/enemy objects.
- Share that boundary across army spawning, builder rewards, HUD statistics and
  active/occupied state. The v1.0.18 persistent-occupancy cleanup, retry purges,
  empty-owner victory gates and elimination production guards remain intact.
- Emit one `[CBA identity] color:Castle-owner/converter` chat line after ten seconds.
  The old converter is used only there, never to choose a gameplay owner. Zero
  Castle-owner means closed/unresolved; occupied Gray and Orange must be positive.

No terrain, placed object, training restriction, balance, control track, Hero
distance or Scorpion lifetime changes. The returning-birth-pad issue ASC-037
remains open and separate.

## Verification and limitations

The 142 repository tests pass (82 Ascendants, 60 other). Four new identity tests
execute the emitted resolver's small C-like subset with mocked engine reads,
instead of reproducing its algorithm separately. They cover all 255 nonempty
occupied-color subsets in two seat orders, actual serialized Castle ids, delayed
objects, invalid/mixed/duplicate owners and caching after elimination. The
cleanup/victory matrix now also includes the exact reported closed-slot 2v4.

Full build and 717-line embedded XS validation pass. Repository Ruff and
whitespace checks pass. Strict audit: 0 errors and 0 warnings; 3,783 triggers
(3,323 initially enabled, 3,774 conservatively reachable), 16,873 conditions,
15,136 effects and 137 variables. Readback comparison against installed v1.0.18
confirms all 956 objects, 20,736 terrain cells and eight restriction sets unchanged.

Artifact: `CBA Hero Ascendants v1.0.19.aoe2scenario`, 161,657 bytes.
SHA-256: `ec4c03df92588582e5c5984e1befdd9d18b289b4553c9a4b86503a098c3991a0`.

These checks do **not** run the DE engine: native unit-id
stability, owner API behavior, garrison cleanup and trigger scheduling remain
live acceptance items.

## Required live check

Start a **new** v1.0.19 match with P1/P3 against P5/P6/P7/P8 and P2/P4 closed.
Capture the ten-second identity line. All six occupied HUD rows must show values;
P2/P4 must remain blank. Confirm every territory produces its own army, then
eliminate Gray and Orange with Universities, walls, gates, towers, foundations,
military and garrisoned units left. All defeated-owned objects must disappear,
living players/Gaia must remain, and the final opponent must not win/lose before
cleanup. Repeat with shuffled colors, resignation, vote-kick and full 4v4.

A running or saved v1.0.18 match will not inherit this change. Previous installed
scenario versions are retained for comparison and recovery.
