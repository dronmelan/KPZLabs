import os


class TestFileManager:

    @staticmethod
    def create_test_files():

        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("Привіт світ!\n")
            f.write("Це тестовий файл.\n")
            f.write("Python - чудова мова програмування!")

        with open("public_data.txt", "w", encoding="utf-8") as f:
            f.write("Публічна інформація\n")
            f.write("Доступна для всіх\n")
            f.write("123 456 789")

        with open("secret_data.txt", "w", encoding="utf-8") as f:
            f.write("Секретна інформація\n")
            f.write("Не для всіх очей!")

        with open("private_info.txt", "w", encoding="utf-8") as f:
            f.write("Приватна інформація\n")
            f.write("Конфіденційні дані")

        print("Тестові файли створено успішно!\n")

    @staticmethod
    def cleanup_test_files():
        files_to_remove = ["test.txt", "public_data.txt", "secret_data.txt", "private_info.txt"]

        removed_count = 0
        for filename in files_to_remove:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    removed_count += 1
            except Exception as e:
                print(f"Не вдалося видалити файл {filename}: {e}")

        if removed_count > 0:
            print(f"\nВидалено {removed_count} тестових файлів")

    @staticmethod
    def list_test_files():
        test_files = ["test.txt", "public_data.txt", "secret_data.txt", "private_info.txt"]
        existing_files = [f for f in test_files if os.path.exists(f)]

        if existing_files:
            print("Наявні тестові файли:")
            for file in existing_files:
                size = os.path.getsize(file)
                print(f"   - {file} ({size} байт)")
        else:
            print("Тестові файли відсутні")