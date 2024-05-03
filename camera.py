import cv2  # Optional for image verification
import numpy as np
from PIL import Image, ImageTk
import io
import logging
from perfdecorator import time_execution



class Camera():
    def __init__(self, host, port=554):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.url = f"rtsp://admin:@{host}:{port}/mode=real&idc=1&ids=1"
        self.frame = None

    def __enter__(self):
        return self.capture()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @time_execution
    def capture(self):
        try:
            cap = cv2.VideoCapture(self.url)
            ret, frame = cap.read()
            cap.release()
            if ret:
                self.frame = frame
                self.logger.info(f"size: {len(frame)}")
                return frame
        except:
            return None

    @time_execution
    def save_to_file(self,filename):
        cv2.imwrite(filename, self.frame)

    def get_jpg(self):
        frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)

        #  Encode as JPEG into a buffer
        image_buffer = io.BytesIO()
        pil_image.save(image_buffer, format="JPEG", quality=90)
        encoded_image = image_buffer.getvalue()
        return encoded_image

    def desc_im(image):
        img_shape = image.shape

        if len(img_shape) == 3:
            if img_shape[2] == 3:
                print("Image Type: BGR (Color)")
            else:
                print("Image Type: Unknown Color Space")
        elif len(img_shape) == 2:
            print("Image Type: Grayscale")
        else:
            print("Image Type: Unknown (Potentially invalid image)")

    def get_addr_port(self):
        return  self.host, self.port

