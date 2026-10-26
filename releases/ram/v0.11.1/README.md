# RAM v0.11.1 leader attack-growth fix

The v0.11.0 playtest found starting leaders were not visibly gaining attack.
This patch replaces the custom XS unit-attribute callbacks with the original
native Change Object Attack mechanism. Every eight game seconds, each of the
eight exact starting leader references receives +3 base pierce attack. All
reserved leaders use that attack class. The original +5 HP effects, timer,
object references, national ranged actors and separate selection are preserved.
Later spawned hero armies are not targeted.

The Data Mod DAT, all voices, balance targets, center rules and other gameplay
are retained. Select the matching version and start a fresh match; existing
matches and saves retain their embedded trigger script/effects.

The prior C++ callback test modeled an engine behavior that native playtesting
did not confirm. It is replaced by explicit native-effect serialization checks;
owner-resolved naming still has its independent sparse-player test. A fresh DE
match is required to verify displayed attack increases through multiple ticks.

Installation/publication and native acceptance are recorded in validation.json.
