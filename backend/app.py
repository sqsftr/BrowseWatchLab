from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_socketio'  # Diperlukan untuk Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")  # Memungkinkan koneksi dari mana saja
LOG_FILE = "logs/traffic.json"

# Pastikan direktori logs ada
def ensure_log_directory():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    # Buat file log jika belum ada
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("")

# Endpoint untuk menerima data dari client
@app.route('/report', methods=['POST'])
def report():
    data = request.json
    ensure_log_directory()
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    # Kirim data ke semua client yang terhubung
    socketio.emit('new_data', data)
    return {"status": "Received"}, 200

# Ambil semua data dari file log
def get_log_entries():
    ensure_log_directory()
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            if not lines:
                return []
            return [json.loads(line) for line in lines]
    except Exception as e:
        print(f"Error reading log file: {e}")
        return []

# Frontend routes
@app.route('/')
def index():
    entries = get_log_entries()
    return render_template("index2.html", entries=entries)

@app.route('/dashboard')
def dashboard():
    try:
        with open(LOG_FILE, "r") as f:
            entries = [json.loads(line) for line in f]
    except FileNotFoundError:
        entries = []
    return render_template('index.html', entries=entries)

@app.route('/halaman1')
def halaman1():
    return render_template('hal_1.html')

@app.route('/halaman2')
def halaman2():
    entries = get_log_entries()
    return render_template('hal_2.html', entries=entries)

@app.route('/halaman3')
def halaman3():
    return render_template('hal_3.html')

@app.route('/halaman4')
def halaman4():
    return render_template('hal_4.html')

@app.route('/halaman5')
def halaman5():
    entries = get_log_entries()
    return render_template('hal_5.html', entries=entries)

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    ensure_log_directory()  # Pastikan direktori logs ada saat aplikasi dimulai
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)