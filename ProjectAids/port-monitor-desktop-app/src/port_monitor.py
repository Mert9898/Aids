import threading
import time
import subprocess
import numpy as np
from sklearn.ensemble import IsolationForest
import logging
import psutil  # Add this import

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
            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=Block Port {port}", "protocol=TCP", "dir=in", f"localport={port}", "action=block"])

    def send_alert(self, anomalies):
        logging.warning(f"Anomalous ports detected: {anomalies}")

    def start_monitoring(self):
        thread = threading.Thread(target=self.monitor_ports)
        thread.daemon = True
        thread.start()