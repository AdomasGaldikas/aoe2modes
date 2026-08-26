from __future__ import annotations

import pytest

from aoe2modes import registry, toolchain
from aoe2modes.paths import paths


@pytest.fixture(scope="session", autouse=True)
def quiet_parser():
    toolchain.configure(verbose=False, xs_check=True)


@pytest.fixture(scope="session")
def repo():
    return paths()


@pytest.fixture(scope="session")
def specs(repo):
    return registry.discover(repo)
