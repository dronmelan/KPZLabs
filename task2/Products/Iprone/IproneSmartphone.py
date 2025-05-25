from typing import Dict
from task2.models.smartphone import Smartphone


class IproneSmartphone(Smartphone):
    def __init__(self):
        super().__init__("IProne", "iPhone 15 Pro", 1199.99)

    def get_device_type(self) -> str:
        return "IProne Смартфон"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Дисплей": "6.1\" Super Retina XDR",
            "Процесор": "A17 Pro Bionic",
            "RAM": "8GB",
            "Накопичувач": "128GB",
            "Камера": "48MP + 12MP + 12MP",
            "ОС": "iOS 17",
            "Особливості": "Face ID, MagSafe, Lightning"
        }