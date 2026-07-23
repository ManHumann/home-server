from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi import UploadFile, File

from app.database import get_db


from app.models.image import Image

from app.services import image_service

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

@router.get("/")
def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()

    return images


@router.post("/")
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    result = image_service.upload_image(file, db)

    return result
