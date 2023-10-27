from PIL import Image
import os

def generate_quadrant_names():
    return ["top_left", "top_right", "bottom_left", "bottom_right"]

def split_and_save(image_path, output_folder, quadrant_names):
    try:
        # Open the image file
        original_image = Image.open(image_path)

        # Get the dimensions of the image
        width, height = original_image.size

        # Calculate half-width and half-height
        half_width, half_height = width // 2, height // 2

        # Define the quadrant coordinates
        quadrants = [
            (0, 0, half_width, half_height),
            (half_width, 0, width, half_height),
            (0, half_height, half_width, height),
            (half_width, half_height, width, height),
        ]

        # Create the "output" directory if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the filename without extension
        filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]

        # Split and save each quadrant
        for i, quadrant_coords in enumerate(quadrants):
            quadrant_image = original_image.crop(quadrant_coords)
            output_filename = f"{filename_without_extension}_{quadrant_names[i]}.png"
            output_path = os.path.join(output_folder, output_filename)
            quadrant_image.save(output_path, "PNG")
        
        print(f"Image '{image_path}' split successfully!")

    except Exception as e:
        print(f"An error occurred for '{image_path}': {e}")

if __name__ == "__main__":
    input_folder = "images"
    output_folder = "output"

    # List all files in the input folder
    image_files = os.listdir(input_folder)

    # Generate quadrant names
    quadrant_names = generate_quadrant_names()

    # Process each image file in the input folder
    for image_filename in image_files:
        image_path = os.path.join(input_folder, image_filename)
        split_and_save(image_path, output_folder, quadrant_names)
