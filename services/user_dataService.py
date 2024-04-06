from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from models.user_data import user_data
from repository.user_dataRepository import User_DataRepository


class User_DataService():

    def __init__(self):
        self.repository = User_DataRepository()
    
    def getAllUsers(self, db: Session):
        return self.repository.get_all(db)
    
    def getUserLogin(self, db: Session, user: str, password: str):
        return self.repository.get_user_login(db, user, password)
    
    def addUser(self, db: Session, user):
        user_in_data= jsonable_encoder(user)
        newuser =user_data(**user_in_data)
        try:
            return self.repository.add(newuser, db)
        except:
            return None
        