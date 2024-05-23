
from fastapi import APIRouter
from controllers import user_dataController
from controllers import ChiksController
from controllers import user_devicesController

api_router = APIRouter()
api_router.include_router(user_dataController.router, tags=["Users"],prefix="/users")
api_router.include_router(ChiksController.router, tags=["Chiks"],prefix="/chiks")
api_router.include_router(user_devicesController.router, tags=["Devices"],prefix="/devices")
