#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the RandomSDSS Project
# https://github.com/mchalela/RandomSDSS
# Copyright (c) 2021, Martin Chalela
# License: MIT
# Full Text: https://github.com/mchalela/RandomSDSS/LICENSE

# ============================================================================
# DOCS
# ============================================================================

"""Generate random points within SDSS DR8 to DR16 footprint."""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib
from functools import wraps

import attr

import numpy as np

from pymangle import Mangle

from scipy.stats import gaussian_kde


# ============================================================================
# CONSTANTS
# ============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

DR_PATH = pathlib.Path(PATH) / "data"

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

# ============================================================================
# EXCEPTIONS
# ============================================================================


class PolygonNotFoundError(FileNotFoundError):
    """Raised when the .ply file doesn't exists."""

    pass


# ============================================================================
# FUNCTIONS
# ============================================================================


def validate_path(method):
    """Check the requested catalog is available."""

    @wraps(method)
    def wrapper(dr, catalog):
        if not (dr in PLY_PATH.keys()):
            raise ValueError(
                f"There is no polygon file for data release {dr}."
            )
        if not (catalog in PLY_PATH[dr].keys()):
            raise ValueError(
                f"There is no polygon file for catalog {catalog} in {dr}."
            )
        return method(dr, catalog)

    return wrapper


@validate_path
def polygon_path(dr, catalog):
    """Return polygon path.

    Parameters
    ----------
    dr: str
        Data Release name: e.g DR16.
    catalog: str
        Catalog name within the specified data release: e.g. BOSS.

    Return
    ------
    path: pathlib.Path
        Object representig the path.
    """
    path = PLY_PATH.get(dr).get(catalog)
    return path


def get_polygon(dr, catalog):
    """Return polygon path.

    Parameters
    ----------
    dr: str
        Data Release name: e.g DR16.
    catalog: str
        Catalog name within the specified data release: e.g. BOSS.

    Return
    ------
    mangle: pymangle.Mangle
        Mangle instance with the polygon information.
    """
    path = polygon_path(dr, catalog)
    if not path.exists():
        raise PolygonNotFoundError(
            f"Polygon file not found. Should be at {path}."
        )
    return Mangle(str(path))


# ============================================================================
# CLASSES
# ============================================================================

# Base class for all Data Releases
@attr.s
class DR:
    """Return polygon path.

    Parameters
    ----------
    dr: str
        Data Release name: e.g DR16.
    catalog: str
        Catalog name within the specified data release: e.g. BOSS.
    """

    dr = attr.ib()
    catalog = attr.ib()

    def __attrs_post_init__(self):
        """Call get_polygon here to ensure self is instantiated."""
        self.mangle_ = get_polygon(self.dr, self.catalog)

    def random(self, size):
        """Generate random RA, DEC points.

        Parameters
        ----------
        size: int
            Number of random points to generate.

        Returns
        -------
        ra: numpy.ndarray
            Right Ascension in degrees.
        dec: numpy.ndarray
            Declination in degrees.
        """
        return self.mangle_.genrand(size)


# One class for each Data Relese
def subclass_as(name):
    """Shortcut to create subclasses of DR.

    Parameters
    ----------
    name: str
        Data Release name: e.g DR16.

    Return
    ------
    DR: randomsdss.DR
        Subclass object of DR with the specified data release.
    """
    attrib_dict = {
        "dr": attr.ib(default=name, init=False, repr=False),
        "catalog": attr.ib(default="SDSS"),
    }
    return attr.make_class(name, attrib_dict, bases=(DR,))


DR8 = subclass_as("DR8")
DR9 = subclass_as("DR9")
DR10 = subclass_as("DR10")
DR11 = subclass_as("DR11")
DR12 = subclass_as("DR12")
DR13 = subclass_as("DR13")
DR14 = subclass_as("DR14")
DR15 = subclass_as("DR15")
DR16 = subclass_as("DR16")


# ============================================================================
# RANDOMS
# ============================================================================


def _random_from_pdf(pdf, x_grid, size, seed=None):
    """Generate random numbers from a Probability Distribution Function."""
    cdf = np.cumsum(pdf)
    cdf /= cdf[-1]
    # randoms
    rng = np.random.default_rng(seed)
    urand = rng.random(size)
    bins = np.searchsorted(cdf, urand)
    return x_grid[bins]


def z_random(z, size=10_000, weights=None, seed=None):
    """Generate random redshift values following the input redshift distribution.

    This function uses scipy.stats.gaussian_kde to compute the Probability
    Density Distribution (PDF).

    Parameters
    ----------
    z: numpy.ndarray
        Redhisft sample to generate a PDF and extract random points.
    size: int
        Number of random points to generate.
    weights: numpy.ndarray
        Weigths of each redshift value to compute a weigthed PDF.
    seed: int
        Set random seed.

    Return
    ------
    z_rand: numpy.ndarray
        Random redshifts.
    """
    z_grid = np.linspace(z.min(), z.max(), size)
    kde = gaussian_kde(z, weights=weights)
    pdf = kde(z_grid)
    z_rand = _random_from_pdf(pdf, z_grid, size, seed)
    return z_rand


def sky_random(dr="DR16", catalog="SDSS", size=10_000):
    """Generate random RA, DEC values within the specified DR and catalog.

    Parameters
    ----------
    dr: str
        Data Release name: e.g DR16.
    catalog: str
        Catalog name within the specified data release: e.g. BOSS.
    size: int
        Number of random points to generate.

    Return
    ------
    ra: numpy.ndarray
        Right Ascension in degrees.
    dec: numpy.ndarray
        Declination in degrees.
    """
    ply = DR(dr=dr, catalog=catalog)
    ra, dec = ply.random(size)
    return ra, dec
