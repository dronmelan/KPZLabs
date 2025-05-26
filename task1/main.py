from task1.adapter import FileLoggerAdapter
from task1.file_writer import FileWriter
from task1.logger import Logger


def main():
    print("=== Демонстрація роботи Logger та FileLoggerAdapter ===\n")

    print("1. Консольний логер:")
    console_logger = Logger()
    console_logger.Log("Це звичайне повідомлення")
    console_logger.Warn("Це попередження")
    console_logger.Error("Це повідомлення про помилку")

    print("\n" + "=" * 50 + "\n")

    print("2. Файловий логер (через адаптер):")

    # Створюємо FileWriter
    file_writer = FileWriter("application.log")

    file_logger = FileLoggerAdapter(file_writer)

    file_logger.Log("Програма запущена успішно")
    file_logger.Warn("Низький рівень пам'яті")
    file_logger.Error("Не вдалося підключитися до бази даних")
    file_logger.Log("Програма завершена")

    print("Повідомлення записані у файл 'application.log'")

    print("\n3. Вміст файлу логів:")
    try:
        with open("application.log", 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("Файл логів не знайдено")

    print("\n=== Демонстрація завершена ===")


if __name__ == "__main__":
    main()