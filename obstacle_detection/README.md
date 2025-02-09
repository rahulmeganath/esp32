# Real-Time Ultrasonic Sensor Monitoring with ESP32 and MQTT

This project demonstrates how to build a **real-time monitoring system** using an **HC-SR04 ultrasonic sensor**, **ESP32**, and an **MQTT broker**. The system measures distance, sends data to an MQTT broker, and visualizes it on a **web-based dashboard**.

---

## **Project Overview**
The system consists of:
1. **Hardware**:
   - **ESP32**: Microcontroller for data processing and communication.
   - **HC-SR04 Ultrasonic Sensor**: Measures distance in real-time.
2. **MQTT Broker**:
   - A broker running on an **Ubuntu system** to receive and manage sensor data.
3. **Python MQTT Client**:
   - Subscribes to the MQTT topic and saves data for visualization.
4. **Web Dashboard**:
   - A frontend built with **HTML**, **JavaScript**, and **Chart.js** to display:
     - Live distance measurements.
     - Status alerts (**Normal**, **Warning**, **Danger**).
     - A dynamic line chart showing distance trends over time.

---

## **Circuit Connections**
Here’s how to connect the HC-SR04 sensor to the ESP32:

| **HC-SR04 Pin** | **ESP32 Pin** |
|------------------|---------------|
| VCC              | 5V            |
| GND              | GND           |
| Trig             | GPIO 5        |
| Echo             | GPIO 18       |

---

## **Features**
- **Real-Time Data**: The ESP32 sends distance data to the MQTT broker every 2 seconds.
- **Status Alerts**:
  - **Normal**: Distance > 50 cm.
  - **Warning**: Distance between 20 cm and 50 cm.
  - **Danger**: Distance < 20 cm.
- **Interactive Dashboard**:
  - Displays live distance, status, and timestamp.
  - Visualizes distance trends using a line chart.
- **MQTT Integration**:
  - Uses the `esp32/ultrasonic` topic for communication.

---

## **How It Works**
1. The **ESP32** reads distance data from the HC-SR04 sensor.
2. The data is published to the MQTT broker on the `esp32/ultrasonic` topic.
3. A **Python MQTT client** subscribes to the topic and saves the data to a `data.json` file.
4. The **web dashboard** reads `data.json` and updates the display in real-time.

---

## **Files**
- **ESP32 Code**: `esp32_ultrasonic_mqtt.py`  
  - Reads distance data and publishes it to the MQTT broker.
- **Python MQTT Client**: `mqtt_subscriber.py`  
  - Subscribes to the MQTT topic and saves data to `data.json`.
- **Web Dashboard**: `index.html`  
  - Displays live data and visualizations.

---

## **Demo**
Check out the **video demo** to see the system in action!

---

## **Why This Project?**
- **Learn IoT Basics**: Combines hardware, networking, and software.
- **Real-World Applications**: Useful for object detection, smart parking systems, and more.
- **Extensible**: Add more sensors or integrate with cloud platforms.

---

## **Future Enhancements**
- Add more sensors (e.g., temperature, humidity).
- Integrate with cloud platforms for remote monitoring.
- Implement user authentication for the dashboard.

---

## **Get Started**
1. Clone this repository.
2. Set up the hardware as per the circuit connections.
3. Run the ESP32 code to start publishing data.
4. Start the Python MQTT client to subscribe to the topic.
5. Serve the `index.html` file using a web server and open it in your browser.

---

## **Dependencies**
- ESP32: `micropython` with `umqtt.simple` library.
- Python: `paho-mqtt` library.
- Frontend: `Chart.js` for visualizations.
- Mosquitto broker

