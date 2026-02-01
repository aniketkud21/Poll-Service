from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime, timezone

class Poll(Base):
    __tablename__ = "polls"

    poll_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    title = Column(String)
    description = Column(String)
    type = Column(String)
    status = Column(String)
    ends_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    questions = relationship("Question", back_populates="poll")

