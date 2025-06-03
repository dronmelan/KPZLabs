from text_reader import TextReader


class SmartTextChecker(TextReader):

    def __init__(self, text_reader):
        self.text_reader = text_reader

    def read_file(self, filename):
        print(f"Відкриття файлу: {filename}")

        result = self.text_reader.read_file(filename)

        if result is not None:
            print(f"Файл '{filename}' успішно відкрито")
            print(f"Файл '{filename}' успішно прочитано")
            print(f"Файл '{filename}' успішно закрито")

            # Підрахунок статистики
            total_lines = len(result)
            total_chars = sum(len(line) for line in result)

            print(f"Статистика файлу '{filename}':")
            print(f"   - Загальна кількість рядків: {total_lines}")
            print(f"   - Загальна кількість символів: {total_chars}")
        else:
            print(f"Не вдалося прочитати файл '{filename}'")

        return result