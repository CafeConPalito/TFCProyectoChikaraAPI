from datetime import datetime
import uuid
from fastapi.encoders import jsonable_encoder
from repository.chiksRepository import chiksRepository
from pymongo.collection import Collection


class chiksService():

    def __init__(self):
        self.repository = chiksRepository()
    
    # def getAllChiks(self, db: Collection):
    #     return self.repository.get_all(db)
    
    def getTopChiks(self, db: Collection):
        return self.repository.get_top_chiks(db)
    
    def getChikByAuthor(self, db: Collection, id: str):
        return self.repository.get_chik_by_author(db, id)
    
    def uploadChik(self, db: Collection, chik, files: list):
        #Generar un id unico
        chik.id=str(uuid.uuid4())
        #Insertar la fecha actual
        chik.date=datetime.now().date()
        #Poner el contador de likes en 0
        chik.likes=0
        db.insert_one(jsonable_encoder(chik))
        
        return db.find_one({"_id":chik.id})