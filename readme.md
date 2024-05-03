# Kenik ip camera simple

**Brief Description:** collection of python tools to get images from kenik ip cameras
## Installation

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

2. Edit config.ini to fit your neads.
3. Run main.py script to get data from all you kenik ip cameras
   ```bash
   python main.py 
   ````
4. Run api.py to get image data by easy http api calls 
   ```bash
   ./runapi.sh
   ```
**Background:**

Kenik ip cameras expoze an rstp endpoint that can be accessed to get still images 
under url: 
```
rtsp://{user}:{password}@{host}:{port}/mode=real&idc=1&ids=1 
```
default configuration set admin account without (empty) password, and exposes this endpoint on port 554


