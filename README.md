
# Random SDSS

[![PyPI version](https://badge.fury.io/py/RandomSDSS.svg)](https://badge.fury.io/py/RandomSDSS)
[![RandomSDSS](https://github.com/mchalela/RandomSDSS/actions/workflows/randomSDSS_ci.yml/badge.svg)](https://github.com/mchalela/RandomSDSS/actions/workflows/randomSDSS_ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/mchalela/RandomSDSS/badge.svg?branch=main)](https://coveralls.io/github/mchalela/RandomSDSS?branch=main)
[![Documentation Status](https://readthedocs.org/projects/randomsdss/badge/?version=latest)](https://randomsdss.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Generate random points in the Sloan Digital Sky Survey (SDSS) DR8 to DR16 footprints.

This is a small wrapper around the package pymangle that facilitates
the creation of random points in the SDSS fields. I included 
SDSS polygons for its diferent data releases (DR8 to DR16).


## Basic Usage

```python
import matplotlib.pyplot as plt
import randomsdss

dr12 = randomsdss.DR12(catalog="BOSS")
ra, dec = dr12.sky_random(size=10_000)

plt.figure()
plt.scatter(ra, dec, s=1)
plt.xlabel('RA [deg]')
plt.ylabel('DEC [deg]')
```

<p align="center">
    <img src="https://github.com/mchalela/RandomSDSS/blob/main/docs/source/_static/example.png" alt="DR12 example">
</p>

Alternatively you can get the same result without the need to 
instantiate an object using:

```python
ra, dec = randomsdss.sky_random(dr="DR12", catalog="BOSS", size=10_000)
```

If you also need a random redshift distribution you can provide a sample
of redshifts and a random set will be generated from the underlying 
Probability Density Function (PDF):

```python
z = randomsdss.z_random(z_array, size=10_000)
```

The z_random is a complementary function since does not use any information 
regarding the SDSS catalogs, only the provided redshift array.


### Author
Martin Chalela - email: tinchochalela@gmail.com
