#!/usr/bin/env python
import io
from setuptools import setup
from distutils.extension import Extension

long_description = io.open('README.rst', encoding='utf-8').read()

setup(
    py_modules=['pyjq'],
    test_suite='test_pyjq',
    ext_modules=[Extension("_pyjq", ["_pyjq.c"], libraries=["jq"])],

    name='pyjq',
    version='1.0',
    description='Binding for jq JSON processor.',
    long_description=long_description,
    author='OMOTO Kenji',
    url='http://github.com/doloopwhile/pyjq',
    license='MIT License',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: JavaScript',
    ],
)
