#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from os import path
from setuptools import setup


VERSION = "0.1.0"


def read_readme_contents():
    file_dir = path.abspath(path.dirname(__file__))
    with open(path.join(file_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


tests_require = [
    "black",
    "colorama",
    "flake8",
    "isort",
    "pytest",
    "pytest-cov",
    "pytest-mock",
    "twine",
    "wheel",
]

setup(
    name="thumbor_wand_engine",
    version=VERSION,
    description="ImageMagick imaging engine for Thumbor.",
    long_description=read_readme_contents(),
    long_description_content_type="text/markdown",
    keywords="thumbor imaging imagemagick magickwand magick wand",
    author="Pablo S. Blum de Aguiar",
    author_email="scorphus@gmail.com",
    url="https://github.com/scorphus/thumbor-wand-engine",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Environment :: Plugins",
    ],
    packages=["thumbor_wand_engine"],
    include_package_data=True,
    install_requires=[
        "thumbor",
        "Wand",
    ],
    extras_require={
        "tests": tests_require,
    },
)
