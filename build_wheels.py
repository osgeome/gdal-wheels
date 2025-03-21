#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import platform
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return its output"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=True, text=True, 
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout)
    return result.stdout

def setup_environment():
    """Setup environment variables for the build"""
    # Get GDAL source and installation directories
    gdal_source = os.environ.get('GDAL_SOURCE', os.path.join(os.getcwd(), 'gdal-source'))
    gdal_install = os.environ.get('GDAL_HOME', os.path.join(gdal_source, 'install'))
    
    # Set environment variables
    os.environ['GDAL_HOME'] = gdal_install
    os.environ['GDAL_DATA'] = os.path.join(gdal_install, 'share', 'gdal')
    
    if platform.system() == 'Windows':
        # Windows-specific environment variables
        vcpkg_root = os.environ.get('VCPKG_ROOT', 'C:/vcpkg')
        os.environ['PROJ_LIB'] = os.path.join(vcpkg_root, 'installed/x64-windows/share/proj')
        
        # Add GDAL and vcpkg binaries to PATH
        path = os.environ.get('PATH', '')
        os.environ['PATH'] = f"{os.path.join(gdal_install, 'bin')};{os.path.join(vcpkg_root, 'installed/x64-windows/bin')};{path}"
    
    return gdal_source, gdal_install

def build_gdal(gdal_source, gdal_install):
    """Build GDAL from source"""
    build_dir = os.path.join(gdal_source, 'build')
    
    # Create build directory if it doesn't exist
    os.makedirs(build_dir, exist_ok=True)
    
    # Configure and build GDAL
    if platform.system() == 'Windows':
        # Windows-specific build commands
        cmake_cmd = [
            'cmake', '..',
            '-G', 'Visual Studio 17 2022', '-A', 'x64',
            f'-DCMAKE_INSTALL_PREFIX={gdal_install}',
            '-DBUILD_SHARED_LIBS=ON',
            '-DBUILD_PYTHON_BINDINGS=ON',
            '-DGDAL_USE_JPEG=ON',
            '-DGDAL_USE_PNG=ON',
            '-DGDAL_USE_ZLIB=ON',
            '-DGDAL_USE_CURL=ON',
            '-DGDAL_USE_CRYPTO=ON',
            '-DGDAL_USE_OPENSSL=ON',
            '-DACCEPT_MISSING_SQLITE3_RTREE=ON'
        ]
        
        # Add vcpkg toolchain file if available
        vcpkg_root = os.environ.get('VCPKG_ROOT', 'C:/vcpkg')
        toolchain_file = os.path.join(vcpkg_root, 'scripts/buildsystems/vcpkg.cmake')
        if os.path.exists(toolchain_file):
            cmake_cmd.extend(['-DCMAKE_TOOLCHAIN_FILE=' + toolchain_file])
        
        run_command(cmake_cmd, cwd=build_dir)
        run_command(['cmake', '--build', '.', '--config', 'Release'], cwd=build_dir)
        run_command(['cmake', '--install', '.', '--config', 'Release'], cwd=build_dir)
    else:
        # Unix-specific build commands
        run_command([
            'cmake', '..',
            f'-DCMAKE_INSTALL_PREFIX={gdal_install}',
            '-DBUILD_SHARED_LIBS=ON',
            '-DBUILD_PYTHON_BINDINGS=ON',
            '-DGDAL_USE_JPEG=ON',
            '-DGDAL_USE_PNG=ON',
            '-DGDAL_USE_ZLIB=ON',
            '-DGDAL_USE_CURL=ON',
            '-DGDAL_USE_CRYPTO=ON',
            '-DGDAL_USE_OPENSSL=ON',
            '-DACCEPT_MISSING_SQLITE3_RTREE=ON'
        ], cwd=build_dir)
        run_command(['cmake', '--build', '.'], cwd=build_dir)
        run_command(['cmake', '--install', '.'], cwd=build_dir)

def build_wheel(gdal_source):
    """Build Python wheel for GDAL"""
    # Directory containing Python bindings
    python_dir = os.path.join(gdal_source, 'swig', 'python')
    
    # Build the wheel
    run_command(['pip', 'install', '--upgrade', 'pip', 'wheel', 'setuptools', 'numpy'], cwd=python_dir)
    run_command(['pip', 'wheel', '.', '-w', '../../../wheelhouse'], cwd=python_dir)

def main():
    """Main function"""
    # Setup environment
    gdal_source, gdal_install = setup_environment()
    
    # Create wheelhouse directory
    wheelhouse = os.path.join(os.getcwd(), 'wheelhouse')
    os.makedirs(wheelhouse, exist_ok=True)
    
    # Build GDAL
    build_gdal(gdal_source, gdal_install)
    
    # Build wheel
    build_wheel(gdal_source)
    
    # Verify wheel
    wheels = list(Path(wheelhouse).glob('*.whl'))
    if not wheels:
        print("Error: No wheel was built")
        sys.exit(1)
    
    for wheel in wheels:
        size_mb = wheel.stat().st_size / (1024 * 1024)
        print(f"Built wheel: {wheel.name} ({size_mb:.2f} MB)")
        if size_mb < 1:
            print(f"Warning: Wheel size is suspiciously small ({size_mb:.2f} MB)")

if __name__ == '__main__':
    main()
