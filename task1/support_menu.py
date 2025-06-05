from task1.support_handlers import TechnicalSupportHandler, BillingSupportHandler, GeneralSupportHandler, \
    VIPSupportHandler, SupportRequest


class SupportMenu:
    def __init__(self):
        self.support_chain = self._create_support_chain()

    def _create_support_chain(self):
        vip_handler = VIPSupportHandler()
        technical_handler = TechnicalSupportHandler()
        billing_handler = BillingSupportHandler()
        general_handler = GeneralSupportHandler()

        vip_handler.set_next(technical_handler).set_next(billing_handler).set_next(general_handler)

        return vip_handler

    def start_support_session(self):
        print("=" * 60)
        print("🎧 ЛАСКАВО ПРОСИМО ДО ЦЕНТРУ ПІДТРИМКИ КЛІЄНТІВ 🎧")
        print("=" * 60)

        while True:
            request = SupportRequest()

            if self._ask_vip_status(request):
                result = self.support_chain.process_request(request)
                if result:
                    print("\nВаш запит успішно переадресовано!")
                    if self._ask_continue():
                        continue
                    else:
                        break

            if self._ask_issue_type(request):
                result = self.support_chain.process_request(request)
                if result:
                    print("\nВаш запит успішно переадресовано!")
                    if self._ask_continue():
                        continue
                    else:
                        break

            if self._ask_details(request):
                result = self.support_chain.process_request(request)
                if result:
                    print("\nВаш запит успішно переадресовано!")
                    if self._ask_continue():
                        continue
                    else:
                        break

            if self._ask_final_routing(request):
                result = self.support_chain.process_request(request)
                if result:
                    print("\nВаш запит успішно переадресовано!")
                    if self._ask_continue():
                        continue
                    else:
                        break

            print("\nНа жаль, ми не змогли автоматично визначити відповідний відділ.")
            print("Меню буде перезапущено для нової спроби...")
            print("-" * 60)

    def _ask_vip_status(self, request):
        print("\nРІВЕНЬ 1: Статус клієнта")
        print("1. Я VIP-клієнт")
        print("2. Я звичайний клієнт")
        print("0. Вихід")

        choice = input("\nВаш вибір: ").strip()

        if choice == "1":
            request.is_vip = True
            return True
        elif choice == "2":
            return False
        elif choice == "0":
            print("До побачення!")
            exit()
        else:
            print("Невірний вибір. Спробуйте ще раз.")
            return self._ask_vip_status(request)

    def _ask_issue_type(self, request):
        print("\n📋 РІВЕНЬ 2: Тип проблеми")
        print("1. Технічні проблеми (інтернет, обладнання, налаштування)")
        print("2. Питання про рахунки та платежі")
        print("3. Загальні питання (послуги, тарифи, консультації)")
        print("4. Інше")
        print("0. Повернутися до попереднього меню")

        choice = input("\nВаш вибір: ").strip()

        if choice == "1":
            request.issue_type = "technical"
            return True
        elif choice == "2":
            request.issue_type = "billing"
            return True
        elif choice == "3":
            request.issue_type = "general"
            return True
        elif choice == "4":
            return False
        elif choice == "0":
            return self._ask_vip_status(request)
        else:
            print("Невірний вибір. Спробуйте ще раз.")
            return self._ask_issue_type(request)

    def _ask_details(self, request):
        print("\nРІВЕНЬ 3: Деталізація проблеми")
        print("1. Проблема з підключенням до інтернету")
        print("2. Питання про останній рахунок")
        print("3. Інформація про нові тарифи")
        print("4. Жодне з перерахованого")
        print("0. Повернутися до попереднього меню")

        choice = input("\nВаш вибір: ").strip()

        if choice == "1":
            request.issue_type = "technical"
            return True
        elif choice == "2":
            request.issue_type = "billing"
            return True
        elif choice == "3":
            request.issue_type = "general"
            return True
        elif choice == "4":
            return False
        elif choice == "0":
            return self._ask_issue_type(request)
        else:
            print("Невірний вибір. Спробуйте ще раз.")
            return self._ask_details(request)

    def _ask_final_routing(self, request):
        print("\nРІВЕНЬ 4: Останній вибір")
        print("Оскільки ми не змогли точно визначити ваш запит,")
        print("будь ласка, оберіть найближчий варіант:")
        print("1. Технічна підтримка")
        print("2. Відділ біллінгу")
        print("3. Загальна підтримка")
        print("0. Розпочати спочатку")

        choice = input("\nВаш вибір: ").strip()

        if choice == "1":
            request.issue_type = "technical"
            return True
        elif choice == "2":
            request.issue_type = "billing"
            return True
        elif choice == "3":
            request.issue_type = "general"
            return True
        elif choice == "0":
            return False
        else:
            print("Невірний вибір. Спробуйте ще раз.")
            return self._ask_final_routing(request)

    def _ask_continue(self):
        print("\nБажаєте звернутися ще раз?")
        print("1. Так")
        print("2. Ні")

        choice = input("\nВаш вибір: ").strip()

        if choice == "1":
            return True
        elif choice == "2":
            print("\nДякуємо за звернення! До побачення! 👋")
            return False
        else:
            print("Невірний вибір. Спробуйте ще раз.")
            return self._ask_continue()