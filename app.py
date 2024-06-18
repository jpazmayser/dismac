import os
from flask import Flask, request, jsonify
import logging
from transcribe import transcribe_audio
from synthesize import synthesize_text
from speech_processor import process_speech
from webhook_handler import handle_webhook

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio_route():
    return transcribe_audio(request)

@app.route('/synthesize', methods=['POST'])
def synthesize_text_route():
    return synthesize_text(request)

@app.route('/webhook', methods=['POST'])
def webhook_route():
    return handle_webhook(request)

@app.route('/process_speech', methods=['POST'])
def process_speech_route():
    return process_speech(request)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
