from task2.Factories.DeviceFactory import DeviceFactory
from task2.Products.Kiaomi.KiaomiEBook import KiaomiEBook
from task2.Products.Kiaomi.KiaomiLaptop import KiaomiLaptop
from task2.Products.Kiaomi.KiaomiNetbook import KiaomiNetbook
from task2.Products.Kiaomi.KiaomiSmartphone import KiaomiSmartphone
from task2.models.ebook import EBook
from task2.models.laptop import Laptop
from task2.models.netbook import Netbook
from task2.models.smartphone import Smartphone


class KiaomiFactory(DeviceFactory):

    def create_laptop(self) -> Laptop:
        return KiaomiLaptop()

    def create_netbook(self) -> Netbook:
        return KiaomiNetbook()

    def create_ebook(self) -> EBook:
        return KiaomiEBook()

    def create_smartphone(self) -> Smartphone:
        return KiaomiSmartphone()

    def get_brand_name(self) -> str:
        return "Kiaomi"