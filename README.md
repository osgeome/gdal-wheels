# GDAL Wheels

This repository contains GitHub Actions workflows for building GDAL Python wheels for Windows.

## Overview

The build process uses the native GDAL Python bindings from the [GDAL repository](https://github.com/OSGeo/gdal) and builds wheels for various Python versions.

## Simplified Build Process

We've created a simplified approach for building GDAL wheels on Windows:

1. Uses vcpkg for dependency management (simpler than Micromamba)
2. Direct Python setup with GitHub's built-in actions
3. Streamlined CMake configuration
4. Custom build script that handles the entire process

### Key Files

- `build_wheels.py`: A Python script that handles the entire build process
- `setup.py`: A simplified setup file for building the Python bindings
- `.github/workflows/build-wheels-simple.yml`: The GitHub Actions workflow file

## Usage

You can trigger a build manually from the GitHub Actions tab by selecting the "Build GDAL Wheels (Simple)" workflow and providing:

- Python version (default: 3.11)
- GDAL version (default: v3.10.2)

## Dependencies

The build process installs these dependencies via vcpkg:

- proj
- sqlite3
- curl
- tiff
- libpng
- jpeg
- zlib
- openssl

## Troubleshooting

### Common Issues

1. **Missing DLLs**: Make sure the PATH includes both the GDAL bin directory and the vcpkg bin directory
2. **CMake Configuration Errors**: Check that all required dependencies are properly installed via vcpkg
3. **Small Wheel Size**: If the wheel is suspiciously small (<1MB), the Python bindings weren't properly included

## Documentation

For more information about GDAL Python bindings, see the [official GDAL Python documentation](https://gdal.org/api/python_bindings.html).