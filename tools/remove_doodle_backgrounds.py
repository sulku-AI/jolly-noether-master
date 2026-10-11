#!/usr/bin/env python3
"""Create transparent PNG cutouts for decorative assets referenced by index.html."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
MARKER = (3, 7, 11, 0)
CHECKERBOARD_ASSETS = {"asset-13"}


class DoodleSourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "img":
            return
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        output = attributes.get("src")
        source = attributes.get("data-source") or output
        if "doodle" in classes and source and output:
            self.assets.append((source, output))


def light_neutral(pixel: tuple[int, ...], threshold: int = 198) -> bool:
    red, green, blue = pixel[:3]
    return min(red, green, blue) >= threshold and max(red, green, blue) - min(red, green, blue) <= 52


def border_samples(image: Image.Image) -> list[tuple[int, int, int]]:
    pixels = image.load()
    width, height = image.size
    step = max(1, min(width, height) // 250)
    samples: list[tuple[int, int, int]] = []
    for x in range(0, width, step):
        for y in (0, height - 1):
            pixel = pixels[x, y]
            if light_neutral(pixel):
                samples.append(pixel[:3])
    for y in range(0, height, step):
        for x in (0, width - 1):
            pixel = pixels[x, y]
            if light_neutral(pixel):
                samples.append(pixel[:3])
    return samples


def median_background(samples: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    if not samples:
        return (255, 255, 255)
    return tuple(round(median(channel)) for channel in zip(*samples))


def matte_connected_background(image: Image.Image, full_neutral_key: bool) -> tuple[Image.Image, tuple[int, int, int]]:
    rgba = image.convert("RGBA")
    samples = border_samples(rgba)
    background = median_background(samples)
    working = rgba.copy()
    width, height = working.size

    if full_neutral_key:
        source_pixels = rgba.load()
        result_pixels = working.load()
        for y in range(height):
            for x in range(width):
                if light_neutral(source_pixels[x, y], threshold=188):
                    result_pixels[x, y] = MARKER
    else:
        pixels = working.load()
        step = max(1, min(width, height) // 250)
        seeds = [(x, y) for x in range(0, width, step) for y in (0, height - 1)]
        seeds.extend((x, y) for y in range(0, height, step) for x in (0, width - 1))
        for x, y in seeds:
            current = pixels[x, y]
            if current[3] and light_neutral(current):
                ImageDraw.floodfill(working, (x, y), MARKER, thresh=30)

    matte = working.getchannel("A")
    inner_edge = matte.filter(ImageFilter.MinFilter(3))
    source_data = rgba.get_flattened_data()
    matte_data = matte.get_flattened_data()
    inner_data = inner_edge.get_flattened_data()
    result: list[tuple[int, int, int, int]] = []

    for source_pixel, alpha_mask, interior in zip(source_data, matte_data, inner_data):
        red, green, blue, _ = source_pixel
        if alpha_mask == 0:
            result.append((red, green, blue, 0))
            continue
        if interior == 255:
            result.append((red, green, blue, 255))
            continue

        alpha = max(abs(red - background[0]), abs(green - background[1]), abs(blue - background[2]))
        if alpha < 16:
            result.append((red, green, blue, 0))
            continue

        opacity = alpha / 255
        unmatte = tuple(
            max(0, min(255, round((channel - matte_color * (1 - opacity)) / opacity)))
            for channel, matte_color in zip((red, green, blue), background)
        )
        result.append((*unmatte, alpha))

    cutout = Image.new("RGBA", (width, height))
    cutout.putdata(result)
    bbox = cutout.getchannel("A").getbbox()
    if bbox:
        padding = max(3, round(max(width, height) * 0.012))
        left = max(0, bbox[0] - padding)
        top = max(0, bbox[1] - padding)
        right = min(width, bbox[2] + padding)
        bottom = min(height, bbox[3] + padding)
        cutout = cutout.crop((left, top, right, bottom))
    return cutout, background


def parse_assets(index_path: Path) -> list[tuple[str, str]]:
    parser = DoodleSourceParser()
    parser.feed(index_path.read_text(encoding="utf-8"))
    return list(dict.fromkeys(parser.assets))


def main() -> None:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("--only", nargs="*", help="Process only these source basenames for a pilot run.")
    argument_parser.add_argument("--output", default="assets/doodles-transparent", help="Output folder relative to the workspace root.")
    args = argument_parser.parse_args()

    assets = parse_assets(ROOT / "index.html")
    if args.only:
        selected = set(args.only)
        assets = [
            (source, output)
            for source, output in assets
            if selected.intersection(
                {
                    Path(source).name,
                    Path(source).stem,
                    Path(output).name,
                    Path(output).stem,
                }
            )
        ]
        matched = {
            value
            for source, output in assets
            for value in (Path(source).name, Path(source).stem, Path(output).name, Path(output).stem)
        }
        missing = selected - matched
        if missing:
            raise SystemExit(f"No doodle source found for: {', '.join(sorted(missing))}")

    output_dir = ROOT / args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    if not assets:
        raise SystemExit("No <img class=\"doodle\"> sources found in index.html")

    active_outputs: set[Path] = set()
    for relative_source, relative_output in assets:
        source_path = ROOT / relative_source
        if not source_path.is_file():
            raise SystemExit(f"Missing doodle source: {relative_source}")
        with Image.open(source_path) as source_image:
            source_image.load()
            cutout, background = matte_connected_background(
                source_image,
                full_neutral_key=source_path.stem in CHECKERBOARD_ASSETS,
            )

        output_path = ROOT / relative_output
        if output_path.suffix.lower() != ".png":
            output_path = output_dir / f"{source_path.stem}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cutout.save(output_path, format="PNG", optimize=True)
        active_outputs.add(output_path.resolve())
        alpha = cutout.getchannel("A")
        transparent_pixels = alpha.histogram()[0]
        total_pixels = alpha.width * alpha.height
        print(
            f"{source_path.name} -> {output_path.relative_to(ROOT)} | "
            f"matte={background} | transparent={transparent_pixels / total_pixels:.1%} | "
            f"size={cutout.width}x{cutout.height}"
        )

    for stale_output in output_dir.glob("*.png"):
        if stale_output.resolve() not in active_outputs:
            stale_output.unlink()
            print(f"removed stale generated cutout: {stale_output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()