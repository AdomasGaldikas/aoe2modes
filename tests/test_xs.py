from __future__ import annotations

import pytest

from aoe2modes.lib.xs import XsError, read_xs, substitute


def test_substitutes_placeholders():
    assert substitute("const int N = ${COUNT};", {"COUNT": 8}) == "const int N = 8;"


def test_missing_placeholder_is_an_error():
    with pytest.raises(XsError, match="WAVE_INTERVAL"):
        substitute("int i = ${WAVE_INTERVAL};", {})


def test_source_without_placeholders_is_untouched():
    source = "void main() {}\n"
    assert substitute(source, {}) == source


def test_read_xs_reports_missing_file(tmp_path):
    with pytest.raises(XsError, match="not found"):
        read_xs(tmp_path / "nope.xs")


def test_shared_libs_have_no_placeholders(repo):
    for path in sorted(repo.shared_xs.rglob("*.xs")):
        # Shared libraries are included by every mode, so they must not depend on
        # per-mode build variables.
        read_xs(path)
