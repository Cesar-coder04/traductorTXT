from flask import Flask, render_template, request, send_file
from translator import traducir_texto, obtener_idiomas
from speech import texto_a_audio, texto_a_audio_bytes, audio_a_texto

import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    idiomas = obtener_idiomas()

    resultado = ""
    texto = ""
    origen = "es"
    destino = "es"

    if request.method == "POST":
        texto = request.form.get("texto", "")
        origen = request.form.get("origen", origen)
        destino = request.form.get("destino", destino)

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
    idioma = request.form["idioma"]
    texto = audio_a_texto(idioma)
    return {"texto": texto}

@app.route("/tts", methods=["POST"])
def tts():
    # Generate audio (WAV) for the given text using Azure Speech and return it as a response.
    texto = request.form.get("texto", "")
    idioma = request.form.get("idioma", "es-ES")

    audio_bytes = texto_a_audio_bytes(texto, idioma)
    return send_file(io.BytesIO(audio_bytes), mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)