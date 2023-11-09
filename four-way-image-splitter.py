from PIL import Image
import os
import datetime
import argparse
import shutil


def generate_quadrant_names():
    return ["tl", "tr", "bl", "br"]


def get_current_date_folder():
    current_date = datetime.datetime.now().strftime('%d_%b_%Y')
    return os.path.join("output", current_date + "_splits")


def split_and_save(image_path, output_folder, quadrant_names, input_image_index, prefix=None):
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
            if prefix:
                output_filename = f"{prefix}_{filename_without_extension[:10]}_{input_image_index + 1}_{quadrant_names[i]}.png"
            else:
                output_filename = f"{filename_without_extension[:10]}_{input_image_index + 1}_{quadrant_names[i]}.png"
            output_path = os.path.join(output_folder, output_filename)
            quadrant_image.save(output_path, "PNG")

        print(f"Image '{image_path}' split successfully!")

        # Move the source image to the archive folder in the project directory
        archive_folder = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "archive")
        os.makedirs(archive_folder, exist_ok=True)
        archive_path = os.path.join(
            archive_folder, os.path.basename(image_path))
        shutil.move(image_path, archive_path)
        print(f"Source image '{image_path}' moved to archive folder!")

    except Exception as e:
        print(f"An error occurred for '{image_path}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split and save images.')
    parser.add_argument(
        '--name', help='Prefix for output filenames', default=None)
    args = parser.parse_args()

    input_folder = "images"
    image_files = os.listdir(input_folder)
    quadrant_names = generate_quadrant_names()

    for input_image_index, image_filename in enumerate(image_files):
        image_path = os.path.join(input_folder, image_filename)
        output_folder = get_current_date_folder()
        split_and_save(image_path, output_folder, quadrant_names,
                       input_image_index, args.name)
