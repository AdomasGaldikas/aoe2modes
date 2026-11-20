# CBA Naval Admirals v0.3.1

The v0.3 scenario produced a DE startup error: `default0.xs(649)` reported an
invalid expression/condition, then failures parsing a FOR loop and `navalTick`.
Reading the game's generated `default0.xs` locates the reported line beside the
first center-control reward condition: `hold > 0 && hold % 30 == 0`. DE's line
reporting differs slightly from the file's displayed line numbers.

The hotfix calculates both reward remainders in separate integer statements,
then uses simple comparisons in braced condition bodies. The 30-second prestige
and 90-second siege cadence is unchanged. Harbor geometry and construction are unchanged.

Nearby ships now heal continuously at 1 HP per game second within 14 tiles of a
surviving own port, including completed built ports. The old ten-second damage
cooldown is removed. Healing does not stack across nearby ports, preserves
fractional HP, stops outside the harbor and never exceeds actual maximum HP.

`xs-check` and the C++ execution harness accepted the original expression. They
are not the game's parser. A new regression inspects serialized conditions before
translation and rejects modulo combined with logical operators. Runtime checks
exercise the 30/90-second boundaries, queued siege and contested reset, as well
as the new healing rate, maximum HP and additional-port healing. The
unfinished-port defeat test now explicitly resets its mock participation state.

Build/install `cba_naval`, select **CBA Naval Admirals v0.3.1**, and start a fresh
match. The failed v0.3 file remains available for comparison. Automated checks
cannot establish DE startup acceptance; the rewritten condition still needs a
fresh engine load.
