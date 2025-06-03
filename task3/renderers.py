from task3.renderer_interface import Renderer


class VectorRenderer(Renderer):

    def render_circle(self, x, y, radius):
        print(f"Drawing Circle as vector: center=({x}, {y}), radius={radius}")
        print("  -> Using mathematical equations and curves")

    def render_square(self, x, y, side):
        print(f"Drawing Square as vector: position=({x}, {y}), side={side}")
        print("  -> Using geometric paths and lines")

    def render_triangle(self, x1, y1, x2, y2, x3, y3):
        print(f"Drawing Triangle as vector: points=({x1},{y1}), ({x2},{y2}), ({x3},{y3})")
        print("  -> Using vector paths and nodes")

    def get_type(self):
        return "Vector Graphics"


class RasterRenderer(Renderer):

    def render_circle(self, x, y, radius):
        print(f"Drawing Circle as pixels: center=({x}, {y}), radius={radius}")
        print("  -> Rasterizing circle using pixel grid")

    def render_square(self, x, y, side):
        print(f"Drawing Square as pixels: position=({x}, {y}), side={side}")
        print("  -> Filling pixel array with square pattern")

    def render_triangle(self, x1, y1, x2, y2, x3, y3):
        print(f"Drawing Triangle as pixels: points=({x1},{y1}), ({x2},{y2}), ({x3},{y3})")
        print("  -> Rasterizing triangle using scan-line algorithm")

    def get_type(self):
        return "Raster Graphics"


class SVGRenderer(Renderer):

    def render_circle(self, x, y, radius):
        print(f"Generating SVG Circle: <circle cx='{x}' cy='{y}' r='{radius}' />")
        print("  -> Creating scalable vector markup")

    def render_square(self, x, y, side):
        print(f"Generating SVG Square: <rect x='{x}' y='{y}' width='{side}' height='{side}' />")
        print("  -> Creating XML-based vector description")

    def render_triangle(self, x1, y1, x2, y2, x3, y3):
        points = f"{x1},{y1} {x2},{y2} {x3},{y3}"
        print(f"Generating SVG Triangle: <polygon points='{points}' />")
        print("  -> Creating web-compatible vector format")

    def get_type(self):
        return "SVG Graphics"