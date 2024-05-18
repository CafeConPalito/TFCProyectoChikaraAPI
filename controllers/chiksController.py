from datetime import datetime
from typing import Annotated, List, Optional, Union
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pymongo.collection import Collection

from config.blob import list_blobs, upload_blob
from config.db_mongo import get_collection

from config.jwt import get_user_id
from decorators.decorator import Security
from middlewares.verify_token_route import VerifyTokenRoute
from schemas.chiksSchema import Comment, chiksSchema
from services.chiksService import chiksService

router= APIRouter()

@cbv(router)
class chiksController:

    def __init__(self):
        self.service =  chiksService()

    # @router.get("/",response_model=List[chiksSchema],status_code=200)
    # def getAllChiks(self ,db: Collection = Depends(get_collection)):
    #     return [chiks for chiks in self.service.getAllChiks(db)]

    @router.get("/top",response_model=List[chiksSchema],status_code=200)
    def getTopChiks(self, db: Collection = Depends(get_collection)):
        chiks= self.service.getTopChiks(db)
        if chiks:
            result=[]
            for chik in chiks:
                result.append(chik)
            return result
        raise HTTPException(status_code=404, detail="Chiks not found")

    
    @router.get("/findbyauthor",response_model=List[chiksSchema],status_code=200)
    def getChikByAuthor(self,request:Request, db: Collection = Depends(get_collection)):
        user_id= get_user_id(request.headers["Authorization"].split(" ")[1])

        chiks = self.service.getChikByAuthor(db, user_id)
        if chiks:
            result=[]
            for chik in chiks:
                result.append(chik)
            return result
        raise HTTPException(status_code=404, detail="Chiks not found")
    
    @router.post("/create",response_model=chiksSchema,status_code=200)
    def createChik(self,request:Request,newchik:chiksSchema , db: Collection = Depends(get_collection)):
        #Insertar el id del usuario que esta creando el chik
        newchik.author= get_user_id(request.headers["Authorization"].split(" ")[1])

        #Con los datos del chik, se procede a insertar en Mongo Atlas
        chiks=self.service.uploadChik(db, newchik)

        #Si se inserto correctamente, se retorna el chik creado
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/addcomment",response_model=chiksSchema,status_code=200)
    def addComment(self,request:Request, id:str, comment:Comment, db: Collection = Depends(get_collection)):
        user_id= get_user_id(request.headers["Authorization"].split(" ")[1])
        chiks=self.service.addComment(db, id, user_id, comment)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/addmencion",response_model=chiksSchema,status_code=200)
    def addMencion(self,id:str, mencion:str, db: Collection = Depends(get_collection)):
        chiks=self.service.addMencion(db, id, mencion)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/addlike",response_model=chiksSchema,status_code=200)
    def addLike(self,id:str, db: Collection = Depends(get_collection)):
        chiks=self.service.addLike(db, id)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/deletelike",response_model=chiksSchema,status_code=200)
    def deleteLike(self,id:str, db: Collection = Depends(get_collection)):
        chiks=self.service.deleteLike(db, id)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")

        
            

	