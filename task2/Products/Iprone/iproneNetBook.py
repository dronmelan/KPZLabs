from typing import Dict
from task2.models.netbook import Netbook


class IproneNetbook(Netbook):
    def __init__(self):
        super().__init__("IProne", "MacBook 12\"", 999.99)

    def get_device_type(self) -> str:
        return "IProne Нетбук"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Процесор": "Apple M2 4-core",
            "RAM": "8GB Unified Memory",
            "Накопичувач": "256GB SSD",
            "Дисплей": "12\" Retina",
            "ОС": "macOS",
            "Вага": "0.92 кг"
        }