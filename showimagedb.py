
import tkinter as tk
from PIL import Image, ImageTk
from camerasqlite import camerasqlite
import cv2
import numpy as np
import io
def display_image(image_id):

    db = camerasqlite()
    blob_data = db.get(image_id)
    image = Image.open(io.BytesIO(blob_data))
    #pil_image = Image.fromarray(blob_data)
    # Conversion from binary data to image
    #img = Image.open(io.BytesIO(blob_data))

    photo = ImageTk.PhotoImage(image)

    image_label.config(image=photo)
    image_label.image = photo  # Keep a reference

# Tkinter setup
root = tk.Tk()
image_label = tk.Label(root)
image_label.pack()

display_image(10)  # Fetch an image with a specific ID

root.mainloop()
