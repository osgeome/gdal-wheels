#!/usr/bin/env python3

import os
import platform
import sys
import glob
from setuptools import setup, Extension, find_packages

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
    
    # Add Windows-specific libraries
    libraries.extend(['ws2_32', 'crypt32'])
else:
    # Unix-specific paths and libraries
    lib_dirs = [os.path.join(gdal_home, 'lib')]
    include_dirs = [os.path.join(gdal_home, 'include')]
    libraries = ['gdal']
    extra_compile_args = ['-std=c++11']

# Get GDAL version
gdal_version = os.environ.get('GDAL_VERSION', '3.10.2').lstrip('v')

# Define the extension module
gdal_module = Extension(
    'osgeo._gdal',
    sources=['gdal_wrap.c'],
    include_dirs=include_dirs,
    library_dirs=lib_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
)

ogr_module = Extension(
    'osgeo._ogr',
    sources=['ogr_wrap.c'],
    include_dirs=include_dirs,
    library_dirs=lib_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
)

osr_module = Extension(
    'osgeo._osr',
    sources=['osr_wrap.c'],
    include_dirs=include_dirs,
    library_dirs=lib_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
)

gdalconst_module = Extension(
    'osgeo._gdalconst',
    sources=['gdalconst_wrap.c'],
    include_dirs=include_dirs,
    library_dirs=lib_dirs,
    libraries=libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
)

# Check if the SWIG-generated files exist
for source in ['gdal_wrap.c', 'ogr_wrap.c', 'osr_wrap.c', 'gdalconst_wrap.c']:
    if not os.path.exists(source):
        print(f"Warning: {source} not found. The wheel might not include all GDAL functionality.")

# Setup configuration
setup(
    name='GDAL',
    version=gdal_version,
    description='GDAL: Geospatial Data Abstraction Library',
    author='OSGeo',
    author_email='gdal-dev@lists.osgeo.org',
    url='https://gdal.org',
    license='MIT',
    packages=['osgeo'],
    ext_modules=[gdal_module, ogr_module, osr_module, gdalconst_module],
    package_data={'': ['*.dll', '*.so', '*.dylib']},
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
