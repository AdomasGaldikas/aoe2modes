"""Command line entry point: ``aoe2modes <command>``."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from aoe2modes import __version__, registry, toolchain
from aoe2modes.builder import BuildError, BuildResult, build_mode, build_order, deploy
from aoe2modes.config import ConfigError, ModeSpec
from aoe2modes.paths import find_game_scenario_dir, paths


def _resolve_specs(args: argparse.Namespace) -> list[ModeSpec]:
    repo = paths()
    if getattr(args, "all", False) or not args.modes:
        specs = registry.discover(repo)
        if not specs:
            raise ConfigError(f"No modes found in {repo.modes}")
        return specs
    return [registry.get(mode_id, repo) for mode_id in args.modes]


# --- commands ----------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> int:
    specs = registry.discover()
    if not specs:
        print("No modes yet. Create one with: aoe2modes new <id>")
        return 0
    width = max(len(spec.id) for spec in specs)
    for spec in specs:
        tags = f"  [{', '.join(spec.tags)}]" if spec.tags else ""
        print(f"{spec.id:<{width}}  v{spec.version:<8} {spec.name}{tags}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    for spec in _resolve_specs(args):
        players = spec.players
        teams = " vs ".join("+".join(str(int(p)) for p in team) for team in players.teams) or "free-for-all"
        xs_files = list(spec.xs.include) + list(spec.xs.scripts)
        print(f"{spec.name}  (id: {spec.id}, v{spec.version})")
        if spec.description:
            print(f"  {spec.description}")
        print(f"  authors    {', '.join(spec.authors) or '-'}")
        print(f"  tags       {', '.join(spec.tags) or '-'}")
        print(f"  map        {spec.map.size}x{spec.map.size}  {spec.map.terrain.name}")
        print(f"  players    {players.count}  ({teams})")
        print(f"  age / pop  {players.starting_age.name}  /  {players.population_cap}")
        print(f"  resources  {', '.join(f'{k} {v}' for k, v in players.resources.items())}")
        print(f"  base       {spec.base or 'blank DE scenario'}")
        print(f"  xs         {', '.join(xs_files) or '-'}")
        print(f"  output     {spec.output_name}")
        print()
    return 0


def _report(result: BuildResult) -> None:
    print(
        f"  {result.spec.id:<20} -> {result.output.name}"
        f"  ({result.triggers} triggers, {result.units} units,"
        f" {result.xs_lines} xs lines, {result.seconds:.2f}s)"
    )


def cmd_build(args: argparse.Namespace) -> int:
    specs = _resolve_specs(args)
    out_dir = Path(args.out).resolve() if args.out else None
    scenario_dir: Path | None = None

    if args.deploy:
        scenario_dir = Path(args.scenario_dir).expanduser() if args.scenario_dir else find_game_scenario_dir()
        if scenario_dir is None:
            print(
                "Could not locate the AoE2:DE scenario folder. "
                "Pass --scenario-dir or set AOE2_SCENARIO_DIR.",
                file=sys.stderr,
            )
            return 2

    print(f"Building {len(specs)} mode(s)")
    failures = 0
    for spec in build_order(specs):
        try:
            result = build_mode(spec, out_dir=out_dir, verbose=args.verbose, xs_check=not args.no_xs_check)
        except BuildError as exc:
            print(f"  {spec.id:<20} FAILED: {exc}", file=sys.stderr)
            failures += 1
            continue
        _report(result)
        if scenario_dir is not None:
            print(f"  {'':<20}    deployed to {deploy(result, scenario_dir)}")

    return 1 if failures else 0


def cmd_deploy(args: argparse.Namespace) -> int:
    scenario_dir = Path(args.scenario_dir).expanduser() if args.scenario_dir else find_game_scenario_dir()
    if scenario_dir is None:
        print("Could not locate the AoE2:DE scenario folder. Pass --scenario-dir or set AOE2_SCENARIO_DIR.",
              file=sys.stderr)
        return 2

    repo = paths()
    for spec in _resolve_specs(args):
        built = repo.dist / spec.output_name
        if not built.is_file():
            print(f"  {spec.id:<20} not built yet — run: aoe2modes build {spec.id}", file=sys.stderr)
            return 1
        print(f"  {spec.id:<20} -> {deploy(built, scenario_dir)}")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    repo = paths()
    target = repo.modes / args.mode_id
    if target.exists():
        print(f"{target} already exists", file=sys.stderr)
        return 1
    if not repo.template.is_dir():
        print(f"Template missing at {repo.template}", file=sys.stderr)
        return 1

    shutil.copytree(repo.template, target)
    toml_path = target / "mode.toml"
    text = toml_path.read_text(encoding="utf-8")
    text = text.replace('id = "_template"', f'id = "{args.mode_id}"')
    text = text.replace('name = "Template Mode"', f'name = "{args.name or args.mode_id}"')
    toml_path.write_text(text, encoding="utf-8")

    print(f"Created {target}")
    print(f"Next: edit {toml_path} and {target / 'build.py'}, then run: aoe2modes build {args.mode_id}")
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    """Structural trigger diff between two ``.aoe2scenario`` files."""
    from aoe2modes.lib.diff import diff_triggers, format_report, load_pair

    toolchain.configure(verbose=args.verbose, xs_check=False)
    a = Path(args.a).expanduser()
    b = Path(args.b).expanduser()
    scenario_a, scenario_b = load_pair(a, b)
    report = diff_triggers(scenario_a, scenario_b)
    # Include the parent folder in the label when two files share a stem — many
    # of our base scenarios are named base.aoe2scenario inside their mode folder.
    if a.stem == b.stem:
        label_a, label_b = f"{a.parent.name}/{a.stem}", f"{b.parent.name}/{b.stem}"
    else:
        label_a, label_b = a.stem, b.stem
    print(format_report(report, a_label=label_a, b_label=label_b))
    return 0


def cmd_decompile(args: argparse.Namespace) -> int:
    """Turn a base scenario into regenerable Python under ``modes/<id>/generated/``.

    This runs in its own process on purpose. The parser leaks version-scoped global
    state, so the scenario being read (often v1.51) cannot coexist with the blank
    v1.58 scenario the rebuild starts from — writing source decouples the two.
    """
    from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

    from aoe2modes.lib.decompile import decompile

    toolchain.configure(verbose=args.verbose, xs_check=False)

    if args.mode:
        spec = registry.get(args.mode, paths())
        source = Path(args.file).expanduser() if args.file else (spec.base or spec.reference)
        if source is None:
            raise ConfigError(f"{spec.id}: no scenario.base in mode.toml and no file given")
        out_dir = spec.directory / "generated"
    else:
        if not args.file:
            raise ConfigError("decompile needs either --mode <id> or a scenario file")
        source = Path(args.file).expanduser()
        if not args.out:
            raise ConfigError("decompile <file> needs --out <dir> (or use --mode <id>)")
        out_dir = Path(args.out).expanduser()

    scenario = AoE2DEScenario.from_file(str(source))
    report = decompile(scenario, out_dir, source_label=source.name, chunk_size=args.chunk_size)
    print(report.summary())
    print()
    print("Next: point the mode's build.py at generated.apply(ctx), drop scenario.base")
    print("from mode.toml, then run `aoe2modes verify <mode>` to prove the rebuild matches.")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Build a decompiled mode and prove it still matches the scenario it came from.

    Read order is load-bearing. The rebuild targets the newest scenario version, so it
    is snapshotted first; loading the older original afterwards downgrades the parser's
    global version state and would make the newer file's fields unreadable.
    """
    from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

    from aoe2modes.lib.verify import compare, snapshot

    spec = registry.get(args.mode, paths())
    original = Path(args.against).expanduser() if args.against else (spec.reference or spec.base)
    if original is None:
        raise ConfigError(
            f"{spec.id}: nothing to verify against — pass --against <file>, or keep the "
            "original as scenario.base while decompiling"
        )

    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(args.out).expanduser() if args.out else Path(tmp)
        result = build_mode(spec, out_dir=out_dir, verbose=args.verbose, xs_check=False)
        print(f"built {result.output.name}: {result.triggers} triggers, {result.units} units")

        rebuilt = snapshot(AoE2DEScenario.from_file(str(result.output)))
        source = snapshot(AoE2DEScenario.from_file(str(original)))

    report = compare(source, rebuilt)
    print(report.summary())
    return 0 if report.ok else 1


