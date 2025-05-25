from task2.models.laptop import Laptop
from typing import Dict

class BalaxyLaptop(Laptop):
    def __init__(self):
        super().__init__("Balaxy", "Galaxy Book3 Pro", 1099.99)

    def get_device_type(self) -> str:
        return "Balaxy Ноутбук"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Процесор": "Intel Core i7-1360P",
            "RAM": "16GB LPDDR5",
            "Накопичувач": "512GB NVMe SSD",
            "Дисплей": "14\" AMOLED 2.8K",
            "ОС": "Windows 11",
            "Особливості": "S Pen підтримка, DeX режим"
        }