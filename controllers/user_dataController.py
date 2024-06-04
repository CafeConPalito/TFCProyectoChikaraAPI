import datetime
from typing import List
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response
from sqlalchemy.orm import Session

from azure.communication.email import EmailClient
from config.jwt import generate_token, get_user_id
from decorators.decorator import security, oauth2_scheme
from models.user_data import user_data
from schemas.UserDataSchema import UserDataSchemaReceived, UserDataSchemaSend
from services.user_dataService import User_DataService
from config.db_depend import get_db
from pymongo.collection import Collection
from config.db_mongo import get_collection


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
	def UserLogin(self, user: str, password: str,phone_id=Header(),phone_model=Header(),phone_brand=Header(), db: Session = Depends(get_db)):
		result=self.service.getUserLogin(db,phone_id,phone_model,phone_brand, user, password)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return generate_token(result.dict())
	
	@router.get("/search",response_model=bool,status_code=200)
	def search(self,user:str, db: Session = Depends(get_db)):
		#Buscar por usarname
		result=self.service.findUserByName(db, user)
		#Si no se encuentra buscar por email
		if result is None:
			result=self.service.findUserByEmail(db, user)
			#Si no se encuentra lanzar error 404 Not found
			if result is None:
				raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.get("/searchuser",response_model=bool,status_code=200)
	def searchUser(self,user:str, db: Session = Depends(get_db)):
		#Buscar por usarname
		result=self.service.findUserByName(db, user)
		#Si no se encuentra buscar por email
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.get("/searchemail",response_model=bool,status_code=200)
	def searchEmail(self,email:str, db: Session = Depends(get_db)):
		#Buscar por usarname
		result=self.service.findUserByEmail(db, email)
		#Si no se encuentra buscar por email
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True

	@router.post("/register",response_model=bool,status_code=201)
	def UserRegister(self, user: UserDataSchemaReceived, db: Session = Depends(get_db)):
		result= self.service.addUser(db, user)
		if result is None:
			raise HTTPException(status_code=400,detail="Not Created")
		return True
	
	@router.put("/recovery",response_model=bool,status_code=200)
	def recovery(self,email:str,username:str,pwd:str, db: Session = Depends(get_db)):
		#Buscar por email
		result=self.service.recovery(db, email,username,pwd)
		#Si no se encuentra lanzar error 404 Not found
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.get("/getuser",response_model=UserDataSchemaSend,status_code=200)
	@security()
	def get_user(self,request:Request, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
		id_user= get_user_id(request.headers["Authorization"].split(" ")[1])
		result=self.service.get_user(db, id_user)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return result
	
	@router.put("/update",response_model=bool,status_code=200)
	@security()
	def update_user(self,request:Request, user: UserDataSchemaReceived, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
		id_user= get_user_id(request.headers["Authorization"].split(" ")[1])
		result=self.service.update_user(db, id_user, user)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.delete("/delete",response_model=bool,status_code=200)
	@security()
	def delete_user(self,request:Request, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),dbmongo:Collection = Depends(get_collection)):
		id_user= get_user_id(request.headers["Authorization"].split(" ")[1])
		result=self.service.delete_user(db, id_user,dbmongo)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
