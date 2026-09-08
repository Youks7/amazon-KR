#!/usr/bin/env python3
"""Check JPEG/PNG exports against explicit targets; warnings require visual review."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png"}
FORMATS = {"JPEG", "PNG"}
MODES = {"RGB", "RGBA", "L", "LA", "P", "CMYK"}
ALPHA_RULES = {"opaque", "transparent"}
TARGETS = ("width", "height", "format", "mode", "alpha")


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    unchecked: list[str] = field(default_factory=list)
    actual: str = ""


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("dimension must be a positive integer")
    return number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="Image file or directory")
    parser.add_argument("--manifest", type=Path, help="JSON with per-file image targets")
    parser.add_argument("--width", type=positive_int)
    parser.add_argument("--height", type=positive_int)
    parser.add_argument("--format", choices=sorted(FORMATS))
    parser.add_argument("--mode", choices=sorted(MODES))
    parser.add_argument("--alpha", choices=sorted(ALPHA_RULES),
                        help="opaque: every pixel opaque; transparent: some alpha < 255")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories")
    args = parser.parse_args()
    if (args.path is None) == (args.manifest is None):
        parser.error("provide exactly one of path or --manifest")
    if args.manifest is not None and (
        args.recursive or any(getattr(args, key) is not None for key in TARGETS)
    ):
        parser.error("--manifest cannot be combined with directory/target flags")
    return args


def collect(path: Path, recursive: bool) -> list[Path]:
    if path.is_file():
        return [path]
    pattern = "**/*" if recursive else "*"
    return sorted(p for p in path.glob(pattern)
                  if p.is_file() and p.suffix.lower() in SUPPORTED)


def read_manifest(path: Path) -> list[tuple[Path, argparse.Namespace]]:
    """Paths are relative to the manifest, or absolute; no files are modified."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict) or set(data) != {"images"}:
        raise ValueError("manifest must contain only an images array")
    rows = data["images"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("manifest images must be a nonempty array")
    jobs = []
    seen = set()
    for index, row in enumerate(rows, 1):
        label = f"images[{index}]"
        if not isinstance(row, dict):
            raise ValueError(f"{label} must be an object")
        required = {"path", "width", "height", "format"}
        if not required <= row.keys() or set(row) - ({"path"} | set(TARGETS)):
            raise ValueError(f"{label}: required path/width/height/format; "
                             "optional mode/alpha; unknown fields are not allowed")
        if not isinstance(row["path"], str) or not row["path"].strip():
            raise ValueError(f"{label}: path must be a nonempty string")
        for key in ("width", "height"):
            if type(row[key]) is not int or row[key] <= 0:
                raise ValueError(f"{label}: {key} must be a positive integer")
        for key, choices in (("format", FORMATS), ("mode", MODES), ("alpha", ALPHA_RULES)):
            if key in row and (not isinstance(row[key], str) or row[key] not in choices):
                raise ValueError(f"{label}: invalid {key}")
        image_path = (path.parent / row["path"]).resolve()
        if image_path in seen:
            raise ValueError(f"{label}: duplicate image path {image_path}")
        seen.add(image_path)
        if not image_path.is_file():
            raise ValueError(f"{label}: image file does not exist: {image_path}")
        jobs.append((image_path, argparse.Namespace(**{key: row.get(key) for key in TARGETS})))
    return jobs


def looks_like_baked_checkerboard(image: Image.Image) -> bool:
    """Look for a two-color alternating grid in visible corner pixels.

    This is a heuristic: it cannot prove fake transparency and can miss patterns.
    Both axes must alternate repeatedly; two-color stripes/splits are not a grid.
    """
    width, height = image.size
    size = min(96, width, height)
    if size < 8:
        return False
    step = max(1, size // 32)
    for left, top in ((0, 0), (width - size, 0),
                      (0, height - size), (width - size, height - size)):
        patch = image.crop((left, top, left + size, top + size)).convert("RGBA")
        rows = []
        palette = {}
        for y in range(0, size, step):
            row = []
            for x in range(0, size, step):
                r, g, b, a = patch.getpixel((x, y))
                # Transparent hidden RGB values are not visible background evidence.
                color = (r // 16, g // 16, b // 16, a == 255)
                palette.setdefault(color, len(palette))
                row.append(palette[color])
            rows.append(row)
        if len(palette) != 2 or not all(color[3] for color in palette):
            continue
        horizontal = rows[0]
        vertical = [row[0] for row in rows]
        def transitions(values: list[int]) -> int:
            return sum(a != b for a, b in zip(values, values[1:]))
        if transitions(horizontal) < 3 or transitions(vertical) < 3:
            continue
        if all(value == (horizontal[x] ^ vertical[y] ^ rows[0][0])
               for y, row in enumerate(rows) for x, value in enumerate(row)):
            return True
    return False


def validate(path: Path, args: argparse.Namespace) -> Result:
    result = Result(unchecked=[key for key in TARGETS if getattr(args, key, None) is None])
    with Image.open(path) as image:
        image.load()  # Decode pixels; a readable header alone is insufficient.
        actual_format = image.format or "UNKNOWN"
        alpha_min, alpha_max = image.convert("RGBA").getchannel("A").getextrema()
        result.actual = (f"{image.width}x{image.height} {actual_format} "
                         f"mode={image.mode} alpha_range={alpha_min}..{alpha_max}")
        if actual_format not in FORMATS:
            result.errors.append(f"unsupported format={actual_format}")
        actual = {"width": image.width, "height": image.height,
                  "format": actual_format, "mode": image.mode}
        for key, value in actual.items():
            expected = getattr(args, key, None)
            if expected is not None and value != expected:
                result.errors.append(f"{key}={value}, expected={expected}")
        alpha_rule = getattr(args, "alpha", None)
        if alpha_rule == "opaque" and alpha_min < 255:
            result.errors.append("alpha: expected all pixels opaque")
        elif alpha_rule == "transparent" and alpha_min == 255:
            result.errors.append("alpha: expected some transparent pixels; all are opaque")
        if actual_format == "PNG" and looks_like_baked_checkerboard(image):
            result.warnings.append("possible baked checkerboard; visually review "
                                   "the pattern even when an alpha channel exists")
    return result


def main() -> int:
    args = parse_args()
    try:
        if args.manifest is not None:
            jobs = read_manifest(args.manifest)
        else:
            if not args.path.exists():
                raise ValueError(f"path does not exist: {args.path}")
            images = collect(args.path, args.recursive)
            if not images:
                raise ValueError("no supported images found")
            jobs = [(path, args) for path in images]
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    failures = warnings = 0
    for path, targets in jobs:
        try:
            result = validate(path, targets)
        except Exception as exc:
            # Keep processing the rest of the batch after a damaged file.
            result = Result(errors=[f"unreadable: {exc}"])
        failures += bool(result.errors)
        warnings += len(result.warnings)
        status = "FAIL" if result.errors else "PASS"
        print(f"{status} {path}: {result.actual}")
        for error in result.errors:
            print(f"  ERROR: {error}")
        for warning in result.warnings:
            print(f"  WARNING: {warning}")
        if result.unchecked:
            print(f"  NOT_CHECKED target constraints: {', '.join(result.unchecked)}")
    print(f"Checked {len(jobs)} image(s); failures={failures}; warnings={warnings}")
    print("PASS/exit 0 covers file decoding and supplied constraints only. "
          "Missing targets are not verified; warnings require visual review. "
          "Visual/product/text/platform compliance is not certified by this script.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
