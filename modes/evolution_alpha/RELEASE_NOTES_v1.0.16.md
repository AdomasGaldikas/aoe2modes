# CBA Hero: Ascendants v1.0.16 candidate

This release fixes six issues found while auditing v1.0.15 and brings the lowest
active Hero distance to the Army HOLD line, directly in front of each Castle row.
The Penguin's snowy OFF position still stops production. It preserves the
50-second Scorpion reward lifetime, the side-wall wipe, and the front/University
barriers. The map and all placed objects are unchanged.

## Corrections

| Issue | Before | v1.0.16 |
| --- | --- | --- |
| ASC-031: color-dependent roster | Different colors omitted different training bans. Examples include Green's Genoese Crossbowmen and Elite Camel Archers, Yellow's Elite Conquistadors and Outposts, and Trade Carts for every color except Orange. | Every color uses the union of the existing disabled-unit, building, and technology lists, with duplicates removed. This closes omissions without enabling previously banned options. Normal civilization availability still applies. |
| ASC-032: returning Genghis deleted | The 2,000, 3,500, and both 5,000-kill loops removed an existing Genghis Khan on their creation tile. | Production waits while an owned Genghis occupies that tile. The old unit survives, and the new-unit HP/attack bonus cannot be applied repeatedly to it. |
| ASC-033: center reward destroys parked units | The Trebuchet reward removed owned packed units on its marker before creation. | The reward waits for that tile to be clear of owned packed units. Existing Trebuchets and other packed units are preserved. |
| ASC-034: stale Hero order after OFF | Turning Heroes off between creation and routing left the movement pulse armed. Re-enabling could then apply an old order. | Hero OFF clears the pending Hero route as well as setting production to zero. Re-enabling alone cannot resurrect that pulse. |
| ASC-035: Imperial transition race | The active Goth Barracks remover could execute before the separate Imperial trigger disabled it. | The remover and Anarchy activation independently require Imperial Age to be unresearched. Once Imperial is researched, neither can destroy or re-arm Barracks removal. |
| ASC-036: combat can cast votes | A vote Outpost's absence counted as a vote, but the marker had no attack protection. | All 24 markers are unattackable through initial and owner-resolved setup. Their owners can still delete them to vote. |

The roster decision deliberately preserves existing restrictions rather than
inventing a new balance: 143 distinct disabled units, 14 buildings, and one technology
are shared across the eight colors. Castle-created armies and trigger rewards can
still create their specified units; these lists control ordinary availability.

## Audit coverage and limits

ASC-038: all 64 Hero L1 color/owner mappings now target canonical `(21,54)` instead
of `(25,54)`. Readback tests derive the row axis from placed Castles, compare L1
against actual Army HOLD orders, require one-cell adjacency to a Castle footprint,
and check tile connectivity from the Hero pad with friendly gates open. L2–L5,
the controller lanes, and unit creation pads are unchanged. Scenario instructions
explain the closest setting.

The source review covered the XS color/lobby conversion, army and builder generation,
Hero kill bands and OFF behavior, route pulses, defeat/resignation/vote cleanup,
wall deletion paths, center and side-island rewards, Goth progression, roster
restrictions, controller safety, and the existing geometry contracts. Regressions
exercise all 64 color/trigger-owner mappings where relevant.

The 50-second Scorpion removal is intentional, as confirmed by the user. Both Scorpion
training types are disabled for all colors. Its eight owner-specific cleanup
triggers and reward behavior are retained. Packed Trebuchets remain forbidden in
the Castle exclusion zones for all owners; those existing rules are unchanged.

The trigger/XS identity boundary was checked against the
[engine developer's XS reference](https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/xs-scripting-in-age-of-empires-ii-definitive-edition).
XS still uses `xsGetWorldPlayerId`; trigger fields use the independent Castle-row
resolver. The XS runtime is unchanged in this release.

Automated checks cannot establish that every possible gameplay issue is absent.
In particular, movement effects select units spatially during a creation pulse:
a manually returning unit sharing that selection area during a later birth can
still be selected. The pulse prevents continuous retasking between births but is
not a per-unit identity guarantee. Replacing that mechanism requires an engine-tested
way to order only newly created references. This limitation is now explicitly tracked
as ASC-037 rather than described as fully proven safe.

Required in-game checks: parked Genghis at each late-tier spawn pad; occupied center
reward pad; Hero OFF immediately after a birth and then ON; Goth Imperial transition;
attempted attacks and intentional deletion of vote markers; identical civilization
menus across colors; and the established full/sparse/shuffled lobby acceptance matrix.

## Verification

- All 125 repository tests pass: 65 Ascendants and 60 other tests. The final
  public-instructions and closest-Hero checks also pass in a targeted rerun.
- Full build and 616-line embedded XS validation pass. The only XS difference from
  v1.0.15 is the generated version comment; runtime logic is unchanged.
- Strict readback audit: 0 errors, 0 warnings; 3,647 triggers, 15,009 conditions,
  14,936 effects, 956 units, and 121 variables. There are 3,187 initially enabled
  and 3,638 conservatively reachable triggers.
- Readback confirms all 956 placed objects and all 20,736 terrain cells unchanged
  from v1.0.15. No wall, gate, controller track, or shoreline was moved.
- Repository Ruff and whitespace checks pass. No live DE match was run.
- Artifact: `CBA Hero Ascendants v1.0.16.aoe2scenario`, 153,600 bytes.
- SHA-256: `e76e6fd20e4f2ab0e7419234131e01cac45f11b9c3572c831a6b0637351c03ad`.

Installed alongside the previous version in the user's DE scenario folder; its
SHA-256 matches the artifact above. Start a new match; an existing saved or running
match cannot pick up scenario-file changes.
