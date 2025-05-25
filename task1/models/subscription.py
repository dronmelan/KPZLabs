from abc import ABC, abstractmethod
from typing import List

class Subscription(ABC):
    def __init__(self, monthly_fee: float, minimum_period_months: int,
                 channels: List[str], features: List[str]):
        self.monthly_fee = monthly_fee
        self.minimum_period_months = minimum_period_months
        self.channels = channels
        self.features = features

    @abstractmethod
    def get_subscription_type(self) -> str:
        pass

    def display_info(self):
        print(f"Тип підписки: {self.get_subscription_type()}")
        print(f"Щомісячна плата: ${self.monthly_fee}")
        print(f"Мінімальний період: {self.minimum_period_months} місяців")
        print(f"Канали: {', '.join(self.channels)}")
        print(f"Можливості: {', '.join(self.features)}")
        print("=" * 50)