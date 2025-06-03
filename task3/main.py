from task3.graphics_editor import GraphicsEditor
from task3.renderers import RasterRenderer, SVGRenderer, VectorRenderer
from task3.shapes import Circle, Square, Triangle


def main():
    print("=== Графічний редактор з патерном Міст ===\n")

    vector_renderer = VectorRenderer()
    raster_renderer = RasterRenderer()
    svg_renderer = SVGRenderer()

    print("1. Створення фігур з різними рендерерами:")
    print("-" * 45)

    circle = Circle(vector_renderer, x=50, y=50, radius=25)
    square = Square(raster_renderer, x=100, y=100, side=30)
    triangle = Triangle(svg_renderer, x1=0, y1=0, x2=30, y2=    0, x3=15, y3=25)

    circle.draw()
    square.draw()
    triangle.draw()

    print(f"\n{'=' * 60}")
    print("2. Зміна рендерерів (демонстрація гнучкості Bridge pattern):")
    print("-" * 60)

    print("\nЗміна рендерера для кола з векторного на растровий:")
    circle.set_renderer(raster_renderer)
    circle.draw()

    print("\nЗміна рендерера для квадрата з растрового на SVG:")
    square.set_renderer(svg_renderer)
    square.draw()

    print("\nЗміна рендерера для трикутника з SVG на векторний:")
    triangle.set_renderer(vector_renderer)
    triangle.draw()

    print(f"\n{'=' * 60}")
    print("3. Робота з графічним редактором:")
    print("-" * 60)

    editor = GraphicsEditor()

    editor_circle = Circle(vector_renderer, x=200, y=200, radius=40)
    editor_square = Square(vector_renderer, x=300, y=300, side=50)
    editor_triangle = Triangle(vector_renderer, x1=400, y1=400, x2=450, y2=400, x3=425, y3=450)

    editor.add_shape(editor_circle)
    editor.add_shape(editor_square)
    editor.add_shape(editor_triangle)

    editor.draw_all_shapes()

    print(f"\n{'=' * 60}")
    print("4. Зміна глобального рендерера:")
    print("-" * 60)

    editor.set_global_renderer(raster_renderer)
    editor.draw_all_shapes()

    editor.set_global_renderer(svg_renderer)
    editor.draw_all_shapes()

    print(f"\n{'=' * 60}")
    print("5. Демонстрація операцій з фігурами:")
    print("-" * 60)

    print("\nПереміщення кола:")
    editor_circle.move(10, -5)
    editor_circle.draw()

    print("\nЗміна розміру квадрата:")
    editor_square.set_side(75)
    editor_square.draw()

    print("\nЗміна точок трикутника:")
    editor_triangle.set_points(500, 500, 600, 500, 550, 600)
    editor_triangle.draw()

    print(f"\n{'=' * 60}")
    print("6. Інформація про фігури в редакторі:")
    print("-" * 60)
    print(editor.get_shapes_info())

    print("=== Демонстрація завершена ===")


if __name__ == "__main__":
    main()