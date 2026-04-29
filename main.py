from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'message': 'API funcionando'})

@app.route('/verify/<uid>')
def verify(uid):
    return jsonify({
        'success': True,
        'uid': uid,
        'nickname': 'Test Player',
        'region': 'BR'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)