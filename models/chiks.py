from typing import List, Optional, Union
from datetime import date
import uuid
from pydantic import BaseModel

class Content(BaseModel):
    position: int
    value: str
    type: str

class Comment(BaseModel):
    user: uuid.UUID
    comment: str
    date: date

class Chiks(BaseModel):
    _id: str
    title: str
    author: uuid.UUID
    author_name: str
    date: date
    likes: int
    isprivate: str
    content: List[Content]
    comments: List[Comment]
    mencions: List[uuid.UUID]
