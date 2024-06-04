from abc import ABC, abstractmethod

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

class AbstractRepository(ABC):

    entity:object = NotImplementedError

    @abstractmethod
    def __init__(self,entity:object):
        self.entity=entity

    def get_all(self,db:Session):
        return db.query(self.entity).order_by(self.entity.id).all()

    def get_by_id(self, id:int,db:Session):
        return db.query(self.entity).filter(self.entity.id==id).one()

    def find_by_id(self, id:int,db:Session):
        return db.query(self.entity).filter(self.entity.id==id).first()

    def get_actives(self,db:Session):
        return db.query(self.entity).filter(self.entity.is_active==True).all()

    def add(self, entity,db:Session):
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, entity,idOld, db:Session):
        entity["id"] = idOld
        db.query(self.entity).filter(self.entity.id == idOld).update(entity)
        db.commit()
        return entity

    def delete(self, entity, db:Session):
        entity.active= False
        db.query(self.entity).filter(self.entity.id == entity.id).update(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def permanent_delete(self, entity,db:Session):
        db.delete(entity)
        db.commit()
        return None
