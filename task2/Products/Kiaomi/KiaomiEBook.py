from typing import Dict
from task2.models.ebook import EBook


class KiaomiEBook(EBook):
    def __init__(self):
        super().__init__("Kiaomi", "Mi Reader Pro", 199.99)

    def get_device_type(self) -> str:
        return "Kiaomi Електронна книга"

    def get_specifications(self) -> Dict[str, str]:
        return {
            "Дисплей": "7.8\" E Ink Carta",
            "Роздільність": "1872×1404",
            "Накопичувач": "32GB",
            "Підсвічування": "24 LED",
            "Захист": "IPX8 водозахист",
            "Батарея": "до 6 тижнів читання",
            "Формати": "EPUB, PDF, MOBI, TXT"
        }