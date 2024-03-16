from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from config.logger import startLogger
from routers.routers import api_router

app = FastAPI()
app.title = "Chikara API"
app.version = "0.1.0"
app.description = "API REST para el manejo de usuarios y chiks en la aplicación multiplataforma Chikara"

startLogger()
load_dotenv()

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)