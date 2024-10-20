from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Cambia esta URL por la dirección IP de tu servidor local
LOCAL_SERVER_URL = 'http://<TU_IP_LOCAL>:5000/send_command'

@app.route('/')
def index():
    # Renderiza la página HTML
    return render_template_string(open('index.html').read())

@app.route('/control', methods=['POST'])
def control():
    command = request.json.get('command')
    if command in ['0', '1']:
        # Enviar el comando al servidor local
        response = requests.post(LOCAL_SERVER_URL, json={'command': command})
        if response.status_code == 200:
            return {'status': 'success', 'command': command}, 200
    return {'status': 'error', 'message': 'Invalid command'}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)