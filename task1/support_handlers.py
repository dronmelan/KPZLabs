from abc import ABC, abstractmethod
from enum import Enum


class SupportLevel(Enum):
    TECHNICAL = "технічна підтримка"
    BILLING = "біллінг та платежі"
    GENERAL = "загальні питання"
    VIP = "VIP-підтримка"


class SupportRequest:
    def __init__(self, issue_type=None, is_vip=False, problem_complexity=None):
        self.issue_type = issue_type
        self.is_vip = is_vip
        self.problem_complexity = problem_complexity
        self.resolved = False


class SupportHandler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def can_handle(self, request):
        pass

    @abstractmethod
    def handle(self, request):
        pass

    def process_request(self, request):
        if self.can_handle(request):
            return self.handle(request)
        elif self._next_handler:
            return self._next_handler.process_request(request)
        else:
            return None


class VIPSupportHandler(SupportHandler):
    def can_handle(self, request):
        return request.is_vip

    def handle(self, request):
        print(f"\n🌟 VIP-ПІДТРИМКА 🌟")
        print("Ви підключені до пріоритетної лінії підтримки.")
        print("Ваше питання буде розглянуто в першочерговому порядку.")
        print("Очікуваний час відповіді: до 5 хвилин.")
        request.resolved = True
        return SupportLevel.VIP


class TechnicalSupportHandler(SupportHandler):
    def can_handle(self, request):
        return request.issue_type == "technical"

    def handle(self, request):
        print(f"\n🔧 ТЕХНІЧНА ПІДТРИМКА")
        print("Ви підключені до відділу технічної підтримки.")
        print("Наші спеціалісти допоможуть вам з технічними проблемами.")
        print("Очікуваний час відповіді: до 15 хвилин.")
        request.resolved = True
        return SupportLevel.TECHNICAL


class BillingSupportHandler(SupportHandler):
    def can_handle(self, request):
        return request.issue_type == "billing"

    def handle(self, request):
        print(f"\n💰 ВІДДІЛ БІЛЛІНГУ")
        print("Ви підключені до відділу платежів та біллінгу.")
        print("Ми допоможемо з питаннями щодо рахунків та платежів.")
        print("Очікуваний час відповіді: до 10 хвилин.")
        request.resolved = True
        return SupportLevel.BILLING


class GeneralSupportHandler(SupportHandler):
    def can_handle(self, request):
        return request.issue_type == "general"

    def handle(self, request):
        print(f"\nЗАГАЛЬНА ПІДТРИМКА")
        print("Ви підключені до загального відділу підтримки.")
        print("Ми допоможемо з загальними питаннями та консультаціями.")
        print("Очікуваний час відповіді: до 20 хвилин.")
        request.resolved = True
        return SupportLevel.GENERAL