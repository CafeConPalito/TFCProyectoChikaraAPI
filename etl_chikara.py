from datetime import datetime
import threading
from dotenv import load_dotenv
from loguru import logger as Logger
from config.db import engine
from sqlalchemy.orm import sessionmaker

from config.email import sendEmailBirthday
from models.user_data import user_data


def cron_etl():

    # ------------------- 1. Cargar variables de entorno --------------------------------------------------------------
    Logger.info("Empezando ETL")    
    load_dotenv()


    # ------------------- 2. Obtener fecha del sistema ----------------------------------------------------------------
    current_date = datetime.now().date()

    # ------------------- 3. Crear sesión con la database ---------------------------------

    SessionLocal = sessionmaker(bind = engine)

    db = SessionLocal()


    # ------------------- 4. Consultar usuarios que cumplen años hoy ---------------------------------
    list = db.query(user_data).filter(user_data.birthdate==current_date).all()

    for user in list:
        Logger.info(f"Enviando email a {user.email} por su cumpleaños")
        hiloemail = threading.Thread(target=sendEmailBirthday, args=(user.email,user.user_name))
        hiloemail.start()

    # ------------------- 5. Cerrar sesión ---------------------------------
    db.close()

    Logger.info("ETL finalizado")
