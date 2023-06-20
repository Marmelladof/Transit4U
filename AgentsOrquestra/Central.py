import datetime
import os
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

PASSWORD = os.getenv("PASSWORD")
CENTRAL_AGENT_ID = os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")


class Central(Agent):
    class InformBehav(PeriodicBehaviour):
        async def run(self):
            _input  = input("Should we change Lights?")

            if _input in ["Y", "y"]:

                print(f"PeriodicSenderBehaviour running at {datetime.datetime.now().time()}: {self.counter}")
                msg = Message(to=self.get("receiver_jid"))  # Instantiate the message
                msg.body = "changeLights"  # Set the message content

                await self.send(msg)
                print("Message sent!")

            if self.counter == 100000:
                self.kill()
            self.counter += 1

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

        async def on_start(self):
            self.counter = 0
    
    # class RecvBehav(CyclicBehaviour):
    #     async def run(self):
    #         print("RecvBehav1.2 running")
    #         msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
    #         if msg:
    #             print("Message received with content: {}".format(msg.body))
    #         else:
    #             print("Did not received any message after 10 seconds")
    #             self.kill()

    #     async def on_end(self):
    #         await self.agent.stop()

    async def setup(self):
        print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(period=2, start_at=start_at)
        # c = self.RecvBehav()
        self.add_behaviour(b)
        # self.add_behaviour(c)


# class ReceiverAgent(Agent):
#     class RecvBehav(CyclicBehaviour):
#         async def run(self):
#             print("RecvBehav running")
#             msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
#             if msg:
#                 print("Message received with content: {}".format(msg.body))
#                 msg = Message(to=self.get("sender_jid"))  # Instantiate the message
#                 msg.body = "Received your <Hello World>"  # Set the message content

#                 await self.send(msg)
#                 print("Message sent!")
#             else:
#                 print("Did not received any message after 10 seconds")
#                 self.kill()

#         async def on_end(self):
#             await self.agent.stop()

#     async def setup(self):
#         print("ReceiverAgent started")
#         b = self.RecvBehav()
#         self.add_behaviour(b)
