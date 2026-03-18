"""Funciones de traducción usando Azure Translator.

Este módulo se encarga de:
- obtener la lista de idiomas soportados por la API
- traducir texto entre dos idiomas

NOTA: Las claves (CLAVE) están embebidas para simplificar el ejemplo, pero en producción
recomiendo leerlas de variables de entorno.
"""

import requests
import uuid
from requests.exceptions import RequestException

CLAVE = "2HDx26ckfKhImGGCPmDnlX0LP9pjs8j7EFYA6GB76rxDnberSEEAJQQJ99CCAC5RqLJXJ3w3AAAbACOGixjt"
REGION = "westeurope"
ENDPOINT = "https://api.cognitive.microsofttranslator.com"

def obtener_idiomas():
    """Obtiene el listado de idiomas disponibles para traducción.

    Retorna un diccionario con claves de idioma (por ejemplo, 'es', 'en') y datos de cada idioma.
    En caso de error retorna un diccionario vacío.
    """
    url = f"{ENDPOINT}/languages?api-version=3.0"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("translation", {}) or {}
    except RequestException as exc:
        # En un proyecto real, usa logging en lugar de print.
        print(f"[translator] Error al obtener idiomas: {exc}")
        return {}
    except ValueError as exc:
        print(f"[translator] Respuesta inválida de la API de idiomas: {exc}")
        return {}

def traducir_texto(texto, idioma_origen, idioma_destino):
    """Traduce texto entre dos idiomas usando Azure Translator.

    Args:
        texto: Texto de entrada.
        idioma_origen: Código del idioma de origen (ej. 'es').
        idioma_destino: Código del idioma destino (ej. 'en').

    Returns:
        La versión traducida del texto.
    """
    path = "/translate?api-version=3.0"
    url = ENDPOINT + path + f"&from={idioma_origen}&to={idioma_destino}"

    headers = {
        "Ocp-Apim-Subscription-Key": CLAVE,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    body = [{"text": texto}]

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[0]["translations"][0]["text"]
    except RequestException as exc:
        raise RuntimeError("Error al conectar con el servicio de traducción.") from exc
    except (KeyError, IndexError, ValueError) as exc:
        raise RuntimeError("Respuesta inesperada de la API de traducción.") from exc