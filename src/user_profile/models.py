import enum
from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Boolean, DateTime, Text, UniqueConstraint, func,Enum
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base
from datetime import datetime, timezone, timedelta
import uuid
from sqlalchemy.orm import relationship

# IST is UTC+5:30
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

def generate_uuid():
    return str(uuid.uuid4())


class BaseModel(Base):
    """Base model with audit fields (created_at, updated_at, created_by, updated_by, is_deleted)"""
    __abstract__ = True
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=get_ist_now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=get_ist_now, onupdate=get_ist_now, server_default=func.now())
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")


class UserProfile(BaseModel):
    __tablename__ = "users_profile"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    username = Column(String, nullable=False)

class QuestionType(str, enum.Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    MATRIX_ONE = "matrix_one"
    MATRIX_ANY = "matrix_any"
    OPEN_TEXT = "open_text"

class Question(BaseModel):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    que_order = Column(Integer, nullable=False)
    # Relationship to options (empty for open_text)
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan",lazy="selectin")

    # # For matrix questions, rows and columns
    matrix_rows = Column(JSON, nullable=True)
    matrix_cols = Column(JSON, nullable=True)

class QuestionOption(BaseModel):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    text = Column(String, nullable=False)
    question = relationship("Question", back_populates="options")

class UserAnswer(BaseModel):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))

    # Stores answer data dynamically:
    # - Single choice: option_id (int)
    # - Multiple choice: option_ids ([int])
    # - Matrix: dict {"row": [selected columns]} or {"row": selected_col}
    # - Open text: text
    answer_data = Column(JSON, nullable=False)

    question = relationship("Question")
