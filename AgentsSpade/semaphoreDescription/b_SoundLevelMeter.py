from web_api.resources.event import check_duplicated_equip_entry


class b_SoundLevelMeter:

    def __init__(self, equipment_config: dict, metrics) -> None:
        self.metrics = metrics
        self.equipment_config = {}
        self.setup_required_parameters(equipment_config)

    @staticmethod
    def required_fields():
        return ["Brand", "Model", "SerialNr"]

    @staticmethod
    def get_valid_data() -> dict:
        return {
            "metrics_valid":
                [
                   "LAF0.5sMax",
                   "LAF0.5sMin",
                   "LAI",
                   "LAF",
                   "LAI0.5sMax",
                   "LAI0.5sMin",
                   "LAIeq0.5s",
                   "LAIT3",
                   "LAIT5",
                   "LCpeak"
                ],
            "spectrum_valid":
                [
                    "Leq0.5s",
                    "LF"
                ]
        }

    @staticmethod
    def get_valid_list_order() -> list:
        return ["Brand",
                "Model",
                "Serial Nr",
                "State",
                "Locked"]

    def setup_required_parameters(self, equiment_info) -> dict:
        if not isinstance(equiment_info["Brand"], str) or\
           not isinstance(equiment_info["Model"], str) or\
           not isinstance(equiment_info["State"], str) or\
           not isinstance(equiment_info["SerialNr"], str) or\
           "Locked" not in equiment_info:
            raise ValueError("Invalid Fields")

        self.equipment_config["Brand"] = equiment_info["Brand"]
        self.equipment_config["Model"] = equiment_info["Model"]
        self.equipment_config["State"] = equiment_info["State"]
        self.equipment_config["Locked"] = equiment_info["Locked"]
        self.equipment_config["SerialNr"] = equiment_info["SerialNr"]

    def validate_parameters(self, parameter_keys) -> None:
        if "SerialNr" in parameter_keys:
            valid_entry = check_duplicated_equip_entry(
                            {"SerialNr": self.equipment_config["SerialNr"],
                             "Brand": self.equipment_config["Brand"]})
            if not valid_entry["success"]:
                raise ValueError(valid_entry["message"])

    def get_equipment_info(self) -> dict:
        raise NotImplementedError

    def delete_audio(self, audio_location) -> str:
        raise NotImplementedError

    def health_check(self) -> bool:
        raise NotImplementedError

    def get_list_audio_files(self) -> list:
        raise NotImplementedError

    def download_audio(self, audio_location: any) -> dict:
        raise NotImplementedError

    def config_metrics(self) -> None:
        raise NotImplementedError

    def get_metric(self, metric_name: str) -> tuple:
        raise NotImplementedError

    def get_hour_correction(self) -> int:
        raise NotImplementedError

    def get_metrics(self, metrics=None) -> dict:
        raise NotImplementedError

    def start_record(self) -> None:
        raise NotImplementedError

    def stop_record(self) -> None:
        raise NotImplementedError

    def current_location(self) -> None:
        """Get geolocation of equipment
        If not found return None"""
        raise NotImplementedError
