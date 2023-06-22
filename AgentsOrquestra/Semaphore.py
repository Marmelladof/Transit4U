import os
import time
import serial
from datetime import datetime

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour  # , PeriodicBehaviour, OneShotBehaviour
# from spade.message import Message
from spade.template import Template

PASSWORD = os.getenv("PASSWORD")
CENTRAL_AGENT_ID = os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")
CHANGE_LIGHT_FREQUENCY = 30


class Semaphore(Agent):

    def __init__(self, jid: str, password: str):
        print("Iniciating Semaphore")
        super().__init__(jid, password)
        self.next_light_change = datetime.now().timestamp() + CHANGE_LIGHT_FREQUENCY
        self.arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)

    # class InformBehav(PeriodicBehaviour):
    #     async def run(self):
    #         print(f"PeriodicSenderBehaviour running at {datetime.now().time()}: {self.counter}")
    #         msg = Message(to=self.get("receiver_jid"))  # Instantiate the message
    #         msg.body = "Hello World"  # Set the message content

    #         await self.send(msg)
    #         print("Message sent!")

    #         if self.counter == 5:
    #             self.kill()
    #         self.counter += 1

    #     async def on_end(self):
    #         # stop agent from behaviour
    #         await self.agent.stop()

    #     async def on_start(self):
    #         self.counter = 0
    
    class RecvBehav(CyclicBehaviour):
        print("Semaphore RecvBehav running")
        async def run(self):
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
                if "changeLights" in msg.body:
                    result = self.agent.changeLights()
                    self.agent.next_light_change = datetime.now().timestamp() + CHANGE_LIGHT_FREQUENCY
                    print(result)

    # class ChangeLights(CyclicBehaviour):
    #     async def run(self):
    #         if self.agent.next_light_change <= datetime.now().timestamp():
    #             self.agent.next_light_change = datetime.now().timestamp() + CHANGE_LIGHT_FREQUENCY
    #             result = self.agent.changeLights()
    #             print(result)
    #         else:
    #             time.sleep(0.1)

    #     async def on_end(self):
    #         await self.agent.stop()

    async def setup(self):
        print(f"SEMAPHORE AGENT: {datetime.now().time()}")
        start_at = datetime.now()
        # b = self.InformBehav(period=2, start_at=start_at)
        c = self.RecvBehav()
        # d = self.ChangeLights()
        # self.add_behaviour(b, template)
        self.add_behaviour(c)
        # self.add_behaviour(d, template)

    def health_check(self) -> bool:
        raise NotImplementedError

    def check_condition(self) -> bool:
        return True

    def serialReader(self) -> None:
        data = self.arduino.readline()
        data = data.decode("utf-8")
        if data in self.actions:
            # self.actions[data]()
            return data
        return None

    def serialWriter(self, message) -> None:
        self.arduino.write(bytes(message, 'utf-8'))

    def changeLights(self) -> dict:
        print("Changing Lights")
        self.serialWriter("changeLights")
        return {"success": True,
                "message": "Lights changed"}

    def flickerLights(self) -> dict:
        print("Flickering Lights")
        self.serialWriter("flickerLights")
        return {"success": True,
                "message": "Lights flickered"}
