import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import config
from app.models.image import Image


def upload_image(file: UploadFile, db: Session):

    # Get file extension (.png, .jpg, etc.)
    extension = Path(file.filename).suffix

    # Generate unique filename
    stored_filename = f"{uuid.uuid4()}{extension}"

    # Full path where image will be stored
    destination = Path(config.UPLOAD_DIR) / stored_filename

    # Save image to filesystem
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create Image object
    image = Image(
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(destination),
        mime_type=file.content_type,
        file_size=destination.stat().st_size
    )

    # Save metadata to PostgreSQL
    db.add(image)
    db.commit()
    db.refresh(image)

    # Return response
    return image
