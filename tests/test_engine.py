#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from io import BytesIO
from os.path import abspath
from os.path import dirname
from os.path import join
from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine as PileEngine
from thumbor_wand_engine.engine import Engine
from unittest.mock import MagicMock
from wand.color import Color
from wand.image import IMAGE_TYPES
from wand.image import ORIENTATION_TYPES

import pytest


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


def get_context():
    cfg = Config(
        SECURITY_KEY="ACME-SEC",
        ENGINE="thumbor_wand_engine",
        IMAGE_METADATA_READ_FORMATS="exif,xmp",
    )
    cfg.LOADER = "thumbor.loaders.file_loader"
    cfg.FILE_LOADER_ROOT_PATH = STORAGE_PATH
    cfg.STORAGE = "thumbor.storages.no_storage"
    return Context(config=cfg)


@pytest.fixture
def engine():
    return Engine(get_context())


@pytest.fixture
def green_engine(engine):
    engine.image = engine.gen_image((1, 1), "green")
    return engine


@pytest.fixture
def green_image(green_engine, mocker):
    return mocker.spy(green_engine, "image")


@pytest.fixture
def transp_engine(engine):
    with open(join(STORAGE_PATH, "paletted-transparent.png"), "rb") as image_file:
        buffer = image_file.read()
    engine.load(buffer, "png")
    return engine


@pytest.fixture
def transp_pixels(transp_engine):
    return sum(a == 0 for a in transp_engine.image.export_pixels()[3::4])


def test_gen_image(engine):
    size = 179, 359
    green_image = engine.gen_image(size, "green")
    assert green_image.size == size
    assert Color("green") in green_image.histogram
    assert green_image.histogram[Color("green")] == size[0] * size[1]


def test_create_image(engine):
    with open(join(STORAGE_PATH, "image.jpg"), "rb") as image_file:
        buffer = image_file.read()
    engine.load(buffer, None)
    assert engine.image.format == "JPEG"


def test_create_image_16bit_per_channel_lsb(engine):
    with open(join(STORAGE_PATH, "gradient_lsb_16bperchannel.tif"), "rb") as image_file:
        buffer = image_file.read()
    assert buffer is not None
    engine.load(buffer, None)
    assert engine.image.format == "TIFF"
    assert engine.image.size == (100, 100)


def test_load_tif_8bit_per_channel(engine):
    with open(join(STORAGE_PATH, "gradient_8bit.tif"), "rb") as image_file:
        buffer = image_file.read()
    assert buffer is not None
    engine.load(buffer, None)
    assert engine.image.format == "TIFF"
    assert engine.image.size == (100, 100)


def test_set_image_data_JPG(engine):
    with open(join(STORAGE_PATH, "image.jpg"), "rb") as image_file:
        buffer = image_file.read()
    assert buffer is not None
    engine.load(buffer, None)
    _, data = engine.image_data_as_rgb()
    engine.set_image_data(data)
    assert engine.image.format == "JPEG"
    assert engine.image.size == (300, 400)


def test_set_image_data_PNG(engine):
    with open(join(STORAGE_PATH, "1bit.png"), "rb") as image_file:
        buffer = image_file.read()
    assert buffer is not None
    engine.load(buffer, None)
    _, data = engine.image_data_as_rgb()
    engine.set_image_data(data)
    assert engine.image.format == "PNG"
    assert engine.image.size == (691, 212)


def test_compare_image_data_and_mode(engine):
    pil_engine = PileEngine(get_context())
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


def test_get_and_set_image_data(engine):
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


