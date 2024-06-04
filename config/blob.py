import os
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings
from dotenv import load_dotenv

load_dotenv()

STORAGE_CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')
STORAGE_CONTAINER=os.getenv('STORAGE_CONTAINER')

blob_service_client=BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)

def upload_blob(blob_name:str,content_type:str, data:bytes):
    try:
        blob_client = blob_service_client.get_blob_client(container=STORAGE_CONTAINER, blob=blob_name)
        result= blob_client.upload_blob(data, content_settings=ContentSettings(content_type=content_type))
    except Exception as e:
        print(e)

def delete_blob(blob_name:str):
    try:
        blob_client = blob_service_client.get_blob_client(container=STORAGE_CONTAINER, blob=blob_name)
        result= blob_client.delete_blob()
    except Exception as e:
        pass

def list_blobs():
    try:
        container_client = blob_service_client.get_container_client(STORAGE_CONTAINER)
        blobs_list = container_client.list_blobs()
        for blob in blobs_list:
            print(blob)
        
    except Exception as e:
        pass
