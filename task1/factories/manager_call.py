from task1.factories.subscription_creator import SubscriptionCreator
from task1.models.domestic_subscription import DomesticSubscription
from task1.models.educational_subscription import EducationalSubscription
from task1.models.premium_subscription import PremiumSubscription


class ManagerCall(SubscriptionCreator):
    def create_domestic_subscription(self) -> DomesticSubscription:
        print("☎️ Створення домашньої підписки через дзвінок менеджеру з персональною консультацією")
        subscription = DomesticSubscription()
        subscription.features.append("Персональна підтримка менеджера")
        subscription.features.append("Гнучкі умови оплати")
        return subscription

    def create_educational_subscription(self) -> EducationalSubscription:
        print("☎️ Створення освітньої підписки через дзвінок менеджеру з додатковою знижкою для студентів")
        subscription = EducationalSubscription()
        subscription.monthly_fee *= 0.8  # Додаткова знижка 20%
        subscription.features.append("Індивідуальний план навчання")
        return subscription

    def create_premium_subscription(self) -> PremiumSubscription:
        print("☎️ Створення преміум підписки через дзвінок менеджеру з VIP обслуговуванням")
        subscription = PremiumSubscription()
        subscription.features.append("24/7 VIP підтримка")
        subscription.features.append("Персональні рекомендації")
        subscription.features.append("Пріоритетний доступ до новинок")
        return subscription