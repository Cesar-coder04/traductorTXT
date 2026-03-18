"""Funciones de texto-a-voz y voz-a-texto usando Azure Cognitive Services.

Este módulo encapsula los calls a Azure Speech SDK para:
- convertir texto en audio (TTS)
- convertir audio (micrófono) en texto (ASR)

NOTA: las credenciales están embebidas en variables para simplicidad, pero se
recomienda guardarlas en variables de entorno en un proyecto real.
"""

import azure.cognitiveservices.speech as speechsdk
import os
import tempfile

CLAVE_SPEECH = "FGR5ICm81XvfuSllSeTvNnaL5rBbVaneBlCag2PnSvGpOxVmKtM5JQQJ99CCAC5RqLJXJ3w3AAAYACOGLpG2"
REGION_SPEECH = "westeurope"

def texto_a_audio(texto, idioma="es-ES"):
    """Convierte un texto en audio usando la API de Azure Speech.

    Este método usa la funcionalidad de síntesis de voz local del SDK y devuelve
    la razón del resultado (por ejemplo, si se completó con éxito).
    """
    try:
        speech_config = speechsdk.SpeechConfig(subscription=CLAVE_SPEECH, region=REGION_SPEECH)
        speech_config.speech_synthesis_language = idioma

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = synthesizer.speak_text_async(texto).get()

        return result.reason
    except Exception as exc:
        # En producción, usar logging y no exponer detalles internos.
        raise RuntimeError(f"Error al sintetizar audio: {exc}") from exc


def texto_a_audio_bytes(texto, idioma="es-ES"):
    """Genera audio WAV desde texto y devuelve los bytes resultantes.

    Este método se usa para crear un archivo de audio que pueda enviarse al
    navegador y reproducirse desde JS.
    """
    try:
        speech_config = speechsdk.SpeechConfig(subscription=CLAVE_SPEECH, region=REGION_SPEECH)
        speech_config.speech_synthesis_language = idioma
        # Usar un formato WAV común para que sea reproducible en todos los navegadores.
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = synthesizer.speak_text_async(texto).get()

        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError(f"TTS failed: {result.reason}")

        stream = speechsdk.AudioDataStream(result)
    except Exception as exc:
        raise RuntimeError(f"Error generando audio: {exc}") from exc

    # Guardar en un archivo temporal, leerlo como bytes y borrar el temporal.
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
    """Convierte audio del micrófono en texto.

    Este método realiza una única captura de voz (no es un stream continuo)
    y devuelve el texto reconocido por Azure.
    """
    try:
        speech_config = speechsdk.SpeechConfig(subscription=CLAVE_SPEECH, region=REGION_SPEECH)
        speech_config.speech_recognition_language = idioma

        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text

        if result.reason == speechsdk.ResultReason.NoMatch:
            raise RuntimeError("No se reconoció voz. Intenta de nuevo.")

        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation = speechsdk.CancellationDetails.from_result(result)
            raise RuntimeError(f"Reconocimiento cancelado: {cancellation.reason} - {cancellation.error_details}")

        raise RuntimeError(f"Resultado inesperado del reconocimiento: {result.reason}")
    except Exception as exc:
        raise RuntimeError(f"Error al reconocer voz: {exc}") from exc