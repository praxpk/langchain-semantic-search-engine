from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title="Semantic Search Engine API")
UPLOAD_DIR = Path("uploads")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/pdf/upload")
async def upload_pdf(file: UploadFile = File(...)) -> dict:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid4().hex}.pdf"
    destination = UPLOAD_DIR / safe_name
    destination.write_bytes(content)

    return {"filename": file.filename, "stored_as": safe_name, "bytes": len(content)}
