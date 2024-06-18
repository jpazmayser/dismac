from google.cloud import texttospeech
import base64
import logging
from flask import jsonify

def synthesize_text(request):
    try:
        text = request.json.get('text')
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        audio_content = base64.b64encode(response.audio_content).decode('utf-8')
        logging.info("Text synthesized successfully")
        return jsonify({"audioContent": audio_content})
    except Exception as e:
        logging.error(f"Error synthesizing text: {e}")
        return jsonify({"error": str(e)}), 500
