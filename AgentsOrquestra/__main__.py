import os
import spade

# from spade.agent import Agent
# from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
# from spade.message import Message
# from spade.template import Template

from .Semaphore import Semaphore
from .Central import Central

PASSWORD = os.getenv("PASSWORD")
CENTRAL_AGENT_ID = os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")


async def main():
    passwd = PASSWORD
    receiver_jid = SEMAPHORE_AGENT_1_ID
    sender_jid = CENTRAL_AGENT_ID

    semaphore_agent = Semaphore(jid=receiver_jid, password=passwd)
    central_agent = Central(sender_jid, passwd)

    await semaphore_agent.start(auto_register=True)

    central_agent.set("receiver_jid", receiver_jid) # store receiver_jid in the sender knowledge base
    semaphore_agent.set("sender_jid", sender_jid) # store receiver_jid in the sender knowledge base
    await central_agent.start(auto_register=True)

    await spade.wait_until_finished(semaphore_agent)
    await central_agent.stop()
    await semaphore_agent.stop()
    print("Agents finished")

if __name__ == "__main__":
    spade.run(main())