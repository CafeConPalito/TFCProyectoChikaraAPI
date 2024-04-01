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