
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
    def get_user_login(self, db,phone_id,phone_model,phone_brand, user: str, password: str):
        result = None
        device = None
        
        if user[0]=="@": #Comprueba si el email empieza por @, si es así, es un username
            result= db.query(self.entity).filter(self.entity.user_name == user, self.entity.pwd == password).first()
            if result:
                #Crea un nuevo objeto user_log con el id del usuario
                userlognew=user_log(id_user=result.id)
                #Añade un nuevo registro en la tabla user_log
                self.user_logRepository.add(userlognew,db)

                #Comprueba si el phone_id no está en la tabla user_devices
                device_db=db.query(user_devices).filter(user_devices.phone_id == phone_id).filter(user_devices.id_user==result.id).first()

                if device_db is None:
                    #Crea un nuevo objeto user_devices con el phone_id y el id del usuario
                    userdevicesnew=user_devices(phone_id=phone_id,id_user=result.id,
                                                phone_model=phone_model,phone_brand=phone_brand)
                    #Añade un nuevo registro en la tabla user_devices
                    device=self.user_devicesRepository.add(userdevicesnew,db)
                    return result,device,False
                else:
                    #Comprueba si el dispositivo está bloqueado
                    if device_db.block==True:
                        return result,device_db,True
                    return result,None,False
            else:
                return None,None,False

        else:
            result= db.query(self.entity).filter(self.entity.email == user, self.entity.pwd == password).first()
            if result:
                #Crea un nuevo objeto user_log con el id del usuario
                userlognew=user_log(id_user=result.id)
                #Añade un nuevo registro en la tabla user_log
                self.user_logRepository.add(userlognew,db)

                #Comprueba si el phone_id no está en la tabla user_devices
                device_db=db.query(user_devices).filter(user_devices.phone_id == phone_id).filter(user_devices.id_user==result.id).first()

                if device_db is None:
                    #Crea un nuevo objeto user_devices con el phone_id y el id del usuario
                    userdevicesnew=user_devices(phone_id=phone_id,id_user=result.id,
                                                phone_model=phone_model,phone_brand=phone_brand)
                    #Añade un nuevo registro en la tabla user_devices
                    device=self.user_devicesRepository.add(userdevicesnew,db)
                    return result,device,False
                else:
                    #Comprueba si el dispositivo está bloqueado
                    if device_db.block==True:
                        return result,device_db,True
                    return result,None,False
            else:
                return None,None,False

   
    def find_user_by_email(self, db, email: str):
        return db.query(self.entity).filter(self.entity.email == email).first()
    
    def find_user_by_name(self, db, user: str):
        return db.query(self.entity).filter(self.entity.user_name == user).first()
    
    def get_user(self, db, id: str):
        return db.query(self.entity).filter(self.entity.id == id).first()
    
    def delete_chiks_by_user(self, id, dbmongo):
        return dbmongo.delete_many({"author":id})
