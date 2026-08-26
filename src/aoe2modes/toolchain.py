"""Environment fixups for AoE2ScenarioParser itself.

Two things are worth normalising before any build:

1. ``xs-check`` ships inside the wheel without the executable bit on some installs,
   which makes every write fail with ``PermissionError``. We repair it in place.
2. The parser prints a wall of progress output by default; builds are quieter without it.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

from AoE2ScenarioParser import settings


def xs_check_binary() -> Path:
    from AoE2ScenarioParser.objects.support import xs_check

    folder = Path(xs_check.__file__).parent.parent.parent / "dependencies" / "xs-check"
    return folder / ("xs-check.exe" if os.name == "nt" else "xs-check")


def ensure_xs_check_executable() -> bool:
    """Give the bundled ``xs-check`` binary its executable bit. Returns True if usable."""
    binary = xs_check_binary()
    if not binary.is_file():
        return False
    if os.access(binary, os.X_OK):
        return True
    try:
        mode = binary.stat().st_mode
        binary.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        return False
    return os.access(binary, os.X_OK)


def configure(*, verbose: bool = False, xs_check: bool = True) -> None:
    """Prepare the parser for a build run."""
    settings.PRINT_STATUS_UPDATES = verbose
    settings.NOTIFY_UNKNOWN_BYTES = verbose

    if xs_check and ensure_xs_check_executable():
        settings.ENABLE_XS_CHECK_INTEGRATION = True
    else:
        settings.ENABLE_XS_CHECK_INTEGRATION = False
