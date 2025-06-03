from text_reader import TextReader


class SmartTextReader(TextReader):

    def __init__(self):
        self.content = None
        self.is_open = False

    def read_file(self, filename):
        try:
            self._open_file(filename)
            self._read_content(filename)
            self._close_file()
            return self.content
        except FileNotFoundError:
            print(f"Помилка: Файл '{filename}' не знайдено!")
            return None
        except Exception as e:
            print(f"Помилка при читанні файлу: {e}")
            return None

    def _open_file(self, filename):
        self.is_open = True

    def _read_content(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.content = []
            for line in lines:
                line = line.rstrip('\n')
                char_array = list(line)
                self.content.append(char_array)

    def _close_file(self):
        self.is_open = False