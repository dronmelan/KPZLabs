from abc import ABC, abstractmethod
from task2.models.device import Device


class EBook(Device, ABC):
    @abstractmethod
    def get_device_type(self) -> str:
        return "Електронна книга"