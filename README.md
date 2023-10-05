# Four-Way Image Splitter

This Python script is designed to split images into four equal quadrants (top-left, top-right, bottom-left, and bottom-right) and save them as separate PNG files. It is a useful tool for dividing images into smaller segments for various purposes.

## Getting Started

### Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Pillow (PIL) library for image processing

You can install Pillow using pip:

```bash
pip install Pillow
````

### Usage

1. Place your image files in the "images" folder.

2. Run the script by executing the following command in your terminal:

```bash
python image-splitter.py
```

3. The script will automatically split all image files in the "images" folder and save the quadrants as separate PNG files in the "output" folder. Each quadrant will be prefixed with the original image's filename.

4. You can find the split images in the "output" folder.

### Customization

- You can change the input and output folder names by modifying the `input_folder` and `output_folder` variables in the script.

- By default, the script saves the split images in PNG format. If you want to save them in a different format, you can change the format in the `quadrant_image.save()` method.

## Example

Suppose you have an image named "example.jpg" in the "images" folder. After running the script, the split images will be named as follows:

- example_quadrant_1.png (Top-Left Quadrant)
- example_quadrant_2.png (Top-Right Quadrant)
- example_quadrant_3.png (Bottom-Left Quadrant)
- example_quadrant_4.png (Bottom-Right Quadrant)

## Author

- Ryan Dagley
