from os.path import abspath
from os.path import dirname
from os.path import join
from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine as PileEngine
from imagemagick_engine.engine import Engine
from unittest import TestCase


STORAGE_PATH = abspath(join(dirname(__file__), "./fixtures/images/"))


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
