#!/usr/bin/env python
import platform

from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension


libraries = ["jq", "onig"]
if platform.architecture()[1] == "WindowsPE":
    libraries.append("shlwapi")

pyjq = Extension(
    "_pyjq",
    sources=["_pyjq.pyx"],
    libraries=libraries,
)

setup(
    ext_modules=cythonize([pyjq]),
    py_modules=["pyjq"],
)
