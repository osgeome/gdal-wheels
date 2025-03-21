#!/usr/bin/env python3

import os
import platform
import sys
from setuptools import setup, Extension

# Get GDAL installation directory from environment
gdal_home = os.environ.get('GDAL_HOME', '')
if not gdal_home:
    raise ValueError("GDAL_HOME environment variable must be set")

# Platform-specific settings
is_windows = platform.system() == 'Windows'
lib_dirs = []
include_dirs = []
libraries = []
extra_link_args = []
extra_compile_args = []

if is_windows:
    # Windows-specific paths and libraries
    lib_dirs = [
        os.path.join(gdal_home, 'lib'),
        os.path.join(os.environ.get('VCPKG_ROOT', 'C:/vcpkg'), 'installed/x64-windows/lib')
    ]
    include_dirs = [
        os.path.join(gdal_home, 'include'),
        os.path.join(os.environ.get('VCPKG_ROOT', 'C:/vcpkg'), 'installed/x64-windows/include')
    ]
    libraries = ['gdal_i']
    extra_compile_args = ['/EHsc', '/bigobj', '/MP']
else:
    # Unix-specific paths and libraries
    lib_dirs = [os.path.join(gdal_home, 'lib')]
    include_dirs = [os.path.join(gdal_home, 'include')]
    libraries = ['gdal']
    extra_compile_args = ['-std=c++11']

# Define the extension module
gdal_module = Extension(
    '_gdal',
    sources=['gdal_wrap.c'],
    include_dirs=include_dirs,
    library_dirs=lib_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
)

# Setup configuration
setup(
    name='gdal',
    version=os.environ.get('GDAL_VERSION', '3.10.2').lstrip('v'),
    description='GDAL: Geospatial Data Abstraction Library',
    author='OSGeo',
    author_email='gdal-dev@lists.osgeo.org',
    url='https://gdal.org',
    license='MIT',
    packages=['osgeo'],
    ext_modules=[gdal_module],
    py_modules=['gdal', 'ogr', 'osr', 'gdalconst'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    python_requires='>=3.9',
)
