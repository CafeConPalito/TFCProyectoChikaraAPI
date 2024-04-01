from typing import List, Union
from datetime import date
import uuid
from pydantic import BaseModel

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
    content: str
    type: str

class Comment(BaseModel):
    user: uuid.UUID
    comment: str
    date: date

class chiksSchema(BaseModel):
    _id: str
    title: str
    author: uuid.UUID
    date: date
    likes: int
    status: str
    content: List[Content]
    comments: List[Comment]
    mencions: List[uuid.UUID]
