from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from rembg import remove

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
    return {
        "status": "healthy"
    }


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
        result = remove(data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Background removal failed: {str(e)}"
        )

    return Response(
        content=result,
        media_type="image/png",
        headers={
            "Content-Disposition": "attachment; filename=bgerase-result.png"
        }
                )
