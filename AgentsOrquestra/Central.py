import datetime
import os
import json
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from spade.message import Message
from .semaphoreLogic import semaphoreLogic
PASSWORD = os.getenv("PASSWORD")
CENTRAL_AGENT_ID = os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")


class Central(Agent):

    def __init__(self, jid: str, password: str, semaphores: dict):
        self.semaphores = semaphores
        super().__init__(jid, password)
    class InformBehav(PeriodicBehaviour):
        async def run(self):
            for semaphore in self.agent.semaphores.keys():
                interpreter_jid = self.agent.semaphores[semaphore]["Interpreter"]
                print(f"PeriodicCameraCheck running at {datetime.datetime.now().time()}")
                msg = Message(to=interpreter_jid)  # Instantiate the message
                msg.body = "checkCameras"  # Set the message content

                await self.send(msg)
                print(f"Central here!!\n\tMessage sent to {interpreter_jid}: checkCameras.")
                print(json.dumps(self.agent.semaphores[semaphore], indent=2))

    class RecvBehav(CyclicBehaviour):
        print("Central RecvBehav running")
        async def run(self):
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                print("Central here!!:\n\tMessage received with content: {}".format(msg.body))
                interpreter_jid = str(msg.sender)
                for semaphore in self.agent.semaphores.keys():
                    if interpreter_jid == self.agent.semaphores[semaphore]["Interpreter"]:
                        values = json.loads(msg.body)
                        result = self.agent.semaphore_logic(values, self.agent.semaphores[semaphore])
                        print("Central here!!")
                        if result["change"]:
                            print("\n\tGreen light to change semaphore! (eheh, get it? Green Light?)")
                            msg = Message(to=self.get("semaphore_jid"))  # Instantiate the message
                            msg.body = "changeLights"  # Set the message content

                            await self.send(msg)
                            print("\t\tMessage sent: changeLights")
                        else:
                            print("\n\tRed light to change semaphore! (eheh, get it? Red Light?)")
                        # Update state of semaphore
                        for key in result["update"]:
                            self.agent.semaphores[semaphore][key] = result["update"][key]


        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(period=60, start_at=start_at)
        c = self.RecvBehav()
        self.add_behaviour(b)
        self.add_behaviour(c)
    
    def semaphore_logic(self, values, semaphore):
        semaphore = semaphoreLogic(semaphore)
        result = semaphore.change_lights(values)
        return result
