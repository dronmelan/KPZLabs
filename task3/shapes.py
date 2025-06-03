import math
from task3.shape_interface import Shape


class Circle(Shape):

    def __init__(self, renderer, x=0, y=0, radius=10):
        super().__init__(renderer)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        print(f"\n--- Drawing Circle ---")
        print(f"Renderer: {self.renderer.get_type()}")
        self.renderer.render_circle(self.x, self.y, self.radius)
        print(f"Area: {math.pi * self.radius ** 2:.2f}")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print(f"Circle moved by ({dx}, {dy}). New position: ({self.x}, {self.y})")

    def get_info(self):
        return f"Circle: center=({self.x}, {self.y}), radius={self.radius}"

    def set_radius(self, radius):
        self.radius = radius
        print(f"Circle radius changed to: {radius}")


class Square(Shape):

    def __init__(self, renderer, x=0, y=0, side=10):
        super().__init__(renderer)
        self.x = x
        self.y = y
        self.side = side

    def draw(self):
        print(f"\n--- Drawing Square ---")
        print(f"Renderer: {self.renderer.get_type()}")
        self.renderer.render_square(self.x, self.y, self.side)
        print(f"Area: {self.side ** 2}")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print(f"Square moved by ({dx}, {dy}). New position: ({self.x}, {self.y})")

    def get_info(self):
        return f"Square: position=({self.x}, {self.y}), side={self.side}"

    def set_side(self, side):
        self.side = side
        print(f"Square side changed to: {side}")


class Triangle(Shape):

    def __init__(self, renderer, x1=0, y1=0, x2=10, y2=0, x3=5, y3=10):
        super().__init__(renderer)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.x3, self.y3 = x3, y3

    def draw(self):
        print(f"\n--- Drawing Triangle ---")
        print(f"Renderer: {self.renderer.get_type()}")
        self.renderer.render_triangle(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
        area = self._calculate_area()
        print(f"Area: {area:.2f}")

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.x3 += dx
        self.y3 += dy
        print(f"Triangle moved by ({dx}, {dy})")

    def get_info(self):
        return f"Triangle: points=({self.x1},{self.y1}), ({self.x2},{self.y2}), ({self.x3},{self.y3})"

    def set_points(self, x1, y1, x2, y2, x3, y3):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.x3, self.y3 = x3, y3
        print("Triangle points updated")

    def _calculate_area(self):
        a = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        b = math.sqrt((self.x3 - self.x2) ** 2 + (self.y3 - self.y2) ** 2)
        c = math.sqrt((self.x1 - self.x3) ** 2 + (self.y1 - self.y3) ** 2)

        s = (a + b + c) / 2

        if s * (s - a) * (s - b) * (s - c) >= 0:
            return math.sqrt(s * (s - a) * (s - b) * (s - c))
        else:
            return 0