# CBA Hero 4v4: RA v1.3

Adds **Scorpion Backup** to the existing compact combat display. The header is
`P# | K | D | R | B`; B shows **1** before use, **A** during the backup window,
and **0** after use. The active row retains the same combat variables and display
order. Closed colors remain hidden, and final rows remain after elimination.

The movable activation unit is named **Skorpion King**. Its help text and map
instructions explain moving to the marked side island for six Scorpions for
50 seconds, once per player. The separate white King retains its kill-counter
name and attack statistic. DE's description effect targets a unit type rather
than an instance, so the shared normal-King tooltip explains both roles; P1's
King Sancho type receives only the backup instructions.

Native state uses eight new variables, ids 145–152: 1 available, 2 active
(rendered as A), 0 spent. Activation consumes the King and sets active state;
the same 50-second cleanup that removes the Scorpions sets spent state. Early
elimination ends the active indicator. An explicit available-state condition
prevents reuse. HUD setup waits for native occupied-color ownership and does
not need the independent XS identity token.

## Validation

92 RA tests passed. The new serialized-trigger replay exercises all 64
color/owner pairs with normal setup, delayed HUD setup during an active backup,
and early defeat. It checks six creates for the resolved owner, no second
activation, timed removal, final spent rows and hidden unused colors. Label
checks select the actual activation reference and preserve the white counter.
All 152 repository tests, Ruff and XS lint passed.

Strict readback audit: zero errors/warnings; 4,057 triggers (3,517 initially
enabled, 4,048 conservatively reachable), 19,178 conditions, 14,346 effects,
956 objects, 153 variables and 2,138 embedded XS lines. A v1.2 snapshot comparison
confirms unchanged terrain, placed objects, player settings and lobby options.
The six Scorpion positions, buffs and 50-second lifetime remain unchanged.

## Live acceptance

The native objective-row transitions, B-column spacing and help-text presentation
need a fresh DE match. Automated replay does not execute DE rendering or engine
scheduling. Previous v1.2 birth-order and sparse-lobby acceptance gaps remain in
[the issue register](../../docs/ascendants-issue-register.md).

Artifact: `dist/CBA Hero 4v4 RA v1.3.aoe2scenario`.
SHA-256: `a5b5ac9f71685452b2774e68e7127535b9e01a435039664eec08d817274e76e1`.
