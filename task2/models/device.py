from abc import ABC, abstractmethod
from typing import Dict


class Device(ABC):

    def __init__(self, brand: str, model: str, price: float):
        self.brand = brand
        self.model = model
        self.price = price

    @abstractmethod
    def get_device_type(self) -> str:
        pass

    @abstractmethod
    def get_specifications(self) -> Dict[str, str]:
        pass

    def display_info(self):
        print(f"🔹 {self.get_device_type()}")
        print(f"   Бренд: {self.brand}")
        print(f"   Модель: {self.model}")
        print(f"   Ціна: ${self.price}")
        print(f"   Характеристики:")
        for key, value in self.get_specifications().items():
            print(f"     • {key}: {value}")
        print()