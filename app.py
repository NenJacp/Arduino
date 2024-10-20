from flask import Flask, request, render_template_string
import serial
import time
from datetime import datetime
import threading

app = Flask(__name__)

# Cambia 'COM4' por el puerto correspondiente en tu sistema
arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # Espera a que se establezca la conexión

# Lista para almacenar el historial de eventos
event_history = []
last_event_time = None  # Variable para almacenar el tiempo del último evento

def read_from_serial():
    global last_event_time  # Usar la variable global
    while True:
        if arduino.in_waiting > 0:
            command = arduino.read().decode('utf-8')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if command in ['0', '1']:
                action = "Encendido" if command == '1' else "Apagado"
                # Verificar si el evento es en el mismo segundo
                if last_event_time is None or current_time != last_event_time:
                    event_history.append(f'{action} a las {current_time}')
                    last_event_time = current_time  # Actualizar el tiempo del último evento

# Iniciar el hilo para leer del puerto serie
threading.Thread(target=read_from_serial, daemon=True).start()

@app.route('/')
def index():
    # Renderiza la página HTML con el historial
    return render_template_string(open('index.html').read(), history=event_history)

@app.route('/control')
def control():
    command = request.args.get('command')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if command in ['0', '1']:
        arduino.write(command.encode())  # Enviar comando al Arduino
        # Agregar evento al historial
        action = "Encendido" if command == '1' else "Apagado"
        # Verificar si el evento es en el mismo segundo
        if last_event_time is None or current_time != last_event_time:
            event_history.append(f'{action} a las {current_time}')
            last_event_time = current_time  # Actualizar el tiempo del último evento
        return f'Comando {command} enviado'
    return 'Comando no válido', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)