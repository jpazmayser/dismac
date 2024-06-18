from twilio.twiml.voice_response import VoiceResponse
import logging
import requests
import base64
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import uuid

# Ruta al archivo JSON de credenciales de la cuenta de servicio
SERVICE_ACCOUNT_FILE = 'dismac-426800-ff871aa56fe6.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
PROJECT_ID = 'dismac-426800'

def get_access_token():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        credentials.refresh(Request())
        return credentials.token
    except Exception as e:
        logging.error(f"Error getting access token: {e}")
        raise

def detect_intent_text(session_id, text, language_code='en-US'):
    try:
        access_token = get_access_token()
        url = f'https://dialogflow.googleapis.com/v2/projects/{PROJECT_ID}/agent/sessions/{session_id}:detectIntent'
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "queryInput": {
                "text": {
                    "text": text,
                    "languageCode": language_code
                }
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error detecting intent: {e}")
        raise

def synthesize_speech(text):
    try:
        url = 'https://flask-app-hw4wgca47a-vp.a.run.app/synthesize'
        response = requests.post(url, json={'text': text})
        response.raise_for_status()
        return base64.b64decode(response.json()['audioContent'])
    except Exception as e:
        logging.error(f"Error synthesizing speech: {e}")
        raise

def process_speech(request):
    response = VoiceResponse()
    try:
        if 'SpeechResult' in request.form:
            speech_result = request.form['SpeechResult']
            logging.info(f"Received speech: {speech_result}")

            session_id = str(uuid.uuid4())
            try:
                dialogflow_response = detect_intent_text(session_id, speech_result)
                fulfillment_text = dialogflow_response['queryResult']['fulfillmentText']
                logging.info(f"Fulfillment text: {fulfillment_text}")
            except Exception as e:
                logging.error(f"Error in Dialogflow request: {e}")
                response.say("An error occurred while processing your speech with Dialogflow.")
                return str(response)

            try:
                audio_content = synthesize_speech(fulfillment_text)
                response.play(base64.b64encode(audio_content).decode('utf-8'))
            except Exception as e:
                logging.error(f"Error in Text-to-Speech request: {e}")
                response.say("An error occurred while synthesizing the speech.")
        else:
            logging.error("No SpeechResult in request")
            response.say("Sorry, I didn't catch that.")
        return str(response)
    except Exception as e:
        logging.error(f"Error processing speech: {e}")
        response.say("An error occurred while processing your request.")
        return str(response)

# Configuración del logger para registrar errores y mensajes informativos
logging.basicConfig(level=logging.DEBUG)
