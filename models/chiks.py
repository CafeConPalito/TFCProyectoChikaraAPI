from typing import List, Union
from datetime import date
import uuid
from pydantic import BaseModel

class Content(BaseModel):
    position: int
    content: str
    type: str

class Comment(BaseModel):
    user: uuid.UUID
    comment: str
    date: date

class Chiks(BaseModel):
    title: str
    author: uuid.UUID
    date: date
    likes: int
    status: str
    content: List[Content]
    comments: List[Comment]
    mencions: List[uuid.UUID]
