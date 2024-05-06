import logging
import argparse
import configparser
import time
import threading
from camerasqlite import camerasqlite
from cameraworker import CameraWorker, CameraWorkerList





logging_format = "%(asctime)s - %(levelname)s - %(message)s"

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="APP")
    parser.add_argument("-l", "--log", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level")
    parser.add_argument('--log_file', type=str, help='Path to the log file')
    parser.add_argument('-t', '--repeat_time', type=int, help='time in seconds\
     for repetition of image gathering')
    args = parser.parse_args()

    # Configure Logging
    logging.basicConfig(level=getattr(logging, args.log.upper()))
    formatter = logging.Formatter(logging_format)
    handler = logging.StreamHandler()  # Or other handler like FileHandler
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    for ohandler in logger.handlers:
        logger.removeHandler(ohandler)
    logger.addHandler(handler)
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)  # Create the FileHandler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    #for handler in logger.handlers:
    #    logger.info(f"Handler: {handler}")  # Handler object
    #    logger.info(f"  Level: {handler.level}")
    #    logger.info(f"  Formatter: {handler.formatter}")
    logger = logging.getLogger(__name__)
    logger.info(f'{__name__} is running,,,')
    config = configparser.ConfigParser()
    config.read('config.ini')

    ip_addresses = []
    network_section = config['cameras']

    for key, value in network_section.items():
        if key.startswith('cam'):  # Filter keys that are IP addresses
            ip_addresses.append(value)

    logger.info(f"will capture from {ip_addresses}")
    camlist = CameraWorkerList.createlist(ip_addresses)
    database = camerasqlite()
    thread_running = threading.Thread()
    if args.repeat_time:
        while True:
            logger.info('perform continuous gathering...')
            if not thread_running.is_alive() :
                thread_running = threading.Thread(target=CameraWorker.runallthread, args=(camlist,))
                thread_running.start()
            else:
                logger.warning("thread still running, will check on next iteration,\
                 consider increasing cooldown time")
            time.sleep(args.repeat_time)
    else:
        CameraWorker.runall(camlist,database)
    logger.info("exit...")

