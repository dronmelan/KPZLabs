from typing import Dict
from task2.models.laptop import Laptop


class KiaomiLaptop(Laptop):
    def __init__(self):
        super().__init__("Kiaomi", "Mi Laptop Pro 15", 899.99)

    def get_device_type(self) -> str:
        return "Kiaomi Ноутбук"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Процесор": "Intel Core i7-12700H",
            "RAM": "16GB DDR4",
            "Накопичувач": "512GB NVMe SSD",
            "Дисплей": "15.6\" OLED 3.5K",
            "Відеокарта": "NVIDIA RTX 3050",
            "ОС": "Windows 11",
            "Особливості": "Швидка зарядка 100W"
        }