# Importing Libraries
import serial
import time


class Event:
    def __init__(self) -> None:
        print("Created")

    def check_condition(self) -> bool:
        response = input("Should we change the lights? (y-Y/n-N):")
        if response in ["Y", "y", "\n"]:
            return True
        return False

    def action(self):
        print("Changing Lights")
        SerialWriter("changeLights")


class OtherEvent:
    def __init__(self) -> None:
        print("Created")

    def check_condition(self) -> bool:
        response = input("Should flicker the lights? (y-Y/n-N):")
        if response in ["Y", "y", "\n"]:
            return True
        return False

    def action(self):
        print("Flickering Lights")
        SerialWriter("flickerLights")


triggerMessages = {"changeLights": Event,
                   "flickerLights": OtherEvent}


arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)


def changeLights():
    SerialWriter("changeLights")


def SerialWriter(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(1)
    data = arduino.readline()
    return data.decode("utf-8")


def SerialReader(parse):
    if parse in triggerMessages:
        new_event = triggerMessages[parse]()
        if new_event.check_condition():
            new_event.action()
        # Wait for success message
        time.sleep(1)
        data = arduino.readline()
        print(data.decode("utf-8"))


while True:
    data = arduino.readline()
    SerialReader(data.decode("utf-8"))
