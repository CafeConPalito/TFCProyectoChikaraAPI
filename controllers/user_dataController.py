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
 
	@router.get("/login",response_model=str,status_code=200,summary="Iniciar sesión")
	def UserLogin(self, user: str, password: str,phone_id=Header(),phone_model=Header(),phone_brand=Header(), db: Session = Depends(get_db)):
		"""
		# Iniciar sesión

		## Args:
			phone_id (Header|str): Id del telefono
			phone_model (Header|str): Modelo del telefono
			phone_brand (Header|str): Marca del telefono
			user (query|str): Nombre de usuario o email
			password (query|str): Contraseña

		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			str: JWT token
		"""

		result=self.service.getUserLogin(db,phone_id,phone_model,phone_brand, user, password)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return generate_token(result.dict())
	
	@router.get("/search",response_model=bool,status_code=200,summary="Buscar usuario")
	def search(self,user:str, db: Session = Depends(get_db)):
		"""
		# Buscar usuario por nombre de usuario o email

		## Args:
			user (query|str): Nombre de usuario o email
		
		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			bool: True si se encontró el usuario
		"""

		#Buscar por usarname
		result=self.service.findUserByName(db, user)
		#Si no se encuentra buscar por email
		if result is None:
			result=self.service.findUserByEmail(db, user)
			#Si no se encuentra lanzar error 404 Not found
			if result is None:
				raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.get("/searchuser",response_model=bool,status_code=200,summary="Buscar usuario por nombre de usuario")
	def searchUser(self,user:str, db: Session = Depends(get_db)):
		"""
		# Buscar usuario por nombre de usuario

		## Args:
			user (query|str): Nombre de usuario
		
		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			bool: True si se encontró el usuario
		"""
		#Buscar por usarname
		result=self.service.findUserByName(db, user)
		#Si no se encuentra buscar por email
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.get("/searchemail",response_model=bool,status_code=200,summary="Buscar usuario por email")
	def searchEmail(self,email:str, db: Session = Depends(get_db)):
		"""
		# Buscar usuario por email

		## Args:
			email (query|str): Email
		
		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			bool: True si se encontró el usuario
		"""

		#Buscar por usarname
		result=self.service.findUserByEmail(db, email)
		#Si no se encuentra buscar por email
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True

	@router.post("/register",response_model=bool,status_code=201,summary="Registrar usuario")
	def UserRegister(self, user: UserDataSchemaReceived, db: Session = Depends(get_db)):
		"""
		# Registrar usuario

		## Args:
			user (body|UserDataSchemaReceived): Datos del usuario
		
		## Raises:
			HTTPException(400): No se pudo crear el usuario

		## Returns:
			bool: True si se creó el usuario
		"""
		result= self.service.addUser(db, user)
		if result is None:
			raise HTTPException(status_code=400,detail="Not Created")
		return True
	
	@router.put("/recovery",response_model=bool,status_code=200,summary="Recuperar contraseña")
	def recovery(self,email:str,username:str,pwd:str, db: Session = Depends(get_db)):
		"""
		# Recuperar contraseña

		## Args:
			email (query|str): Email
			username (query|str): Nombre de usuario
			pwd (query|str): Nueva Contraseña

		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			bool: True si se recuperó la contraseña
		"""
		#Buscar por email
		result=self.service.recovery(db, email,username,pwd)
		#Si no se encuentra lanzar error 404 Not found
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.get("/getuser",response_model=UserDataSchemaSend,status_code=200,summary="Obtener usuario")
	@security()
	def get_user(self,request:Request, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
		"""
		# Obtener usuario de la sesión

		## Args:
			token (Header|authentication): JWT token
		
		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			UserDataSchemaSend: Datos del usuario
		"""
		id_user= get_user_id(request.headers["Authorization"].split(" ")[1])
		result=self.service.get_user(db, id_user)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return result
	
	@router.put("/update",response_model=bool,status_code=200,summary="Actualizar usuario")
	@security()
	def update_user(self,request:Request, user: UserDataSchemaReceived, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
		"""
		# Actualizar usuario de la sesión

		## Args:
			token (Header|authentication): JWT token
			user (body|UserDataSchemaReceived): Datos del usuario
		
		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			bool: True si se actualizó el usuario
		"""

		id_user= get_user_id(request.headers["Authorization"].split(" ")[1])
		result=self.service.update_user(db, id_user, user)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
	@router.delete("/delete",response_model=bool,status_code=200,summary="Eliminar usuario")
	@security()
	def delete_user(self,request:Request, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),dbmongo:Collection = Depends(get_collection)):
		"""
		# Eliminar usuario de la sesión

		## Args:
			token (Header|authentication): JWT token
		
		## Raises:
			HTTPException(404): No se encontró el usuario
		
		## Returns:
			bool: True si se eliminó el usuario
		"""
		id_user= get_user_id(request.headers["Authorization"].split(" ")[1])
		result=self.service.delete_user(db, id_user,dbmongo)
		if result is None:
			raise HTTPException(status_code=404,detail="Not Found")
		return True
	
