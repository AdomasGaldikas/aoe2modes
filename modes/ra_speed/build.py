"""RA's maintained map/rules with an isolated teammate-loss Speed Rush layer."""

from dataclasses import replace

from aoe2modes import registry
from aoe2modes.builder import _load_build_module

from .rush import configure_speed_rush


def build(ctx):
    base = registry.get("evolution_alpha", ctx.repo)
    if ctx.spec.map != base.map or ctx.spec.players != base.players:
        raise ValueError("Speed must use the normal RA map and player settings")
    shared = _load_build_module(base)
    # Read the shared hero roster from RA's config, keeping Speed's own name/version.
    # The managers, XS chunks and substitution dict remain the same shared objects.
    shared.build(replace(ctx, spec=replace(ctx.spec, directory=base.directory)))
    units = {unit for row in shared.CIV_SPAWN_RULES.values()
             for unit in shared._unit_family(row[0])}
    configure_speed_rush(ctx, units, shared)
