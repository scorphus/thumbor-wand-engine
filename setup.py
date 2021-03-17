#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from os import path
from setuptools import find_packages
from setuptools import setup


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
]

setup(
    name="thumbor_wand_engine",
    version="0.0.1",
    description="ImageMagick imaging engine for Thumbor.",
    long_description=read_readme_contents(),
    long_description_content_type="text/markdown",
    keywords="thumbor imaging imagemagick magickwand magick wand",
    author="Pablo S. Blum de Aguiar",
    author_email="scorphus@gmail.com",
    url="https://github.com/scorphus/thumbor-wand-engine",
    license="MIT",
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "thumbor",
        "Wand",
    ],
    extras_require={
        "tests": tests_require,
    },
)
