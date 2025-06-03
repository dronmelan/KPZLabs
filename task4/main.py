from smart_text_reader import SmartTextReader
from smart_text_checker import SmartTextChecker
from smart_text_reader_locker import SmartTextReaderLocker
from test_file_manager import TestFileManager


def main():
    print("=== Демонстрація роботи SmartTextReader з патерном Проксі ===\n")

    TestFileManager.create_test_files()
    TestFileManager.list_test_files()
    print()

    print("1. Тестування базового SmartTextReader:")
    print("-" * 50)
    basic_reader = SmartTextReader()
    result = basic_reader.read_file("test.txt")
    if result:
        print("Результат читання (двомірний масив):")
        for i, line in enumerate(result):
            print(f"Рядок {i + 1}: {line}")
    print()

    print("2. Тестування SmartTextChecker (з логуванням):")
    print("-" * 50)
    logged_reader = SmartTextChecker(SmartTextReader())
    result = logged_reader.read_file("test.txt")
    print()

    print("3. Тестування SmartTextReaderLocker (з обмеженням доступу):")
    print("-" * 50)
    locked_reader = SmartTextReaderLocker(SmartTextReader(), r'(secret|private)')

    print("Спроба читання дозволеного файлу:")
    result = locked_reader.read_file("test.txt")
    if result:
        print("Файл успішно прочитано")

    print("\nСпроба читання забороненого файлу:")
    result = locked_reader.read_file("secret_data.txt")
    print()

    print("4. Комбінування проксі (логування + обмеження):")
    print("-" * 50)
    combined_reader = SmartTextChecker(
        SmartTextReaderLocker(SmartTextReader(), r'(secret|private)')
    )

    print("Читання дозволеного файлу з логуванням:")
    result = combined_reader.read_file("public_data.txt")

    print("\nСпроба читання забороненого файлу з логуванням:")
    result = combined_reader.read_file("private_info.txt")
    print()

    print("5. Демонстрація різних правил доступу:")
    print("-" * 50)

    txt_locker = SmartTextReaderLocker(SmartTextReader(), r'\.txt$')
    print("Правило: заборона .txt файлів")
    print("Спроба читання test.txt:")
    txt_locker.read_file("test.txt")

    with open("data.log", "w", encoding="utf-8") as f:
        f.write("Лог файл\nДозволений для читання")

    print("Спроба читання data.log:")
    result = txt_locker.read_file("data.log")
    if result:
        print("Файл data.log успішно прочитано")

    import os
    if os.path.exists("data.log"):
        os.remove("data.log")

    print()

    TestFileManager.cleanup_test_files()


def demonstrate_advanced_usage():
    print("\n=== Розширені можливості ===")

    with open("ukrainian_text.txt", "w", encoding="utf-8") as f:
        f.write("Слава Україні!\n")
        f.write("Героям слава!\n")
        f.write("Україна переможе!")

    analyzer = SmartTextChecker(SmartTextReader())
    print("Аналіз українського тексту:")
    result = analyzer.read_file("ukrainian_text.txt")

    if result:
        print("\nДетальний розбір по символах:")
        for i, line in enumerate(result):
            print(f"Рядок {i + 1}:")
            for j, char in enumerate(line):
                print(f"  [{j}]: '{char}' (код: {ord(char)})")

    import os
    if os.path.exists("ukrainian_text.txt"):
        os.remove("ukrainian_text.txt")


if __name__ == "__main__":
    main()
    demonstrate_advanced_usage()