from camera import Camera
import argparse




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Capture one image from kenik ip camera')
    # Positional argument
    parser.add_argument('camera_ip_address', help='ip address of resolvable name of kenik ip camera')
    # Optional arguments
    parser.add_argument('-o', '--output', default='image.jpg',  help='Output file name')
    parser.add_argument('-dbf', '--databasefile', default='main.db', help='SQLite database file')
    parser.add_argument('--port', type=int, default=554, help='use custom port number (other than 554)')
    parser.add_argument( '-d','--database', action='store_false', help='output to SQLite')
    args = parser.parse_args()
    cam = Camera(args.camera_ip_address,args.port)
    cam.capture()
    if args.database:
        cam.save_to_file(args.output)
    else:
        from camerasqlite import camerasqlite
        db = camerasqlite(args.databasefile)
        db.store(cam.get_jpg())