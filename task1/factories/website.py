from task1.factories.subscription_creator import SubscriptionCreator
from task1.models.domestic_subscription import DomesticSubscription
from task1.models.educational_subscription import EducationalSubscription
from task1.models.premium_subscription import PremiumSubscription


class WebSite(SubscriptionCreator):
    def create_domestic_subscription(self) -> DomesticSubscription:
        print("🌐 Створення домашньої підписки через веб-сайт з онлайн знижкою 5%")
        subscription = DomesticSubscription()
        subscription.monthly_fee *= 0.95  # Знижка 5%
        return subscription

    def create_educational_subscription(self) -> EducationalSubscription:
        print("🌐 Створення освітньої підписки через веб-сайт з безкоштовним пробним періодом")
        subscription = EducationalSubscription()
        subscription.features.append("Безкоштовний пробний період 7 днів")
        return subscription

    def create_premium_subscription(self) -> PremiumSubscription:
        print("🌐 Створення преміум підписки через веб-сайт з додатковими можливостями")
        subscription = PremiumSubscription()
        subscription.features.append("Веб-ексклюзивний контент")
        return subscription