from datetime import datetime
from typing import Annotated, List, Optional, Union
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pymongo.collection import Collection

from config.blob import list_blobs, upload_blob
from config.db_mongo import get_collection

from config.jwt import get_user_id
from decorators.decorator import security, oauth2_scheme
from middlewares.verify_token_route import VerifyTokenRoute
from schemas.chiksSchema import Comment, chiksSchema
from services.chiksService import ChiksService

from sqlalchemy.orm import Session
from config.db_depend import get_db

router= APIRouter()

@cbv(router)
class ChiksController:

    def __init__(self):
        self.service =  ChiksService()


    @router.get("/top",response_model=List[chiksSchema],status_code=200)
    @security()
    def getTopChiks(self, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        chiks= self.service.get_top_chiks(db)
        if chiks:
            result=[]
            for chik in chiks:
                result.append(chik)
            return result
        raise HTTPException(status_code=404, detail="Chiks not found")

    
    @router.get("/findbyauthor",response_model=List[chiksSchema],status_code=200)
    @security()
    def getChikByAuthor(self,request:Request, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        user_id= get_user_id(request.headers["Authorization"].split(" ")[1])

        chiks = self.service.get_chik_by_author(db, user_id)
        if chiks:
            result=[]
            for chik in chiks:
                result.append(chik)
            return result
        raise HTTPException(status_code=404, detail="Chiks not found")
    
    @router.post("/create",response_model=chiksSchema,status_code=200)
    @security()
    def createChik(self,request:Request,newchik:chiksSchema , db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme),db2: Session = Depends(get_db)):
        #Insertar el id del usuario que esta creando el chik
        newchik.author= get_user_id(request.headers["Authorization"].split(" ")[1])

        #Con los datos del chik, se procede a insertar en Mongo Atlas
        chiks=self.service.upload_chik(db,db2, newchik)

        #Si se inserto correctamente, se retorna el chik creado
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/addcomment",response_model=chiksSchema,status_code=200)
    @security()
    def addComment(self,request:Request, id:str, comment:Comment, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        user_id= get_user_id(request.headers["Authorization"].split(" ")[1])
        chiks=self.service.add_comment(db, id, user_id, comment)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/addmencion",response_model=chiksSchema,status_code=200)
    @security()
    def addMencion(self,id:str, mencion:str, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        chiks=self.service.add_mencion(db, id, mencion)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/addlike",response_model=chiksSchema,status_code=200)
    @security()
    def addLike(self,id:str, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        chiks=self.service.add_like(db, id)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.post("/deletelike",response_model=chiksSchema,status_code=200)
    @security()
    def deleteLike(self,id:str, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        chiks=self.service.delete_like(db, id)
        if chiks:
            return chiks
        raise HTTPException(status_code=401, detail="Not created")
    
    @router.get("/search/{text}",response_model=List[chiksSchema],status_code=200)
    @security()
    def search_chiks(self,text:str, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        chiks=self.service.search_chiks(db, text)
        if chiks:
            result=[]
            for chik in chiks:
                result.append(chik)
            return result
        raise HTTPException(status_code=404, detail="Chiks not found")
    
    @router.get("/getchik/{id}",response_model=chiksSchema,status_code=200)
    @security()
    def get_chik(self,id:str, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        chik=self.service.get_chik_by_id(db, id)
        if chik:
            return chik
        raise HTTPException(status_code=404, detail="Chik not found")
    
    @router.delete("/delete/{id}",response_model=bool,status_code=200)
    @security()
    def delete_chik(self,id:str, db: Collection = Depends(get_collection),token: str = Depends(oauth2_scheme)):
        chik=self.service.delete_chik(db, id)
        if chik:
            return True
        raise HTTPException(status_code=404, detail="Chik not found")

        
            

	