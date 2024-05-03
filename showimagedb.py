
import tkinter as tk
from PIL import Image, ImageTk
from camerasqlite import camerasqlite
import argparse
import cv2
import numpy as np
import io

def display_image(image_id):

    db = camerasqlite()
    blob_data = db.get(image_id)
    image = Image.open(io.BytesIO(blob_data))
    new_width = 800
    new_height = 600
    new_size = (new_width, new_height)  # A tuple
    resized_img = image.resize(new_size)

    #pil_image = Image.fromarray(blob_data)
    # Conversion from binary data to image
    #img = Image.open(io.BytesIO(blob_data))

    photo = ImageTk.PhotoImage(resized_img)

    image_label.config(image=photo)
    image_label.image = photo  # Keep a reference

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='show one image from database made for kenik ip cameras')
    parser.add_argument('index',  type=int,  help='index number to retrieve from db and show')
    args = parser.parse_args()
    root = tk.Tk()
    image_label = tk.Label(root)
    image_label.pack()
    print(args.index)
    display_image(args.index)  # Fetch an image with a specific ID

    root.mainloop()
