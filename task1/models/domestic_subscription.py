from task1.models.subscription import Subscription

class DomesticSubscription(Subscription):
    def __init__(self):
        super().__init__(
            monthly_fee=19.99,
            minimum_period_months=1,
            channels=["National Geographic", "Discovery", "History Channel", "BBC", "CNN"],
            features=["HD якість", "2 одночасних підключення", "Доступ до архіву"]
        )

    def get_subscription_type(self) -> str:
        return "Домашня підписка"