def cmd_inspect(args: argparse.Namespace) -> int:
    """Summarise an existing .aoe2scenario — the fastest way to reverse-engineer a
    published CBA Hero scenario before rebuilding it here."""
    from AoE2ScenarioParser.datasets.scenario_variant import ScenarioVariant
    from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

    toolchain.configure(verbose=args.verbose, xs_check=False)
    scenario = AoE2DEScenario.from_file(str(Path(args.file).expanduser()))

    tm, um, mm, pm = (
        scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.player_manager,
    )
    print(f"file        {args.file}")
    version = ".".join(str(part) for part in scenario.scenario_version_tuple)
    print(f"version     {version}  variant {ScenarioVariant(scenario.variant).name}")
    print(f"map         {mm.map_size}x{mm.map_size}")
    print(f"players     {pm.active_players} active")
    print(f"units       {sum(len(units) for units in um.units)}")
    print(f"triggers    {len(tm.triggers)}")
    print(f"variables   {len(tm.variables)}")

    if args.triggers:
        print()
        print(tm.get_summary_as_string())
    return 0


# --- parser ------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aoe2modes", description=__doc__)
    parser.add_argument("--version", action="version", version=f"aoe2modes {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="show parser progress output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_list = subparsers.add_parser("list", help="list every mode in modes/")
    p_list.set_defaults(func=cmd_list)

    p_info = subparsers.add_parser("info", help="show a mode's resolved configuration")
    p_info.add_argument("modes", nargs="*", help="mode ids (default: all)")
    p_info.set_defaults(func=cmd_info)

    p_build = subparsers.add_parser("build", help="build one or more modes into dist/")
    p_build.add_argument("modes", nargs="*", help="mode ids (default: all)")
    p_build.add_argument("--all", action="store_true", help="build every mode")
    p_build.add_argument("--out", help="output directory (default: dist/)")
    p_build.add_argument("--deploy", action="store_true", help="copy the result into the game folder")
    p_build.add_argument("--scenario-dir", help="override the game's scenario folder")
    p_build.add_argument("--no-xs-check", action="store_true", help="skip XS linting")
    p_build.set_defaults(func=cmd_build)

    p_deploy = subparsers.add_parser("deploy", help="copy already-built scenarios into the game folder")
    p_deploy.add_argument("modes", nargs="*", help="mode ids (default: all)")
    p_deploy.add_argument("--scenario-dir", help="override the game's scenario folder")
    p_deploy.set_defaults(func=cmd_deploy)

    p_new = subparsers.add_parser("new", help="scaffold a new mode from modes/_template")
    p_new.add_argument("mode_id", help="folder-safe id, e.g. cba_hero_blitz")
    p_new.add_argument("--name", help="display name")
    p_new.set_defaults(func=cmd_new)

    p_inspect = subparsers.add_parser("inspect", help="summarise an existing .aoe2scenario file")
    p_inspect.add_argument("file")
    p_inspect.add_argument("--triggers", action="store_true", help="also dump the trigger summary")
    p_inspect.set_defaults(func=cmd_inspect)

    p_diff = subparsers.add_parser("diff", help="structural trigger diff between two scenarios")
    p_diff.add_argument("a", help="baseline scenario")
    p_diff.add_argument("b", help="successor scenario")
    p_diff.set_defaults(func=cmd_diff)

    p_dec = subparsers.add_parser(
        "decompile", help="turn a scenario into regenerable Python under modes/<id>/generated/"
    )
    p_dec.add_argument("file", nargs="?", help="scenario to decompile (default: the mode's scenario.base)")
    p_dec.add_argument("--mode", help="mode id to write into")
    p_dec.add_argument("--out", help="output directory when not using --mode")
    p_dec.add_argument(
        "--chunk-size", type=int, default=250, help="triggers per generated part file (default: 250)"
    )
    p_dec.set_defaults(func=cmd_decompile)

    p_verify = subparsers.add_parser(
        "verify", help="rebuild a mode from source and diff it against its original scenario"
    )
    p_verify.add_argument("mode", help="mode id")
    p_verify.add_argument("--against", help="scenario to compare with (default: the mode's original)")
    p_verify.add_argument("--out", help="build directory (default: a temporary folder)")
    p_verify.set_defaults(func=cmd_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ConfigError, BuildError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
