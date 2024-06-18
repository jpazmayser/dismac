from google.cloud import speech
import logging
from flask import jsonify

def transcribe_audio(request):
    try:
        audio = request.files['audio']
        client = speech.SpeechClient()
        audio_content = audio.read()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
        )

        response = client.recognize(config=config, audio=audio)
        transcript = response.results[0].alternatives[0].transcript
        logging.info(f"Transcription result: {transcript}")
        return jsonify({"transcript": transcript})
    except Exception as e:
        logging.error(f"Error transcribing audio: {e}")
        return jsonify({"error": str(e)}), 500
