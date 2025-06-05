from task1.support_menu import SupportMenu


def main():
    try:
        menu = SupportMenu()
        menu.start_support_session()
    except KeyboardInterrupt:
        print("\n\nСесію перервано користувачем. До побачення! 👋")
    except Exception as e:
        print(f"\n Сталася помилка: {e}")


if __name__ == "__main__":
    main()