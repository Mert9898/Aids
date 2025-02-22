import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import socket
import psutil
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to get open ports
def get_open_ports():
    open_ports = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN':
            open_ports.append(conn.laddr.port)
    return open_ports

# Function to scan for threats
def scan_for_threats(open_ports):
    logging.info("Scanning for threats...")
    threats: list = []
    for port in open_ports:
        if port %2 == 0:
            threats.append("Even port number detected")
            threats.append(port)
        if threats:
            logging.warning(f"Threats detected: {threats}")
        else:
            logging.info("No threats detected")

# Function to monitor threats in real-time
def monitor_threats(delay=5):
    try:
        while True:
            open_ports = get_open_ports()
            scan_for_threats(open_ports)
            logging.info(f"Scanned for threats on open ports: {open_ports}")
            #       Add a delay to avoid excessive CPU usage
            time.sleep(5)
    except KeyboardInterrupt:   
        print("Threat monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    monitor_threats()