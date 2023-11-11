from PIL import Image
import os
import datetime
import argparse
import shutil


class ImageSplitter:
    def __init__(self, input_folder, output_folder, prefix=None):
        # Initialize with input folder, output folder, and an optional prefix for filenames
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.prefix = prefix
        self.quadrant_names = ["tl", "tr", "bl", "br"]

    def generate_quadrant_names(self):
        # Generate and return quadrant names
        return self.quadrant_names

    def get_current_date_folder(self):
        # Generate a subfolder in the output folder with the current date and "_splits"
        current_date = datetime.datetime.now().strftime('%d_%b_%Y')
        return os.path.join(self.output_folder, current_date + "_splits")

    def split_and_save(self, image_path, input_image_index):
        try:
            # Open the original image
            original_image = Image.open(image_path)
            width, height = original_image.size
            half_width, half_height = width // 2, height // 2

            # Define quadrant coordinates
            quadrants = [
                (0, 0, half_width, half_height),
                (half_width, 0, width, half_height),
                (0, half_height, half_width, height),
                (half_width, half_height, width, height),
            ]

            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)
            filename_without_extension = os.path.splitext(
                os.path.basename(image_path))[0]

            for i, quadrant_coords in enumerate(quadrants):
                # Crop each quadrant and save it as a separate image
                quadrant_image = original_image.crop(quadrant_coords)
                if self.prefix:
                    output_filename = f"{self.prefix}_{filename_without_extension[:10]}_{input_image_index + 1}_{self.quadrant_names[i]}.png"
                else:
                    output_filename = f"{filename_without_extension[:10]}_{input_image_index + 1}_{self.quadrant_names[i]}.png"
                output_path = os.path.join(self.output_folder, output_filename)
                quadrant_image.save(output_path, "PNG")

            print(f"Image '{image_path}' split successfully!")

            # Prompt the user if they want to archive the source image
            archive_choice = input(
                "Do you want to archive the source image? (yes/no): ").strip().lower()
            if archive_choice == "yes":
                # Move the source image to the archive folder in the project directory
                archive_folder = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "archive")
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
    output_folder = "output"
    image_files = os.listdir(input_folder)

    image_splitter = ImageSplitter(input_folder, output_folder, args.name)

    for input_image_index, image_filename in enumerate(image_files):
        image_path = os.path.join(input_folder, image_filename)
        image_splitter.split_and_save(image_path, input_image_index)
