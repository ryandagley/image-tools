from PIL import Image
import os
import datetime  # Import the datetime module


def generate_quadrant_names():
    return ["tl", "tr", "bl", "br"]


def get_current_date_folder():
    # Get the current date in the format '6_NOV_2023'
    current_date = datetime.datetime.now().strftime('%d_%b_%Y')
    # Create the folder path
    return os.path.join("output", current_date + "_splits")


def split_and_save(image_path, output_folder, quadrant_names, input_image_index):
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
            output_filename = f"{filename_without_extension[:10]}_{input_image_index + 1}_{quadrant_names[i]}.png"
            output_path = os.path.join(output_folder, output_filename)
            quadrant_image.save(output_path, "PNG")

        print(f"Image '{image_path}' split successfully!")

    except Exception as e:
        print(f"An error occurred for '{image_path}': {e}")


if __name__ == "__main__":
    input_folder = "images"
    image_files = os.listdir(input_folder)
    quadrant_names = generate_quadrant_names()

    for input_image_index, image_filename in enumerate(image_files):
        image_path = os.path.join(input_folder, image_filename)
        output_folder = get_current_date_folder()  # Get the current date folder
        split_and_save(image_path, output_folder,
                       quadrant_names, input_image_index)