@pytest.mark.parametrize(
    "image_type, expected_mode",
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
def test_get_image_mode(image_type, expected_mode, engine):
    engine.image = engine.gen_image((1, 1), "green")
    engine.image.type = image_type
    assert engine.get_image_mode() == expected_mode


@pytest.mark.parametrize(
    "image_type, expected_type",
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
def test_convert_to_grayscale(image_type, expected_type, engine):
    engine.image = engine.gen_image((1, 1), "green")
    engine.image.type = image_type
    image = engine.convert_to_grayscale()
    assert engine.image.type == image.type == expected_type


def test_convert_to_grayscale_update_image_false(engine):
    image_type, expected_type = TRUECOLOR_TYPE, GRAYSCALE_TYPE
    engine.image = engine.gen_image((1, 1), "green")
    engine.image.type = image_type
    image = engine.convert_to_grayscale(update_image=False)
    assert image.type == expected_type
    assert engine.image.type != expected_type


@pytest.mark.parametrize("image_type", IMAGE_TYPES)
def test_convert_to_grayscale_alpha_false(image_type, engine):
    engine.image = engine.gen_image((1, 1), "green")
    engine.image.type = image_type
    image = engine.convert_to_grayscale(alpha=False)
    assert engine.image.type == image.type == GRAYSCALE_TYPE


@pytest.mark.parametrize("image_type", IMAGE_TYPES)
def test_enable_alpha(image_type, engine):
    engine.image = engine.gen_image((1, 1), "green")
    engine.image.type = image_type
    engine.enable_alpha()
    assert engine.image.type == TRUECOLORALPHA_TYPE


def test_can_create_image_from_buffer(engine):
    with open(join(STORAGE_PATH, "paletted-transparent.png"), "rb") as image_file:
        buffer = image_file.read()
    engine.load(buffer, ".png")
    assert engine.image.format == "PNG"
    assert engine.image.type == TRUECOLORALPHA_TYPE
    assert engine.image.colors <= 256


@pytest.mark.parametrize(
    "image_file, expected_format",
    [
        ("paletted-transparent.png", "PNG"),
        ("image.jpg", "JPEG"),
        ("image.webp", "WEBP"),
        ("image.webp", "WEBP"),
        ("animated.gif", "GIF"),
        ("gradient_8bit.tif", "TIFF"),
        ("Commons-logo.svg", "PNG"),  # `BaseEngine.load` converts SVG to PNG
    ],
)
def test_can_create_image_from_buffer_extension_none(
    image_file, expected_format, engine
):
    with open(join(STORAGE_PATH, image_file), "rb") as image_file:
        buffer = image_file.read()
    engine.load(buffer, None)
    assert engine.image.format == expected_format


def test_can_read_as_is(engine):
    with open(join(STORAGE_PATH, "paletted-transparent.png"), "rb") as image_file:
        buffer = image_file.read()
    engine.load(buffer, ".png")
    img = engine.create_image(BytesIO(engine.read()))
    assert img.format == "PNG"
    assert img.type == TRUECOLORALPHA_TYPE
    assert img.colors <= 256


@pytest.mark.parametrize(
    "image_format, expected_type",
    [
        ("PNG", TRUECOLORALPHA_TYPE),
        ("WEBP", TRUECOLORALPHA_TYPE),
        ("JPEG", TRUECOLOR_TYPE),
    ],
)
def test_can_read_as_format(image_format, expected_type, engine):
    with open(join(STORAGE_PATH, "paletted-transparent.png"), "rb") as image_file:
        buffer = image_file.read()
    engine.load(buffer, ".png")
    img = engine.create_image(BytesIO(engine.read(f".{image_format.lower()}")))
    assert img.format == image_format
    assert img.type == expected_type


@pytest.mark.parametrize(
    "image_format, quality", [("WEBP", 75), ("WEBP", 50), ("JPEG", 75), ("JPEG", 50)]
)
def test_can_read_as_format_quality(image_format, quality, engine):
    with open(join(STORAGE_PATH, "paletted-transparent.png"), "rb") as image_file:
        buffer = image_file.read()
    engine.load(buffer, ".png")
    img = engine.create_image(BytesIO(engine.read(f".{image_format.lower()}", quality)))
    assert engine.image.compression_quality == quality
    assert img.format == image_format


@pytest.mark.parametrize(
    "image, filters, expected_output",
    [
        (None, ["gifv"], False),
        (MagicMock(animation=False), ["gifv", "blur"], False),
        (MagicMock(animation=True), ["blur", "fill"], False),
        (MagicMock(animation=True), [], False),
        (MagicMock(animation=True), ["gifv"], True),
        (MagicMock(animation=True), ["gifv", "fill"], True),
    ],
)
def test_is_multiple(image, filters, expected_output, engine):
    engine = Engine(MagicMock())
    engine.image = image
    engine.context.request.filters = filters
    assert engine.is_multiple() is expected_output


def test_resize_preserves_transparency(transp_engine, transp_pixels):
    width, height = transp_engine.image.size
    transp_engine.resize(width // 2, height // 2)
    img = transp_engine.create_image(BytesIO(transp_engine.read(".png")))
    assert img.type == TRUECOLORALPHA_TYPE
    assert img.format == "PNG"
    expected_transp_pixels = transp_pixels // 4 * 0.974  # 2.6% tolerance
    assert sum(a == 0 for a in img.export_pixels()[3::4]) >= expected_transp_pixels


@pytest.mark.parametrize("degrees", [90, 180, 270])
def test_rotate_preserves_transparency(degrees, transp_engine, transp_pixels):
    transp_engine.rotate(degrees)
    img = transp_engine.create_image(BytesIO(transp_engine.read(".png")))
    assert img.type == TRUECOLORALPHA_TYPE
    assert img.format == "PNG"
    expected_transp_pixels = transp_pixels
    assert sum(a == 0 for a in img.export_pixels()[3::4]) == expected_transp_pixels


def test_strip_icc(green_engine, green_image):
    green_engine.strip_icc()
    green_image.profiles.__delitem__.assert_called_once_with("icc")


def test_strip_exif(green_engine, green_image):
    green_engine.strip_exif()
    assert green_image.profiles.__delitem__.call_count == 3
    green_image.profiles.__delitem__.assert_any_call("exif")
    green_image.profiles.__delitem__.assert_any_call("iptc")
    green_image.profiles.__delitem__.assert_any_call("xmp")


def test_flip_vertically(green_engine, green_image):
    green_engine.flip_vertically()
    green_image.flip.assert_called_once_with()


def test_flip_horizontally(green_engine, green_image):
    green_engine.flip_horizontally()
    green_image.flop.assert_called_once_with()


def test_crop(green_engine, green_image):
    green_engine.crop(1.0, 2.0, 3.0, 4.0)
    green_image.crop.assert_called_once_with(left=1, top=2, right=3, bottom=4)


def test_resize(green_engine, green_image):
    green_engine.resize(1.0, 2.0)
    green_image.resize.assert_called_once_with(1, 2)


@pytest.mark.parametrize("degrees", [60, 90, 123.45])
def test_rotate(degrees, green_engine, green_image):
    green_engine.rotate(degrees)
    green_image.rotate.assert_called_once_with(degrees)


@pytest.mark.parametrize(
    "pos, merge, expected_operator",
    [
        ((359, 179), True, "over"),
        ((179, 359), False, "atop"),
    ],
)
def test_paste(pos, merge, expected_operator, green_engine, green_image):
    other_engine = MagicMock()
    green_engine.paste(other_engine, pos, merge)
    green_image.composite.assert_called_once_with(
        other_engine.image, pos[0], pos[1], expected_operator
    )


@pytest.mark.parametrize(
    "orientation_int, orientation_str", enumerate(ORIENTATION_TYPES)
)
def test_get_orientation(orientation_int, orientation_str, green_engine):
    green_engine.image.orientation = orientation_str
    assert green_engine.get_orientation() == orientation_int


def test_reorientate(green_engine, green_image):
    green_engine.reorientate()
    green_image.auto_orient.assert_called_once_with()


@pytest.mark.parametrize(
    "method",
    [
        "convert_to_grayscale",
        "enable_alpha",
        "gen_image",
        "get_orientation",
        "image_data_as_rgb",
        "is_multiple",
        "paste",
        "read",
        "resize",
        "rotate",
        "set_image_data",
        "strip_exif",
        "strip_icc",
    ],
)
def test_engine_implements_required_method(method):
    assert method in vars(Engine)
    assert callable(getattr(Engine, method))


def test_engine_implements_required_property():
    assert "size" in vars(Engine)
    assert isinstance(Engine.size, property)
