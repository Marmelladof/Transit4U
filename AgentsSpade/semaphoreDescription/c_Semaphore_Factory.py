from .b_Semaphore import b_Semaphore
# from .b_road_crossSemaphore import b_road_crossSemaphore


def available_scenarios() -> dict:
    scenarios = {}

    scenarios["Road"] = {}
    scenarios["Road"][True] = b_Semaphore
    # scenarios["Road"][False] = b_road_crossSemaphore

    # scenarios["Intersection"] = {}
    # scenarios["Intersection"][True] = b_intersectionSemaphore
    # scenarios["Intersection"][False] = b_intersectionSemaphore

    return scenarios


def create_b_Semaphore(semaphore) -> b_Semaphore:
    try:
        options = available_scenarios()
        return options[semaphore["Scenerio"]][semaphore["Crosswalk"]](semaphore)  # noqa: E501
    except Exception as e:
        if isinstance(e, KeyError):
            raise ValueError("Missing Arguments: {}".format(e.args))

        elif 'Invalid Fields' in e.args:
            raise ValueError("Invalid Fields, check equipment info {}"
                             .format(semaphore))
