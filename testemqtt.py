import paho.mqtt.client as mqtt
import threading

# Set up some global variables
broker = "mqtt-dashboard.com"
port = 1883
username = "xicoteste"
password = "123"
topic = "test"

# Callback function on successful connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    # Subscribe here to the topic
    client.subscribe(topic)

# Callback function on message receipt
def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()} on topic {msg.topic}")

def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a manual interface.
    client.loop_forever()

# Start MQTT client in a separate thread
mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.start()

# Continue with the rest of your program here
print("The rest of the program continues to run...")
