from fastapi.responses import FileResponse
from models.user_devices import user_devices
from repository.user_devicesRepository import user_devicesRepository


class User_DevicesService():

    def __init__(self):
        self.repository = user_devicesRepository()

    def blockDevice(self, db, id: str):
        result = db.query(user_devices).filter(user_devices.id == id).first()
        if result is None:
            return FileResponse("resources/static/errorblock.html")
        
        result=self.repository.update({"block": True},id,db)

        if result["block"] == True:
            return FileResponse("resources/static/block.html")
        
    def unblockDevice(self, db, id: str):
        result = db.query(user_devices).filter(user_devices.id == id).first()
        if result is None:
            return FileResponse("resources/static/errorunblock.html")
        
        result=self.repository.update({"block": False},id,db)

        if result["block"] == False:
            return FileResponse("resources/static/unblock.html")

    
    