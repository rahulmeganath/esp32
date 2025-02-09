import paho.mqtt.client as mqtt
import json

# MQTT Broker Configuration
MQTT_BROKER = "192.168.0.104"  # Replace with your MQTT broker IP
MQTT_TOPIC = "esp32/ultrasonic"

# Callback when a message is received
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"📥 Received: {payload}")

    # Save the data to a JSON file for the frontend
    try:
        data = json.loads(payload)
        with open("data.json", "w") as file:
            json.dump(data, file)
        print("✅ Data saved to data.json")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# Set up MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the broker
try:
    client.connect(MQTT_BROKER)
    print(f"✅ Connected to MQTT Broker: {MQTT_BROKER}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

# Subscribe to the topic
client.subscribe(MQTT_TOPIC)
print(f"🎧 Subscribed to topic: {MQTT_TOPIC}")

# Start the loop to listen for messages
client.loop_forever()