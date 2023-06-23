import paho.mqtt.client as mqtt
import os
import serial

broker = os.getenv("BROKER")
port = 1883
username = os.getenv("USER")
password = os.getenv("BROKERPASS")
topic = os.getenv("TOPIC")


class Arduino():
    def __init__(self):
        self.arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)

    # Callback function on successful connection

    def on_connect(client, userdata, flags, rc):
        print("MQTT Subscriber active :))")
        client.subscribe(topic)

    # Callback function on message receipt
    def on_message(client, userdata, msg, self):
        self.changeLights()

    def start_mqtt(self):
        print("Starting MQTT Subscriber!!")

        client = mqtt.Client()
        client.username_pw_set(username, password)

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(broker, port, 60)

        client.loop_forever()

    def serialWriter(self, message) -> None:
        self.arduino.write(bytes(message, 'utf-8'))

    def changeLights(self) -> dict:
        print("Changing Lights")
        self.serialWriter("changeLights")
        return {"success": True,
                "message": "Lights changed"}
