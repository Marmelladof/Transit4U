from datetime import datetime

MAX_WAITING_TIME = 60
MAX_FIXED_TIME = 300

class semaphoreLogic():
    def __init__(self, semaphore):
        self.cameras = semaphore["Cameras"]
        self.state_options = semaphore["State_options"]
        self.current_state = semaphore["Current_state"]
        self.last_change = semaphore["last_change"]
        self.waiting = semaphore["Waiting"]
        self.default_state = semaphore["default_state"]
    
    def change_lights(self, camera_results):
        ts = datetime.now().timestamp()

        # Waiting person/car scenario
        if self.waiting and \
           (ts - self.last_change) >= MAX_WAITING_TIME:
            print("Max waiting time exceeded. Changing lights!")

            return {"change": True, "update": {"Waiting": False,
                                               "last_change": ts}}
        # Too long on same light scenario
        if (ts - self.last_change) >= MAX_FIXED_TIME:
            print("Max fixed time exceeded. Changing lights!")

            return {"change": True, "update": {"last_change": ts}}
        
        states = list(self.state_options.keys())
        json_temp = {state: 0 for state in states}
        for camera in camera_results.keys():
            for state in states:
                if camera in self.state_options[state]:
                    json_temp[state] += camera_results[camera]
        states_sorted = sorted(json_temp.items(), key=lambda x:x[1])
        print(states_sorted)
        # RETURNS LIST OF TUPLES WITH SORTED VALUES i.e. [('A', 100), ('B', 2)] 
        if self.current_state == states_sorted[1][0]:
            if states_sorted[1][1] > 0:
                return {"change": False,
                        "update": {"Waiting": True}}
            else:
                return {"change": False,
                        "update": {"Waiting": False}}
        else:
            if states_sorted[0][1] > 0:
                return {"change": True, "update": {"last_change": ts,
                                                   "Waiting": True}}
            else:
                return {"change": True, "update": {"last_change": ts,
                                                   "Waiting": False}}
