from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from enum import Enum

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    domain: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    status: Optional[str] = Field(default="pending", max_length=20)


class UserRead(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    MATRIX_ONE = "matrix_one"
    MATRIX_ANY = "matrix_any"
    OPEN_TEXT = "open_text"


class OptionCreate(BaseModel):
    text: str

class QuestionCreate(BaseModel):
    text: str
    type: QuestionType
    que_order:int
    options: Optional[List[OptionCreate]] = None  # For single/multiple choice
    matrix_rows: Optional[List[str]] = None       # For matrix questions
    matrix_cols: Optional[List[str]] = None       # For matrix questions

class OptionRead(BaseModel):
    id: int
    text: str


class QuestionRead(BaseModel):
    id: int
    que_order:int
    text: str
    type: QuestionType
    options: Optional[List[OptionRead]] = None  # For single/multiple choice
    matrix_rows: Optional[List[str]] = None       # For matrix questions
    matrix_cols: Optional[List[str]] = None 
    model_config = ConfigDict(from_attributes=True)