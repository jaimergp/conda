# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
import functools

import pluggy

from . import solvers, specs


# FUTURE: Python 3.9+, replace w/ functools.cache
@functools.lru_cache(maxsize=None)
def get_plugin_manager():
    pm = pluggy.PluginManager("conda")
    pm.register(solvers)
    pm.add_hookspecs(specs)
    pm.load_setuptools_entrypoints("conda")
    return pm
