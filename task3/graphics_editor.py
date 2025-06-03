class GraphicsEditor:

    def __init__(self):
        self.shapes = []
        self.current_renderer = None

    def add_shape(self, shape):
        self.shapes.append(shape)
        print(f"Added {shape.get_info()} to editor")

    def set_global_renderer(self, renderer):
        self.current_renderer = renderer
        for shape in self.shapes:
            shape.set_renderer(renderer)
        print(f"\nGlobal renderer set to: {renderer.get_type()}")

    def draw_all_shapes(self):
        print(f"\n{'=' * 50}")
        print("DRAWING ALL SHAPES IN EDITOR")
        print(f"{'=' * 50}")

        if not self.shapes:
            print("No shapes to draw!")
            return

        for i, shape in enumerate(self.shapes, 1):
            print(f"\n[Shape {i}]")
            shape.draw()

    def get_shapes_info(self):
        if not self.shapes:
            return "No shapes in editor"

        info = "Shapes in editor:\n"
        for i, shape in enumerate(self.shapes, 1):
            info += f"{i}. {shape.get_info()}\n"
        return info