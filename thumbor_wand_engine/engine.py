#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>

from thumbor.engines import BaseEngine
from thumbor.utils import deprecated
from wand.drawing import Drawing
from wand.image import Image
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


class Engine(BaseEngine):
    def gen_image(self, size, color):
        return Image().blank(*size, color)

    def create_image(self, buffer):
        return Image(blob=buffer)

    @property
    def size(self):
        return self.image.size

    def resize(self, width, height):
        self.image.resize(int(width), int(height))

    def crop(self, left, top, right, bottom):
        self.image.crop(
            left=int(left), top=int(top), right=int(right), bottom=int(bottom)
        )

    def flip_vertically(self):
        self.image.flip()

    def flip_horizontally(self):
        self.image.flop()

    def read(self, extension=None, quality=None):
        if extension is not None:
            self.extension = extension
        image_format = self.extension.lstrip(".")
        if self.image.format != image_format:
            self.image.format = image_format
        if quality is not None:
            self.image.compression_quality = quality
        return self.image.make_blob()

    @deprecated("Use image_data_as_rgb instead.")
    def get_image_data(self):
        return bytes(self.image.export_pixels(channel_map=self.get_image_mode()))

    @deprecated("Use image_data_as_rgb instead.")
    def get_image_mode(self):
        if self._is_image_type_alpha():
            return "RGBA"
        return "RGB"

    def image_data_as_rgb(self, update_image=True):
        return self.get_image_mode(), self.get_image_data()

    def set_image_data(self, data):
        self.image.import_pixels(
            width=self.image.width,
            height=self.image.height,
            channel_map=self.get_image_mode(),
            data=data,
        )

    def draw_rectangle(self, x, y, width, height):
        with Drawing() as draw:
            draw.fill_color = "transparent"
            draw.stroke_color = "white"
            draw.stroke_width(1)
            draw.rectangle(x, y, width=width, height=height)
            draw(self.image)

    def paste(self, other_engine, pos, merge=True):
        self.image.alpha_channel = True
        other_engine.image.alpha_channel = True

        operator = "over" if merge else "atop"
        self.image.composite(other_engine.image, pos[0], pos[1], operator)

    def enable_alpha(self):
        """enable_alpha is expected to not only enable the alpha channel but
        also convert the image to truecolor/rgb, regardlessly; this method
        should have a more explicit name — but that ship has sailed =/"""
        self.image.type = TRUECOLORALPHA_TYPE

    def convert_to_grayscale(self, update_image=True, alpha=True):
        image = self.image.clone()
        if alpha and self._is_image_type_alpha():
            image.type = GRAYSCALEALPHA_TYPE
        else:
            image.type = GRAYSCALE_TYPE
        if update_image:
            self.image = image
        return image

    def rotate(self, degrees):
        self.image.rotate(degrees)

    def _is_image_type_alpha(self):
        return self.image.type in (
            GRAYSCALEALPHA_TYPE,
            PALETTEALPHA_TYPE,
            TRUECOLORALPHA_TYPE,
            COLORSEPARATIONALPHA_TYPE,
            PALETTEBILEVELALPHA_TYPE,
        )
