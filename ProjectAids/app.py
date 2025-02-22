from flask import Flask, jsonify, render_template
import threading
import time
import psutil

app = Flask(__name__)
open_ports = []

def get_open_ports():
    global open_ports
    while True:
        open_ports = [conn.laddr.port for conn in psutil.net_connections(kind='inet') if conn.status == 'LISTEN']
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/open_ports')
def api_open_ports():
    return jsonify(open_ports)

if __name__ == "__main__":
    threading.Thread(target=get_open_ports).start()
    app.run(debug=True)