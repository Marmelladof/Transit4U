import os
import spade
from datetime import datetime

# from spade.agent import Agent
# from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
# from spade.message import Message
# from spade.template import Template

from .Semaphore import Semaphore
from .Central import Central
from .Interpreter import Interpreter

PASSWORD = os.getenv("PASSWORD")
CENTRAL_AGENT_ID = os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")
INTERPRETER_AGENT_2_ID = os.getenv("INTERPRETER_AGENT_2_ID")
MAX_TIME_WITH_WAITING = "???"

SEMAPHORES = \
            {SEMAPHORE_AGENT_1_ID:
                {"Cameras":
                    ["cam1_car",
                     "cam2_car",
                     "cam3_people",
                     "cam4_people"],
                 "State_options":
                    {"A": ["cam1_car", "cam2_car"],
                     "B": ["cam3_people", "cam4_people"]},                
                 "Current_state": "A",
                 "Interpreter": INTERPRETER_AGENT_1_ID,
                 "last_change": 0,
                 "Waiting": False,
                 "default_state": "A"
                }
            }

async def main():
    passwd = PASSWORD
    semaphore_jid = SEMAPHORE_AGENT_1_ID
    central_jid = CENTRAL_AGENT_ID
    interpreter_jid = INTERPRETER_AGENT_1_ID
    camera_jid = CAMERA_AGENT_1_ID
    central_agent = Central(jid=central_jid, password=passwd, semaphores=SEMAPHORES)

    # Setup interpreter and semaphore angents
    for semaphore in SEMAPHORES.keys():
        semaphore_agent = Semaphore(jid=semaphore, password=passwd)
        SEMAPHORES[semaphore]["last_change"] = datetime.now().timestamp()
        interpreter_agent = Interpreter(jid=SEMAPHORES[semaphore]["Interpreter"],
                                        password=passwd,
                                        cameras=SEMAPHORES[semaphore]["Cameras"])
        await semaphore_agent.start(auto_register=True)
        interpreter_agent.set("camera_jid", camera_jid) # store receiver_jid in the sender knowledge base
        await interpreter_agent.start(auto_register=True)

    central_agent.set("interpreter_jid", interpreter_jid) # store receiver_jid in the sender knowledge base
    central_agent.set("semaphore_jid", semaphore_jid) # store receiver_jid in the sender knowledge base
    await central_agent.start(auto_register=True)

    await spade.wait_until_finished(semaphore_agent)
    await spade.wait_until_finished(interpreter_agent)
    await central_agent.stop()
    await semaphore_agent.stop()
    await interpreter_agent.stop()
    print("Agents finished")

if __name__ == "__main__":
    spade.run(main())