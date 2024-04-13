from datetime import datetime
import os
from azure.communication.email import EmailClient
from dotenv import load_dotenv

from models.user_devices import user_devices

load_dotenv()

def sendEmail(result,device: user_devices):
    email = EmailClient.from_connection_string(os.getenv('connection_string'))
    url=os.getenv('url')

    message = {
    "senderAddress": os.getenv('email'),
    "recipients":  {
    "to": [{"address": f"{result.email}" }],
    },
    "content": {
    "subject": "Nuevo inicio de sesión sospechoso en chikara",
    "html": "<html><head></head><body><h1>Se ha iniciado sesión en tu cuenta a las: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+
    f"</h1><br><h2>Hola {result.user_name},</h2><br>"+
    "<p>Se ha iniciado sesión en tu cuenta desde un dispositivo desconocido.</p>"+
    "<p>Datos del dispositivo:</p>"+
    "<ul>"+
    "<li>Modelo: "+device.phone_model+"</li>"+
    "<li>Marca: "+device.phone_brand+"</li>"+
    "<li>Id: "+device.phone_id+"</li>"+
    "</ul>"+
    "<p>Si no has sido tú, te recomendamos que tomes medidas inmediatas para asegurar la seguridad de tu cuenta.</p>"+
    "<p>Para bloquear el dispositivo, haz clic en el siguiente enlace:</p>"+
    f'<a href="{url}/api/v1/devices/block/{device.id}" target="_blank">Bloquear dispositivo</a>'+
    "<p>Si has sido tú quien inició sesión, ignora este mensaje.</p><br><p>Este es un mensaje automático. Por favor, no responder a este correo electrónico.</p></body></html>"
    }
    }
    print(message)
    poller = email.begin_send(message)
    resultemail = poller.result()
