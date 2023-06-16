import json
import os

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

PASSWORD = os.getenv("PASSWORD")
CENTRAL_AGENT_ID = "afonsobmelo"  # os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")


class centralAgent(Agent):

    def __init__(self, jid, password) -> None:
        super().__init__(jid, password)

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
        fsm.add_state(name="waiting", state=self.waiting())

        fsm.add_transition(source="sending", dest="waiting")
        fsm.add_transition(source="waiting", dest="sending")

        self.add_behaviour(fsm)

    # After this you can add any function you like depending on the
    # behaviours of your agent

    class RequestBehav(State):
        async def run(self):
            new_msg = Message(to=SEMAPHORE_AGENT_1_ID)
            new_msg.set_metadata("performative", "inform")

            trigger = input("Actions to take:\n\t"
                            "1. Change Lights\n\t"
                            "2. Flicker Lights")

            if trigger == "1":
                request = "changeLights"
            if trigger == "2":
                request = "flickerLights"

            new_msg_object = {
                "request": request
            }
            msg_json = json.dumps(new_msg_object)

            new_msg.body = msg_json  # Set the message content
            await self.send(new_msg)

    class ReciveBehav(CyclicBehaviour):
        async def run(self):
            # wait for a message for 5 seconds
            msg = await self.receive(timeout=2)
            if msg:
                if str(msg.sender) == SEMAPHORE_AGENT_1_ID:
                    msg_object = json.loads(msg.body)

                    action = str(msg_object["request"])

                    decision = input(f"Agent asking for permission to take action: {action}")  # noqa: E501

                    if decision in ["y", "Y", "\n"]:
                        new_msg = Message(to=SEMAPHORE_AGENT_1_ID)
                        new_msg.set_metadata("performative", "inform")

                        new_msg_object = {
                            "request": action
                        }
                        msg_json = json.dumps(new_msg_object)

                        new_msg.body = msg_json  # Set the message content
                        await self.send(new_msg)

            else:
                self.agent.agent_say("Finishing")
                # self.agent.agent_say("Did not received any message after 10 seconds")  # noqa: E501
                await self.agent.stop()

    # async def setup(self):
    #     self.agent_say("Agent starting . . .")
    #     requestB = self.RequestBehav()
    #     reciveB = self.ReciveBehav()
    #     template = Template()
    #     template.set_metadata("performative", "inform")
    #     self.add_behaviour(requestB, template)
    #     self.add_behaviour(reciveB, template)
