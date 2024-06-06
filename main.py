from loguru import logger as Logger
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from config.logger import startLogger
from etl_chikara import cron_etl
from routers.routers import api_router
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(root_path="/api/v1")
app.title = "Chikara API"
app.version = "0.7.9"
app.description = "API REST para el manejo de usuarios y chiks en la aplicación multiplataforma Chikara"

startLogger()
load_dotenv()

app.include_router(api_router)
scheduler = BackgroundScheduler()

def cron():
    cron_etl()

@scheduler.scheduled_job('cron',hour=5,minute=0)
def firstUpdate():
    cron()

@app.on_event("startup")
def startUp():
    Logger.info("Starting up the API")
    scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)