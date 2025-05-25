from typing import Dict
from task2.models.ebook import EBook


class IproneEBook(EBook):
    def __init__(self):
        super().__init__("IProne", "iPad Air eReader", 599.99)

    def get_device_type(self) -> str:
        return "IProne Електронна книга"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Дисплей": "10.9\" Liquid Retina",
            "Процесор": "Apple M1",
            "Накопичувач": "64GB",
            "Підтримка": "Apple Pencil",
            "Батарея": "до 10 годин читання",
            "Особливості": "True Tone, антибліковий"
        }