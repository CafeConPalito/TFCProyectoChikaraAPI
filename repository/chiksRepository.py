from models.chiks import Chiks as chiks


class chiksRepository():
    def __init__(self):
        self.entity = chiks
    
    def get_all(self, db):
        return db.find()
    
    def get_top_chiks(self, db):
        return db.find({"isprivate": False}).sort("likes", -1).limit(10)
    
    def get_chik_by_author(self, db, id):
        return db.find({"author": id})
    
    def search_chiks(self, db, query:str):
        return db.find({
            "$or": [
                {"titulo": {"$regex": query, "$options": "i"}},
                {"contenido": {"$regex": query, "$options": "i"}}
            ]
        })
