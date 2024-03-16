from sqlalchemy.orm import Session
from repository.user_dataRepository import User_DataRepository


class User_DataService():

    def __init__(self):
        self.repository = User_DataRepository()
    
    def getAllUsers(self, db: Session):
        return self.repository.get_all(db)