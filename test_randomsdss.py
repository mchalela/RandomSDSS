#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the RandomSDSS Project
# https://github.com/mchalela/RandomSDSS
# Copyright (c) 2021, Martin Chalela
# License: MIT
# Full Text: https://github.com/mchalela/RandomSDSS/LICENSE

# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib
from unittest.mock import PropertyMock, patch

import numpy as np

from pymangle import Mangle

import pytest

import randomsdss
from randomsdss import DR, DR10, DR11, DR12, DR13, DR14, DR15, DR16, DR8, DR9

# ============================================================================
# CONSTANTS
# ============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

DR_PATH = pathlib.Path(PATH) / "randomsdss" / "data"

DRX = {
    8: DR8,
    9: DR9,
    10: DR10,
    11: DR11,
    12: DR12,
    13: DR13,
    14: DR14,
    15: DR15,
    16: DR16,
}

# ============================================================================
# TEST INITIALIZATIONS
# ============================================================================


def test_DR_invalid():
    with pytest.raises(ValueError):
        DR(dr="DR5", catalog="SDSS")


@pytest.mark.parametrize("release", range(8, 17))
def test_DR_init(release):
    dr = DR(dr=f"DR{release}", catalog="SDSS")
    assert dr.dr == f"DR{release}"
    assert dr.catalog == "SDSS"
    assert hasattr(dr, "mangle_")


@pytest.mark.parametrize("cat", ["SDSS"])
def test_DR8_init(cat):
    dr8 = DR8(cat)
    assert dr8.dr == "DR8"
    assert dr8.catalog == cat
    assert hasattr(dr8, "mangle_")

    with pytest.raises(ValueError):
        dr8 = DR8("BOSS")


@pytest.mark.parametrize("release", range(9, 13))
@pytest.mark.parametrize("cat", ["SDSS", "BOSS"])
def test_DR9to12_init(release, cat):
    dr = DRX[release](cat)
    assert dr.catalog == cat
    assert hasattr(dr, "mangle_")

    with pytest.raises(ValueError):
        DRX[release]("eBOSS")


@pytest.mark.parametrize("cat", ["SDSS"])
def test_DR13_init(cat):
    dr13 = DR13(cat)
    assert dr13.dr == "DR13"
    assert dr13.catalog == cat
    assert hasattr(dr13, "mangle_")

    with pytest.raises(ValueError):
        DR13("BOSS")


@pytest.mark.parametrize("cat", ["SDSS", "LRG_N", "LRG_S", "QSO_N", "QSO_S"])
def test_DR14_init(cat):
    dr14 = DR14(cat)
    assert dr14.dr == "DR14"
    assert dr14.catalog == cat
    assert hasattr(dr14, "mangle_")

    with pytest.raises(ValueError):
        DR14("BOSS")


@pytest.mark.parametrize("cat", ["SDSS"])
def test_DR15_init(cat):
    dr15 = DR15(cat)
    assert dr15.dr == "DR15"
    assert dr15.catalog == cat
    assert hasattr(dr15, "mangle_")

    with pytest.raises(ValueError):
        DR15("BOSS")


@pytest.mark.parametrize("cat", ["SDSS", "eBOSS"])
def test_DR16_init(cat):
    dr16 = DR16(cat)
    assert dr16.catalog == cat
    assert hasattr(dr16, "mangle_")

    with pytest.raises(ValueError):
        DR16("BOSS")


# ============================================================================
# TEST HELPER FUNCTIONS
# ============================================================================


def test_polygon_path():
    expected = DR_PATH / "dr16" / "DR16.SDSS.ply"
    path = randomsdss.polygon_path(dr="DR16", catalog="SDSS")
    assert isinstance(path, pathlib.Path)
    assert expected == path


def test_get_polygon():
    poly = randomsdss.get_polygon(dr="DR16", catalog="SDSS")
    assert isinstance(poly, Mangle)


def test_get_polygon_error():
    with patch.object(pathlib.Path, "exists", return_value=False) as exists:
        with pytest.raises(randomsdss.PolygonNotFoundError):
            randomsdss.get_polygon(dr="DR16", catalog="SDSS")
        exists.assert_called_once()


# ============================================================================
# TEST RANDOM GENERATION FUNCTIONS
# ============================================================================


@pytest.mark.parametrize("release", range(8, 17))
def test_sky_random(release):
    dr_obj = DRX[release]("SDSS")
    ra, dec = randomsdss.sky_random(dr=f"DR{release}", catalog="SDSS", size=9)
    assert len(ra) == 9
    assert len(dec) == 9
    assert np.all(dr_obj.mangle_.contains(ra, dec))


def test_z_random():
    rng = np.random.default_rng(seed=42)
    z_dist = rng.normal(0.5, 0.1, size=5_000)
    mask = z_dist > 0.4
    z_dist = z_dist[mask]

    z_rand = randomsdss.z_random(z_dist, size=1_000, seed=50)

    assert len(z_rand == 1_000)
    assert np.all(z_rand > 0.4)


# ============================================================================
# TEST WRAP OF PYMANGLE
# ============================================================================


def test_DR_sky_random():
    with patch.object(Mangle, "genrand") as method:
        dr16 = DR16()
        dr16.sky_random(1)
        method.assert_called_once_with(1)


def test_DR_box_random():
    with patch.object(Mangle, "genrand_range") as method:
        dr16 = DR16()
        dr16.box_random(150.0, 200.0, 20, 30, size=10)
        # in pymangle size is the first parameter
        method.assert_called_once_with(10, 150.0, 200.0, 20, 30)


def test_DR_contains():
    with patch.object(Mangle, "contains") as method:
        dr16 = DR16()
        dr16.contains(0.0, 0.0)
        method.assert_called_once_with(0.0, 0.0)


def test_DR_polyid_and_weight():
    with patch.object(Mangle, "polyid_and_weight") as method:
        dr16 = DR16()
        dr16.polyid_and_weight(0.0, 0.0)
        method.assert_called_once_with(0.0, 0.0)


def test_DR_polyid():
    with patch.object(Mangle, "polyid") as method:
        dr16 = DR16()
        dr16.polyid(0.0, 0.0)
        method.assert_called_once_with(0.0, 0.0)


def test_DR_weight():
    with patch.object(Mangle, "weight") as method:
        dr16 = DR16()
        dr16.weight(0.0, 0.0)
        method.assert_called_once_with(0.0, 0.0)


def test_DR_area():
    with patch.object(Mangle, "area", new_callable=PropertyMock) as method:
        dr16 = DR16()
        dr16.area
        method.assert_called_once()


def test_DR_weights():
    with patch.object(Mangle, "weights", new_callable=PropertyMock) as method:
        dr16 = DR16()
        dr16.weights
        method.assert_called_once()


def test_DR_npoly():
    with patch.object(Mangle, "npoly", new_callable=PropertyMock) as method:
        dr16 = DR16()
        dr16.npoly
        method.assert_called_once()


def test_DR_set_weights_value():
    with patch.object(Mangle, "weights", new_callable=PropertyMock) as method:
        dr16 = DR16()
        w = 0.5
        dr16.set_weights(w)

        expected = w * np.ones(dr16.npoly).reshape((1, -1))
        np.testing.assert_array_equal(expected, method.call_args[0])


def test_DR_set_weights_array():
    with patch.object(Mangle, "weights", new_callable=PropertyMock) as method:
        dr16 = DR16()
        w = 0.8 * np.ones(dr16.npoly)
        dr16.set_weights(w)

        expected = w.reshape((1, -1))
        np.testing.assert_array_equal(expected, method.call_args[0])
