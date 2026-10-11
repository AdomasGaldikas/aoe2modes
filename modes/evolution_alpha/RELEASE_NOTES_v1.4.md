# CBA Hero 4v4: RA v1.4

Recurring Hero births are silent. Their exact-reference creation and immediate
movement orders remain in place. Builder cues are unchanged.

The six main allied rear routes now have sixteen-tile spans, twice v1.3's width.
Existing gate throats stay narrow and opposing-team water gaps remain closed.
Owner-resolved one-second guards kill hostile units and foundations in opposing
protected routes, including after a protected teammate is eliminated. Thirty-eight
Gaia warning flames sit on dry route margins. Sixty-four native visibility triggers
request opposing-side flames visible and allied-side flames hidden for each resolved
player. Per-player rendering is an engine acceptance case, not an automated result.

## Population selection

One scenario offers 200 / 250 / 300 / 500 gameplay population. Default is 250.
The lowest active occupied color receives the Population chooser on the isolated
north island once its independent XS identity arrives; the host should take that
color. Move it to a numbered pad within the first 60 seconds. The choice then locks
and the chooser is removed. This is an in-game selector, not a lobby dropdown.

All automatic births use actual population costs. Four-Castle waves stop at the
remaining budget, Hero loops wait at the cap, and complete builder pairs and
six-Scorpion backup wait for their full combined cost before consuming the reward.
Fractional and zero population costs are preserved. Removing 576 old integer Hero
count gates avoids ceilings inconsistent with the selected population.

The declared engine ceiling is 501. Resource 32 sets the selected cap plus the
permanent Penguin reserve and temporary chooser reserve; resource 4 refreshes free
housing headroom. This replaces extra civilization population allowances with the
shared choice. Lowering the limit never removes existing troops. Native cleanup
and the existing Castle/defeat/identity-condition sweep are unchanged; ASC-053 now
tracks 2,923 remaining native player conditions, including 64 cleanup count gates.

## Current civilizations and Mirror

Saxons, Varangians and Danes have Elite Castle-army entries, two-raze first builder
thresholds, and base/Elite training bans. Civilization and unit ids were checked
against the installed game's civilization data and English strings. All 62
civilizations have spawn and builder entries. The three new balance values use
the common infantry baseline and remain provisional until gameplay acceptance.

Exact Mirror pairing remains unresolved. The available XS API reports the engine's
resolved civilization, and no supported original-Mirror getter or civilization
reassignment API was found. This release does not substitute a different army while
leaving civilization bonuses and technology trees mismatched. For exact pairs,
explicitly choose matching civilizations for P1/P5, P2/P6, P3/P7 and P4/P8 in the
lobby, including when all players would otherwise choose Mirror.

## Validation

The release build passes embedded XS lint. Strict serialized audit reports zero
errors and warnings: 4,123 triggers, 3,583 initially enabled, 4,114 conservatively
reachable, 19,500 conditions, 14,481 effects, 999 objects, 153 variables (0–152),
and 3,153 XS lines. The map report has 12,680 land cells, 8,056 water cells,
104 closed-gate regions and 82 open-gate regions; the north chooser adds one island.
All objects are on dry terrain and route centerlines remain clear.

The emitted-XS replay checks independently numbered color/XS identities, delayed
identity and failed ownership transfer, all four population choices, fractional
costs, full batch deferral, per-birth ceilings, controller reserves, housing
headroom, exact lock timing and overfull armies when lowering the choice. Structural
checks cover all 64 hazard ownership mappings, visibility reference groups,
six route connections and gate containment, Hero silence, new civilization arrays
and training bans. All 156 repository tests are validated, including 96 RA tests:
the full suite passed 155 tests, then the remaining test passed after its legacy
59-civilization threshold expectation was extended to all 62 civilizations.
Ruff and diff checks also passed.

## Live acceptance

No game/input automation was run for this release. A fresh DE match still needs to
check selector movement and protection, population resource behavior for manual
training at all four choices, engine spawn failures, multiplayer scheduling,
new civilization balance, Hero audio, route deaths and enemy-only flame visibility.
Previous sparse-lobby, native-condition and Scorpion HUD acceptance gaps remain.
These automated checks do not establish engine acceptance.

Artifact: `dist/CBA Hero 4v4 RA v1.4.aoe2scenario`.
SHA-256: `966b6acf2009847c285685b45625666ff15eec762fac747dfb9aa41715aa7509`.
