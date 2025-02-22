from flask import Flask, jsonify, render_template
import threading
import time
import subprocess

# Ensure psutil is installed
try:
    import psutil
except ImportError:
    subprocess.check_call(["python", '-m', 'pip', 'install', 'psutil'])
    import psutil

app = Flask(__name__)
open_ports = []

def get_open_ports():
    global open_ports
    while True:
        try:
            open_ports = [conn.laddr.port for conn in psutil.net_connections(kind='inet') if conn.status == 'LISTEN']
        except Exception as e:
            print(f"An error occurred while getting open ports: {e}")
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/open_ports')
def api_open_ports():
    return jsonify(open_ports)

if __name__ == "__main__":
    # Start the background thread to get open ports
    thread = threading.Thread(target=get_open_ports)
    thread.daemon = True  # Ensure the thread exits when the main program exits
    thread.start()
    
    # Run the Flask app
    app.run(debug=True)