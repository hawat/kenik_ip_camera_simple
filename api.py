from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
import io  # For working with image data in memory
from camerasqlite import camerasqlite

app = FastAPI(
    title="kenik ipcamera from-db-images api",
    description="This API serves images from an SQLite Database",
    version="1.0.0",
)

@app.get("/max_entries", response_model=int)
async def get_maximum_entries():
    db = camerasqlite()
    max_id = db.getmax()
    if max_id:
        return max_id
    else:
        return 0  # If the database is empty

@app.get("/images/{image_id}")
async def get_image(image_id: int):
    db = camerasqlite()
    image_data = db.get(image_id)
    #image_data = Image.open(io.BytesIO(blob_data))
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")  # Adjust mime-type if needed
