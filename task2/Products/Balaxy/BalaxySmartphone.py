from typing import Dict
from task2.models.smartphone import Smartphone


class BalaxySmartphone(Smartphone):
    def __init__(self):
        super().__init__("Balaxy", "Galaxy S24 Ultra", 1299.99)

    def get_device_type(self) -> str:
        return "Balaxy Смартфон"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Дисплей": "6.8\" Dynamic AMOLED 2X",
            "Процесор": "Snapdragon 8 Gen 3",
            "RAM": "12GB LPDDR5X",
            "Накопичувач": "256GB UFS 4.0",
            "Камера": "200MP + 50MP + 12MP + 10MP",
            "ОС": "One UI 6.1 (Android 14)",
            "Особливості": "S Pen вбудований, AI функції"
        }