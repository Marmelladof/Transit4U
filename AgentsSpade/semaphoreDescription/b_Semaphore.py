import serial
import json

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class b_Semaphore(Agent):

    def __init__(self, semaphore) -> None:
        jid = semaphore["jid"]
        password = semaphore["password"]
        super().__init__(jid, password)
        self.my_name = jid
        self.semaphore_config = {}
        self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
        self.actions = {"changeLights": self.changeLights,
                        "flickerLights": self.flickerLights}

    class behavior(FSMBehaviour):
        async def on_start(self):
            pass

        async def on_end(self):
            pass
    # This function is the one that takes care of send a msg to another
    # agent
    # class sending(State):
    #     async def run(self):
    #         agents=[
    #                     #list of agents you want to send them the msg
    #                 ]
    #         for agent in agents:
    #             msg = Message(to=agent)
    #             msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
    #             msg.body = "Your Message"
    #             await self.send(msg)
    #         self.set_next_state("waiting")
    # This function is the one that takes care of receiving a msg
    # from another agent

    class waiting(State):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                # Do what you want with the message in
                # our case we will just print it
                print(msg)
                await self.agent.stop()

    # this function is the one that will setup your agent
    async def setup(self):
        fsm = self.behavior()
        fsm.add_state(name="sending", state=self.RequestBehav(), initial=True)
        fsm.add_state(name="sending", state=self.ReciveBehav(), initial=True)
        fsm.add_state(name="waiting", state=self.waiting())

        fsm.add_transition(source="sending", dest="waiting")
        fsm.add_transition(source="waiting", dest="sending")

        self.add_behaviour(fsm)

    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    def setup_parameters(self, semaphore_info) -> dict:
        if not isinstance(semaphore_info[""], str) or\
           not isinstance(semaphore_info[""], str):
            raise ValueError("Invalid Fields")

        self.semaphore_config[""] = semaphore_info[""]
        self.semaphore_config[""] = semaphore_info[""]

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

    class ReciveBehav(State):
        async def run(self):
            while True:
                # wait for a message for 10 seconds
                msg = await self.receive(timeout=2)
                if msg:
                    if IS_DEBUG:
                        self.agent.agent_say(msg)
                    if str(msg.sender) == "afonsobmelo" + SERVER:
                        msg_object = json.loads(msg.body)

                        action = str(msg_object["request"])
                        if action in self.actions:
                            result = self.actions[action]()

                        # Instantiate the message
                        new_msg = Message(to=str(msg.sender))

                        # Set the "inform" FIPA performative
                        new_msg.set_metadata("performative", "inform")

                        new_msg_object = {
                            "result": str(result),
                            "originID": msg_object["originID"]
                        }
                        msg_json = json.dumps(new_msg_object)

                        new_msg.body = msg_json  # Set the message content
                        await self.send(new_msg)

    class RequestBehav(State):
        async def run(self):
            while True:
                # Instantiate the message
                new_msg = Message(to="transit4ucentral" + SERVER)
                # Set the "inform" FIPA performative
                new_msg.set_metadata("performative", "inform")

                trigger = self.agent.serialReader()
                if trigger:
                    new_msg_object = {
                        "request": str(trigger)
                    }
                    msg_json = json.dumps(new_msg_object)

                    new_msg.body = msg_json  # Set the message content
                    await self.send(new_msg)

    async def setup(self):
        self.agent_say("Agent starting . . .")
        reciveB = self.ReciveBehav()
        requestB = self.ReciveBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(reciveB, template)
        self.add_behaviour(requestB, template)
