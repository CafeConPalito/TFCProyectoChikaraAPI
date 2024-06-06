from typing import List, Optional, Union
from datetime import date
import uuid
from bson import ObjectId
from pydantic import BaseConfig, BaseModel, BaseSettings, Field

class Content(BaseModel):
    position: int
    value: Union[str, bytes]
    type: str

class Comment(BaseModel):
    user: Optional[str]
    comment: str
    date: Optional[str]=None

class chiksSchema(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    author: Optional[str]=None
    author_name: Optional[str]=None
    date: Optional[str]=None
    likes: Optional[int]
    isprivate: bool
    content: List[Content]
    comments: List[Comment]
    mencions: List[str]

