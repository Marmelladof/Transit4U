import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from config import SERVER, IS_DEBUG


class CalculatorAgent(Agent):

    def __init__(self, jid: str, password: str):
        super().__init__(jid, password)
        self.my_name = jid

    def agent_say(self, text):
        print(self.my_name + ":\n\t" + str(text) + "\n")

    class ReciveBehav(CyclicBehaviour):
        async def run(self):

            # wait for a message for 10 seconds
            msg = await self.receive(timeout=2)
            if msg:
                if IS_DEBUG:
                    self.agent.agent_say(msg)
                if str(msg.sender) == "sumagent" + SERVER \
                   or str(msg.sender) == "subtractionAgent" + SERVER \
                   or str(msg.sender) == "multiplicationAgent" + SERVER \
                   or str(msg.sender) == "divitionAgent" + SERVER:

                    msg_object = json.loads(msg.body)

                    # Instantiate the message
                    new_msg = Message(to=msg_object["originID"])

                    # Set the "inform" FIPA performative
                    new_msg.set_metadata("performative", "inform")

                    new_msg_object = {
                        "result": msg_object["result"]
                    }
                    msg_json = json.dumps(new_msg_object)

                    new_msg.body = msg_json  # Set the message content
                    await self.send(new_msg)

                # agent_say("Message sent!")
                else:
                    service_provider = ""
                    msg_object = json.loads(msg.body)
                    operation = msg_object["operation"]

                    if operation == "+":
                        service_provider = "sumagent"
                    elif operation == "-":
                        service_provider = "subtractionAgent"
                    elif operation == "*":
                        service_provider = "multiplicationAgent"
                    elif operation == "/":
                        service_provider = "divitionAgent"

                    # Instantiate the message
                    new_msg = Message(to=service_provider + SERVER)

                    # Set the "inform" FIPA performative
                    new_msg.set_metadata("performative", "inform")

                    new_msg_object = {
                        "op1": 1,
                        "op2": 2,
                        "originID": str(msg.sender)
                    }
                    msg_json = json.dumps(new_msg_object)

                    new_msg.body = msg_json  # Set the message content
                    await self.send(new_msg)

    async def setup(self):
        self.agent_say("Agent starting . . .")
        reciveB = self.ReciveBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(reciveB, template)
