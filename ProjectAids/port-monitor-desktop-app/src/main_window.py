from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QMessageBox
from port_monitor import PortMonitor
import sys
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Monitor")
        self.setGeometry(100, 100, 600, 400)

        self.port_monitor = PortMonitor()
        self.init_ui()
        self.start_monitoring()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Open Ports:")
        self.layout.addWidget(self.label)

        self.port_list = QListWidget()
        self.layout.addWidget(self.port_list)

        self.block_button = QPushButton("Block Selected Port")
        self.block_button.clicked.connect(self.block_selected_port)
        self.layout.addWidget(self.block_button)

    def start_monitoring(self):
        self.monitoring_thread = threading.Thread(target=self.monitor_ports)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def monitor_ports(self):
        while True:
            open_ports = self.port_monitor.get_open_ports()
            self.update_port_list(open_ports)
            self.port_monitor.detect_anomalies(open_ports)
            time.sleep(self.port_monitor.check_interval)

    def update_port_list(self, open_ports):
        self.port_list.clear()
        self.port_list.addItems(map(str, open_ports))

    def block_selected_port(self):
        selected_items = self.port_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No port selected.")
            return

        selected_port = int(selected_items[0].text())
        self.port_monitor.block_ports([selected_port])
        QMessageBox.information(self, "Info", f"Blocked port: {selected_port}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())