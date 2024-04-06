
#import hashlib
from models.user_data import user_data
from models.user_log import user_log
from repository.AbstractRepository import AbstractRepository
from repository.user_logRepository import User_LogRepository


class User_DataRepository(AbstractRepository):
    def __init__(self):
        self.entity = user_data
        self.user_logRepository = User_LogRepository()

    # Sin cifrar a md5 la password
    def get_user_login(self, db, user: str, password: str):
        result = None
        if user[0]=="@": #Comprueba si el email empieza por @, si es así, es un username
            result= db.query(self.entity).filter(self.entity.user_name == user, self.entity.pwd == password).first()
            if result is not None:
                #Crea un nuevo objeto user_log con el id del usuario
                userlognew=user_log(id_user=result.id)
                #Añade un nuevo registro en la tabla user_log
                self.user_logRepository.add(userlognew,db)
                return result
            else:
                return None
            
        result= db.query(self.entity).filter(self.entity.email == user, self.entity.pwd == password).first()
        if result is not None:
                userlognew=user_log(id_user=result.id)
                self.user_logRepository.add(userlognew,db)
                return result
        else:
            return None
    
    # Con cifrado md5 en la password
    # No olvidar descomentar la importación de hashlib
    
    # def get_user_by_email(self, db, email: str, password: str):
    #     if email[0]=="@": #if email starts with @, it is a username
    #         return db.query(self.entity).filter(self.entity.user_name == email, self.entity.pwd == hashlib.md5(password.encode()).hexdigest()).first()
    #     return db.query(self.entity).filter(self.entity.email == email, self.entity.pwd == hashlib.md5(password.encode()).hexdigest()).first()
    
