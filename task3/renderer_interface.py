from abc import ABC, abstractmethod


class Renderer(ABC):

    @abstractmethod
    def render_circle(self, x, y, radius):
        pass

    @abstractmethod
    def render_square(self, x, y, side):
        pass

    @abstractmethod
    def render_triangle(self, x1, y1, x2, y2, x3, y3):
        pass

    @abstractmethod
    def get_type(self):
        pass