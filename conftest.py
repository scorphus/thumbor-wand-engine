#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2022, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from derpconf.config import Config
from thumbor.testing import FilterTestCase
from wand.image import Image
from wand.version import MAGICK_VERSION_INFO

import pytest


Config.allow_environment_variables()


async def get_filtered(
    self, source_image, filter_name, params_string, config_context=None, mode="RGB"
):
    fltr = self.get_filter(filter_name, params_string, config_context)
    image = Image(filename=self.get_fixture_path(source_image))
    fltr.engine.load(image.make_blob(), ".png")
    fltr.context.transformer.img_operation_worker()
    await fltr.run()
    return fltr.engine.image


def get_fixture(self, name, mode="RGB"):
    image = Image(filename=self.get_fixture_path(name))
    return image


@staticmethod
def get_ssim(actual, expected):
    metric = "mean_absolute" if MAGICK_VERSION_INFO[0] > 6 else "mean_squared"
    _, distortion = actual.compare(expected, metric)
    return round(1 - distortion, 3)


@pytest.fixture(autouse=True)
def patch_get_filtered(mocker):
    """Mokey-patch FilterTestCase's methods to use Wand instead of Pillow"""
    mocker.patch.object(FilterTestCase, "get_filtered", get_filtered)
    mocker.patch.object(FilterTestCase, "get_fixture", get_fixture)
    mocker.patch.object(FilterTestCase, "get_ssim", get_ssim)
