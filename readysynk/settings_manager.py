# coding: utf-8

import yaml
from pathlib import Path
from ksupk import singleton_decorator


@singleton_decorator
class SettingsManager:
    def __init__(self, settings_yaml_path: Path | str):
        settings_yaml_path = Path(settings_yaml_path)

        with open(settings_yaml_path, 'r', encoding="utf-8") as file:
            data = yaml.safe_load(file)

        self.data: dict = dict(data)
        self.created: dict = {}

    # =========================================== app

    def get_password(self) -> str:
        return self.data["app"]["password"]

    # =========================================== connection

    def get_connection(self) -> tuple[str, int]:
        return self.data["connection"]["ip"], self.data["connection"]["port"]

    def is_share(self) -> bool:
        return self.data["connection"]["share"]
