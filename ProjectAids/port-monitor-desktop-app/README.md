# Port Monitor Desktop Application

## Overview
The Port Monitor Desktop Application is a tool designed to monitor open ports on your system, detect anomalies, and provide a user-friendly interface for managing these ports. It utilizes machine learning techniques to identify unusual port activity and allows users to block suspicious ports.

## Features
- Real-time monitoring of open ports
- Anomaly detection using Isolation Forest algorithm
- User-friendly graphical interface
- Ability to block anomalous ports
- Display of current open ports and their status

## Installation
To run the application, you need to install the required dependencies. You can do this by running the following command in your terminal:

```
pip install -r requirements.txt
```

## Running the Application
After installing the dependencies, you can start the application by executing the following command:

```
python src/app.py
```

This will launch the desktop application, and you will be able to monitor open ports and manage anomalies through the graphical interface.

## Dependencies
The application requires the following Python packages:
- PyQt5
- psutil
- scikit-learn

Make sure to have these installed before running the application.

## Usage
Once the application is running, you will see the main window displaying the current open ports. The application will continuously monitor these ports and alert you if any anomalies are detected. You can interact with the UI to view details and take actions on the detected ports.

## Contributing
If you would like to contribute to the project, feel free to submit a pull request or open an issue for discussion.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.