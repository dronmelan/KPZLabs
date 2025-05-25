from abc import ABC, abstractmethod
from task2.models.device import Device


class Smartphone(Device, ABC):
    @abstractmethod
    def get_device_type(self) -> str:
        return "Смартфон"