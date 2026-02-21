from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from uuid import UUID


# --------------------
# Enums
# --------------------

class PollType(str, Enum):
    POLL = "POLL"
    SURVEY = "SURVEY"


class PollStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class QuestionType(str, Enum):
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTI_CHOICE = "MULTI_CHOICE"


# --------------------
# Option Schemas
# --------------------

class OptionCreate(BaseModel):
    option_text: str = Field(..., min_length=1)
    order_index: int = Field(..., ge=1)

    model_config = {
        "extra": "forbid"
    }

class OptionUpdate(BaseModel):
    option_id: Optional[UUID] = None
    option_text: str
    order_index: int = Field(..., ge=1)

# --------------------
# Question Schemas
# --------------------

class QuestionCreate(BaseModel):
    question_text: str = Field(..., min_length=1)
    question_type: QuestionType
    order_index: int = Field(..., ge=1)
    options: List[OptionCreate] = Field(..., min_length=2)

    @field_validator("options")
    @classmethod
    def no_duplicate_option_texts(cls, options):
        texts = [opt.option_text.strip().lower() for opt in options]
        if len(texts) != len(set(texts)):
            raise ValueError("Duplicate option_text values are not allowed")
        return options

    model_config = {
        "extra": "forbid"
    }

class QuestionUpdate(BaseModel):
    question_id: Optional[UUID] = None
    question_text: str
    question_type: str
    order_index: int = Field(..., ge=1)
    options: List[OptionUpdate] = Field(..., min_length=2)

    @field_validator("options")
    @classmethod
    def no_duplicate_option_texts(cls, options):
        texts = [opt.option_text.strip().lower() for opt in options]
        if len(texts) != len(set(texts)):
            raise ValueError("Duplicate option_text values are not allowed")
        return options


# --------------------
# Poll Schemas
# --------------------

DEFAULT_POLL_DURATION_DAYS = 7

class PollCreate(BaseModel):
    """
    Poll creation contract.

    Design notes:
    - Nested objects are explicit to avoid positional coupling.
    - Ordering is represented as data (`order_index`).
    - Defaults and validation are enforced at the API boundary.
    """
    
    title: str = Field(..., min_length=1)
    poll_type: PollType
    description: Optional[str] = None
    status: PollStatus = PollStatus.DRAFT
    ends_at: Optional[datetime] = None
    questions: List[QuestionCreate] = Field(..., min_length=1)

    @field_validator("ends_at", mode="before")
    @classmethod
    def set_default_ends_at(cls, value):
        if value is None:
            return datetime.now(timezone.utc) + timedelta(days=DEFAULT_POLL_DURATION_DAYS)
        return value

    model_config = {"extra": "forbid"}

class PollUpdate(BaseModel):
    title: Optional[str] = None
    poll_type: Optional[PollType] = None
    description: Optional[str] = None
    status: Optional[PollStatus] = None
    ends_at: Optional[datetime] = None
    questions: List[QuestionUpdate]