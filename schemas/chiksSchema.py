from typing import List, Optional, Union
from datetime import date
import uuid
from bson import ObjectId
from pydantic import BaseConfig, BaseModel, BaseSettings, Field

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
    value: Union[str, bytes]
    type: str

class Comment(BaseModel):
    user: uuid.UUID
    comment: str
    date: date

class chiksSchema(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    author: Optional[str]=None
    date: Optional[str]=None
    likes: Optional[int]
    isprivate: bool
    content: List[Content]
    comments: List[Comment]
    mencions: List[uuid.UUID]

