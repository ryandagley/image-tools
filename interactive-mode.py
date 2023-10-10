from PIL import Image, ImageTk
import os
import tkinter as tk

# Set the scale factor for thumbnail size (X% of original size)
scale_factor = 0.1  # 10%

# Define the image splitting function
def split_and_save(image_path, output_folder, root):
    try:
        # Open the selected image file
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
            output_filename = f"{filename_without_extension}_quadrant_{i + 1}.png"
            output_path = os.path.join(output_folder, output_filename)
            quadrant_image.save(output_path, "PNG")

        print(f"Image '{image_path}' split successfully!")

        # Close the root window
        root.destroy()

    except Exception as e:
        print(f"An error occurred for '{image_path}': {e}")

# Define the interactive image selection and processing function
def select_and_process_image():
    root = tk.Tk()
    root.title("Image Selector")

    # Set the folder path to the "images" folder in the same directory as the script
    folder_path = os.path.join(os.path.dirname(__file__), "images")

    # Set the initial window size
    root.geometry("800x600")

    selected_image_path = None
    selected_thumbnail = None
    thumbnail_img = None
    thumbnail_width = 0
    thumbnail_height = 0

    def select_image(event):
        nonlocal selected_thumbnail, thumbnail_img, thumbnail_width, thumbnail_height, selected_image_path
        # Get the closest item (image) to the click event
        closest_item = image_canvas.find_closest(event.x, event.y)
        if closest_item:
            selected_index = images.index(image_canvas.gettags(closest_item)[0])
            selected_image = images[selected_index]

            if selected_thumbnail == closest_item:
                # Deselect and unhighlight if the same thumbnail is clicked again
                selected_thumbnail = None
                thumbnail_img = None
                thumbnail_width = 0
                thumbnail_height = 0
                selected_image_path = None
                image_canvas.delete("highlight")
                return

            selected_image_path = os.path.join(folder_path, selected_image)
            thumbnail_img = Image.open(selected_image_path)

            # Calculate the new thumbnail size based on the scale factor
            thumbnail_width = int(thumbnail_img.width * scale_factor)
            thumbnail_height = int(thumbnail_img.height * scale_factor)

            selected_thumbnail = closest_item
            highlight_selected_image()

    def highlight_selected_image():
        # Clear any existing highlights
        image_canvas.delete("highlight")

        # Get the coordinates of the selected thumbnail
        x1, y1 = image_canvas.coords(selected_thumbnail)

        # Calculate the coordinates for the highlight rectangle
        x2 = x1 + thumbnail_width
        y2 = y1 + thumbnail_height

        # Highlight the selected image by drawing a rectangle around it
        image_canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="blue", width=2, tags="highlight"
        )

        # Create a "Split" button below the selected image
        split_button = tk.Button(root, text="Split", command=lambda: split_and_save(selected_image_path, "output", root))
        split_button.place(x=x1, y=y2 + 10)

    # Create a canvas to display image thumbnails
    image_canvas = tk.Canvas(root, width=800, height=600)
    image_canvas.pack()

    images = []

    x = 10
    y = 10

    num_columns = 6  # Number of columns for thumbnail layout

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            image = Image.open(os.path.join(folder_path, filename))

            # Calculate the new thumbnail size based on the scale factor
            thumbnail_width = int(image.width * scale_factor)
            thumbnail_height = int(image.height * scale_factor)

            # Resize the image
            image.thumbnail((thumbnail_width, thumbnail_height))

            photo = ImageTk.PhotoImage(image)
            images.append(filename)
            image_canvas.create_image(x, y, image=photo, anchor=tk.NW, tags=(filename,))
            x += thumbnail_width + 10
            if x > 800 - thumbnail_width:
                x = 10
                y += thumbnail_height + 10

            photo.image = photo

    # Bind the canvas to the select_image function
    image_canvas.bind("<Button-1>", select_image)

    root.mainloop()

if __name__ == "__main__":
    input_folder = "images"
    output_folder = "output"

    # Call the interactive mode to select and process an image
    select_and_process_image()
