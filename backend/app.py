from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)
LOG_FILE = "logs/traffic.json"

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    socketio.emit('new_data', data)
    return {"status": "Received"}, 200

# Frontend routes
@app.route('/')
def index():
    try:
        with open(LOG_FILE, "r") as f:
            entries = [json.loads(line) for line in f]
    except FileNotFoundError:
        entries = []

    return render_template("index.html", entries=entries)


@app.route('/halaman1')
def halaman1():
    return render_template('hal_1.html')

@app.route('/halaman2')
def halaman2():
    try:
        with open(LOG_FILE, "r") as f:
            entries = [json.loads(line) for line in f]
    except FileNotFoundError:
        entries = []
    return render_template('hal_2.html', entries=entries)

@app.route('/halaman3')
def halaman3():
    return render_template('hal_3.html')

@app.route('/halaman4')
def halaman4():
    return render_template('hal_4.html')

@app.route('/halaman5')
def halaman5():
    try:
        with open(LOG_FILE, "r") as f:
            entries = [json.loads(line) for line in f]
    except FileNotFoundError:
        entries = []
    return render_template('hal_5.html', entries=entries)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
