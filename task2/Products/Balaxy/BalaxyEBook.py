from typing import Dict
from task2.models.ebook import EBook


class BalaxyEBook(EBook):
    def __init__(self):
        super().__init__("Balaxy", "Galaxy Tab S9 Reader", 449.99)

    def get_device_type(self) -> str:
        return "Balaxy Електронна книга"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Дисплей": "8.7\" Super AMOLED",
            "Процесор": "Snapdragon 8 Gen 2",
            "RAM": "6GB",
            "Накопичувач": "128GB",
            "S Pen": "включений",
            "ОС": "Android 13",
            "Особливості": "Samsung DeX, книжковий режим"
        }