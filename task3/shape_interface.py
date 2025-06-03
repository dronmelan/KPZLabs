from abc import ABC, abstractmethod


class Shape(ABC):

    def __init__(self, renderer):
        self.renderer = renderer

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self, dx, dy):
        pass

    @abstractmethod
    def get_info(self):
        pass

    def set_renderer(self, renderer):
        self.renderer = renderer
        print(f"Renderer changed to: {renderer.get_type()}")
