# XS scripting

XS is AoE2:DE's scripting language — counters, timers, scaling formulas, match state. It has no
direct access to map coordinates; anything positional stays in triggers. The bridge between the two
is a trigger variable. Language primer: <https://divy1211.github.io/AoE2DE_UGC_Guide/general/xs/beginner/>

## Why it must be embedded

DE transfers an XS file referenced by *filename* to other **players** in the lobby, but not to
spectators. A `Script Call` effect behaves differently: on load, the game moves the script body out
of every such effect into `default0.xs` — on each machine independently. That works for everyone.

So the reliable distribution path is a trigger with a `Script Call` effect, which is exactly what
`xs_manager` builds. The in-editor character limit on `Script Call` does not apply through the parser.

## xs_manager

```py
xs_manager = scenario.xs_manager

xs_manager.initialise_xs_trigger(insert_index=None)   # optional — only to control placement
xs_manager.add_script(xs_file_path="path/to/script.xs")
xs_manager.add_script(xs_string="int a = 1;")          # both kwargs may be used in one call
xs_manager.validate(xs="", xs_path="")                 # run xs-check on demand
xs_manager.validate_scenario_xs()
xs_manager.xs_trigger / xs_manager.script_name / xs_manager.xs_check
```

`add_script` creates the trigger on demand, so `initialise_xs_trigger` is only needed when you care
*where* it lands. Inserting at index 0 in a scenario with 1000+ triggers is slow.

## xs-check

`write_to_file` combines all XS present in effects and conditions and runs it through the bundled
[xs-check](https://github.com/Divy1211/xs-check) binary, printing the result. By default a failure
is reported but does **not** stop the write.

```py
scenario.xs_manager.xs_check.enabled = False
scenario.xs_manager.xs_check.raise_on_error = True        # fail the build instead of warning
scenario.xs_manager.xs_check.timeout_seconds = 120        # default 60
scenario.xs_manager.xs_check.path = "your/path/to/xs-check"
scenario.xs_manager.xs_check.allow_unsupported_versions = True
```

Errors are reported against the *combined* file, but the parser maps them back to the originating
trigger and effect:

```
XS-Check errors origins:
  ⇒ [Trigger #0] 'My Trigger With XS'
     ↳ [Effect #0] Script Call Effect
```

An XS file referenced by filename through the `XsManager` is **not** included in the check — only
scripts added via `add_script` and XS living in effects/conditions.

## Two platform gotchas

- **The bundled binary can ship without its executable bit**, and every write then fails with
  `PermissionError`. `aoe2modes.toolchain.ensure_xs_check_executable` chmods it before builds.
- **`XsManager.validate` writes its temp file with `Path.write_text(xs)` — no encoding argument.**
  On Windows that means cp1252 while xs-check expects UTF-8, so a non-ASCII character anywhere in
  the bundle surfaces as an opaque validation failure. Keep the bundled XS ASCII-only, or patch the
  write.

## Repo conventions

- XS sources live in normal `.xs` files (`xs/lib/` repo-wide, `modes/<id>/*.xs` mode-local) and are
  concatenated at build time by `aoe2modes.lib.xs.bundle_xs`.
- `${NAME}` placeholders are substituted from `ctx.set_xs_vars(...)`. A missing placeholder is an
  error, never a silent pass-through.
- Trigger variables declared in `aoe2modes.lib.variables` are mirrored as `const int VAR_*` in
  `xs/lib/util.xs`. Adding one means editing both sides.
- Division of labour: triggers own coordinates, units and one-shot effects; XS owns counters,
  timers, scaling and match state.
