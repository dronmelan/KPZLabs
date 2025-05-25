import threading
from task3.authenticator import Authenticator
from task3.extended_authenticator import test_singleton_in_thread, ExtendedAuthenticator


def main():
    """Головний метод для демонстрації роботи Singleton"""
    print("=== Тестування Singleton Authenticator ===\n")

    # Тест 1: Створення декількох екземплярів в одному потоці
    print("1. Тест створення декількох екземплярів:")
    auth1 = Authenticator()
    auth2 = Authenticator()
    auth3 = Authenticator()

    print(f"auth1 ID: {id(auth1)}")
    print(f"auth2 ID: {id(auth2)}")
    print(f"auth3 ID: {id(auth3)}")
    print(f"Всі екземпляри однакові: {auth1 is auth2 is auth3}\n")

    # Тест 2: Функціональність
    print("2. Тест функціональності:")
    auth1.authenticate("alice", "password123")
    auth1.authenticate("bob", "secret456")

    print(f"Alice authenticated: {auth2.is_authenticated('alice')}")
    print(f"Bob token: {auth3.get_session_token('bob')}")
    print(f"Instance info: {auth1.get_instance_info()}\n")

    # Тест 3: Багатопоточність
    print("3. Тест багатопоточності:")
    results = []
    threads = []

    # Створення та запуск потоків
    for i in range(5):
        thread = threading.Thread(target=test_singleton_in_thread, args=(i, results))
        threads.append(thread)
        thread.start()

    # Очікування завершення всіх потоків
    for thread in threads:
        thread.join()

    # Аналіз результатів
    print("\nРезультати багатопоточного тестування:")
    unique_ids = set()
    for thread_id, instance_id in results:
        print(f"Thread {thread_id}: Instance ID {instance_id}")
        unique_ids.add(instance_id)

    print(f"Кількість унікальних екземплярів: {len(unique_ids)}")
    print(f"Всі потоки отримали один екземпляр: {len(unique_ids) == 1}\n")

    # Тест 4: Наслідування
    print("4. Тест наслідування:")
    extended_auth1 = ExtendedAuthenticator()
    extended_auth2 = ExtendedAuthenticator()
    base_auth = Authenticator()

    print(f"ExtendedAuthenticator 1 ID: {id(extended_auth1)}")
    print(f"ExtendedAuthenticator 2 ID: {id(extended_auth2)}")
    print(f"Base Authenticator ID: {id(base_auth)}")

    print(f"Extended instances are same: {extended_auth1 is extended_auth2}")
    print(f"Extended and base are different: {extended_auth1 is not base_auth}")
    print(f"Extended method result: {extended_auth1.extended_method()}")

    # Перевірка, що наслідувані класи мають окремі екземпляри
    print(f"Base class users: {len(base_auth._authenticated_users)}")
    print(f"Extended class users: {len(extended_auth1._authenticated_users)}")


if __name__ == "__main__":
    main()