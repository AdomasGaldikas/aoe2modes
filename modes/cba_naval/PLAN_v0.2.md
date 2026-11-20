# Version 0.2 investigation and implementation plan

## Findings

- Confirmed timer defect: 0.1 divided `xsGetTime()` by 1,000 although that API
  returns seconds minus one. Startup waited roughly 50 minutes, the first wave
  roughly 250 minutes. The C++ mock returned milliseconds and hid the defect.
  Use `xsGetGameTime()` directly, as documented in the
  [developer XS reference](https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/xs-scripting-in-age-of-empires-ii-definitive-edition).
- Startup risk: native script conditions can run before the first heartbeat;
  arrays were allocated only in that heartbeat. Allocate them in `main()` and
  make guards return before reading arrays until occupancy has settled.
- Test-lobby defect: production was gated on both teams being occupied. Permit
  one-sided practice production; only competitive victory requires both sides.
- Shared vision was never configured. Embed Cartography and set sharing masks
  from actual occupied XS owners, restricted to their own scenario team.
- Four passive starting ships, slow waves, delayed progression, bare harbors and
  no launch orders for the initial fleet made the opening empty even without bugs.
- The exact reported startup error was not recorded. Do not claim its message
  or engine acceptance has been established by offline checks.

## Version 0.2 design

1. Initialize safely, use the correct seconds clock, launch fleets promptly,
   count successful launches visibly, and test calls before initialization.
2. Keep four ports as lives; add two destructible Guard Towers per harbor and
   ship repair near surviving ports after ten seconds without damage.
3. Start with eight mixed warships; launch two ships per surviving port every
   eight seconds, capped at 120 military population.
4. Give only fresh ships two queued birth orders: leave the harbor, then
   attack-move into the central battle. Leave subsequent manual commands alone.
5. Advance at 20/60/120 kills plus prestige. Award a replaceable Longship,
   Turtle Ship or Admiral flagship. Add a regular siege supply every 75 seconds
   so port attacks are possible without waiting for a first razing.
6. Add four symmetric reef islands for screening/flanking. Central control
   pays +15 prestige every 30 seconds and siege every 90 seconds, contested
   presence still resets continuous control. Razing rewards remain queued.
7. Display participant-only Ports/K/D/R/Tier/Waves rows; derive combat scores
   from actual engine totals, neutralizing unrelated economy/exploration score.
8. Build v0.2 under its own filename, retain the old scenario, run structural,
   navigation and actual-emitted-XS regressions, then deploy the new artifact.

## Acceptance boundary

Offline checks must verify real clock units, pre-init guards, shared-vision masks
with independently numbered owners, successful/failed births, port-bound waves,
queued orders, no later retasking, out-of-combat repair, caps, progression,
rewards, resignation cleanup and competitive victory. Naval connectivity must
account for tower/dock footprints and reefs.

Fresh DE matches still need to verify startup without errors, first and repeat
waves, allied vision with lobby sharing disabled, harbor combat/repair,
pathfinding, HUD/score rendering, AI engagement and multiplayer balance.
