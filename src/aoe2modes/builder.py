"""The build pipeline: mode.toml + build.py -> a writable .aoe2scenario."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from AoE2ScenarioParser.exceptions.asp_exceptions import XsCheckValidationError
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from aoe2modes import toolchain
from aoe2modes.config import ModeSpec
from aoe2modes.context import BuildContext
from aoe2modes.lib import players as players_lib
from aoe2modes.lib import terrain as terrain_lib
from aoe2modes.lib.xs import bundle_xs
from aoe2modes.paths import RepoPaths, paths


class BuildError(RuntimeError):
    """Raised when a mode fails to build."""


def _version_key(spec: ModeSpec) -> tuple[int, int]:
    """Numeric scenario version for build ordering. Blank scenarios use LATEST_VERSION."""
    if spec.scenario_version:
        parts = spec.scenario_version.split(".")
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
    return AoE2DEScenario.LATEST_VERSION


def build_order(specs: list[ModeSpec]) -> list[ModeSpec]:
    """Sort specs newest-first, tie-break by id.

    The AoE2ScenarioParser leaks version-scoped state between scenarios loaded in the
    same process: once you load a v1.51 file, a subsequent v1.58 ``from_default`` or
    ``from_file`` crashes on ``execute_on_load``. Building newest-first keeps older
    scenarios strictly downstream, which sidesteps the leak in every direction we've
    observed. Modes with ``scenario.base`` set should declare ``scenario.version`` so
    the sort key is accurate — see ``modes/big_ytri/mode.toml``.
    """
    return sorted(specs, key=lambda s: (tuple(-v for v in _version_key(s)), s.id))


@dataclass(frozen=True)
class BuildResult:
    spec: ModeSpec
    output: Path
    seconds: float
    triggers: int
    units: int
    xs_lines: int


def _load_build_module(spec: ModeSpec) -> ModuleType:
    script = spec.build_script
    if not script.is_file():
        raise BuildError(f"{spec.id}: missing build.py at {script}")

    module_name = f"aoe2modes._modes.{spec.id}"
    # Load build.py *as a package* rooted at the mode folder, so a decompiled mode can
    # `from .generated import apply` instead of mangling sys.path. Two modes can then
    # both own a `generated` package without colliding.
    loader_spec = importlib.util.spec_from_file_location(
        module_name, script, submodule_search_locations=[str(spec.directory)]
    )
    if loader_spec is None or loader_spec.loader is None:
        raise BuildError(f"{spec.id}: cannot import {script}")

    module = importlib.util.module_from_spec(loader_spec)
    # Register before exec so dataclasses/pickle inside the module resolve correctly.
    sys.modules[module_name] = module
    try:
        loader_spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001 - surfaced with mode context attached
        raise BuildError(f"{spec.id}: build.py raised on import: {exc}") from exc

    if not hasattr(module, "build"):
        raise BuildError(f"{spec.id}: build.py must define `def build(ctx): ...`")
    return module


def _create_scenario(spec: ModeSpec) -> AoE2DEScenario:
    if spec.base is not None:
        return AoE2DEScenario.from_file(str(spec.base))
    if spec.scenario_version:
        return AoE2DEScenario.from_default(spec.scenario_version)
    return AoE2DEScenario.from_default()


def build_mode(
    spec: ModeSpec,
    *,
    out_dir: Path | None = None,
    repo: RepoPaths | None = None,
    verbose: bool = False,
    xs_check: bool = True,
) -> BuildResult:
    """Build one mode and write the resulting scenario file."""
    repo = repo or paths()
    out_dir = out_dir or repo.dist
    started = time.perf_counter()

    toolchain.configure(verbose=verbose, xs_check=xs_check)

    scenario = _create_scenario(spec)
    scenario.variant = spec.variant

    ctx = BuildContext(spec=spec, scenario=scenario, repo=repo, verbose=verbose)

    # Declarative phase — everything mode.toml can express, applied before the
    # mode's own code so build.py can freely override any of it. Skipped when a
    # base scenario is loaded: the base file *is* the declarative state, so
    # reapplying defaults would wipe its map and player setup. Base-loaded modes
    # patch state via build.py instead.
    if spec.base is None:
        terrain_lib.apply_map_spec(ctx.map_manager, spec.map)
        players_lib.apply_players_spec(ctx.player_manager, spec.players)

    module = _load_build_module(spec)
    ctx.log(f"running {spec.id}/build.py")
    try:
        module.build(ctx)
    except Exception as exc:  # noqa: BLE001 - surfaced with mode context attached
        raise BuildError(f"{spec.id}: build(ctx) failed: {exc}") from exc

    xs_source = bundle_xs(ctx)
    if xs_source:
        # A build that ships XS the linter rejects is a broken build, so make it fail
        # here rather than surfacing in-game as a silently dead script.
        ctx.xs_manager.xs_check.ignores = set(spec.xs.ignore_warnings)
        ctx.xs_manager.xs_check.raise_on_error = xs_check
        ctx.xs_manager.add_script(xs_string=xs_source)

    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / spec.output_name
    try:
        scenario.write_to_file(str(output))
    except XsCheckValidationError as exc:
        raise BuildError(f"{spec.id}: XS validation failed:\n{exc}") from exc

    return BuildResult(
        spec=spec,
        output=output,
        seconds=time.perf_counter() - started,
        triggers=len(ctx.trigger_manager.triggers),
        units=sum(len(units) for units in ctx.unit_manager.units),
        xs_lines=xs_source.count("\n") if xs_source else 0,
    )


def deploy(result_or_path: BuildResult | Path, scenario_dir: Path) -> Path:
    """Copy a built scenario into the game's scenario folder."""
    source = result_or_path.output if isinstance(result_or_path, BuildResult) else result_or_path
    scenario_dir.mkdir(parents=True, exist_ok=True)
    destination = scenario_dir / source.name
    shutil.copy2(source, destination)
    return destination
