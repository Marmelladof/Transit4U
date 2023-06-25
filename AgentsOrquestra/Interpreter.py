import os
import time
import json
import serial
from datetime import datetime

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour  # , PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

PASSWORD = os.getenv("PASSWORD")
CENTRAL_AGENT_ID = os.getenv("CENTRAL_AGENT_ID")
CAMERA_AGENT_1_ID = os.getenv("CAMERA_AGENT_1_ID")
SEMAPHORE_AGENT_1_ID = os.getenv("SEMAPHORE_AGENT_1_ID")
INTERPRETER_AGENT_1_ID = os.getenv("INTERPRETER_AGENT_1_ID")
DEBUG = os.getenv("DEBUG", True)
MASK_RCNN = os.getenv("MASK_RCNN", True)
CHANGE_LIGHT_FREQUENCY = 30

if MASK_RCNN:
    from maskrcnn.maskrcnn_predict import image_detection

# Delete this later
else:
    def image_detection(camera):
        sheet_cheat = {'cam1_car': 45, 'cam2_car': 31, 'cam3_people': 1, 'cam4_people': 6}
        return sheet_cheat[camera]


class Interpreter(Agent):

    def __init__(self, jid: str, password: str, cameras: list):
        print("Iniciating Interpreter")
        super().__init__(jid, password)
        self.cameras = cameras

    class RecvBehav(CyclicBehaviour):
        print("Interpreter RecvBehav running")
        async def run(self):
            msg = await self.receive(timeout=5)  # wait for a message for 10 seconds
            if msg:
                
                print("Interpreter here!!:\n\tMessage received with content: {}".format(msg.body))
                if "checkCameras" in msg.body:
                    camera_images = self.agent.get_images(self.agent.cameras)
                    result = self.agent.interpret_images(camera_images)

                    new_msg = Message(to=str(msg.sender))  # Instantiate the message
                    new_msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

                    msg_json = json.dumps(result)

                    print("\n\tSendinfg reply with content: {}".format(msg_json))

                    new_msg.body = msg_json  # Set the message content
                    await  self.send(new_msg)

    async def setup(self):
        print(f"INTERPRETER AGENT: {datetime.now().time()}")
        # b = self.InformBehav(period=2, start_at=start_at)
        c = self.RecvBehav()
        self.add_behaviour(c)

    def get_images(self, camera_list) -> dict:
        if DEBUG:
            local_images = ["ImageDump/istockphoto-155287967-612x612.jpg",
                            "ImageDump/gettyimages-523602632-612x612.jpg",
                            "ImageDump/gettyimages-640848598-170667a.jpg",
                            "ImageDump/Picture1.jpg"]
            response = {camera_list[i]: local_images[i] for i in range(len(camera_list))}
            print(response)
            return response
        else:
            # implement camera agent to retrieve image
            pass
    def interpret_images(self, camera_images):
        car = ['bicycle', 'car', 'motorcycle', 'truck']
        response = {}
        for camera in camera_images.keys():
            maskrcnn_result = image_detection(camera_images[camera])
            print(camera, " got the following detection: ", maskrcnn_result)
            if "car" in camera:
                temp = 0
                for key in maskrcnn_result.keys():
                    if key in car:
                        temp += maskrcnn_result[key]
                response[camera] = temp
            if "people" in camera:
                temp = 0
                if "person" in maskrcnn_result.keys():
                    temp += maskrcnn_result["person"]
                response[camera] = temp
        print(response)
        return response
