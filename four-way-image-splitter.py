from PIL import Image
import os


def generate_quadrant_names():
    return ["tl", "tr", "bl", "br"]


def split_and_save(image_path, output_folder, quadrant_names):
    try:
        original_image = Image.open(image_path)
        width, height = original_image.size
        half_width, half_height = width // 2, height // 2

        quadrants = [
            (0, 0, half_width, half_height),
            (half_width, 0, width, half_height),
            (0, half_height, half_width, height),
            (half_width, half_height, width, height),
        ]

        os.makedirs(output_folder, exist_ok=True)
        filename_without_extension = os.path.splitext(
            os.path.basename(image_path))[0]

        for i, quadrant_coords in enumerate(quadrants):
            quadrant_image = original_image.crop(quadrant_coords)
            output_filename = f"{filename_without_extension[:10]}_{quadrant_names[i]}.png"
            output_path = os.path.join(output_folder, output_filename)
            quadrant_image.save(output_path, "PNG")

        print(f"Image '{image_path}' split successfully!")

    except Exception as e:
        print(f"An error occurred for '{image_path}': {e}")


if __name__ == "__main__":
    input_folder = "images"
    output_folder = "output"
    image_files = os.listdir(input_folder)
    quadrant_names = generate_quadrant_names()

    for image_filename in image_files:
        image_path = os.path.join(input_folder, image_filename)
        split_and_save(image_path, output_folder, quadrant_names)
