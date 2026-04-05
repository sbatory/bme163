# Image Comparison Tool
# Author: Stefan Batory
# BME 163 - Spring 2026
#
# Usage: python compare.py your_image example_image [-dir DIR] [-crop x1 y1 x2 y2]

import argparse
import os
import sys
from PIL import Image, ImageChops
import numpy as np

parser = argparse.ArgumentParser(
    usage=argparse.SUPPRESS,
    description='Compare two images pixel-by-pixel. Outputs the two images overlayed on top of each other,\nthe difference between the two, and a heatmap highlighting differences in red.\nusage: compare.py your_image example_image [-dir DIR] [-crop x1 y1 x2 y2]',
    epilog='Example: python3 compare.py your_image.png example_image.png -dir hw1 -crop 0 0 1380 1200',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    add_help=False)
parser.add_argument('image1', type=str, help=argparse.SUPPRESS)
parser.add_argument('image2', type=str, help=argparse.SUPPRESS)
group = parser.add_argument_group('optional arguments')
group.add_argument('-dir', type=str, default='.',
                   help='folder to save output images (default: current folder)')
group.add_argument('-crop', type=int, nargs=4, metavar=('x1', 'y1', 'x2', 'y2'),
                   help='crop both images to this region before comparing')
if len(sys.argv) == 1:
    print('Error: two images are required\n')
    parser.print_help()
    sys.exit(0)
args = parser.parse_args()

try:
    img1 = Image.open(args.image1)
except FileNotFoundError:
    print(f'Error: could not find "{args.image1}"\n')
    parser.print_help()
    sys.exit(1)

try:
    img2 = Image.open(args.image2)
except FileNotFoundError:
    print(f'Error: could not find "{args.image2}"\n')
    parser.print_help()
    sys.exit(1)

try:
    print(f'Image 1: {img1.size}')
    print(f'Image 2: {img2.size}')

    if img1.size != img2.size:
        img2 = img2.resize(img1.size, Image.LANCZOS)
        print(f'Resized image 2 to {img1.size}')

    if args.crop:
        x1, y1, x2, y2 = args.crop
        img1 = img1.crop((x1, y1, x2, y2))
        img2 = img2.crop((x1, y1, x2, y2))
        print(f'Cropped to ({x1}, {y1}, {x2}, {y2})')

    arr1 = np.array(img1)[:, :, :3]
    arr2 = np.array(img2)[:, :, :3]

    diff = np.abs(arr1.astype(int) - arr2.astype(int))

    print(f'Pixels with diff > 0: {int((diff > 0).sum())}')
    print(f'Pixels with diff > 5: {int((diff > 5).sum())}')
    identical = (diff == 0).all(axis=2).sum()
    total = diff.shape[0] * diff.shape[1]
    print(f'Similarity: {round(identical / total * 100, 2)}%')

    out_dir = os.path.join(getattr(args, 'dir'), 'comparison')
    os.makedirs(out_dir, exist_ok=True)

    amplified = diff.astype(np.uint8)
    diff_path = os.path.join(out_dir, 'difference.png')
    Image.fromarray(amplified).save(diff_path)

    overlay = Image.blend(img1, img2, 0.5)
    overlay_path = os.path.join(out_dir, 'overlay.png')
    overlay.save(overlay_path)

    # Side-by-side: overlay | difference
    diff_img = Image.fromarray(amplified)
    w, h = overlay.size
    side_by_side = Image.new('RGB', (w * 2 + 10, h), (200, 200, 200))
    side_by_side.paste(overlay, (0, 0))
    side_by_side.paste(diff_img, (w + 10, 0))
    sbs_path = os.path.join(out_dir, 'side_by_side.png')
    side_by_side.save(sbs_path)

    # Heatmap: input image with wrong pixels highlighted in bright red
    has_diff = (diff > 0).any(axis=2)
    heatmap = np.array(img1.convert('RGB')).copy()
    heatmap[has_diff] = [255, 0, 0]
    heatmap_path = os.path.join(out_dir, 'heatmap.png')
    Image.fromarray(heatmap.astype(np.uint8)).save(heatmap_path)

    print(f'Saved results to {out_dir}/')

except Exception as e:
    print(f'Error: {e}\n')
    parser.print_help()
    sys.exit(1)
