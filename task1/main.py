from task1.factories.manager_call import ManagerCall
from task1.factories.mobile_app import MobileApp
from task1.factories.website import WebSite


def main():
    print("=== СИСТЕМА ПІДПИСОК НА ВІДЕО ПРОВАЙДЕРА ===\n")

    creators = [
        ("Веб-сайт", WebSite()),
        ("Мобільний додаток", MobileApp()),
        ("Дзвінок менеджеру", ManagerCall())
    ]

    subscription_types = ["domestic", "educational", "premium"]

    for creator_name, creator in creators:
        print(f"\n{'=' * 20} {creator_name.upper()} {'=' * 20}")

        for sub_type in subscription_types:
            try:
                print(f"\n--- Придбання {sub_type} підписки ---")
                subscription = creator.purchase_subscription(sub_type)
                subscription.display_info()
            except ValueError as e:
                print(f"Помилка: {e}")

    print("\n" + "=" * 60)
    print("ПОРІВНЯННЯ ВСІХ ТИПІВ ПІДПИСОК (створені через веб-сайт)")
    print("=" * 60)

    website = WebSite()
    for sub_type in subscription_types:
        subscription = website.purchase_subscription(sub_type)
        subscription.display_info()


if __name__ == "__main__":
    main()