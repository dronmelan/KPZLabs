class FileWriter:

    def __init__(self, filename):
        self.filename = filename

    def Write(self, text):
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(text)

    def WriteLine(self, text):
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(text + '\n')