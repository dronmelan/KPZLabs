from task2.Factories.DeviceFactory import DeviceFactory
from task2.Products.Iprone.IproneEBook import IproneEBook
from task2.Products.Iprone.IproneSmartphone import IproneSmartphone
from task2.Products.Iprone.iproneLaptop import IproneLaptop
from task2.Products.Iprone.iproneNetBook import IproneNetbook
from task2.models.ebook import EBook
from task2.models.laptop import Laptop
from task2.models.netbook import Netbook
from task2.models.smartphone import Smartphone


class IproneFactory(DeviceFactory):

    def create_laptop(self) -> Laptop:
        return IproneLaptop()

    def create_netbook(self) -> Netbook:
        return IproneNetbook()

    def create_ebook(self) -> EBook:
        return IproneEBook()

    def create_smartphone(self) -> Smartphone:
        return IproneSmartphone()

    def get_brand_name(self) -> str:
        return "IProne"

