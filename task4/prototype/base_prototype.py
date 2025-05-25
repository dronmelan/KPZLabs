from abc import abstractmethod, ABC


class Prototype(ABC):

    @abstractmethod
    def clone(self):
        pass