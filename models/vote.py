from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime, timezone

class Vote(Base):
    __tablename__ = "votes"

    vote_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user_id = Column(UUID(as_uuid=True), default=uuid.uuid7)

    option_id = Column(UUID(as_uuid=True), ForeignKey("options.option_id"))
    option = relationship("Option", back_populates="votes")
