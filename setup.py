#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the RandomSDSS Project
# https://github.com/mchalela/RandomSDSS
# Copyright (c) 2021, Martin Chalela
# License: MIT
# Full Text: https://github.com/mchalela/RandomSDSS/LICENSE


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DOCS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""Distribution and installation of RandomSDSS."""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import pathlib

from ez_setup import use_setuptools

from setuptools import setup

use_setuptools()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

REQUIREMENTS = ["attrs", "numpy", "pymangle", "scipy"]

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

with open(PATH / "README.md") as fp:
    LONG_DESCRIPTION = fp.read()

with open(PATH / "randomsdss" / "__init__.py") as fp:
    for line in fp.readlines():
        if line.startswith("__version__ = "):
            VERSION = line.split("=", 1)[-1].replace('"', "").strip()
            break

DESCRIPTION = "Generate random points within SDSS DR8 to DR16 footprint."

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def do_setup():
    setup(
        name="randomsdss",
        version=VERSION,
        description=DESCRIPTION,
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        author=["Martin Chalela"],
        author_email="tinchochalela@gmail.com",
        url="https://github.com/mchalela/RandomSDSS",
        py_modules=["ez_setup"],
        packages=[
            "randomsdss",
            "randomsdss.data",
        ],
        include_package_data=True,
        license="MIT",
        keywords=["random", "sdss", "sky", "pymangle", "mangle"],
        classifiers=[
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.9",
        ],
        install_requires=REQUIREMENTS,
    )


if __name__ == "__main__":
    do_setup()
