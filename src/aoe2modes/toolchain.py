"""Environment fixups for AoE2ScenarioParser itself.

Three things are worth normalising before any build:

1. ``xs-check`` ships inside the wheel without the executable bit on some installs,
   which makes every write fail with ``PermissionError``. We repair it in place.
2. The parser prints a wall of progress output by default; builds are quieter without it.
3. On Windows, ``XsManager.validate`` writes the temp XS file with the platform's
   default encoding (cp1252) but ``xs-check`` expects UTF-8. The parser then reports
   a mysterious "XS validation failed" with no visible errors. We patch it here.
"""

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path

from AoE2ScenarioParser import settings
from AoE2ScenarioParser.objects.managers.xs_manager import XsManager


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


def _patch_xs_validate_encoding() -> None:
    """Force ``XsManager.validate`` to write its temp file as UTF-8.

    The default text-mode write uses ``locale.getencoding()`` which is cp1252 on
    a stock Windows install. ``xs-check`` refuses non-UTF-8 input, so validation
    silently fails on every build. Idempotent.
    """
    if getattr(XsManager.validate, "_utf8_patched", False):
        return

    def validate(self, xs: str = "", xs_path: Path | str = "") -> bool:
        if not xs and not xs_path:
            raise ValueError("Unable to validate XS without XS string or Path")
        if xs_path:
            file = xs_path if isinstance(xs_path, Path) else Path(xs_path)
            if not file.is_file():
                raise ValueError(f"File '{xs_path}' does not exist")
        else:
            _, path = tempfile.mkstemp(suffix=".xs")
            file = Path(path)
            file.write_text(xs, encoding="utf-8")
        return self.xs_check.validate(str(file.absolute()))

    validate._utf8_patched = True  # type: ignore[attr-defined]
    XsManager.validate = validate


def configure(*, verbose: bool = False, xs_check: bool = True) -> None:
    """Prepare the parser for a build run."""
    settings.PRINT_STATUS_UPDATES = verbose
    settings.NOTIFY_UNKNOWN_BYTES = verbose
    settings.SHOW_SCENARIO_VERSION_WARNINGS = False

    _patch_xs_validate_encoding()

    if xs_check and ensure_xs_check_executable():
        settings.ENABLE_XS_CHECK_INTEGRATION = True
    else:
        settings.ENABLE_XS_CHECK_INTEGRATION = False
