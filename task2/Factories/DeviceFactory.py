from abc import ABC, abstractmethod
from typing import List
from task2.models.device import Device
from task2.models.ebook import EBook
from task2.models.laptop import Laptop
from task2.models.netbook import Netbook
from task2.models.smartphone import Smartphone


class DeviceFactory(ABC):

    @abstractmethod
    def create_laptop(self) -> Laptop:
        pass

    @abstractmethod
    def create_netbook(self) -> Netbook:
        pass

    @abstractmethod
    def create_ebook(self) -> EBook:
        pass

    @abstractmethod
    def create_smartphone(self) -> Smartphone:
        pass

    @abstractmethod
    def get_brand_name(self) -> str:
        pass

    def create_all_devices(self) -> List[Device]:
        return [
            self.create_laptop(),
            self.create_netbook(),
            self.create_ebook(),
            self.create_smartphone()
        ]