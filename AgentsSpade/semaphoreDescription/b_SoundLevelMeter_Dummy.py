import random
from datetime import datetime
from io import BytesIO

from equipment.b_SoundLevelMeter import b_SoundLevelMeter

AUDIO_FILES_PROBABILITY = 0.16  # should be one event per minute


class b_SoundLevelMeter_Dummy(b_SoundLevelMeter):

    def __init__(self, equipment_config: dict, metrics) -> None:
        super().__init__(equipment_config, metrics)

    @staticmethod
    def required_fields():
        return b_SoundLevelMeter.required_fields() + []

    def config_metrics(self) -> None:
        valid_data = self.get_valid_data()
        # Match for metrics chosen in job with the specified order
        self.current_metrics = [x for x in self.metrics if x in valid_data["metrics_valid"]]  # noqa: E501
        self.current_spectrums = [x for x in self.metrics if x in valid_data["spectrum_valid"]]  # noqa: E501

    def validate_parameters(self, parameter_keys) -> None:
        return super().validate_parameters(parameter_keys)

    def get_metric(self, metric_name: str) -> tuple:
        # utc time
        return (datetime.now(), random.random())

    @staticmethod
    def get_valid_data() -> dict:
        return b_SoundLevelMeter.get_valid_data()

    @staticmethod
    def get_valid_list_order() -> list:
        return b_SoundLevelMeter.get_valid_list_order()

    def setup_required_parameters(self, equipment_info) -> dict:
        super().setup_required_parameters(equipment_info)
        self.equipment_config["InJob"] = None

    def get_hour_correction(self):
        return 1

    def get_metrics(self, metrics=None) -> dict:

        # Metrics
        # {"LAFMax": (ts, value), "LAI": (ts, value) ....}
        collected_metrics = {}
        for metric in self.current_metrics:
            collected_metrics[metric] = (int(datetime.now().timestamp() * 1000000000),  # noqa: E501
                                         random.random())

        # Spectrums
        # {"Leq0.5s": (ts, [value_list]), "LF": (ts, [value_list]) ....}
        collected_spectrums = {}
        for spectrum in self.current_spectrums:
            spectrum_list = []
            for i in range(36):
                spectrum_list.append(random.randint(0, 100))

            collected_spectrums[spectrum] = (int(datetime.now().timestamp() * 1000000000),  # noqa: E501
                                             spectrum_list)

        return collected_metrics, collected_spectrums

    def health_check(self) -> None:
        return

    def get_list_audio_files(self) -> list:
        # only generates files with a low probability
        if random.random() > AUDIO_FILES_PROBABILITY:
            return []

        return [["equipment/tests/audios/dummy.mp3",
                 datetime.now().timestamp()],
                ["equipment/tests/audios/dummy1.mp3",
                 datetime.now().timestamp()]]

    def delete_audio(self, audio_location) -> str:
        return "Not sure if I should be deleting files..."

    def get_equipment_info(self) -> dict:
        return self.equipment_config

    def download_audio(self, audio_location: any) -> None:

        # Randommize file and give it a current timestamp
        import os
        import shutil
        import string
        import random

        S = 10  # number of characters in the string.
        ran = ''.join(random.choices(
            string.ascii_uppercase + string.digits,
            k=S))

        tmp_file = audio_location[:len(".mp3")]+ran+".mp3"
        shutil.copyfile(audio_location, tmp_file)

        # USE FILE-LIKE OBJECT TO TRANSFER AUDIO FILE
        # audio_name = audio_location.split('/')[-1]

        my_sound = BytesIO()
        with open(tmp_file, "rb") as audio_fr:
            my_sound.write(audio_fr.read())
            my_sound.seek(0)

        # remove temporary file (to generate a new creation date)
        os.remove(tmp_file)

        # with open(audio_name, "wb") as audio_fw:
        #     audio_fw.write(my_sound.read())
        # my_sound.close()

        return {"audio": my_sound,
                "timestamp": datetime.now().timestamp()}

    def start_record(self) -> None:
        return

    def stop_record(self) -> None:
        return

    def current_location(self) -> dict:
        return {"lat": 38.743176, "lng": -9.306287}
