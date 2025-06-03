import re
from text_reader import TextReader


class SmartTextReaderLocker(TextReader):

    def __init__(self, text_reader, restriction_pattern):
        self.text_reader = text_reader
        self.restriction_pattern = re.compile(restriction_pattern)

    def read_file(self, filename):
        if self.restriction_pattern.search(filename):
            print("Access denied!")
            return None

        return self.text_reader.read_file(filename)