#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


try:
    from imagemagick_engine.engine import Engine  # NOQA
except ImportError:
    logging.warning(
        "Could not import imagemagick_engine. Probably due to setup.py installing it."
    )
