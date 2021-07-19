#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   SnakeJazz Project (https://github.com/mchalela/RandomSDSS/).
# Copyright (c) 2021, Martin Chalela
# License: MIT
#   Full Text: https://github.com/mchalela/RandomSDSS/blob/master/LICENSE

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DOCS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Sloan Digital Sky Survey data releases polygons."""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import pathlib

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DR_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

PLY_PATH = {
    "DR8": {"SDSS": DR_PATH / "dr8" / "DR8.SDSS.ply"},
    "DR9": {
        "SDSS": DR_PATH / "dr9" / "DR9.SDSS.ply",
        "BOSS": DR_PATH / "dr9" / "DR9.BOSS.ply",
    },
    "DR10": {
        "SDSS": DR_PATH / "dr10" / "DR10.SDSS.ply",
        "BOSS": DR_PATH / "dr10" / "DR10.BOSS.ply",
    },
    "DR11": {
        "SDSS": DR_PATH / "dr11" / "DR11.SDSS.ply",
        "BOSS": DR_PATH / "dr11" / "DR11.BOSS.ply",
    },
    "DR12": {
        "SDSS": DR_PATH / "dr12" / "DR12.SDSS.ply",
        "BOSS": DR_PATH / "dr12" / "DR12.BOSS.ply",
    },
    "DR13": {"SDSS": DR_PATH / "dr13" / "DR13.SDSS.ply"},
    "DR14": {
        "SDSS": DR_PATH / "dr14" / "DR14.SDSS.ply",
        "LRG_N": DR_PATH / "dr14" / "DR14.LRG_N.ply",
        "LRG_S": DR_PATH / "dr14" / "DR14.LRG_S.ply",
        "QSO_N": DR_PATH / "dr14" / "DR14.QSO_N.ply",
        "QSO_S": DR_PATH / "dr14" / "DR14.QSO_S.ply",
    },
    "DR15": {"SDSS": DR_PATH / "dr15" / "DR15.SDSS.ply"},
    "DR16": {
        "SDSS": DR_PATH / "dr16" / "DR16.SDSS.ply",
        "eBOSS": DR_PATH / "dr16" / "DR16.eBOSS.ply",
    },
}
