import base64
from datetime import datetime
import os
import uuid
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from config.blob import upload_blob
from repository.chiksRepository import chiksRepository
from pymongo.collection import Collection
from loguru import logger as Logger

from schemas.chiksSchema import Comment, chiksSchema


class chiksService():

    def __init__(self):
        self.repository = chiksRepository()
    
    # def getAllChiks(self, db: Collection):
    #     return self.repository.get_all(db)
    
    def getTopChiks(self, db: Collection):
        return self.repository.get_top_chiks(db)
    
    def getChikByAuthor(self, db: Collection, id: str):
        return self.repository.get_chik_by_author(db, id)
    
    def uploadChik(self, db: Collection, chik:chiksSchema):
        load_dotenv()
        STORAGE_URL = os.getenv("STORAGE_URL")
        #Generar un id unico
        chik.id=str(uuid.uuid4())
        #Insertar la fecha actual
        chik.date=datetime.now().date()
        #Poner el contador de likes en 0
        chik.likes=0
        Logger.info(chik)
        for content in chik.content:
            if content.type=="TYPE_IMG":
                Logger.info(content)
                Logger.info(f"Subiendo imagen {content.position} a Azure Blob Storage")
                Logger.info(f"Guardando imagen en {STORAGE_URL}/{chik.id}/{content.position}.webp")
                #Obtener valor de la imagen en base64 y subir a Azure Blob Storage
                upload_blob(f"{chik.id}/{content.position}.webp","image/webp",base64.b64decode(content.value))
                content.value=f"{STORAGE_URL}/{chik.id}/{content.position}.webp"
                Logger.info(content)

                #Convertir a bytes
            elif content.type=="TYPE_TEXT":
                continue

        db.insert_one(jsonable_encoder(chik))
        
        return db.find_one({"_id":chik.id})
    
    def addComment(self, db: Collection, id:str,user_id:str, comment:Comment):
        comment.user=user_id
        comment.date=str(datetime.now().date())
        db.update_one({"_id":id}, {"$push": {"comments": comment.dict()}})
        return db.find_one({"_id":id})
    
    def addMencion(self, db: Collection, id:str, mencion:str):
        db.update_one({"_id":id}, {"$push": {"mencions": mencion}})
        return db.find_one({"_id":id})
    
    def addLike(self, db: Collection, id:str):
        db.update_one({"_id":id}, {"$inc": {"likes": 1}})
        return db.find_one({"_id":id})
    
    def deleteLike(self, db: Collection, id:str):
        db.update_one({"_id":id}, {"$inc": {"likes": -1}})
        return db.find_one({"_id":id})