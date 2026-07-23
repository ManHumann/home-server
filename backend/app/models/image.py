from sqlalchemy import String, BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base

class Image(Base):
    __tablename__ = "images"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True
    )

    original_filename: Mapped[str] = mapped_column( String(255), nullable = False )
    stored_filename: Mapped[str] = mapped_column( String(255), nullable = False )
    file_path: Mapped[str] = mapped_column( String(255), nullable = False )
    mime_type: Mapped[str] = mapped_column( String(255), nullable = False )
    file_size: Mapped[int] = mapped_column( BigInteger , nullable = False )
    uploaded_at : Mapped[datetime] = mapped_column(DateTime, server_default=func.now() , nullable = False )
