from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from PIL import Image
from io import BytesIO

app = FastAPI(
    title="BGErase API",
    description="BGErase Background Removal API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "BGErase API",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG and WEBP images are supported."
        )

    data = await file.read()

    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Image size must be below 10 MB."
        )

    try:
        image = Image.open(BytesIO(data))
        image.verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file."
        )

    return {
        "status": "success",
        "message": "Image received successfully.",
        "filename": file.filename
  }
