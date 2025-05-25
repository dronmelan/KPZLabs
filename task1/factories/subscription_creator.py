from abc import abstractmethod, ABC

from task1.models.domestic_subscription import DomesticSubscription
from task1.models.educational_subscription import EducationalSubscription
from task1.models.premium_subscription import PremiumSubscription
from task1.models.subscription import Subscription


class SubscriptionCreator(ABC):
    @abstractmethod
    def create_domestic_subscription(self) -> DomesticSubscription:
        pass

    @abstractmethod
    def create_educational_subscription(self) -> EducationalSubscription:
        pass

    @abstractmethod
    def create_premium_subscription(self) -> PremiumSubscription:
        pass

    def purchase_subscription(self, subscription_type: str) -> Subscription:
        if subscription_type.lower() == "domestic":
            subscription = self.create_domestic_subscription()
        elif subscription_type.lower() == "educational":
            subscription = self.create_educational_subscription()
        elif subscription_type.lower() == "premium":
            subscription = self.create_premium_subscription()
        else:
            raise ValueError(f"Невідомий тип підписки: {subscription_type}")

        print(f"Підписка створена через: {self.__class__.__name__}")
        return subscription