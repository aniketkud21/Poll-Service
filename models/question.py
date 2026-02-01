from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime, timezone

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    question_text = Column(String)
    order_index = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    poll_id = Column(UUID(as_uuid=True), ForeignKey("polls.poll_id"))
    poll = relationship("Poll", back_populates="questions")

    options = relationship("Option", back_populates="question")