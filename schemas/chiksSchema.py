from typing import List, Optional, Union
from datetime import date
import uuid
from bson import ObjectId
from pydantic import BaseModel, BaseSettings, Field

# def chikSchema(item)->dict:
#     return {
#         "id": str(item["_id"]),
#         "title": item["title"],
#         "author": str(item["author"]),
#         "date": item["date"],
#         "likes": item["likes"],
#         "status": item["status"],
#         "content": item["content"],
#         "comments": item["comments"],
#         "mencions": item["mencions"]
#     }

# def chiksSchema(item)->list:
#     return [chikSchema(item) for item in item]

class Content(BaseModel):
    position: int
    value: str
    type: str

class Comment(BaseModel):
    user: uuid.UUID
    comment: str
    date: date

class chiksSchema(BaseModel):
    _id: str
    id: str
    title: str
    author: Optional[uuid.UUID]
    date: Optional[date]
    likes: int
    isprivate: bool
    content: List[Content]
    comments: List[Comment]
    mencions: List[uuid.UUID]

