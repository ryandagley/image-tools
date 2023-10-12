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

        self.selected_indices = []  # Store selected indices

        self.create_widgets()

    def create_widgets(self):
        # Constants
        scale_factor = 0.11  # 10%
        num_columns = 3  # Number of columns for thumbnail layout

        # Create a frame at the bottom for a bar
        self.bottom_bar = tk.Frame(self.root)
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a canvas to hold the thumbnails and add a vertical scrollbar
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.image_canvas = tk.Canvas(self.canvas_frame, width=800, height=600)
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_canvas.config(yscrollcommand=self.v_scrollbar.set)

        self.canvas_frame.update_idletasks()

        self.canvas_frame.bind("<Configure>", self.on_canvas_configure)

        self.images = []

        x = 10
        y = 10

        for filename in [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]:
            image = Image.open(os.path.join(self.folder_path, filename))

            # Calculate the new thumbnail size based on the scale factor
            thumbnail_width = int(image.width * scale_factor)
            thumbnail_height = int(image.height * scale_factor)

            # Resize the image
            image.thumbnail((thumbnail_width, thumbnail_height))

            photo = ImageTk.PhotoImage(image)
            self.images.append((filename, thumbnail_width, thumbnail_height))
            thumbnail_item = self.image_canvas.create_image(x, y, image=photo, anchor=tk.NW, tags=(filename,))
            x += thumbnail_width + 10
            if x > 800 - thumbnail_width:
                x = 10
                y += thumbnail_height + 10

            photo.image = photo

            # Bind the canvas to the select_image function for each thumbnail item
            self.image_canvas.tag_bind(thumbnail_item, "<Button-1>", self.create_select_image_callback(thumbnail_item))

        # Create a "Cancel" button at the bottom of the window
        cancel_button = tk.Button(self.bottom_bar, text="Cancel", command=self.root.destroy)
        cancel_button.pack(side=tk.LEFT, pady=10)

        # Create a "Split" button on the bottom bar
        split_button = tk.Button(self.bottom_bar, text="Split", command=self.split_and_save)
        split_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def on_canvas_configure(self, event):
        self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))

    def create_select_image_callback(self, thumbnail_item):
        def select_image(event):
            index = self.images.index(next((item for item in self.images if item[0] == self.image_canvas.gettags(thumbnail_item)[0]), None))
            if index is not None:
                if index in self.selected_indices:
                    # Deselect and unhighlight if the same thumbnail is clicked again
                    self.selected_indices.remove(index)
                else:
                    self.selected_indices.append(index)
                self.highlight_selected_images()
        return select_image

    def split_and_save(self):
        try:
            for selected_index in self.selected_indices:
                selected_image_info = self.images[selected_index]
                selected_image_path = os.path.join(self.folder_path, selected_image_info[0])

                # Open the selected image file
                original_image = Image.open(selected_image_path)

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
                output_folder = "output"
                os.makedirs(output_folder, exist_ok=True)

                # Get the filename without extension
                filename_without_extension = os.path.splitext(selected_image_info[0])[0]

                # Split and save each quadrant
                for j, quadrant_coords in enumerate(quadrants):
                    quadrant_image = original_image.crop(quadrant_coords)
                    output_filename = f"{filename_without_extension}_quadrant_{j + 1}.png"
                    output_path = os.path.join(output_folder, output_filename)
                    quadrant_image.save(output_path, "PNG")

                print(f"Image '{selected_image_info[0]}' split successfully!")

            # Clear the selected indices and reset the canvas
            self.selected_indices = []
            self.image_canvas.delete("highlight")

        except Exception as e:
            print(f"An error occurred: {e}")

    def highlight_selected_images(self):
        # Clear any existing highlights
        self.image_canvas.delete("highlight")

        for index in self.selected_indices:
            selected_image_info = self.images[index]
            thumbnail_item = self.image_canvas.find_withtag(selected_image_info[0])[0]

            # Get the coordinates of the selected thumbnail
            x1, y1 = self.image_canvas.coords(thumbnail_item)

            # Calculate the coordinates for the highlight rectangle
            x2 = x1 + selected_image_info[1]
            y2 = y1 + selected_image_info[2]

            # Highlight the selected image by drawing a rectangle around it
            self.image_canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="blue", width=2, tags="highlight"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSplitterApp(root)

    root.mainloop()
