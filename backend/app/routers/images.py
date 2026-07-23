from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import UploadFile, File

from app.database import get_db

from app.schemas.image import ImageResponse

from app.models.image import Image

from app.services import image_service

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
