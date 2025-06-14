import os
import io
import logging
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.utils import remove_background, resize_image

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Image Tools API is running"}

# API endpoints
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        output_data = remove_background(image_data)
        return StreamingResponse(io.BytesIO(output_data), media_type="image/png")
    except Exception as e:
        logger.error(f"Error removing background: {e}")
        return {"error": str(e)}

@app.post("/resize")
async def resize(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...)
):
    try:
        image_data = await file.read()
        resized = resize_image(image_data, width, height)
        return StreamingResponse(io.BytesIO(resized), media_type="image/png")
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        return {"error": str(e)}

# Mount static files last to avoid conflicts
try:
    if os.path.exists("static"):
        app.mount("/", StaticFiles(directory="static", html=True), name="static")
        logger.info("Static files mounted successfully")
    else:
        logger.warning("Static directory not found")
        
        @app.get("/")
        async def root():
            return {"message": "Image Tools API is running", "endpoints": ["/health", "/remove-bg", "/resize"]}
except Exception as e:
    logger.error(f"Error mounting static files: {e}")
    
    @app.get("/")
    async def root():
        return {"message": "Image Tools API is running", "endpoints": ["/health", "/remove-bg", "/resize"]}

# Startup event
@app.on_event("startup")
async def startup_event():
    port = os.environ.get("PORT", "10000")
    logger.info(f"Starting app on port {port}")
    logger.info("Image Tools API startup complete")

# Main execution per Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting server on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)