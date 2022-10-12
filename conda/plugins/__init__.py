# -*- coding: utf-8 -*-
# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations
from typing import Callable, NamedTuple, Optional
from collections.abc import Iterable

import pluggy

_hookspec = pluggy.HookspecMarker("conda")
register = pluggy.HookimplMarker("conda")


class CondaSubcommand(NamedTuple):
    """
    Conda subcommand entry.

    :param name: Subcommand name (e.g., ``conda my-subcommand-name``).
    :param summary: Subcommand summary, will be shown in ``conda --help``.
    :param action: Callable that will be run when the subcommand is invoked.
    """
    name: str
    summary: str
    action: Callable[
        [list[str]],  # arguments
        Optional[int],  # return code
    ]


@_hookspec
def conda_subcommands() -> Iterable[CondaSubcommand]:
    """
    Register external subcommands in conda.

    :return: An iterable of subcommand entries.
    """


class CondaSolver(NamedTuple):
    """
    Conda solver.

    :param name: Subcommand name (e.g., ``conda my-subcommand-name``).
    :param backend: Callable that will instantiated as the solver backend.
    """
    name: str
    backend: Callable[
        [list[str]],  # arguments
        Optional[int],  # return code
    ]


@_hookspec
def conda_solvers() -> Iterable[CondaSolver]:
    """
    Register external solvers in conda.

    :return: An iterable of solvers entries.
    """
