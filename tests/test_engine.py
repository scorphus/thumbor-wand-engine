from imagemagick_engine.engine import Engine
from imagemagick_engine.engine import GRAYSCALE_TYPE
from imagemagick_engine.engine import GRAYSCALEALPHA_TYPE
from os.path import abspath
from os.path import dirname
from os.path import join
from parameterized import parameterized
from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine as PileEngine
from unittest import TestCase
from unittest.mock import Mock


STORAGE_PATH = abspath(join(dirname(__file__), "../thumbor_tests/fixtures/images/"))


class ImageMagickEngineTestCase(TestCase):
    def get_context(self):
        cfg = Config(
            SECURITY_KEY="ACME-SEC",
            ENGINE="thumbor.engines.wand",
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
            ["grayscale", "RGB"],
            ["grayscalematte", "RGBA"],
            ["grayscalealpha", "RGBA"],
            ["truecolor", "RGB"],
            ["truecolormatte", "RGBA"],
            ["truecoloralpha", "RGBA"],
        ],
    )
    def test_get_image_mode(self, image_type, expected_mode):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        assert engine.get_image_mode() == expected_mode

    @parameterized.expand(
        [
            ["grayscale", GRAYSCALE_TYPE],
            ["grayscalematte", GRAYSCALEALPHA_TYPE],
            ["grayscalealpha", GRAYSCALEALPHA_TYPE],
            ["truecolor", GRAYSCALE_TYPE],
            ["truecolormatte", GRAYSCALEALPHA_TYPE],
            ["truecoloralpha", GRAYSCALEALPHA_TYPE],
        ],
    )
    def test_convert_to_grayscale(self, image_type, expected_mode):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        image = engine.convert_to_grayscale()
        assert engine.image.type == image.type == expected_mode

    @parameterized.expand(
        [
            ["truecolor", GRAYSCALE_TYPE],
            ["truecolormatte", GRAYSCALEALPHA_TYPE],
            ["truecoloralpha", GRAYSCALEALPHA_TYPE],
        ],
    )
    def test_convert_to_grayscale_update_image_false(self, image_type, expected_mode):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        image = engine.convert_to_grayscale(update_image=False)
        assert engine.image.type != expected_mode
        assert image.type == expected_mode

    @parameterized.expand(["truecolor", "truecolormatte", "truecoloralpha"])
    def test_convert_to_grayscale_alpha_false(self, image_type):
        engine = Engine(self.context)
        engine.image = Mock(type=image_type)
        image = engine.convert_to_grayscale(alpha=False)
        assert engine.image.type == image.type == GRAYSCALE_TYPE


class ImageMagickEngineTransformationsTestCase(TestCase):
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
