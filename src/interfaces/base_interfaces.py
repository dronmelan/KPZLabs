from abc import ABC, abstractmethod
from typing import Dict, Any

class Feedable(ABC):
    @abstractmethod
    def feed(self, food: 'Food') -> bool:
        pass

class Observable(ABC):
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        pass

class Maintainable(ABC):
    @abstractmethod
    def maintain(self) -> bool:
        pass