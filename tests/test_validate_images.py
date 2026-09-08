"""Regression tests for the export checker. Run: python -m unittest discover -s tests -v."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_images.py"


class ExportChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def save(self, name="image.png", size=(64, 48), mode="RGB", color=None, **options):
        image = Image.new(mode, size, color)
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path, **options)
        return path

    def run_cli(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True, encoding="utf-8")
        return result.returncode, result.stdout + result.stderr

    def manifest(self, rows):
        path = self.root / "targets.json"
        path.write_text(json.dumps({"images": rows}), encoding="utf-8")
        return path

    def checker(self, mode="RGB"):
        image = Image.new(mode, (96, 96), "white")
        draw = ImageDraw.Draw(image)
        for y in range(0, 96, 8):
            for x in range(0, 96, 8):
                if (x // 8 + y // 8) % 2:
                    draw.rectangle((x, y, x + 7, y + 7), fill="gray")
        path = self.root / f"checker-{mode}.png"
        image.save(path)
        return path

    def test_legacy_command_with_targets(self):
        path = self.save("hero.jpg", (970, 300))
        code, out = self.run_cli(path, "--width", 970, "--height", 300, "--format", "JPEG")
        self.assertEqual(code, 0, out)
        self.assertIn("970x300 JPEG", out)

    def test_all_explicit_constraints_pass(self):
        path = self.save()
        code, out = self.run_cli(path, "--width", 64, "--height", 48,
                                 "--format", "PNG", "--mode", "RGB", "--alpha", "opaque")
        self.assertEqual(code, 0, out)
        self.assertNotIn("NOT_CHECKED", out)

    def test_dimensions_mismatch(self):
        code, out = self.run_cli(self.save(), "--width", 100, "--height", 100)
        self.assertEqual(code, 1, out)
        self.assertIn("width=64, expected=100", out)
        self.assertIn("height=48, expected=100", out)

    def test_missing_targets_are_not_verified(self):
        code, out = self.run_cli(self.save(size=(10, 10)))
        self.assertEqual(code, 0, out)
        self.assertIn("NOT_CHECKED target constraints: width, height, format, mode, alpha", out)
        self.assertIn("Missing targets are not verified", out)

    def test_format_mismatch(self):
        code, out = self.run_cli(self.save(), "--format", "JPEG")
        self.assertEqual(code, 1, out)
        self.assertIn("format=PNG, expected=JPEG", out)

    def test_cmyk_fails_when_rgb_required(self):
        code, out = self.run_cli(self.save("cmyk.jpg", mode="CMYK"), "--mode", "RGB")
        self.assertEqual(code, 1, out)
        self.assertIn("mode=CMYK, expected=RGB", out)

    def test_cmyk_without_mode_does_not_claim_mode_check(self):
        code, out = self.run_cli(self.save("cmyk.jpg", mode="CMYK"))
        self.assertEqual(code, 0, out)
        self.assertIn("NOT_CHECKED target constraints: width, height, format, mode, alpha", out)

    def test_transparency_required_fails_for_rgb_and_opaque_rgba(self):
        for mode in ("RGB", "RGBA"):
            with self.subTest(mode=mode):
                path = self.save(f"{mode}.png", mode=mode, color="white")
                code, out = self.run_cli(path, "--alpha", "transparent")
                self.assertEqual(code, 1, out)
                self.assertIn("all are opaque", out)

    def test_real_rgba_transparency(self):
        path = self.save(mode="RGBA", color=(255, 255, 255, 0))
        code, out = self.run_cli(path, "--alpha", "transparent", "--mode", "RGBA")
        self.assertEqual(code, 0, out)

    def test_partial_alpha_fails_opaque_requirement(self):
        path = self.save(mode="RGBA", color=(0, 0, 0, 128))
        code, out = self.run_cli(path, "--alpha", "opaque")
        self.assertEqual(code, 1, out)
        self.assertIn("expected all pixels opaque", out)

    def test_palette_transparency(self):
        image = Image.new("P", (32, 32), 0)
        image.putpalette([255, 255, 255, 0, 0, 0] + [0] * 762)
        path = self.root / "palette.png"
        image.save(path, transparency=0)
        code, out = self.run_cli(path, "--alpha", "transparent", "--mode", "P")
        self.assertEqual(code, 0, out)

    def test_rgb_color_key_transparency(self):
        path = self.save(color="white", transparency=(255, 255, 255))
        code, out = self.run_cli(path, "--alpha", "transparent")
        self.assertEqual(code, 0, out)

    def test_two_color_split_is_not_a_checkerboard(self):
        image = Image.new("RGB", (320, 320), "white")
        ImageDraw.Draw(image).rectangle((0, 0, 24, 319), fill="black")
        path = self.root / "split.png"
        image.save(path)
        code, out = self.run_cli(path)
        self.assertEqual(code, 0, out)
        self.assertNotIn("WARNING:", out)

    def test_stripes_are_not_a_checkerboard(self):
        image = Image.new("RGB", (96, 96), "white")
        draw = ImageDraw.Draw(image)
        for x in range(0, 96, 16):
            draw.rectangle((x, 0, x + 7, 95), fill="black")
        path = self.root / "stripes.png"
        image.save(path)
        code, out = self.run_cli(path)
        self.assertEqual(code, 0, out)
        self.assertNotIn("WARNING:", out)

    def test_checker_is_warning_even_with_opaque_alpha_channel(self):
        for mode in ("RGB", "RGBA"):
            with self.subTest(mode=mode):
                code, out = self.run_cli(self.checker(mode))
                self.assertEqual(code, 0, out)
                self.assertIn("WARNING: possible baked checkerboard", out)
                self.assertIn("warnings=1", out)

    def test_hidden_rgb_checker_does_not_warn(self):
        path = self.checker("RGBA")
        with Image.open(path) as original:
            image = original.copy()
        image.putalpha(0)
        image.save(path)
        code, out = self.run_cli(path, "--alpha", "transparent")
        self.assertEqual(code, 0, out)
        self.assertNotIn("WARNING:", out)

    def test_mixed_manifest_targets(self):
        self.save("hero.jpg", (970, 300))
        self.save("detail.png", (600, 450), mode="RGBA", color=(255, 255, 255, 0))
        manifest = self.manifest([
            {"path": "hero.jpg", "width": 970, "height": 300,
             "format": "JPEG", "mode": "RGB", "alpha": "opaque"},
            {"path": "detail.png", "width": 600, "height": 450,
             "format": "PNG", "mode": "RGBA", "alpha": "transparent"},
        ])
        code, out = self.run_cli("--manifest", manifest)
        self.assertEqual(code, 0, out)
        self.assertIn("Checked 2 image(s)", out)
        self.assertNotIn("NOT_CHECKED", out)

    def test_manifest_path_is_relative_to_manifest_not_cwd(self):
        self.save("sub/image.png")
        manifest = self.manifest([{"path": "sub/image.png", "width": 64,
                                  "height": 48, "format": "PNG"}])
        code, out = self.run_cli("--manifest", manifest)
        self.assertEqual(code, 0, out)

    def test_invalid_manifests(self):
        self.save()
        base = {"path": "image.png", "width": 64, "height": 48, "format": "PNG"}
        variants = [
            [], [dict(base, width=True)], [dict(base, width=0)],
            [dict(base, height="48")], [dict(base, mode="INVALID")],
            [dict(base, alpha="yes")], [dict(base, format=[])],
            [dict(base, path="missing.png")], [dict(base, typo=1)],
            [base, dict(base)], [{"path": "image.png"}], ["not an object"],
        ]
        for rows in variants:
            with self.subTest(rows=rows):
                code, out = self.run_cli("--manifest", self.manifest(rows))
                self.assertEqual(code, 2, out)
                self.assertIn("ERROR:", out)
                self.assertNotIn("Traceback", out)

    def test_malformed_json(self):
        manifest = self.root / "bad.json"
        manifest.write_text("{", encoding="utf-8")
        code, out = self.run_cli("--manifest", manifest)
        self.assertEqual(code, 2, out)
        self.assertNotIn("Traceback", out)

    def test_missing_path_and_empty_directory(self):
        for path in (self.root / "missing", self.root):
            with self.subTest(path=path):
                code, out = self.run_cli(path)
                self.assertEqual(code, 2, out)

    def test_corrupt_image_does_not_stop_batch(self):
        (self.root / "bad.png").write_bytes(b"not an image")
        self.save("valid.png")
        code, out = self.run_cli(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("unreadable:", out)
        self.assertIn("PASS", out)
        self.assertIn("Checked 2 image(s)", out)

    def test_truncated_pixel_data_fails(self):
        path = self.save(size=(200, 200))
        data = path.read_bytes()
        path.write_bytes(data[:50])
        code, out = self.run_cli(path)
        self.assertEqual(code, 1, out)
        self.assertIn("unreadable:", out)

    def test_explicit_unsupported_file(self):
        path = self.save("image.gif")
        code, out = self.run_cli(path)
        self.assertEqual(code, 1, out)
        self.assertIn("unsupported format=GIF", out)

    def test_recursive_directory(self):
        self.save("nested/image.png")
        code, out = self.run_cli(self.root, "--recursive")
        self.assertEqual(code, 0, out)
        self.assertIn("Checked 1 image(s)", out)

    def test_directory_named_png_is_not_an_image(self):
        (self.root / "folder.png").mkdir()
        self.save()
        code, out = self.run_cli(self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("Checked 1 image(s)", out)

    def test_bad_cli_inputs(self):
        path = self.save()
        manifest = self.manifest([{"path": "image.png", "width": 64,
                                  "height": 48, "format": "PNG"}])
        cases = [[], [path, "--width", 0], [path, "--height", -1],
                 [path, "--manifest", manifest],
                 ["--manifest", manifest, "--width", 64],
                 ["--manifest", manifest, "--recursive"]]
        for args in cases:
            with self.subTest(args=args):
                code, out = self.run_cli(*args)
                self.assertEqual(code, 2, out)
                self.assertNotIn("Traceback", out)


if __name__ == "__main__":
    unittest.main()
