import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'export_avatar.py'


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.png'
        Image.new('RGB', (200, 100), 'red').save(self.source)

    def run_export(self, *opts, source=None, name='out.png', width=100, height=100, success=True):
        dest = self.root / name
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(source or self.source), str(dest),
             '--width', str(width), '--height', str(height), *opts],
            capture_output=True, text=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return dest, json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result

    def test_contain_preserves_geometry(self):
        dest, meta = self.run_export('--background', '#ffffff')
        with Image.open(dest) as im:
            self.assertEqual(im.size, (100, 100))
            self.assertEqual(im.getpixel((50, 24)), (255, 255, 255))
            self.assertEqual(im.getpixel((50, 25)), (255, 0, 0))
            self.assertEqual(im.getpixel((50, 74)), (255, 0, 0))
            self.assertEqual(im.getpixel((50, 75)), (255, 255, 255))
        self.assertFalse(meta['upscaled'])

    def test_custom_dimensions(self):
        _, meta = self.run_export(width=91, height=137)
        self.assertEqual((meta['width'], meta['height']), (91, 137))
        self.assertEqual(meta['format'], 'PNG')

    def test_cover_crops_center(self):
        im = Image.new('RGB', (200, 100), 'blue')
        im.paste('red', (50, 0, 150, 100))
        im.save(self.source)
        dest, _ = self.run_export('--fit', 'cover')
        with Image.open(dest) as im:
            self.assertEqual(im.getpixel((0, 50)), (255, 0, 0))
            self.assertEqual(im.getpixel((99, 50)), (255, 0, 0))

    def test_png_auto_preserves_alpha(self):
        Image.new('RGBA', (200, 100), (255, 0, 0, 128)).save(self.source)
        dest, meta = self.run_export()
        self.assertTrue(meta['has_transparency'])
        with Image.open(dest) as im:
            self.assertEqual(im.getpixel((0, 0))[3], 0)
            self.assertEqual(im.getpixel((50, 50))[3], 128)

    def test_opaque_background_composites_alpha(self):
        Image.new('RGBA', (200, 100), (255, 0, 0, 128)).save(self.source)
        dest, meta = self.run_export('--background', '#ffffff')
        self.assertFalse(meta['has_transparency'])
        with Image.open(dest) as im:
            self.assertEqual(im.getpixel((50, 50)), (255, 127, 127))

    def test_transparent_padding_does_not_remove_background(self):
        dest, _ = self.run_export('--background', 'transparent')
        with Image.open(dest) as im:
            self.assertEqual(im.getpixel((0, 0))[3], 0)
            self.assertEqual(im.getpixel((50, 50)), (255, 0, 0, 255))

    def test_jpeg_auto_flattens(self):
        Image.new('RGBA', (200, 100), (255, 0, 0, 0)).save(self.source)
        dest, meta = self.run_export(name='out.jpg')
        self.assertEqual(meta['format'], 'JPEG')
        with Image.open(dest) as im:
            self.assertEqual(im.mode, 'RGB')
            self.assertGreater(min(im.getpixel((50, 50))), 220)

    def test_upscale_requires_explicit_flag(self):
        self.run_export(width=400, height=400, success=False)
        _, meta = self.run_export('--allow-upscale', width=400, height=400)
        self.assertTrue(meta['upscaled'])

    def test_existing_output_and_source_are_protected(self):
        dest, _ = self.run_export()
        before = dest.read_bytes()
        self.run_export(width=90, success=False)
        self.assertEqual(dest.read_bytes(), before)
        self.run_export('--overwrite', width=90)
        before = self.source.read_bytes()
        self.run_export('--overwrite', name='source.png', success=False)
        self.assertEqual(self.source.read_bytes(), before)

    def test_invalid_inputs_create_no_output(self):
        cases = [dict(width=0), dict(height=-1), dict(width=10000, height=10000),
                 dict(name='out.gif'), dict(source=self.root/'missing.png')]
        for case in cases:
            with self.subTest(case=case):
                self.run_export(success=False, **case)
        self.run_export('--background', 'transparent', name='out.jpg', success=False)
        self.run_export('--background', '#ffffff00', success=False)
        self.run_export('--background', 'not-a-color', success=False)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['source.png'])

    def test_exif_rotation(self):
        src = self.root / 'rotated.jpg'
        im = Image.new('RGB', (200, 100), 'red')
        exif = im.getexif()
        exif[274] = 6
        im.save(src, exif=exif)
        _, meta = self.run_export(source=src, width=50, height=100)
        self.assertEqual((meta['source_width'], meta['source_height']), (100, 200))


if __name__ == '__main__':
    unittest.main()
