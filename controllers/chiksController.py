from typing import List, Optional, Union
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from pymongo.collection import Collection

from config.blob import list_blobs, upload_blob
from config.db_mongo import get_collection

from config.jwt import get_user_id
from decorators.decorator import Security
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
        result=[]
        for chiks in self.service.getTopChiks(db):
            chiks["_id"]=str(chiks["_id"])
            result.append(chiks)
        return result
    
    @router.get("/findbyauthor",response_model=List[chiksSchema],status_code=200)
    def getChikByAuthor(self,request:Request, db: Collection = Depends(get_collection)):
        user_id= get_user_id(request.headers["Authorization"].split(" ")[1])

        chiks = self.service.getChikByAuthor(db, user_id)
        if chiks:
            result=[]
            for chiks in self.service.getTopChiks(db):
                chiks["id"]=str(chiks["_id"])
                result.append(chiks)
            return result
        raise HTTPException(status_code=404, detail="Chiks not found")
    
    # @router.post("/create",response_model=str,status_code=200)
    # def createChik(self,request:Request, chik: chiksSchema, db: Collection = Depends(get_collection)):
    #     chik.author= get_user_id(request.headers["Authorization"].split(" ")[1])
    #     return self.service.uploadChik(db, chik)

    @router.post("/upload",status_code=200)
    async def uploadfiles(self,files:Optional[List[UploadFile]]=None):
        cont=1
        if not files:
            raise HTTPException(status_code=404, detail="No files found")
        for file in files:
            data= await file.read()
            upload_blob(f"{cont}.webp","image/webp",data)
            cont+=1

        list_blobs()
        
            

	