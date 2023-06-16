import spade
import os

from semaphoreDescription.c_Semaphore_Factory import create_b_Semaphore
from centralAgent import centralAgent

PASSWORD = os.getenv("PASSWORD")

CENTRAL_AGENT_ID = "afonsobmelo"  # os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")


# async def run_semaphore():

# async def run_central():


if __name__ == "__main__":

    central = centralAgent(jid="afonsobmelo@jabbers.one",
                           password="1Presunto69!")
    func = central.start()

    semaphore_1 = create_b_Semaphore({"jid": SEMAPHORE_AGENT_1_ID,
                                      "password": PASSWORD,
                                      "Scenerio": "Road",
                                      "Crosswalk": True})
    func2 = semaphore_1.start()

    central.RequestBehav()
