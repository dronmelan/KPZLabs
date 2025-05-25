from abc import abstractmethod, ABC
from task2.models.device import Device


class Netbook(Device, ABC):
    @abstractmethod
    def get_device_type(self) -> str:
        return "Нетбук"