import nmap
import requests
import cv2  # Optional for image verification 



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
        except: 
            pass  # Ignore if image capture fails              

# Main execution
if __name__ == "__main__":
    hosts = get_subnet()
    for host in hosts:
        check_potential_camera(host)

