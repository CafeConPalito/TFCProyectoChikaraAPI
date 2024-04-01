
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

DB_USER = os.getenv('DB_USER_MONGO')
DB_PASSWORD = os.getenv('DB_PASSWORD_MONGO')
DB_CLUSTER = os.getenv('DB_CLUSTER')
DB_NAME = os.getenv('DB_NAME_MONGO')
DB_COLLECTION = os.getenv('DB_COLLECTION')

uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}?retryWrites=true&w=majority&appName=ClusterChikara"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
def get_collection():
    try:
        yield client.get_database(DB_NAME).get_collection(DB_COLLECTION)
    finally:
        client.close()



# Para comprobar que tengo conexion a mongodb Atlas
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e) 
