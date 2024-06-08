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
from services.user_devicesService import User_DevicesService

router= APIRouter()

@cbv(router)
class user_devicesController:

    def __init__(self):
        self.service =  User_DevicesService()
        
    @router.get("/block/{id}",response_model=str,status_code=200,summary="Bloquear dispositivo")
    def blockDevice(self,id:str, db: Session = Depends(get_db)):
        """
        # Bloquear dispositivo

        ## Args:
            id (query|str): Id del dispositivo
        
        ## Raises:
            HTTPException(404): No se encontró el dispositivo
        
        ## Returns:
            str: HTML de confirmación
        """
        result=self.service.blockDevice(db,id)
        if result is None:
            raise HTTPException(status_code=404,detail="Not Found")
        return result
    
    @router.get("/unblock/{id}",response_model=str,status_code=200,summary="Desbloquear dispositivo")
    def unblockDevice(self,id:str, db: Session = Depends(get_db)):
        """
        # Desbloquear dispositivo

        ## Args:
            id (query|str): Id del dispositivo
        
        ## Raises:
            HTTPException(404): No se encontró el dispositivo
        
        ## Returns:
            str: HTML de confirmación
        """
        result=self.service.unblockDevice(db,id)
        if result is None:
            raise HTTPException(status_code=404,detail="Not Found")
        return result