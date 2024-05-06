import logging

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import io  # For working with image data in memory
from camerasqlite import camerasqlite
import tempfile
from moviepy.editor import *
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(
    title="kenik ipcamera from-db-images api",
    description="This API serves images from an SQLite Database",
    version="1.0.0",
)

scheduler = BackgroundScheduler()

@app.get("/max_entries", response_model=int)
async def get_maximum_entries():
    db = camerasqlite()
    max_id = db.getmax()
    if max_id:
        return max_id
    else:
        return 0  # If the database is empty


@app.get("/cameras")
async def get_cameras():
    db = camerasqlite()
    cam_list = db.getcameras()
    return {
        "message": "cameras found",
        "cameras": cam_list
    }


@app.get("/cameras/lastimage/")
async def get_image(address: str):
    db = camerasqlite()
    image_data = db.getlastforaddress(address)
    if not image_data:
        raise HTTPException(status_code=404, detail="Image for this address not found")

    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")  # Adjust mime-type if needed


@app.get("/images/{image_id}")
async def get_image(image_id: int | None = None):
    db = camerasqlite()
    image_data = None
    if id:
        image_data = db.get(image_id)
    else:
        maxid = db.getmax()
        image_data = db.get(image_id)
    #image_data = Image.open(io.BytesIO(blob_data))
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")  # Adjust mime-type if needed


# Function to iterate over video file in chunks
def video_stream(path: str):
    with open(path, mode="rb") as file:
        while True:
            chunk = file.read(1024 * 1024)  # Adjust chunk size as needed
            if not chunk:
                break
            yield chunk


@app.get("/video/{address}/{tfrom}/{tto}")
async def get_video(address: str, tfrom: str, tto: str):
    db = camerasqlite()
    print(f"address:{address} from:{tfrom} tto{tto}")
    image_list = db.getidbetweentimestamp(address, tfrom, tto)
    if not image_list or len(image_list) == 0:
        raise HTTPException(status_code=404, detail="Images not found")
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory created: {temp_dir}")
        for imid in image_list:
            image = db.get(imid)
            with open(temp_dir + "/" + str(imid).zfill(12) + ".jpg", 'wb') as f:  # 'wb' for writing in binary mode
                f.write(image)
        file_list = os.listdir(temp_dir)
        sorted_files = sorted(file_list)
        full_paths = [os.path.join(temp_dir, file) for file in sorted_files]

        clips = [ImageClip(img).set_duration(1 / 10) for img in full_paths]
        video_clip = concatenate_videoclips(clips)
        _, temp_vide_file = tempfile.mkstemp(suffix='.mp4')
        #logger = logging.getLogger('moviepy')
        #logger.setLevel(logging.ERROR)  # Change to a higher level (e.g., WARNING) if needed
        video_clip.write_videofile(temp_vide_file, fps=10, verbose=False, logger=None)
    headers = {
        'Content-Type': 'video/mp4'
    }
    return StreamingResponse(video_stream(temp_vide_file), headers=headers)

@app.on_event("startup")
async def startup_event():
    scheduled_task()
    scheduler.add_job(scheduled_task, 'interval', minutes=60)
    scheduler.start()

def scheduled_task():
    logging.basicConfig(level=logging.INFO)  # Adjust logging level as needed
    logger = logging.getLogger(__name__)
    db = camerasqlite()
    db.deleteold(24)
    logger.info('old images purged')