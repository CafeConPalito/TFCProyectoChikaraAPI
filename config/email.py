from datetime import datetime
import os
from azure.communication.email import EmailClient
from dotenv import load_dotenv

from models.user_data import user_data
from models.user_devices import user_devices

load_dotenv()

def sendEmailBlock(result,device: user_devices):
    email = EmailClient.from_connection_string(os.getenv('connection_string'))
    url=os.getenv('url')

    message = {
    "senderAddress": os.getenv('email'),
    "recipients":  {
    "to": [{"address": f"{result.email}" }],
    },
    "content": {
    "subject": "Nuevo inicio de sesión sospechoso en chikara",
    "html": "<html><head></head><body><h1>Se ha iniciado sesión en tu cuenta a las: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S") +" UTC" +
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
    f'<a href="{url}api/v1/devices/block/{device.id}" target="_blank">Bloquear dispositivo</a>'+
    "<p>Si has sido tú quien inició sesión, ignora este mensaje.</p><br><p>Este es un mensaje automático. Por favor, no responder a este correo electrónico.</p></body></html>"
    }
    }
    poller = email.begin_send(message)
    resultemail = poller.result()


def sendEmailUnBlock(result,device: user_devices):
    email = EmailClient.from_connection_string(os.getenv('connection_string'))
    url=os.getenv('url')

    message = {
    "senderAddress": os.getenv('email'),
    "recipients":  {
    "to": [{"address": f"{result.email}" }],
    },
    "content": {
    "subject": "Nuevo intento de inicio desde un dispositivo bloqueado en chikara",
    "html": "<html><head></head><body><h1>Se ha intentando iniciar sesión en tu cuenta a las: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S") +" UTC" +
    f"</h1><br><h2>Hola {result.user_name},</h2><br>"+
    "<p>Se ha intentado iniciar sesión en tu cuenta desde un dispositivo que has bloqueado.</p>"+
    "<p>Datos del dispositivo:</p>"+
    "<ul>"+
    "<li>Modelo: "+device.phone_model+"</li>"+
    "<li>Marca: "+device.phone_brand+"</li>"+
    "<li>Id: "+device.phone_id+"</li>"+
    "</ul>"+
    "<p>Si has sido tú, y quieres desbloquear el dispositivo entra en el siguiente enlace:</p>"+
    f'<a href="{url}api/v1/devices/unblock/{device.id}" target="_blank">Desbloquear dispositivo</a>'+
    "<p>Si no has sido tú quien inició sesión, ignora este mensaje.</p><br><p>Este es un mensaje automático. Por favor, no responder a este correo electrónico.</p></body></html>"
    }
    }
    poller = email.begin_send(message)
    resultemail = poller.result()

def sendEmailWelcome(useremail:str,user_name:str):
    email = EmailClient.from_connection_string(os.getenv('connection_string'))

    message = {
    "senderAddress": os.getenv('email'),
    "recipients":  {
    "to": [{"address": useremail }],
    },
    "content": {
    "subject": "Bienvenido a chikara",
    "html": "<html><head></head><body><h1>Bienvenido a chikara</h1><br><h2>Hola "+user_name+",</h2><br>"+
    "<p>Gracias por registrarte en chikara.</p>"+
    "<p>Esperamos que disfrutes de la experiencia y que encuentres la motivación que buscas.</p>"+
    "<p>Si tienes alguna duda o problema, no dudes en contactar con CafeConPalito</p>"+
    "<p>Un saludo.</p><br><p>Este es un mensaje automático. Por favor, no responder a este correo electrónico.</p></body></html>"
    }
    }
    poller = email.begin_send(message)
    resultemail = poller.result()

# def sendEmailResetPassword(useremail:str,user_name:str,url:str):
#     email = EmailClient.from_connection_string(os.getenv('connection_string'))

#     message = {
#     "senderAddress": os.getenv('email'),
#     "recipients":  {
#     "to": [{"address": useremail }],
#     },
#     "content": {
#     "subject": "Reseteo de contraseña en chikara",
#     "html": "<html><head></head><body><h1>Reseteo de contraseña en chikara</h1><br><h2>Hola "+user_name+",</h2><br>"+
#     "<p>Has solicitado un reseteo de contraseña en chikara.</p>"+
#     "<p>Para resetear tu contraseña, haz clic en el siguiente enlace:</p>"+
#     f'<a href="{url}" target="_blank">Resetear contraseña</a>'+
#     "<p>Si no has sido tú quien solicitó el reseteo, ignora este mensaje.</p><br><p>Este es un mensaje automático. Por favor, no responder a este correo electrónico.</p></body></html>"
#     }
#     }
#     poller = email.begin_send(message)
#     resultemail = poller.result()

def sendEmailBirthday(useremail:str,user_name:str):
    email= EmailClient.from_connection_string(os.getenv('connection_string'))

    message = {
    "senderAddress": os.getenv('email'),
    "recipients":  {
    "to": [{"address": useremail }],
    },
    "content": {
    "subject": "Feliz cumpleaños",
    "html": "<html><head></head><body><h1>Feliz cumpleaños</h1><br><h2>Hola "+user_name+",</h2><br>"+
    "<p>Desde CafeConPalito queremos desearte un feliz cumpleaños.</p>"+
    "<p>Esperamos que disfrutes de este día tan especial.</p>"+
    "<p>Un saludo.</p><br><p>Este es un mensaje automático. Por favor, no responder a este correo electrónico.</p></body></html>"
    }
    }
    poller = email.begin_send(message)
    resultemail = poller.result()