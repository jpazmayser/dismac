import logging
from flask import jsonify, request
import requests
import base64
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Configuration
SERVICE_ACCOUNT_FILE = 'dismac-426800-ff871aa56fe6.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
PROJECT_ID = 'dismac-426800'

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    credentials.refresh(Request())
    return credentials.token

def synthesize_speech(text):
    url = 'https://texttospeech.googleapis.com/v1/text:synthesize'
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": "en-US", "name": "en-US-Standard-B"},
        "audioConfig": {"audioEncoding": "MP3"}
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    audio_content = response.json()['audioContent']
    return base64.b64decode(audio_content)

def handle_webhook(request):
    try:
        req = request.get_json(silent=True, force=True)
        logging.info(f"Request received: {req}")

        # Get fulfillment text from Dialogflow response
        fulfillment_text = req['queryResult'].get('fulfillmentText', '')

        logging.info(f"Fulfillment text: {fulfillment_text}")

        # Convert fulfillment text to speech
        audio_content = synthesize_speech(fulfillment_text)
        
        # Return both text and audio content to Dialogflow
        return jsonify({
            'fulfillmentText': fulfillment_text,
            'payload': {
                'google': {
                    'expectUserResponse': True,
                    'richResponse': {
                        'items': [
                            {
                                'simpleResponse': {
                                    'textToSpeech': fulfillment_text,
                                    'ssml': f'<speak>{fulfillment_text}</speak>'
                                }
                            }
                        ]
                    }
                },
                'audioContent': base64.b64encode(audio_content).decode('utf-8')
            }
        })
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({'fulfillmentText': 'Error processing request.'}), 500
