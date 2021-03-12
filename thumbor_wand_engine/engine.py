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
from wand.image import ORIENTATION_TYPES


GRAYSCALE_TYPE = IMAGE_TYPES[2]
GRAYSCALEALPHA_TYPE = IMAGE_TYPES[3]
TRUECOLORALPHA_TYPE = IMAGE_TYPES[7]


class Engine(BaseEngine):
    def gen_image(self, size, color):
        return Image().blank(*size, color)

    def create_image(self, buffer):
        return Image(blob=buffer)

    def is_multiple(self):
        """is_multiple allows a GIF to be converted to WEBP (e.g. AUTO_WEBP) but
        does not prevent conversion to WEBM or MP4 when `gifv` is used"""
        return bool(
            self.image
            and self.image.animation
            and "gifv" in self.context.request.filters
        )

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
        return "RGBA" if self.image.alpha_channel else "RGB"

    def image_data_as_rgb(self, update_image=True):
        return self.get_image_mode(), self.get_image_data()

    def set_image_data(self, data):
        self.image.import_pixels(
            width=self.image.width,
            height=self.image.height,
            channel_map=self.get_image_mode(),
            data=data,
        )

    def paste(self, other_engine, pos, merge=True):
        operator = "over" if merge else "atop"
        self.image.composite(other_engine.image, pos[0], pos[1], operator)

    def enable_alpha(self):
        """enable_alpha is expected to not only enable the alpha channel but
        also convert the image to truecolor/rgb, regardlessly; this method
        should have a more explicit name — but that ship has sailed =/"""
        self.image.type = TRUECOLORALPHA_TYPE

    def convert_to_grayscale(self, update_image=True, alpha=True):
        image = self.image.clone()
        if alpha and self.image.alpha_channel:
            image.type = GRAYSCALEALPHA_TYPE
        else:
            image.type = GRAYSCALE_TYPE
        if update_image:
            self.image = image
        return image

    def rotate(self, degrees):
        self.image.rotate(degrees)

    def strip_icc(self):
        del self.image.profiles["icc"]

    def strip_exif(self):
        del self.image.profiles["exif"]
        del self.image.profiles["iptc"]
        del self.image.profiles["xmp"]

    def get_orientation(self):
        return ORIENTATION_TYPES.index(self.image.orientation)

    def reorientate(self, *args, **kwargs):
        self.image.auto_orient()

    def draw_rectangle(self, x, y, width, height):  # pragma: no cover
        """draw_rectangle is used only in `/debug` routes"""
        with Drawing() as draw:
            draw.fill_color = "transparent"
            draw.stroke_color = "white"
            draw.stroke_width = 1
            draw.rectangle(x, y, width=width, height=height)
            draw(self.image)
