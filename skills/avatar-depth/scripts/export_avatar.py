#!/usr/bin/env python3
"""Export exact avatar dimensions without stretching; requires Pillow."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageColor, ImageOps


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--width', type=int, required=True)
    p.add_argument('--height', type=int, required=True)
    p.add_argument('--fit', choices=['contain', 'cover'], default='contain')
    p.add_argument('--background', default='auto', help='auto, transparent, or an opaque color')
    p.add_argument('--allow-upscale', action='store_true')
    p.add_argument('--overwrite', action='store_true')
    a = p.parse_args()
    if min(a.width, a.height) < 1 or a.width * a.height > 40_000_000:
        p.error('Use positive dimensions totaling at most 40 million pixels.')
    if a.source.resolve() == a.output.resolve():
        p.error('Keep the source master: output must be a different path.')
    if a.output.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
        p.error('Output must be PNG or JPEG.')
    if a.output.exists() and not a.overwrite:
        p.error('Output exists; choose a new filename or use --overwrite.')
    try:
        with Image.open(a.source) as opened:
            src = ImageOps.exif_transpose(opened).convert('RGBA')
    except (OSError, ValueError, Image.DecompressionBombError) as e:
        p.error(f'Cannot read source image: {e}')
    source_alpha = src.getchannel('A').getextrema()[0] < 255
    background = a.background.lower()
    if background == 'auto':
        background = 'transparent' if source_alpha and a.output.suffix.lower() == '.png' else '#fff6eb'
    transparent = background == 'transparent'
    if transparent and a.output.suffix.lower() != '.png':
        p.error('Transparent output requires PNG.')
    try:
        color = (0, 0, 0, 0) if transparent else ImageColor.getcolor(background, 'RGBA')
    except ValueError as e:
        p.error(str(e))
    if not transparent and color[3] != 255:
        p.error('Use an opaque background color or the word transparent.')
    size = (a.width, a.height)
    ratios = (a.width / src.width, a.height / src.height)
    scale = max(ratios) if a.fit == 'cover' else min(ratios)
    if scale > 1 and not a.allow_upscale:
        p.error('Requested export enlarges the source. Generate a larger master or pass --allow-upscale.')
    if a.fit == 'cover':
        rendered = ImageOps.fit(src, size, method=Image.Resampling.LANCZOS)
    else:
        rendered = ImageOps.contain(src, size, method=Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', size, color)
    canvas.alpha_composite(rendered, ((a.width-rendered.width)//2, (a.height-rendered.height)//2))
    if not transparent:
        canvas = canvas.convert('RGB')
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open('wb' if a.overwrite else 'xb') as target:
        if a.output.suffix.lower() == '.png':
            canvas.save(target, format='PNG', optimize=True)
        else:
            canvas.save(target, format='JPEG', quality=95, subsampling=0)
    with Image.open(a.output) as check:
        assert check.size == size
        has_alpha = 'A' in check.getbands() and check.getchannel('A').getextrema()[0] < 255
        print(json.dumps({'path': str(a.output.resolve()), 'width': check.width,
                          'height': check.height, 'format': check.format,
                          'has_transparency': has_alpha,
                          'source_width': src.width, 'source_height': src.height,
                          'fit': a.fit, 'upscaled': scale > 1,
                          'bytes': a.output.stat().st_size}, ensure_ascii=False))


if __name__ == '__main__':
    main()
