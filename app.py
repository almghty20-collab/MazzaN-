from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import re
import io
import requests

app = Flask(__name__)

def extract_text_from_image(image_bytes):
    """Lee texto desde imagen (bytes) usando OCR."""
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text

def extract_data(text):
    """Extrae datos clave desde el texto del ticket."""
    data = {}

    phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    address = re.search(r'\d{1,5}\s[\w\s]+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)', text, re.IGNORECASE)
    name = re.search(r'(?:Delivery|DELIVERY|Online\s*-\s*DELIVERY)\s*([A-Za-z\s]+)', text)

    if phone:
        data["telefono"] = phone.group().strip()
    if address:
        data["direccion"] = address.group().strip()
    if name:
        data["nombre"] = name.group(1).strip()

    return data

@app.route('/')
def home():
    return "🚀 Mazza OCR server is running!"

@app.route('/ocr', methods=['POST'])
def ocr_from_image():
    """Endpoint para procesar imagen (por URL o archivo)."""
    if 'file' in request.files:
        image_bytes = request.files['file'].read()
    elif 'url' in request.json:
        image_url = request.json['url']
        image_bytes = requests.get(image_url).content
    else:
        return jsonify({"error": "No image provided"}), 400

    text = extract_text_from_image(image_bytes)
    info = extract_data(text)
    return jsonify({
        "texto": text,
        "extraido": info
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
