from typing import List, Union
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo.collection import Collection

from config.db_mongo import get_collection

from config.jwt import get_user_id
from middlewares.verify_token_route import VerifyTokenRoute
from schemas.chiksSchema import chiksSchema
from services.chiksService import chiksService

router= APIRouter(route_class=VerifyTokenRoute)

@cbv(router)
class chiksController:

    def __init__(self):
        self.service =  chiksService()

    # @router.get("/",response_model=List[chiksSchema],status_code=200)
    # def getAllChiks(self ,db: Collection = Depends(get_collection)):
    #     return [chiks for chiks in self.service.getAllChiks(db)]

    @router.get("/top",response_model=List[chiksSchema],status_code=200)
    def getTopChiks(self, db: Collection = Depends(get_collection)):
        return [chiks for chiks in self.service.getTopChiks(db)]
    
    @router.get("/you",response_model=List[chiksSchema],status_code=200)
    def getChikByAuthor(self,request:Request, id: Union[str,None]= None, db: Collection = Depends(get_collection)):
        if id is None:
            id= get_user_id(request.headers["Authorization"].split(" ")[1])

        chiks = self.service.getChikByAuthor(db, id)
        if chiks:
            return [chik for chik in chiks]
        raise HTTPException(status_code=404, detail="Chiks not found")

	