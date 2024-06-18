import json
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Ruta al archivo JSON de credenciales de la cuenta de servicio
SERVICE_ACCOUNT_FILE = 'dismac-426800-ff871aa56fe6.json'

# Scopes necesarios para acceder a la API de Dialogflow
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Autenticación con las credenciales de la cuenta de servicio
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Crear un request para obtener el token
credentials.refresh(Request())

# Obtener el token de acceso
access_token = credentials.token
print(f"Access Token: {access_token}")
