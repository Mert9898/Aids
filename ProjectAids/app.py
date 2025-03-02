from flask import Flask, jsonify, render_template
import threading
import time
import subprocess
import numpy as np
from sklearn.ensemble import IsolationForest
import logging
import smtplib
from email.mime.text import MIMEText

# Ensure psutil is installed
try:
    import psutil
except ImportError:
    subprocess.check_call(["python", '-m', 'pip', 'install', 'psutil'])
    import psutil

app = Flask(__name__)

class PortMonitor:
    def __init__(self, contamination=0.05, check_interval=5):
        self.open_ports = []
        self.open_ports_history = []
        self.model = None
        self.contamination = contamination
        self.check_interval = check_interval
        self.initialize_model()

    def initialize_model(self):
        initial_ports = self.get_open_ports()
        self.open_ports_history.append(initial_ports)
        self.model = self.train_isolation_forest(np.array(initial_ports).reshape(-1, 1))

    def get_open_ports(self):
        try:
            return [conn.laddr.port for conn in psutil.net_connections(kind='inet') if conn.status == 'LISTEN']
        except Exception as e:
            logging.error(f"An error occurred while getting open ports: {e}")
            return []

    def detect_anomalies(self, ports):
        if self.model:
            predictions = self.model.predict(np.array(ports).reshape(-1, 1))
            anomalies = [port for port, prediction in zip(ports, predictions) if prediction == -1]
            if anomalies:
                logging.warning(f"Anomalous ports detected: {anomalies}")
                self.block_ports(anomalies)
                self.send_alert(anomalies)

    def update_model(self):
        if len(self.open_ports_history) > 1:
            try:
                history_array = np.array([np.array(ports) for ports in self.open_ports_history], dtype=object)
                flattened_history = np.hstack(history_array).reshape(-1, 1)
                self.model = self.train_isolation_forest(flattened_history)
            except ValueError as e:
                logging.error(f"Error updating model: {e}")

    def monitor_ports(self):
        while True:
            current_ports = self.get_open_ports()
            self.open_ports = current_ports
            self.detect_anomalies(current_ports)
            self.open_ports_history.append(current_ports)
            self.update_model()
            time.sleep(self.check_interval)

    def train_isolation_forest(self, open_ports_history):
        model = IsolationForest(n_estimators=100, contamination=self.contamination)
        model.fit(open_ports_history)
        return model

    def block_ports(self, ports):
        for port in ports:
            logging.info(f"Blocking port: {port}")
            # Example: Use iptables or firewall-cmd on Linux, netsh on Windows
            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=Block Port {port}", "protocol=TCP", "dir=in", f"localport={port}", "action=block"])

    def send_alert(self, anomalies):
        msg = MIMEText(f"Anomalous ports detected: {anomalies}")
        msg['Subject'] = 'Intrusion Detection Alert'
        msg['From'] = 'ozkanmertayaz@gmail.com'
        msg['To'] = 'yzmrtzkn@outlook.com'

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('ozkanmertayaz@gmail.com', '06191999Mao%')
                server.sendmail(msg['From'], [msg['To']], msg.as_string())
            logging.info("Alert sent successfully")
        except Exception as e:
            logging.error(f"Failed to send alert: {e}")

port_monitor = PortMonitor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/open_ports')
def api_open_ports():
    return jsonify(port_monitor.open_ports)

if __name__ == "__main__":
    # Start the background thread to get open ports and detect anomalies
    thread = threading.Thread(target=port_monitor.monitor_ports)
    thread.daemon = True  # Ensure the thread exits when the main program exits
    thread.start()
    
    # Run the Flask app
    app.run(debug=True)