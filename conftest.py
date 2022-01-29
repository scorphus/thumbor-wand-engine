#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2022, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from decimal import Decimal
from decimal import getcontext
from derpconf.config import Config
from thumbor.testing import FilterTestCase
from wand.image import Image
from wand.version import MAGICK_VERSION_INFO

import pytest


Config.allow_environment_variables()


STRICT_TESTS_SSIM_PRECISION = {
    "test_blur_filter_with_zero_radius": 2,
    "test_rotate_filter_with_invalid_value": 2,
}


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


@pytest.fixture
def get_ssim():
    def get_ssim(precision=None):
        def get_ssim(actual, expected):
            metric = "mean_absolute" if MAGICK_VERSION_INFO[0] > 6 else "mean_squared"
            _, distortion = actual.compare(expected, metric)
            if precision is not None:
                getcontext().prec = precision
            return Decimal(1) - Decimal(distortion)

        return staticmethod(get_ssim)

    return get_ssim


@pytest.fixture(autouse=True)
def auto_patch_filter_test_case_methods(mocker, request, get_ssim):
    """Monkey patch FilterTestCase's methods to use Wand instead of Pillow"""
    mocker.patch.object(FilterTestCase, "get_filtered", get_filtered)
    mocker.patch.object(FilterTestCase, "get_fixture", get_fixture)
    precision = STRICT_TESTS_SSIM_PRECISION.get(request.node.name)
    mocker.patch.object(FilterTestCase, "get_ssim", get_ssim(precision))
