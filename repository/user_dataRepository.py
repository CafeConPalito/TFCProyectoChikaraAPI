
#import hashlib
from fastapi import Request
from models.user_data import user_data
from models.user_devices import user_devices
from models.user_log import user_log
from repository.AbstractRepository import AbstractRepository
from repository.user_logRepository import User_LogRepository
from repository.user_devicesRepository import user_devicesRepository


class User_DataRepository(AbstractRepository):
    def __init__(self):
        self.entity = user_data
        self.user_logRepository = User_LogRepository()
        self.user_devicesRepository = user_devicesRepository()

    # Sin cifrar a md5 la password
    def get_user_login(self, db,request: Request, user: str, password: str):
        result = None
        #Comprueba si el phone_id no está en la tabla user_devices
        device_db=db.query(user_devices).filter(user_devices.phone_id == request.headers.get("phone_id")).first()
        if device_db is None:
            if user[0]=="@": #Comprueba si el email empieza por @, si es así, es un username
                result= db.query(self.entity).filter(self.entity.user_name == user, self.entity.pwd == password).first()
                if result is not None:
                    #Crea un nuevo objeto user_log con el id del usuario
                    userlognew=user_log(id_user=result.id)
                    #Añade un nuevo registro en la tabla user_log
                    self.user_logRepository.add(userlognew,db)
                    #Crea un nuevo objeto user_devices con el phone_id y el id del usuario
                    userdevicesnew=user_devices(phone_id=request.headers.get("phone_id"),id_user=result.id,
                                                phone_model=request.headers.get("phone_model"),phone_brand=request.headers.get("phone_brand"))
                    #Añade un nuevo registro en la tabla user_devices
                    device=self.user_devicesRepository.add(userdevicesnew,db)
                    return result,device
                else:
                    return result,None
            else: #Si no es un username, es un email   
                result= db.query(self.entity).filter(self.entity.email == user, self.entity.pwd == password).first()
                if result is not None:
                    userlognew=user_log(id_user=result.id)
                    self.user_logRepository.add(userlognew,db)
                    #Crea un nuevo objeto user_devices con el phone_id y el id del usuario
                    userdevicesnew=user_devices(phone_id=request.headers.get("phone_id"),id_user=result.id,
                                                phone_model=request.headers.get("phone_model"),phone_brand=request.headers.get("phone_brand"))
                    #Añade un nuevo registro en la tabla user_devices
                    device=self.user_devicesRepository.add(userdevicesnew,db)
                    return result,device
                else:
                    return result,None
        else:
            if device_db.block==False:
                if user[0]=="@": #Comprueba si el email empieza por @, si es así, es un username
                    result= db.query(self.entity).filter(self.entity.user_name == user, self.entity.pwd == password).first()
                    if result is not None:
                        #Crea un nuevo objeto user_log con el id del usuario
                        userlognew=user_log(id_user=result.id)
                        #Añade un nuevo registro en la tabla user_log
                        self.user_logRepository.add(userlognew,db)

                    return result,None
                else: #Si no es un username, es un email   
                    result= db.query(self.entity).filter(self.entity.email == user, self.entity.pwd == password).first()
                    if result is not None:
                        userlognew=user_log(id_user=result.id)
                        self.user_logRepository.add(userlognew,db)
                        #Crea un nuevo objeto user_devices con el phone_id y el id del usuario
                        userdevicesnew=user_devices(phone_id=request.headers.get("phone_id"),id_user=result.id,
                                                    phone_model=request.headers.get("phone_model"),phone_brand=request.headers.get("phone_brand"))
                        #Añade un nuevo registro en la tabla user_devices
                        device=self.user_devicesRepository.add(userdevicesnew,db)
                    return result,None
            return result,None
        
    def find_user_by_email(self, db, email: str):
        return db.query(self.entity).filter(self.entity.email == email).first()
    
    def find_user_by_name(self, db, user: str):
        return db.query(self.entity).filter(self.entity.user_name == user).first()
    
    # Con cifrado md5 en la password
    # No olvidar descomentar la importación de hashlib
    
    # def get_user_by_email(self, db, email: str, password: str):
    #     if email[0]=="@": #if email starts with @, it is a username
    #         return db.query(self.entity).filter(self.entity.user_name == email, self.entity.pwd == hashlib.md5(password.encode()).hexdigest()).first()
    #     return db.query(self.entity).filter(self.entity.email == email, self.entity.pwd == hashlib.md5(password.encode()).hexdigest()).first()
    
