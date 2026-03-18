import azure.cognitiveservices.speech as speechsdk
import os
import tempfile

CLAVE_SPEECH = "FGR5ICm81XvfuSllSeTvNnaL5rBbVaneBlCag2PnSvGpOxVmKtM5JQQJ99CCAC5RqLJXJ3w3AAAYACOGLpG2"
REGION_SPEECH = "westeurope"

def texto_a_audio(texto, idioma="es-ES"):
    speech_config = speechsdk.SpeechConfig(subscription=CLAVE_SPEECH, region=REGION_SPEECH)
    speech_config.speech_synthesis_language = idioma

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(texto).get()

    return result.reason


def texto_a_audio_bytes(texto, idioma="es-ES"):
    """Return a WAV audio blob for the given text using Azure Cognitive Services."""
    speech_config = speechsdk.SpeechConfig(subscription=CLAVE_SPEECH, region=REGION_SPEECH)
    speech_config.speech_synthesis_language = idioma
    # Use a standard WAV format so browsers can play it without extra codecs.
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    )

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(texto).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"TTS failed: {result.reason}")

    stream = speechsdk.AudioDataStream(result)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        stream.save_to_wav_file(tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

def audio_a_texto(idioma="es-ES"):
    speech_config = speechsdk.SpeechConfig(subscription=CLAVE_SPEECH, region=REGION_SPEECH)
    speech_config.speech_recognition_language = idioma

    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = recognizer.recognize_once()

    return result.text