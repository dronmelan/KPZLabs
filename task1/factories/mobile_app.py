from task1.factories.subscription_creator import SubscriptionCreator
from task1.models.domestic_subscription import DomesticSubscription
from task1.models.educational_subscription import EducationalSubscription
from task1.models.premium_subscription import PremiumSubscription


class MobileApp(SubscriptionCreator):
    def create_domestic_subscription(self) -> DomesticSubscription:
        print("📱 Створення домашньої підписки через мобільний додаток з мобільними сповіщеннями")
        subscription = DomesticSubscription()
        subscription.features.append("Push-сповіщення про новий контент")
        return subscription

    def create_educational_subscription(self) -> EducationalSubscription:
        print("📱 Створення освітньої підписки через мобільний додаток з мобільними навчальними інструментами")
        subscription = EducationalSubscription()
        subscription.features.append("Мобільні тести та квізи")
        subscription.features.append("Синхронізація з календарем")
        return subscription

    def create_premium_subscription(self) -> PremiumSubscription:
        print("📱 Створення преміум підписки через мобільний додаток з мобільними бонусами")
        subscription = PremiumSubscription()
        subscription.features.append("Завантаження для офлайн перегляду")
        subscription.features.append("Голосове управління")
        return subscription