from PIL import Image
import os
import datetime
import argparse
import shutil


class ImageSplitter:
    def __init__(self, input_folder, output_folder, prefix=None):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.prefix = prefix
        self.quadrant_names = ["tl", "tr", "bl", "br"]

    def generate_quadrant_names(self):
        return self.quadrant_names

    def get_current_date_folder(self):
        current_date = datetime.datetime.now().strftime('%d_%b_%y').upper()
        output_folder = os.path.join(
            "output", current_date + '_splits')
        # Create the folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        return output_folder

    def split_and_save(self, image_path, input_image_index):
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

            os.makedirs(self.output_folder, exist_ok=True)
            filename_without_extension = os.path.splitext(
                os.path.basename(image_path))[0]

            for i, quadrant_coords in enumerate(quadrants):
                quadrant_image = original_image.crop(quadrant_coords)
                if self.prefix:
                    output_filename = f"{self.prefix}_{filename_without_extension}_{input_image_index + 1}_{self.quadrant_names[i]}.png"
                else:
                    output_filename = f"{filename_without_extension}_{input_image_index + 1}_{self.quadrant_names[i]}.png"
                output_path = os.path.join(
                    self.get_current_date_folder(), output_filename)
                quadrant_image.save(output_path, "PNG")

            print(f"Image '{image_path}' split successfully!")

        except Exception as e:
            print(f"An error occurred for '{image_path}': {e}")

    def archive_intake_images(self):
        archive_choice = input(
            "Do you want to move the source images to the archive folder? (y/n): ").strip().lower()
        if archive_choice == "y":
            archive_folder = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "archive")
            os.makedirs(archive_folder, exist_ok=True)

            image_files = os.listdir(self.input_folder)
            for image_filename in image_files:
                source_image_path = os.path.join(
                    self.input_folder, image_filename)
                archive_path = os.path.join(archive_folder, image_filename)
                shutil.move(source_image_path, archive_path)
                print(
                    f"Source image '{source_image_path}' moved to archive folder!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split and save images.')
    parser.add_argument(
        '--name', help='Prefix for output filenames', default=None)
    args = parser.parse_args()

    input_folder = "images"
    project_directory = os.path.dirname(os.path.realpath(__file__))
    current_date = datetime.datetime.now().strftime('%d_%b_%y').upper()
    output_folder = os.path.join(
        "output", current_date + '_splits')
    image_files = os.listdir(input_folder)

    image_splitter = ImageSplitter(input_folder, output_folder, args.name)

    for input_image_index, image_filename in enumerate(image_files):
        image_path = os.path.join(input_folder, image_filename)
        image_splitter.split_and_save(image_path, input_image_index)

    image_splitter.archive_intake_images()
