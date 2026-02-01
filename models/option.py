from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime, timezone

class Option(Base):
    __tablename__ = "options"

    option_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    option_text = Column(String)
    order_index = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.question_id"))
    question = relationship("Question", back_populates="options")
    
    votes = relationship("Vote", back_populates="option")