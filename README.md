# GDAL Wheels

This repository contains GitHub Actions workflows for building GDAL Python wheels using Micromamba.

## Overview

The build process uses the native GDAL Python bindings from the [GDAL repository](https://github.com/OSGeo/gdal) and builds wheels for various Python versions.

## Build Process

The workflow:

1. Checks out this repository and the GDAL source code
2. Sets up a Micromamba environment with the necessary dependencies
3. Builds wheels using cibuildwheel in the GDAL source directory
4. Uploads the built wheels as artifacts and creates releases for tagged versions

## Dependencies

The build environment uses the following key dependencies:

- GDAL (from conda-forge)
- NumPy 2.0.0+ (for Python 3.9+)
- oldest-supported-numpy (for Python 3.8)
- setuptools 67.0.0+
- wheel
- cibuildwheel

## Usage

You can trigger a build manually from the GitHub Actions tab by selecting the "Build GDAL Wheels with Micromamba" workflow and providing:

- Python version (default: 3.10)
- GDAL version (default: v3.10.2)

## Documentation

For more information about GDAL Python bindings, see the [official GDAL Python documentation](https://gdal.org/api/python_bindings.html).