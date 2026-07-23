from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import UploadFile, File

from app.database import get_db

from app.schemas.image import ImageResponse

from app.models.image import Image

from app.services import image_service

from fastapi.responses import FileResponse
from fastapi import HTTPException
from pathlib import Path


router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

@router.get("/", response_model=list[ImageResponse])
def get_images(db: Session = Depends(get_db)):
    return db.query(Image).all()

@router.post("/", response_model=ImageResponse)
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
    ):
    return image_service.upload_image(file, db)

@router.get("/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == image_id).first()

    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(
        image.file_path,
        media_type=image.mime_type,
        #filename=image.original_filename
    )
