from task1.models.subscription import Subscription


class PremiumSubscription(Subscription):
    def __init__(self):
        super().__init__(
            monthly_fee=49.99,
            minimum_period_months=1,
            channels=["HBO", "Netflix Originals", "Amazon Prime", "Disney+", "Sports Channels", "Movie Channels"],
            features=["4K якість", "10 одночасних підключень", "Ексклюзивний контент", "Без реклами", "Ранній доступ"]
        )

    def get_subscription_type(self) -> str:
        return "Преміум підписка"