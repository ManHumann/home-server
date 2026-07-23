from datetime import datetime

from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: int
    original_filename: str
    stored_filename: str
    mime_type: str
    file_size: int
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }
