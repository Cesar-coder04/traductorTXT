# Traductor IA

Pequeña aplicación web en Flask que permite:

- Traducir texto entre idiomas usando Azure Translator.
- Reconocer voz desde el micrófono y convertirla a texto (Speech-to-Text).
- Generar audio (TTS) desde texto y reproducirlo en el navegador.

## Estructura principal

- `app.py`: servidor Flask, routes y renderizado de la interfaz.
- `translator.py`: comunicación con Azure Translator.
- `speech.py`: interacción con Azure Speech (TTS/ASR).
- `templates/index.html`: interfaz web principal (HTML + JavaScript).
- `static/style.css`: estilos visuales.

## Uso local

1. Crear entorno virtual y activar (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la app:
   ```bash
   python app.py
   ```

4. Abrir en el navegador:
   `http://127.0.0.1:5000`

---

**NOTA:** Las claves de Azure están embebidas en el código para facilitar pruebas. En un proyecto real es mejor guardarlas en variables de entorno o en un gestor de secretos.
