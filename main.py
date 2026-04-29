from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Permite que tu web consulte esta API

# Configuración (tomada de Garena)
API_URL = "https://shop.garena.my/api/auth/player_id_login"
APP_ID = 100067

# IMPORTANTE: Necesitas obtener estas cookies de Garena
# Ve a shop.garena.my, abre herramientas de desarrollador (F12)
# Copia las cookies "datadome" y "session_key"
COOKIE_HEADER = "region=MY; datadome=TU_DATADOME; session_key=TU_SESSION_KEY"

@app.route('/verify/<uid>', methods=['GET'])
def verify_player(uid):
    """Verifica un ID de Free Fire y devuelve su información"""
    
    headers = {
        'Content-Type': 'application/json',
        'Cookie': COOKIE_HEADER
    }
    
    payload = {
        "app_id": APP_ID,
        "login_id": uid
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        data = response.json()
        
        # Verificar si la respuesta es exitosa
        if 'error' in data:
            return jsonify({
                'success': False,
                'message': 'ID no encontrado o inválido'
            }), 404
        
        # Extraer información del jugador
        if 'img_url' in data and 'region' in data and 'nickname' in data:
            return jsonify({
                'success': True,
                'uid': uid,
                'nickname': data['nickname'],
                'region': data['region'],
                'avatar': data['img_url']
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Respuesta inesperada de Garena'
            }), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'message': f'Error de conexión: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'online',
        'message': 'API de verificación de Free Fire funcionando'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)