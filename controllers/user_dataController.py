from typing import List
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user_data import user_data
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
	
	@router.get("/login",response_model=UserDataSchema,status_code=200)
	def UserLogin(self, email: str, password: str, db: Session = Depends(get_db)):
		result=self.service.getUserLogin(db, email, password)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return result
	
	@router.post("/register",response_model=UserDataSchema,status_code=201)
	def UserRegister(self, user: UserDataSchema, db: Session = Depends(get_db)):
		result= self.service.addUser(db, user)
		if result is None:
			raise HTTPException(status_code=400,detail="Not Created")
		return result
