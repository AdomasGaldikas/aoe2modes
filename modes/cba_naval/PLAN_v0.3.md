# v0.3: harbor construction and land containment

Implemented from the request for narrower access, surrounding ground and earned civilians.

- Each harbor is an isolated land ring around its lagoon, with one four-tile sea
  entrance. A three-tile water moat also separates land from the outer map edge.
  There are no land connections between colors or to the four reef islands.
- Starting batteries flank the mouth, with two shore Archers. All fresh ships
  leave through a common waypoint beyond that mouth before attack-moving to sea.
- Actual kills at 30/60/90/120 earn one Villager and 400 wood/150 stone. Placement
  retries retain the entitlement; resources arrive only with a successful birth.
  Prestige does not manufacture builder rewards. Civilian orders stay manual.
- Only Dock, Watch Tower and Archery Range construction is enabled. Only Archers
  are trainable. Transporters, workers, other troops/buildings and research stay
  disabled. Supplies replace gathering; limits include foundations and queued units.
- Up to two additional completed ports add lives, two ships per wave and repair.
  Foundations do not count. Elimination is latched permanently at zero completed
  ports. Four additional towers, one range and twelve live Archers bound expansion.
- Docks must lie inside the lagoon, clear of the mouth; invalid/excess placement
  is removed and refunded at its configured cost. This protects navigation.
- HUD adds delivered Builders beside the previous Ports/K/D/R/Tier/Waves data.

Automated acceptance exercises the emitted XS and serialized native defeat graph,
with independently numbered owners/selectors. It checks reward retries, exact supply
credits, completion/lives/waves, limits/refunds, no resurrection and cleanup of all
land and sea assets. Geometry checks seal the mouth and flood-fill the eight separate
land components, with sample additional dock footprints. These checks do not simulate
DE construction, garrisoning, unit radii or pathfinding; those need a fresh live match.

Construction completion compares `xsGetUnitBuildPoints` against the building's
`cTrainTime` attribute. APIs are documented in the
[developer XS reference](https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/xs-scripting-in-age-of-empires-ii-definitive-edition).
The v0.3 artifact is separate from v0.2 so both versions remain selectable.
