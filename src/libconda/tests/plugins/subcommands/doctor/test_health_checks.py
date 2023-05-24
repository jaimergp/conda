# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Iterable

import pytest

from conda.base.context import conda_tests_ctxt_mgmt_def_pol
from conda.common.io import env_vars
from conda.plugins.subcommands.doctor.health_checks import (
    display_health_checks,
    find_packages_with_missing_files,
)
from conda.testing.integration import make_temp_env


@pytest.fixture
def env_ok(tmp_path: Path) -> Iterable[tuple[Path, str, str, str]]:
    """Fixture that returns a testing environment with no missing files"""
    package = uuid.uuid4().hex

    (tmp_path / "bin").mkdir(parents=True, exist_ok=True)
    (tmp_path / "lib").mkdir(parents=True, exist_ok=True)
    (tmp_path / "conda-meta").mkdir(parents=True, exist_ok=True)

    bin_doctor = f"bin/{package}"
    (tmp_path / bin_doctor).touch()

    lib_doctor = f"lib/{package}.py"
    (tmp_path / lib_doctor).touch()

    (tmp_path / "conda-meta" / f"{package}.json").write_text(
        json.dumps({"files": [bin_doctor, lib_doctor]})
    )

    yield tmp_path, bin_doctor, lib_doctor, package


@pytest.fixture
def env_broken(env_ok: tuple[Path, str, str, str]) -> tuple[Path, str, str, str]:
    """Fixture that returns a testing environment with missing files"""
    prefix, bin_doctor, _, _ = env_ok
    (prefix / bin_doctor).unlink()
    return env_ok


def test_no_missing_files(env_ok: tuple[Path, str, str, str]):
    """Test that runs for the case with no missing files"""
    prefix, _, _, _ = env_ok
    assert find_packages_with_missing_files(prefix) == {}


def test_missing_files(env_broken: tuple[Path, str, str, str]):
    prefix, bin_doctor, _, package = env_broken
    assert find_packages_with_missing_files(prefix) == {package: [bin_doctor]}


@pytest.mark.parametrize("verbose", [True, False])
def test_display_health_checks(env_ok: tuple[Path, str, str, str], verbose: bool):
    """Run display_health_checks without and with missing files."""
    prefix, bin_doctor, lib_doctor, package = env_ok
    with env_vars(
        {"CONDA_PREFIX": prefix},
        stack_callback=conda_tests_ctxt_mgmt_def_pol,
    ):
        display_health_checks(prefix, verbose=verbose)
        (prefix / bin_doctor).unlink()
        display_health_checks(prefix, verbose=verbose)
