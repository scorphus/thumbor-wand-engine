#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from os.path import abspath
from os.path import dirname
from os.path import join
from parameterized import parameterized
from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine as PileEngine
from thumbor_wand_engine.engine import Engine
from unittest import TestCase
from unittest.mock import Mock
from wand.image import IMAGE_TYPES


(
    UNDEFINED_TYPE,
    BILEVEL_TYPE,
    GRAYSCALE_TYPE,
    GRAYSCALEALPHA_TYPE,
    PALETTE_TYPE,
    PALETTEALPHA_TYPE,
    TRUECOLOR_TYPE,
    TRUECOLORALPHA_TYPE,
    COLORSEPARATION_TYPE,
    COLORSEPARATIONALPHA_TYPE,
    OPTIMIZE_TYPE,
    PALETTEBILEVELALPHA_TYPE,
) = IMAGE_TYPES


STORAGE_PATH = abspath(join(dirname(__file__), "../thumbor_tests/fixtures/images/"))


class WandEngineTestCase(TestCase):
    def get_context(self):
        cfg = Config(
            SECURITY_KEY="ACME-SEC",
            ENGINE="thumbor_wand_engine",
            IMAGE_METADATA_READ_FORMATS="exif,xmp",
        )
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = STORAGE_PATH
        cfg.STORAGE = "thumbor.storages.no_storage"
        return Context(config=cfg)

    def setUp(self):
        self.context = self.get_context()

    def test_create_engine(self):
        engine = Engine(self.context)
        assert isinstance(engine, Engine)

    def test_create_image(self):
        engine = Engine(self.context)
        with open(join(STORAGE_PATH, "image.jpg"), "rb") as image_file:
            buffer = image_file.read()
        engine.load(buffer, None)
        assert engine.image.format == "JPEG"

    def test_create_image_16bit_per_channel_lsb(self):
        engine = Engine(self.context)
        with open(
            join(STORAGE_PATH, "gradient_lsb_16bperchannel.tif"), "rb"
        ) as image_file:
            buffer = image_file.read()
        assert buffer is not None
        engine.load(buffer, None)
        assert engine.image.format == "TIFF"
        assert engine.image.size == (100, 100)

    def test_load_tif_8bit_per_channel(self):
        engine = Engine(self.context)
        with open(join(STORAGE_PATH, "gradient_8bit.tif"), "rb") as image_file:
            buffer = image_file.read()
        assert buffer is not None
        engine.load(buffer, None)
        assert engine.image.format == "TIFF"
        assert engine.image.size == (100, 100)

    def test_set_image_data_JPG(self):
        engine = Engine(self.context)
        with open(join(STORAGE_PATH, "image.jpg"), "rb") as image_file:
            buffer = image_file.read()
        assert buffer is not None
        engine.load(buffer, None)
        _, data = engine.image_data_as_rgb()
        engine.set_image_data(data)
        assert engine.image.format == "JPEG"
        assert engine.image.size == (300, 400)

    def test_set_image_data_PNG(self):
        engine = Engine(self.context)
        with open(join(STORAGE_PATH, "1bit.png"), "rb") as image_file:
            buffer = image_file.read()
        assert buffer is not None
        engine.load(buffer, None)
        _, data = engine.image_data_as_rgb()
        engine.set_image_data(data)
        assert engine.image.format == "PNG"
        assert engine.image.size == (691, 212)

    def test_compare_image_data_and_mode(self):
        engine = Engine(self.context)
        pil_engine = PileEngine(self.context)
        with open(join(STORAGE_PATH, "1bit.png"), "rb") as image_file:
            buffer = image_file.read()
        assert buffer is not None
        engine.load(buffer, ".png")
        pil_engine.load(buffer, ".png")
        pil_mode, pil_data = pil_engine.image_data_as_rgb()
        mode, data = engine.image_data_as_rgb()
        assert mode == pil_mode
        assert len(data) == len(pil_data)
        assert data[:100] == pil_data[:100]
        assert data[-100:] == pil_data[-100:]

    def test_get_and_set_image_data(self):
        engine = Engine(self.context)
        with open(join(STORAGE_PATH, "1bit.png"), "rb") as image_file:
            buffer = image_file.read()
        assert buffer is not None
        engine.load(buffer, ".png")
        _, data_before = engine.image_data_as_rgb()
        engine.set_image_data(data_before)
        _, data_after = engine.image_data_as_rgb()
        assert len(data_before) == len(data_after)
        assert data_before[:100] == data_after[:100]
        assert data_before[-100:] == data_after[-100:]

    @parameterized.expand(
        [
            (UNDEFINED_TYPE, "RGB"),
            (BILEVEL_TYPE, "RGB"),
            (GRAYSCALE_TYPE, "RGB"),
            (GRAYSCALEALPHA_TYPE, "RGBA"),
            (PALETTE_TYPE, "RGB"),
            (PALETTEALPHA_TYPE, "RGBA"),
            (TRUECOLOR_TYPE, "RGB"),
            (TRUECOLORALPHA_TYPE, "RGBA"),
            (COLORSEPARATION_TYPE, "RGB"),
            (COLORSEPARATIONALPHA_TYPE, "RGBA"),
            (OPTIMIZE_TYPE, "RGB"),
            (PALETTEBILEVELALPHA_TYPE, "RGBA"),
        ],
    )
    def test_get_image_mode(self, image_type, expected_mode):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        assert engine.get_image_mode() == expected_mode

    @parameterized.expand(
        [
            (UNDEFINED_TYPE, GRAYSCALE_TYPE),
            (BILEVEL_TYPE, GRAYSCALE_TYPE),
            (GRAYSCALE_TYPE, GRAYSCALE_TYPE),
            (GRAYSCALEALPHA_TYPE, GRAYSCALEALPHA_TYPE),
            (PALETTE_TYPE, GRAYSCALE_TYPE),
            (PALETTEALPHA_TYPE, GRAYSCALEALPHA_TYPE),
            (TRUECOLOR_TYPE, GRAYSCALE_TYPE),
            (TRUECOLORALPHA_TYPE, GRAYSCALEALPHA_TYPE),
            (COLORSEPARATION_TYPE, GRAYSCALE_TYPE),
            (COLORSEPARATIONALPHA_TYPE, GRAYSCALEALPHA_TYPE),
            (OPTIMIZE_TYPE, GRAYSCALE_TYPE),
            (PALETTEBILEVELALPHA_TYPE, GRAYSCALEALPHA_TYPE),
        ],
    )
    def test_convert_to_grayscale(self, image_type, expected_type):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        image = engine.convert_to_grayscale()
        assert engine.image.type == image.type == expected_type

    def test_convert_to_grayscale_update_image_false(self):
        image_type, expected_type = TRUECOLOR_TYPE, GRAYSCALE_TYPE
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        image = engine.convert_to_grayscale(update_image=False)
        assert image.type == expected_type
        assert engine.image.type != expected_type

    @parameterized.expand(IMAGE_TYPES)
    def test_convert_to_grayscale_alpha_false(self, image_type):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        image = engine.convert_to_grayscale(alpha=False)
        assert engine.image.type == image.type == GRAYSCALE_TYPE

    @parameterized.expand(IMAGE_TYPES)
    def test_enable_alpha(self, image_type):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        engine.enable_alpha()
        assert engine.image.type == TRUECOLORALPHA_TYPE

    def test_can_create_image_from_buffer(self):
        engine = Engine(self.context)
        with open(join(STORAGE_PATH, "paletted-transparent.png"), "rb") as image_file:
            buffer = image_file.read()
        engine.load(buffer, ".png")
        assert engine.image.format == "PNG"
        assert engine.image.type == TRUECOLORALPHA_TYPE
        assert engine.image.colors <= 256

    @parameterized.expand(
        [
            ("paletted-transparent.png", "PNG"),
            ("image.jpg", "JPEG"),
            ("image.webp", "WEBP"),
            ("image.webp", "WEBP"),
            ("animated.gif", "GIF"),
            ("gradient_8bit.tif", "TIFF"),
            ("Commons-logo.svg", "PNG"),  # `BaseEngine.load` converts SVG to PNG
        ]
    )
    def test_can_create_image_from_buffer_extension_none(
        self, image_file, expected_format
    ):
        engine = Engine(self.context)
        with open(join(STORAGE_PATH, image_file), "rb") as image_file:
            buffer = image_file.read()
        engine.load(buffer, None)
        assert engine.image.format == expected_format


class WandEngineTransformationsTestCase(TestCase):
    def setUp(self):
        self.engine = Engine({})
        self.engine.image = Mock()

    def test_flip_vertically(self):
        self.engine.flip_vertically()
        self.engine.image.flip.assert_called_once_with()

    def test_flip_horizontally(self):
        self.engine.flip_horizontally()
        self.engine.image.flop.assert_called_once_with()

    def test_crop(self):
        self.engine.crop(1.0, 2.0, 3.0, 4.0)
        self.engine.image.crop.assert_called_once_with(left=1, top=2, right=3, bottom=4)

    def test_resize(self):
        self.engine.resize(1.0, 2.0)
        self.engine.image.resize.assert_called_once_with(1, 2)
