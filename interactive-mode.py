from PIL import Image, ImageTk
import os
import tkinter as tk

class ImageSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Selector")
        
        # Set the folder path to the "images" folder in the same directory as the script
        self.folder_path = os.path.join(os.path.dirname(__file__), "images")

        # Set the initial window size
        self.root.geometry("1000x800")

        self.selected_image_path = None
        self.selected_thumbnail = None
        self.thumbnail_img = None
        self.thumbnail_width = 0
        self.thumbnail_height = 0

        self.create_widgets()

    def create_widgets(self):
        # Create a frame at the bottom for a bar
        self.bottom_bar = tk.Frame(self.root)
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.image_canvas = tk.Canvas(self.root, width=800, height=600)
        self.image_canvas.pack()

        self.images = []

        x = 10
        y = 10

        num_columns = 3  # Number of columns for thumbnail layout

        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                image = Image.open(os.path.join(self.folder_path, filename))

                # Calculate the new thumbnail size based on the scale factor
                thumbnail_width = int(image.width * scale_factor)
                thumbnail_height = int(image.height * scale_factor)

                # Resize the image
                image.thumbnail((thumbnail_width, thumbnail_height))

                photo = ImageTk.PhotoImage(image)
                self.images.append(filename)
                self.image_canvas.create_image(x, y, image=photo, anchor=tk.NW, tags=(filename,))
                x += thumbnail_width + 10
                if x > 800 - thumbnail_width:
                    x = 10
                    y += thumbnail_height + 10

                photo.image = photo

        # Bind the canvas to the select_image function
        self.image_canvas.bind("<Button-1>", self.select_image)

        # Create a "Cancel" button at the bottom of the window
        cancel_button = tk.Button(self.bottom_bar, text="Cancel", command=self.root.destroy)
        cancel_button.pack(side=tk.BOTTOM, pady=10)

    def split_and_save(self):
        try:
            # Open the selected image file
            original_image = Image.open(self.selected_image_path)

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
            filename_without_extension = os.path.splitext(os.path.basename(self.selected_image_path))[0]

            # Split and save each quadrant
            for i, quadrant_coords in enumerate(quadrants):
                quadrant_image = original_image.crop(quadrant_coords)
                output_filename = f"{filename_without_extension}_quadrant_{i + 1}.png"
                output_path = os.path.join(output_folder, output_filename)
                quadrant_image.save(output_path, "PNG")

            print(f"Image '{self.selected_image_path}' split successfully!")

            # Close the root window
            self.root.destroy()

        except Exception as e:
            print(f"An error occurred for '{self.selected_image_path}': {e}")

    def select_image(self, event):
        # Get the closest item (image) to the click event
        closest_item = self.image_canvas.find_closest(event.x, event.y)
        if closest_item:
            selected_index = self.images.index(self.image_canvas.gettags(closest_item)[0])
            selected_image = self.images[selected_index]

            if self.selected_thumbnail == closest_item:
                # Deselect and unhighlight if the same thumbnail is clicked again
                self.selected_thumbnail = None
                self.thumbnail_img = None
                self.thumbnail_width = 0
                self.thumbnail_height = 0
                self.selected_image_path = None
                self.image_canvas.delete("highlight")
                return

            self.selected_image_path = os.path.join(self.folder_path, selected_image)
            self.thumbnail_img = Image.open(self.selected_image_path)

            # Calculate the new thumbnail size based on the scale factor
            self.thumbnail_width = int(self.thumbnail_img.width * scale_factor)
            self.thumbnail_height = int(self.thumbnail_img.height * scale_factor)

            self.selected_thumbnail = closest_item
            self.highlight_selected_image()

    def highlight_selected_image(self):
        # Clear any existing highlights
        self.image_canvas.delete("highlight")

        # Get the coordinates of the selected thumbnail
        x1, y1 = self.image_canvas.coords(self.selected_thumbnail)

        # Calculate the coordinates for the highlight rectangle
        x2 = x1 + self.thumbnail_width
        y2 = y1 + self.thumbnail_height

        # Highlight the selected image by drawing a rectangle around it
        self.image_canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="blue", width=2, tags="highlight"
        )

        # Create a "Split" button below the selected image
        split_button = tk.Button(self.root, text="Split", command=self.split_and_save)
        split_button.place(x=x1, y=y2 + 10)

if __name__ == "__main__":
    scale_factor = 0.1  # 10%
    input_folder = "images"
    output_folder = "output"

    root = tk.Tk()
    app = ImageSplitterApp(root)

    root.mainloop()
