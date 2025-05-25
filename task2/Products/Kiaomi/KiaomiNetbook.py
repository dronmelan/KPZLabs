from typing import Dict
from task2.models.netbook import Netbook


class KiaomiNetbook(Netbook):
    def __init__(self):
        super().__init__("Kiaomi", "Mi Notebook Air 13", 649.99)

    def get_device_type(self) -> str:
        return "Kiaomi Нетбук"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Процесор": "Intel Core i5-1235U",
            "RAM": "8GB LPDDR4",
            "Накопичувач": "256GB SSD",
            "Дисплей": "13.3\" IPS Full HD",
            "ОС": "Windows 11",
            "Вага": "1.3 кг",
            "Батарея": "до 11 годин"
        }