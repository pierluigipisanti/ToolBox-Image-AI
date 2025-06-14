from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.utils import remove_background, resize_image
import io

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_data = await file.read()
    output_data = remove_background(image_data)
    return StreamingResponse(io.BytesIO(output_data), media_type="image/png")

@app.post("/resize")
async def resize(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...)
):
    image_data = await file.read()
    resized = resize_image(image_data, width, height)
    return StreamingResponse(io.BytesIO(resized), media_type="image/png")
