# app/database/models.py

from sqlalchemy import Column, Text
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base

from datetime import datetime

Base = declarative_base()


class Claim(Base):

    __tablename__ = "claims_master"

    claim_id = Column(
        String,
        primary_key=True
    )

    file_key = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    created_date = Column(
        DateTime,
        default=datetime.utcnow
    )
    extracted_text = Column(
        Text,
        nullable=True
    )

    extraction_status = Column(
        String,
        nullable=True
    )