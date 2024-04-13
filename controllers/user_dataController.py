import datetime
from typing import List
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from azure.communication.email import EmailClient
from config.jwt import generate_token
from middlewares.verify_token_route import VerifyTokenRoute
from models.user_data import user_data
from schemas.UserDataSchema import UserDataSchemaReceived, UserDataSchemaSend
from services.user_dataService import User_DataService
from config.db_depend import get_db


router= APIRouter()

@cbv(router)
class user_dataController:

	def __init__(self):
		self.service =  User_DataService()

	# @router.get("/",response_model=List[UserDataSchema],status_code=200)
	# def getAllUsers(self ,db: Session = Depends(get_db)):
	# 	return self.service.getAllUsers(db)
	
	# @router.get("/login",response_model=UserDataSchema,status_code=200)
	# def UserLogin(self, email: str, password: str, db: Session = Depends(get_db)):
	# 	result=self.service.getUserLogin(db, email, password)
	# 	if result is None:
	# 		raise HTTPException(status_code=404,detail="Not Found")
	# 	return result
 
	@router.get("/login",response_model=str,status_code=200)
	def UserLogin(self,request:Request, user: str, password: str, db: Session = Depends(get_db)):
		# phone_id = request.headers.get("phone_id")
		# phone_model = request.headers.get("phone_model")
		# phone_brand = request.headers.get("phone_brand")
		result=self.service.getUserLogin(db,request, user, password)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return generate_token(result.dict())
	
	@router.get("/searchemail",response_model=bool,status_code=200)
	def searchEmail(self,email:str, db: Session = Depends(get_db)):
		result=self.service.findUserByEmail(db, email)
		return True if result else False

	
	@router.get("/searchuser",response_model=bool,status_code=200)
	def searchUser(self,user:str, db: Session = Depends(get_db)):
		result=self.service.findUserByName(db, user)
		return True if result else False
	
	@router.post("/register",response_model=UserDataSchemaSend,status_code=201)
	def UserRegister(self, user: UserDataSchemaReceived, db: Session = Depends(get_db)):
		result= self.service.addUser(db, user)
		if result is None:
			raise HTTPException(status_code=400,detail="Not Created")
		return result
