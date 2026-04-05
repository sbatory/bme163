# BME 163 Image Comparison Tool

A pixel-by-pixel image comparison tool built for BME 163 (Data Visualization). Designed to help students verify that their matplotlib output matches the provided example figures as closely as possible.

## What It Does

Given two images, the tool:

- Compares every pixel across all three color channels (R, G, B)
- Reports a **similarity percentage** and pixel difference counts
- Generates the following visuals in a `comparison/` subfolder:
  - **overlay.png** — both images blended on top of each other at 50% opacity
  - **difference.png** — the raw pixel-by-pixel difference between the two images
  - **heatmap.png** — your image with every differing pixel highlighted in bright red
  - **side_by_side.png** — overlay and difference placed next to each other

## Requirements

- Python 3
- [Pillow](https://pypi.org/project/Pillow/) — `pip install Pillow`
- [NumPy](https://pypi.org/project/numpy/) — `pip install numpy`

## Usage

### Basic comparison

```
python compare.py your_image.png example_image.png
```

### Save results to a specific folder

```
python compare.py your_image.png example_image.png -dir hw1
```

Results will be saved to `hw1/comparison/`.

### Crop to a specific region

Useful for comparing a single panel. For BME 163 assignments, `-crop 0 0 1400 1200` typically covers the left panel:

```
python compare.py your_image.png example_image.png -dir hw1 -crop 0 0 1400 1200
```

### Example output

```
Image 1: (3000, 1200)
Image 2: (3000, 1200)
Cropped to (0, 0, 1400, 1200)
Pixels with diff > 0: 0
Pixels with diff > 5: 0
Similarity: 100.0%
Saved results to hw1/comparison/
```

## Notes

- If the two images have different dimensions, the second image is automatically resized to match the first.
- Run `python compare.py` with no arguments to see the built-in help.

## Author

Stefan Batory — BME 163, Spring 2026
