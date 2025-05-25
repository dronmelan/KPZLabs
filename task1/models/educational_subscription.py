from task1.models.subscription import Subscription


class EducationalSubscription(Subscription):
    def __init__(self):
        super().__init__(
            monthly_fee=9.99,
            minimum_period_months=3,
            channels=["Educational TV", "Science Channel", "Documentary Channel", "MIT OpenCourseWare"],
            features=["Студентська знижка", "Навчальні матеріали", "Офлайн перегляд"]
        )

    def get_subscription_type(self) -> str:
        return "Освітня підписка"