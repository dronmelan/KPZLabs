from typing import Dict
from task2.models.smartphone import Smartphone


class KiaomiSmartphone(Smartphone):
    def __init__(self):
        super().__init__("Kiaomi", "Mi 14 Ultra", 799.99)

    def get_device_type(self) -> str:
        return "Kiaomi Смартфон"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Дисплей": "6.73\" AMOLED 2K",
            "Процесор": "Snapdragon 8 Gen 3",
            "RAM": "12GB LPDDR5",
            "Накопичувач": "256GB UFS 4.0",
            "Камера": "50MP Leica + 50MP + 50MP",
            "ОС": "MIUI 15 (Android 14)",
            "Особливості": "120W швидка зарядка"
        }