from derpconf.config import Config
from thumbor.testing import FilterTestCase
from wand.image import Image

import pytest


Config.allow_environment_variables()


async def get_filtered(
    self,
    source_image,
    filter_name,
    params_string,
    config_context=None,
    mode="RGB",
):
    fltr = self.get_filter(filter_name, params_string, config_context)
    image = Image(filename=self.get_fixture_path(source_image))

    # Special case for the quality test, because the quality filter
    # doesn't really affect the image, it only sets a context value
    # for use on save. But here we convert the result,
    # we do not save it
    if params_string == "quality(10)":
        img_buffer = image.make_blob()  # TODO: quality has to be reduce here
        fltr.engine.load(img_buffer, ".jpg")
    else:
        img_buffer = image.make_blob()
        fltr.engine.load(img_buffer, ".png")

    fltr.context.transformer.img_operation_worker()

    await fltr.run()

    fltr.engine.image = fltr.engine.image.convert(mode)

    return fltr.engine.image


def get_fixture(self, name, mode="RGB"):
    image = Image(filename=self.get_fixture_path(name))
    return image


@staticmethod
def get_ssim(actual, expected):
    # TODO: change from "mean_squared" to "structural_similarity"
    # Check https://docs.wand-py.org/en/latest/wand/image.html#wand.image.COMPARE_METRICS
    _, metric = actual.compare(expected, "mean_squared")
    return round(1 - metric, 4)


@pytest.fixture(autouse=True)
def patch_get_filtered(mocker):
    """Mokey-patch FilterTestCase's methods to use Wand instead of Pillow"""
    mocker.patch.object(FilterTestCase, "get_filtered", get_filtered)
    mocker.patch.object(FilterTestCase, "get_fixture", get_fixture)
    mocker.patch.object(FilterTestCase, "get_ssim", get_ssim)