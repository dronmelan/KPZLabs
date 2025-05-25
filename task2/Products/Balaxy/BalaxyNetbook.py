from typing import Dict
from task2.models.netbook import Netbook


class BalaxyNetbook(Netbook):
    def __init__(self):
        super().__init__("Balaxy", "Galaxy Book Go", 549.99)

    def get_device_type(self) -> str:
        return "Balaxy Нетбук"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Процесор": "Snapdragon 7c Gen 2",
            "RAM": "8GB LPDDR4X",
            "Накопичувач": "128GB eUFS",
            "Дисплей": "14\" TFT Full HD",
            "ОС": "Windows 11",
            "Підключення": "5G LTE",
            "Батарея": "до 18 годин"
        }