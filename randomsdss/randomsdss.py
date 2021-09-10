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

"""Generate random points within SDSS DR8 to DR16 footprint."""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from functools import wraps

import attr

import numpy as np

from pymangle import Mangle

from scipy.stats import gaussian_kde

from .data import PLY_PATH

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXCEPTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PolygonNotFoundError(FileNotFoundError):
    """Raised when the .ply file doesn't exists."""

    pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTIONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
    """Return pymangle polygon object.

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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASSES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Base class for all Data Releases
@attr.s
class DR:
    """Base Data Release class.

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

    @property
    def area(self):
        """Get the area of the catalog."""
        return self.mangle_.area

    @property
    def npoly(self):
        """Get the number of polygons."""
        return self.mangle_.npoly

    @property
    def weights(self):
        """Array of polygons weights."""
        return self.mangle_.weights

    def set_weights(self, weights):
        """Set new weights for polygons.

        Parameters
        ----------
        weight: float or numpy.ndarray
            Poligons weights.
        """
        if np.size(weights) == 1:
            weights = np.full(self.npoly, weights)
        self.mangle_.weights = weights

    def sky_random(self, size):
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

    def box_random(self, ra_min, ra_max, dec_min, dec_max, size):
        """Generate random RA, DEC points within a box.

        Parameters
        ----------
        ra_min: float
            Right Ascension lower bound in degrees.
        ra_max: float
            Right Ascension upper bound in degrees.
        dec_min: float
            Declination lower bound in degrees.
        dec_max: float
            Declination upper bound in degrees.
        size: int
            Number of random points to generate.

        Returns
        -------
        ra: numpy.ndarray
            Right Ascension in degrees.
        dec: numpy.ndarray
            Declination in degrees.
        """
        return self.mangle_.genrand_range(
            size, ra_min, ra_max, dec_min, dec_max
        )

    def contains(self, ra, dec):
        """Check if point is inside the catalog area.

        Parameters
        ----------
        ra: numpy.ndarray
            Right Ascension in degrees.
        dec: numpy.ndarray
            Declination in degrees.

        Returns
        -------
        bool:
            True if inside, False otherwise.
        """
        return self.mangle_.contains(ra, dec)

    def polyid_and_weight(self, ra, dec):
        """Get polygon id and weight of input point.

        Parameters
        ----------
        ra: numpy.ndarray
            Right Ascension in degrees.
        dec: numpy.ndarray
            Declination in degrees.

        Returns
        -------
        pid: numpy.ndarray
            Polygon id. -1 if outside of catalog area.
        weight: numpy.ndarray
            Poligon weight. 0 if outside of catalog area.
        """
        return self.mangle_.polyid_and_weight(ra, dec)

    def polyid(self, ra, dec):
        """Get polygon id of input point.

        Parameters
        ----------
        ra: numpy.ndarray
            Right Ascension in degrees.
        dec: numpy.ndarray
            Declination in degrees.

        Returns
        -------
        pid: numpy.ndarray
            Polygon id. -1 if outside of catalog area.
        """
        return self.mangle_.polyid(ra, dec)

    def weight(self, ra, dec):
        """Get polygon weight of input point.

        Parameters
        ----------
        ra: numpy.ndarray
            Right Ascension in degrees.
        dec: numpy.ndarray
            Declination in degrees.

        Returns
        -------
        weight: numpy.ndarray
            Poligon weight. 0 if outside of catalog area.
        """
        return self.mangle_.weight(ra, dec)


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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RANDOMS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
    """Generate random redshift values following the input distribution.

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
    ra, dec = ply.sky_random(size)
    return ra, dec
