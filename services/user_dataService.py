import os
import threading
from fastapi import Request, logger
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.email import sendEmail
from models.user_data import user_data
from repository.user_dataRepository import User_DataRepository
from azure.communication.email import EmailClient


class User_DataService():

    def __init__(self):
        self.repository = User_DataRepository()
    
    def getAllUsers(self, db: Session):
        return self.repository.get_all(db)
    
    def getUserLogin(self, db: Session,request: Request, user: str, password: str):
        result,control=self.repository.get_user_login(db,request, user, password)
        if control is not None:
            #Enviamos email de inicio de sesion
            hiloemail = threading.Thread(target=sendEmail, args=(result,control))
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
            return self.repository.add(newuser, db)
        except:
            return None
        