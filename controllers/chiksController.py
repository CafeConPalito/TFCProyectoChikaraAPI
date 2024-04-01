from typing import List
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection

from config.db_mongo import get_collection

from schemas.chiksSchema import chiksSchema
from services.chiksService import chiksService

router= APIRouter()

@cbv(router)
class chiksController:

    def __init__(self):
        self.service =  chiksService()

    # @router.get("/",response_model=List[chiksSchema],status_code=200)
    # def getAllChiks(self ,db: Collection = Depends(get_collection)):
    #     return [chiks for chiks in self.service.getAllChiks(db)]

    @router.get("/",response_model=List[chiksSchema],status_code=200)
    def getTopChiks(self, db: Collection = Depends(get_collection)):
        return [chiks for chiks in self.service.getTopChiks(db)]
    
    @router.get("/{id}",response_model=List[chiksSchema],status_code=200)
    def getChikByAuthor(self, id: str, db: Collection = Depends(get_collection)):
        chiks = self.service.getChikByAuthor(db, id)
        if chiks:
            return [chik for chik in chiks]
        raise HTTPException(status_code=404, detail="Chiks not found")

	