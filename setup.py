#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


tests_require = [
    "black",
    "colorama",
    "flake8",
    "isort",
    "pytest",
    "pytest-cov",
]

setup(
    name="imagemagick engine",
    version="0.0.1",
    description="ImageMagick imaging engine for Thumbor.",
    long_description="""
ImageMagick imaging engine for Thumbor.
""",
    keywords="thumbor imaging imagemagick",
    author="https://github.com/scorphus",
    author_email="scorphus@gmail.com",
    url="",
    license="MIT",
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "thumbor>=7.0.0a1",
        "Wand==0.6.*,>=0.6.3",
    ],
    extras_require={
        "tests": tests_require,
    },
)
