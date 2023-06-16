# from .b_Semaphore import b_Semaphore

# class b_road_crossSemaphore(b_Semaphore):

#     def __init__(self) -> None:
#         self.semaphore_config = {}

#     @staticmethod
#     def required_fields():
#         return []

#     @staticmethod
#     def get_data() -> str:
#         return "Trigger"

#     def setup_parameters(self, semaphore_info) -> dict:
#         if not isinstance(semaphore_info[""], str) or\
#            not isinstance(semaphore_info[""], str):
#             raise ValueError("Invalid Fields")

#         self.semaphore_config[""] = semaphore_info[""]
#         self.semaphore_config[""] = semaphore_info[""]

#     def health_check(self) -> bool:
#         raise NotImplementedError

#     def check_condition(self) -> bool:
#         raise NotImplementedError

#     def serialReader(self) -> bool:
#         while True:
#             data = self.arduino.readline()
#             data = data.decode("utf-8")
#             if data in self.actions:
#                 new_event = self.actions[data]()

#     def serialWriter(self, message) -> None:
#         self.arduino.write(bytes(message, 'utf-8'))
