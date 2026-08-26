# Data triggers

A way to hand-pick areas, tiles, units or triggers **in the in-game editor** and read them back by
name in Python — instead of hard-coding coordinates you measured by eye.

## How it works

A data trigger is an ordinary trigger whose *name* carries a prefix and a label, holding any
conditions/effects whose selection fields you filled in. The effect or condition type is irrelevant;
`load_data_triggers` only looks at the selection attributes (e.g. `area_x1`/`area_y1`/`area_x2`/
`area_y2` for an area).

| Type | Trigger name prefixes | Selected in-game with |
| --- | --- | --- |
| `Area` | `area:`, `areas:` | the **Set Area** button (effects & conditions) |
| `Tile` | `tile:`, `tiles:` | **Set Location** (effects) or **Set Area** (effects & conditions) |
| `Unit` | `object:`, `objects:` | **Set Objects**, **Set Location**, or **Set Area** (all units inside it) |
| `Trigger` | `trigger:`, `triggers:` | the **Trigger List** dropdown of a (de)activate effect |

## Usage

1. In the editor: create a trigger named `area:cool_middle_area`.
2. Add e.g. a `Bring Object to Area` condition and use **Set Area** to select the region.
3. Save the scenario.

```py
trigger_data = scenario.actions.load_data_triggers()

cool_area = trigger_data.areas['cool_middle_area']   # List[Area]
trigger_data.objects.TCs                             # attribute access also works
trigger_data.objects['name with space']              # ... except for keys with spaces
```

The result exposes four dicts — `.areas`, `.tiles`, `.objects`, `.triggers` — each mapping label to
a **list**, because one trigger can hold many selections and several triggers may share a label.

```py
from typing import List
from AoE2ScenarioParser.helper.attr_dict import AttrDict
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.data_objects.unit import Unit
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile

areas:    AttrDict[str, List[Area]]    = trigger_data.areas
tiles:    AttrDict[str, List[Tile]]    = trigger_data.tiles
triggers: AttrDict[str, List[Trigger]] = trigger_data.triggers
objects:  AttrDict[str, List[Unit]]    = trigger_data.objects
```

## Watch out

- **The data triggers are deleted by the call.** `load_data_triggers()` removes every trigger it
  matched. Pass `remove_template_triggers=False` to keep them.
- Labels should be unique per data type; same-label triggers merge into one list.
- One **Set Area** selection can yield many `Tile` objects but only one `Area`.

## Fit with this repo

`aoe2modes` builds scenarios from code and TOML rather than from a hand-authored base, so data
triggers are mostly relevant when reverse-engineering an existing CBA Hero variant — pair them with
`aoe2modes inspect <file.aoe2scenario> --triggers` to recover geometry before rebuilding it here.
Anything you extract should end up as explicit coordinates in `build.py` or `mode.toml`, so the
build stays reproducible without the source scenario.
