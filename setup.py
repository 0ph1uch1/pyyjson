import os
import platform
import subprocess
import sys

from setuptools import Extension, setup  # type: ignore
from setuptools.command.build_ext import build_ext  # type: ignore


class CMakeExtension(Extension):
    def __init__(self, name, cmake_lists_dir='.', **kwargs):
        Extension.__init__(self, name, sources=[], **kwargs)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)


class cmake_build_ext(build_ext):
    def build_extensions(self):
        # Ensure that CMake is present and working
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        for ext in self.extensions:
            ext_fullpath = self.get_ext_fullpath(ext.name)
            extdir = os.path.abspath(os.path.dirname(ext_fullpath))
            # cfg = 'Debug' if options['--debug'] == 'ON' else 'Release'
            cfg = 'Release'
            py_executable = sys.executable

            cmake_args = [
                f'-DCMAKE_BUILD_TYPE={cfg}',
                f'-DCMAKE_INSTALL_PREFIX={extdir}',
                f'-DPython_ROOT_DIR={os.path.dirname(os.path.dirname(os.path.dirname(os.__file__)))}',
                f'-DPYTHON_EXECUTABLE={py_executable}',
            ]

            # We can handle some platform-specific settings at our discretion
            if platform.system() == 'Windows':
                plat = ('x64' if platform.architecture()[0] == '64bit' else 'Win32')
                # cmake_args += [
                # These options are likely to be needed under Windows
                # '-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE',
                # '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
                # ]
                # Assuming that Visual Studio and MinGW are supported compilers
                if self.compiler.compiler_type == 'msvc':
                    cmake_args += [
                        f'-DCMAKE_GENERATOR_PLATFORM={plat}',
                    ]
                else:
                    cmake_args += [
                        '-G', 'MinGW Makefiles',
                    ]
            # cmake_args += cmake_cmd_args

            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            # Config
            subprocess.check_call(['cmake', ext.cmake_lists_dir] + cmake_args,
                                  cwd=self.build_temp)

            # Build
            subprocess.check_call(['cmake', '--build', '.', '--config', cfg, '--target', 'install'],
                                  cwd=self.build_temp)

            # rename
            if platform.system() != 'Windows':
                os.rename(os.path.join(extdir, 'pyyjson.so'), ext_fullpath)
            else:
                os.rename(os.path.join(extdir, 'bin/pyyjson.dll'), ext_fullpath)


with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="pyyjson",
    version="0.9.0",
    url='https://github.com/0ph1uch1/pyyjson',
    project_urls={
        'Bug Tracker': 'https://github.com/0ph1uch1/pyyjson/issues',
        'Source Code': 'https://github.com/0ph1uch1/pyyjson',
    },
    description='yyjson for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    ext_modules=[
        CMakeExtension(name="pyyjson")
    ],
    cmdclass=dict(build_ext=cmake_build_ext)
)
