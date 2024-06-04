from datetime import datetime, timedelta
import threading
from dotenv import load_dotenv
from loguru import logger as Logger
from config.db import engine
from sqlalchemy.orm import sessionmaker

from config.db_mongo import get_collection
from config.email import send_email_motivacion_day, send_email_motivacion_days, sendEmailBirthday
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

    # ------------------- 6. Conexión a Mongo ---------------------------------

    db_mongo= get_collection()

    SessionLocal = sessionmaker(bind = engine)

    db2 = SessionLocal()

    # ------------------- 7. Consultar todos los chiks que llevan un dia subido ---------------------------------
    fecha_filtro = current_date - timedelta(days=1)

    list2 = db_mongo.find({"date":fecha_filtro})

    for chik in list2:
        user=db2.query(user_data).filter(user_data.id==chik['user_id']).first()
        if user is None:
            continue
        hiloemail = threading.Thread(target=send_email_motivacion_day, args=(user.email,user.user_name,chik['title']))
        hiloemail.start()

    # ------------------- 8. Consultar todos los chiks que llevan 21 dias subidos ---------------------------------
    fecha_filtro = current_date - timedelta(days=21)

    list3 = db_mongo.find({"date":fecha_filtro})

    for chik in list3:
        user=db2.query(user_data).filter(user_data.id==chik['user_id']).first()
        if user is None:
            continue
        hiloemail = threading.Thread(target=send_email_motivacion_days, args=(user.email,user.user_name,chik['title']))
        hiloemail.start()

    # ------------------- 9. Cerrar sesión ---------------------------------
    db2.close()

    # ------------------- 6. Fin del ETL ---------------------------------

    Logger.info("ETL finalizado")
