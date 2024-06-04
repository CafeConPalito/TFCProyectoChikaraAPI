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
        
    @router.get("/block/{id}",response_model=str,status_code=200)
    def blockDevice(self,id:str, db: Session = Depends(get_db)):
        result=self.service.blockDevice(db,id)
        if result is None:
            raise HTTPException(status_code=404,detail="Not Found")
        return result
    
    @router.get("/unblock/{id}",response_model=str,status_code=200)
    def unblockDevice(self,id:str, db: Session = Depends(get_db)):
        result=self.service.unblockDevice(db,id)
        if result is None:
            raise HTTPException(status_code=404,detail="Not Found")
        return result