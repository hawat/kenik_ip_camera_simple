# Kenik ip camera simple 
![Alt text](readme_images/screen1.jpg?raw=true "Title")

**Brief Description:** collection of python tools to get images from kenik ip cameras, 
## Installation
Keep in mind that this software is "work in progress", and as it work for most parts - you can find bugs, errors, or even something not work at all.

**Current capabilities:**

Stores still images from unlimited number of ip cameras compressed to jpg format with native resolution, 
Old images are automatically deleted after 24h
You can get any image using bundled REST compatible api, or combine images from time period ang create MP4 video file - also served by API.
Can be installed as standalone tools, or as a DOCKER container.

TO DO: web GUI

**Prerequisites:**
* Python 3.5 or newer
* opencv2
* numpy
* PIL
* nmap (for autodiscovery of cam's on the local network)

**Instructions:**

1. Clone the repository:
   ```bash
   git clone [https://github.com/hawat/kenik_ip_camera_simple.git]
   ```
 2. Edit config.ini to fit your neads.

   You can perform autodetection to discover any cameras that support kenik rdsp compatible data collection using
bundled pscan.py tool.
3. Run main.py script to get data from all you kenik ip cameras
   ```bash
   python main.py 
   ````
4. Run api.py to get image data by easy http api calls 
   ```bash
   ./runapi.sh
   ```
5. You can run it as a docker container, for that you must kreate a Docker image by:
   ```
   docker build -t kenikcamerasimple .
   docker run -d kenikcamerasimple
   ```
API endpoint listen on port 8000, and can be easily changed by editing runapi.sh.    

**Background:**

Kenik ip cameras expose an rstp endpoint that can be accessed to get still images 
under url: 
```
rtsp://{user}:{password}@{host}:{port}/mode=real&idc=1&ids=1 
```
default configuration set admin account without (empty) password, and exposes this endpoint on port 554


