from task2.Factories.BalaxyFactory import BalaxyFactory
from task2.Factories.IproneFactory import IproneFactory
from task2.Factories.KiaomiFactory import KiaomiFactory
from task2.Factories.DeviceFactory import DeviceFactory
from task2.models.device import Device
from typing import List


class TechManufacturer:

    def __init__(self):
        self.factories = {
            "iprone": IproneFactory(),
            "kiaomi": KiaomiFactory(),
            "balaxy": BalaxyFactory()
        }

    def get_factory(self, brand: str) -> DeviceFactory:
        brand = brand.lower()
        if brand not in self.factories:
            raise ValueError(f"Невідомий бренд: {brand}. Доступні: {list(self.factories.keys())}")
        return self.factories[brand]

    def produce_device(self, brand: str, device_type: str) -> Device:
        factory = self.get_factory(brand)
        device_type = device_type.lower()

        if device_type == "laptop":
            return factory.create_laptop()
        elif device_type == "netbook":
            return factory.create_netbook()
        elif device_type == "ebook":
            return factory.create_ebook()
        elif device_type == "smartphone":
            return factory.create_smartphone()
        else:
            raise ValueError(f"Невідомий тип девайсу: {device_type}")

    def produce_full_line(self, brand: str) -> List[Device]:
        factory = self.get_factory(brand)
        return factory.create_all_devices()

    def get_available_brands(self) -> List[str]:
        return list(self.factories.keys())