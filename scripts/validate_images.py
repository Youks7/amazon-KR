#!/usr/bin/env python3
"""Validate image dimensions, format, mode, and accidental checkerboard-like corners."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


SUPPORTED = {".jpg", ".jpeg", ".png"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="Image file or directory")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--format", choices=("JPEG", "PNG"))
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories")
    return parser.parse_args()


def collect(path: Path, recursive: bool) -> list[Path]:
    if path.is_file():
        return [path]
    pattern = "**/*" if recursive else "*"
    return sorted(p for p in path.glob(pattern) if p.suffix.lower() in SUPPORTED)


def looks_like_baked_checkerboard(image: Image.Image) -> bool:
    """Flag only a strong two-color checker pattern near image corners."""
    rgb = image.convert("RGB")
    sample = max(2, min(rgb.width, rgb.height) // 32)
    points = []
    for y in range(0, min(rgb.height, sample * 6), sample):
        for x in range(0, min(rgb.width, sample * 6), sample):
            points.append(rgb.getpixel((x, y)))
    quantized = {(r // 16, g // 16, b // 16) for r, g, b in points}
    return len(quantized) == 2 and len(points) >= 16


def validate(path: Path, args: argparse.Namespace) -> list[str]:
    problems: list[str] = []
    with Image.open(path) as image:
        width, height = image.size
        actual_format = image.format or "UNKNOWN"
        if args.width is not None and width != args.width:
            problems.append(f"width={width}, expected={args.width}")
        if args.height is not None and height != args.height:
            problems.append(f"height={height}, expected={args.height}")
        if args.format is not None and actual_format != args.format:
            problems.append(f"format={actual_format}, expected={args.format}")
        if actual_format == "JPEG" and image.mode not in {"RGB", "L", "CMYK"}:
            problems.append(f"unexpected JPEG mode={image.mode}")
        if actual_format == "PNG" and "A" not in image.mode and looks_like_baked_checkerboard(image):
            problems.append("possible baked checkerboard; PNG has no alpha channel")
    return problems


def main() -> int:
    args = parse_args()
    if not args.path.exists():
        print(f"ERROR: path does not exist: {args.path}", file=sys.stderr)
        return 2
    images = collect(args.path, args.recursive)
    if not images:
        print("ERROR: no supported images found", file=sys.stderr)
        return 2

    failures = 0
    for path in images:
        try:
            problems = validate(path, args)
        except Exception as exc:
            problems = [f"unreadable: {exc}"]
        if problems:
            failures += 1
            print(f"FAIL {path}: {'; '.join(problems)}")
        else:
            print(f"PASS {path}")
    print(f"Checked {len(images)} image(s); failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

