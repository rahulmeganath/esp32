import network
import time
import machine
import ubinascii
from umqtt.simple import MQTTClient

# MQTT Broker Configuration
MQTT_BROKER = "192.168.0.104"  # Change to your Ubuntu MQTT broker IP
MQTT_TOPIC = "esp32/ultrasonic"

# Ultrasonic Sensor Pins
TRIG_PIN = 5
ECHO_PIN = 18

# Initialize Sensor Pins
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

# Constants for Alerts
WARNING_DISTANCE = 50  # Distance in cm for warning
DANGER_DISTANCE = 20   # Distance in cm for danger

# Read distance from HC-SR04
def get_distance():
    """
    Measures distance using HC-SR04 ultrasonic sensor.
    Returns distance in centimeters (cm).
    """
    trig.off()
    time.sleep_us(2)  # Ensure trigger is LOW
    trig.on()
    time.sleep_us(10)  # 10µs pulse to trigger measurement
    trig.off()

    pulse_start = pulse_end = 0

    # Wait for echo response (avoid infinite loop)
    start_time = time.ticks_ms()
    while echo.value() == 0:
        pulse_start = time.ticks_us()
        if time.ticks_diff(time.ticks_ms(), start_time) > 100:  # Timeout 100ms
            print("Echo timeout, object too far or sensor error.")
            return None

    while echo.value() == 1:
        pulse_end = time.ticks_us()
        if time.ticks_diff(time.ticks_ms(), start_time) > 100:  # Timeout 100ms
            print("Echo timeout, object too far or sensor error.")
            return None

    # Calculate distance in cm
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 0.0343) / 2  # Speed of sound: 343 m/s → 0.0343 cm/µs

    return round(distance, 2) if distance > 2 and distance < 400 else None  # Valid range: 2cm to 400cm

# Get Current Timestamp
def get_timestamp():
    """
    Returns the current timestamp in the format: YYYY-MM-DD HH:MM:SS.
    Note: ESP32 does not have a real-time clock, so this is based on uptime.
    """
    uptime_seconds = time.time()
    # Convert to a human-readable format (assuming 1970-01-01 as the start date)
    return time.localtime(uptime_seconds)

# Connect to MQTT Broker
def mqtt_connect():
    """
    Connects to the MQTT broker.
    Returns an MQTT client object.
    """
    client_id = ubinascii.hexlify(machine.unique_id()).decode()
    client = MQTTClient(client_id, MQTT_BROKER)
    try:
        client.connect()
        print("✅ Connected to MQTT Broker:", MQTT_BROKER)
        return client
    except Exception as e:
        print("❌ MQTT Connection Failed:", e)
        return None

# Publish Distance Data with Alerts
def publish_data(client):
    """
    Reads distance, determines status (normal, warning, danger),
    and publishes data to the MQTT broker every 2 seconds.
    """
    if not client:
        print("❌ MQTT client not connected.")
        return

    while True:
        distance = get_distance()
        if distance is not None:
            # Determine status based on distance
            if distance < DANGER_DISTANCE:
                status = "danger"
            elif distance < WARNING_DISTANCE:
                status = "warning"
            else:
                status = "normal"

            # Get current timestamp
            timestamp = get_timestamp()
            timestamp_str = f"{timestamp[0]}-{timestamp[1]:02d}-{timestamp[2]:02d} {timestamp[3]:02d}:{timestamp[4]:02d}:{timestamp[5]:02d}"

            # Prepare payload
            payload = f'{{"distance_cm": {distance}, "status": "{status}", "timestamp": "{timestamp_str}"}}'
            print(f"📡 Publishing: {payload}")

            try:
                client.publish(MQTT_TOPIC, payload)
            except Exception as e:
                print("⚠️ Publish Error:", e)
        else:
            print("⚠️ Invalid measurement, skipping publish.")

        time.sleep(2)  # Send data every 2 seconds

# Main Execution
try:
    client = mqtt_connect()
    if client:
        publish_data(client)
except Exception as e:
    print("❌ Error:", e)
