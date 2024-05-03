import nmap
#import requests
import cv2  # Optional for image verification
import numpy as np



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


# Determine your subnet (adjust the CIDR notation as needed)
def get_subnet():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.4.0/24', arguments='-n -sP -PE -PS554')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    return [host for host, state in hosts_list if state == 'up']


def create_montage(images, rows, cols):
    h, w = images[0].shape[:2]
    montage = np.zeros((rows * h, cols * w, 3), dtype='uint8')  # Assuming 3-channel images

    k = 0
    for i in range(rows):
        for j in range(cols):
            if k < len(images):
                montage[i * h: (i + 1) * h, j * w: (j + 1) * w] = images[k]
            k += 1

    return montage

# Protocol checks
def check_potential_camera(host):
    common_ports = [554]  # Add more as needed
    for port in common_ports:
        url = f"rtsp://admin:@{host}:{port}/mode=real&idc=1&ids=1"
        #url = f"http://{host}:{port}"
        print(f">>{host}:{port}>>{url}")
        # Optional: Attempt to grab an image for verification
        try:
            cap = cv2.VideoCapture(url)
            ret, frame = cap.read()
            cap.release()
            if ret:
                print(f"Potential camera found: {url}")
                desc_im(frame)
                return frame
        except: 
            pass  # Ignore if image capture fails
    return None

# Main execution
if __name__ == "__main__":
    hosts = get_subnet()
    images = []
    for host in hosts:
        img = check_potential_camera(host)
        if img is not None:
            images.append(img)
    if len(images)>0:
        montage_img = create_montage(images, rows=2, cols=2)  # Arrange in 2 rows, 2 columns
        img_show = cv2.resize(montage_img, (800, 600), interpolation=cv2.INTER_AREA)
        cv2.imshow('Montage', img_show)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
