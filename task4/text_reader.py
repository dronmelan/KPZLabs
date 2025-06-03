from abc import ABC, abstractmethod


class TextReader(ABC):

    @abstractmethod
    def read_file(self, filename):
        pass