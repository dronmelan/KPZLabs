from task2.models.laptop import Laptop
from typing import Dict


class IproneLaptop(Laptop):
    def __init__(self):
        super().__init__("IProne", "MacBook Air M3", 1299.99)

    def get_device_type(self) -> str:
        return "IProne Ноутбук"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Процесор": "Apple M3 8-core",
            "RAM": "16GB Unified Memory",
            "Накопичувач": "512GB SSD",
            "Дисплей": "13.6\" Liquid Retina",
            "ОС": "macOS Sonoma",
            "Особливості": "Touch ID, MagSafe зарядка"
        }