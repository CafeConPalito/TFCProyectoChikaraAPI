from typing import List
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.UserDataSchema import UserDataSchema
from services.user_dataService import User_DataService
from config.db_depend import get_db


router= APIRouter()

@cbv(router)
class user_dataController:

	def __init__(self):
		self.service =  User_DataService()

	@router.get("/",response_model=List[UserDataSchema],status_code=200)
	def getAllUsers(self ,db: Session = Depends(get_db)):
		return self.service.getAllUsers(db)