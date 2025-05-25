from task2.Factories.DeviceFactory import DeviceFactory
from task2.Products.Balaxy.BalaxyEBook import BalaxyEBook
from task2.Products.Balaxy.BalaxyLaptop import BalaxyLaptop
from task2.Products.Balaxy.BalaxyNetbook import BalaxyNetbook
from task2.Products.Balaxy.BalaxySmartphone import BalaxySmartphone
from task2.models.ebook import EBook
from task2.models.laptop import Laptop
from task2.models.netbook import Netbook
from task2.models.smartphone import Smartphone


class BalaxyFactory(DeviceFactory):

    def create_laptop(self) -> Laptop:
        return BalaxyLaptop()

    def create_netbook(self) -> Netbook:
        return BalaxyNetbook()

    def create_ebook(self) -> EBook:
        return BalaxyEBook()

    def create_smartphone(self) -> Smartphone:
        return BalaxySmartphone()

    def get_brand_name(self) -> str:
        return "Balaxy"
