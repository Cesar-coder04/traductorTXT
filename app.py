"""Web app principal del traductor.

Esta aplicación usa Flask para servir una UI simple que permite:
- traducir texto usando Azure Translator
- grabar voz y convertirla a texto con Azure Speech
- generar audio en WAV desde texto usando Azure Speech y reproducirlo en el navegador
"""

from flask import Flask, render_template, request, send_file
from translator import traducir_texto, obtener_idiomas
from speech import texto_a_audio, texto_a_audio_bytes, audio_a_texto

import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """Renderiza la página principal y maneja las traducciones.

    GET: muestra la página con valores por defecto.
    POST: recibe texto + idiomas y devuelve el texto traducido.
    """

    # Lista de idiomas soportados por el traductor (obtenida de la API de Azure).
    idiomas = obtener_idiomas()

    resultado = ""
    texto = ""
    origen = "es"
    destino = "es"

    if request.method == "POST":
        # Mantener lo que el usuario seleccionó para que la UI no “reseteé”.
        texto = request.form.get("texto", "")
        origen = request.form.get("origen", origen)
        destino = request.form.get("destino", destino)

        # Llamada a la API de traducción.
        resultado = traducir_texto(texto, origen, destino)

    return render_template(
        "index.html",
        idiomas=idiomas,
        resultado=resultado,
        texto=texto,
        origen=origen,
        destino=destino,
    )

@app.route("/audio", methods=["POST"])
def audio():
    """API endpoint para convertir voz (micrófono) a texto.

    Este endpoint se puede usar desde el frontend para obtener texto dictado.
    """
    idioma = request.form["idioma"]
    texto = audio_a_texto(idioma)
    return {"texto": texto}

@app.route("/tts", methods=["POST"])
def tts():
    """Genera un WAV desde texto (TTS) y lo devuelve como respuesta.

    Se usa desde el frontend cuando el navegador no tiene voz disponible para el
    idioma seleccionado o cuando se quiere forzar TTS en servidor.
    """
    texto = request.form.get("texto", "")
    idioma = request.form.get("idioma", "es-ES")

    audio_bytes = texto_a_audio_bytes(texto, idioma)
    return send_file(io.BytesIO(audio_bytes), mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)