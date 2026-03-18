import requests
import uuid

CLAVE = "2HDx26ckfKhImGGCPmDnlX0LP9pjs8j7EFYA6GB76rxDnberSEEAJQQJ99CCAC5RqLJXJ3w3AAAbACOGixjt"
REGION = "westeurope"
ENDPOINT = "https://api.cognitive.microsofttranslator.com"

def obtener_idiomas():
    url = f"{ENDPOINT}/languages?api-version=3.0"
    response = requests.get(url)
    return response.json()["translation"]

def traducir_texto(texto, idioma_origen, idioma_destino):
    path = "/translate?api-version=3.0"
    url = ENDPOINT + path + f"&from={idioma_origen}&to={idioma_destino}"

    headers = {
        "Ocp-Apim-Subscription-Key": CLAVE,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    body = [{"text": texto}]

    response = requests.post(url, headers=headers, json=body)
    return response.json()[0]["translations"][0]["text"]