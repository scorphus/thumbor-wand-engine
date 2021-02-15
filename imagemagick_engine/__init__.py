#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-imagemagick-engine
# https://github.com/scorphus/thumbor-imagemagick-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>

import logging

try:
    from imagemagick_engine.engine import Engine  # NOQA
except ImportError:
    logging.warning(
        "Could not import imagemagick_engine. Probably due to setup.py installing it."
    )
