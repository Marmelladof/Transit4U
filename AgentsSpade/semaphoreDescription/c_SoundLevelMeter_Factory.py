from equipment.b_SoundLevelMeter import b_SoundLevelMeter

from equipment.b_SoundLevelMeter_Dummy import \
    b_SoundLevelMeter_Dummy
from equipment.b_SoundLevelMeter_Dummy_OnlyMetrics import \
    b_SoundLevelMeter_Dummy_OnlyMetrics
from equipment.b_SoundLevelMeter_DummyWebDevice import \
    b_SoundLevelMeter_DummyWebDevice
from equipment.b_SoundLevelMeter_01db_Cube import \
    b_SoundLevelMeter_01db_Cube


def available_equipments_brands_and_models() -> dict:
    brand_models = {}

    brand_models["Dummy"] = {}
    brand_models["Dummy"]["Dummy"] = b_SoundLevelMeter_Dummy
    brand_models["Dummy"]["OnlyMetrics"] = b_SoundLevelMeter_Dummy_OnlyMetrics

    brand_models["01db"] = {}
    brand_models["01db"]["Cube"] = b_SoundLevelMeter_01db_Cube

    brand_models["ISQ"] = {}
    brand_models["ISQ"]["Docker Device"] = b_SoundLevelMeter_DummyWebDevice

    return brand_models


def create_b_SoundLevelMeter(equipment, metrics) -> b_SoundLevelMeter:
    try:
        options = available_equipments_brands_and_models()
        return options[equipment["Brand"]][equipment["Model"]](equipment,
                                                               metrics)
    except Exception as e:
        if isinstance(e, KeyError):
            raise ValueError("Missing Arguments: {}".format(e.args))

        elif 'Invalid Fields' in e.args:
            raise ValueError("Invalid Fields, check equipment info {}"
                             .format(equipment))
        raise ValueError(
            "Invalid equipment Brand or Model ({}, {})"
            .format(equipment["Brand"], equipment["Model"]))
