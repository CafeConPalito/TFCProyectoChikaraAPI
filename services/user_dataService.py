import os
import threading
from fastapi import Request, logger
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.email import sendEmailBlock, sendEmailUnBlock, sendEmailWelcome
from models.user_data import user_data
from repository.user_dataRepository import User_DataRepository
from azure.communication.email import EmailClient


class User_DataService():

    def __init__(self):
        self.repository = User_DataRepository()
    
    def getAllUsers(self, db: Session):
        return self.repository.get_all(db)
    
    def getUserLogin(self, db: Session,request: Request, user: str, password: str):
        result,device,bloqueado=self.repository.get_user_login(db,request, user, password)
        if bloqueado:
            hiloemail = threading.Thread(target=sendEmailUnBlock, args=(result,device))
            hiloemail.start()
            return None
        if device is not None:
            #Enviamos email de inicio de sesion
            hiloemail = threading.Thread(target=sendEmailBlock, args=(result,device))
            hiloemail.start()
        
        return result
    
    def findUserByEmail(self, db: Session, email: str):
        return self.repository.find_user_by_email(db, email)
    
    def findUserByName(self, db: Session, user: str):
        return self.repository.find_user_by_name(db, user)
    
    def addUser(self, db: Session, user):
        user_in_data= jsonable_encoder(user)
        newuser =user_data(**user_in_data)
        try:
            result= self.repository.add(newuser, db)
            if result:
                hiloemail = threading.Thread(target=sendEmailWelcome, args=(newuser.email,newuser.user_name))
                hiloemail.start()
            return True
        except:
            return None
        