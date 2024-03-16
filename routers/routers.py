
from fastapi import APIRouter
from controllers import user_dataController

api_router = APIRouter()
api_router.include_router(user_dataController.router, tags=["Users"],prefix="/users")
