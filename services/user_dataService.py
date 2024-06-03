import os
import threading
from fastapi import Request, logger
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.email import sendEmailBlock, sendEmailRecovery, sendEmailUnBlock, sendEmailWelcome
from models.user_data import user_data
from repository.user_dataRepository import User_DataRepository
from azure.communication.email import EmailClient


class User_DataService():

    def __init__(self):
        self.repository = User_DataRepository()
    
    def getAllUsers(self, db: Session):
        return self.repository.get_all(db)
    
    def getUserLogin(self, db: Session,phone_id,phone_model,phone_brand, user: str, password: str):
        result,device,bloqueado=self.repository.get_user_login(db,phone_id,phone_model,phone_brand, user, password)
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
        
    def add_user(self, db: Session, user,pwd:str):
        user_in_data= jsonable_encoder(user)
        newuser =user_data(**user_in_data)
        newuser.pwd=pwd
        try:
            result= self.repository.add(newuser, db)
            if result:
                hiloemail = threading.Thread(target=sendEmailWelcome, args=(newuser.email,newuser.user_name))
                hiloemail.start()
            return True
        except:
            return None
        
    def recovery(self,db:Session, email:str,username:str,pwd:str):
        result=self.repository.find_user_by_email(db, email)
        #Compruebo que el email y el username coinciden
        if result.user_name!=username:
            return None
        if result is not None:
            entity={"pwd":pwd}
            self.repository.update(entity,result.id,db)
            hiloemail = threading.Thread(target=sendEmailRecovery, args=(result.email,result.user_name))
            hiloemail.start()
            return True
        return None
    
    def get_user(self, db: Session, id: str):
        return self.repository.get_user(db, id)
    
    def update_user(self, db: Session, id: str, user):
        user=jsonable_encoder(user)
        return self.repository.update(user, id, db)
    
    def update_user_good(self, db: Session, id: str, user,pwd:str):
        user=jsonable_encoder(user)
        # user.append({"pwd":pwd})
        user["pwd"]=pwd
        return self.repository.update(user, id, db)
    
    def delete_user(self, db: Session, id: str,dbmongo):
        #Borrar usuario
        user=self.repository.find_by_id(id, db)
        self.repository.permanent_delete(user, db)

        #Borrar sus chiks
        self.repository.delete_chiks_by_user(id, dbmongo)

        return True
    
        