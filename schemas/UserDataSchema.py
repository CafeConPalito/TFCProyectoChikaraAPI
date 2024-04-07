from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import uuid

class UserDataSchemaSend(BaseModel):
	id: Optional[uuid.UUID]
	user_name: Optional[str]
	email: Optional[str]
	pwd: Optional[str]
	first_name: Optional[str]
	first_last_name: Optional[str]
	second_last_name: Optional[str]
	birthdate: Optional[date]
	account_creation: Optional[datetime]
	is_premium: Optional[bool]
	
	class Config:
		orm_mode = True

class UserDataSchemaReceived(BaseModel):
	user_name: str
	email: str
	pwd: str
	first_name: str
	first_last_name: str
	second_last_name: Optional[str]
	birthdate: date
	is_premium: Optional[bool]
	
	class Config:
		orm_mode = True