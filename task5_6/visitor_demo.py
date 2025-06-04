from light_html import LightElementNode, LightTextNode
from flyweight import LightElementNodeFlyweight
from html_processor import HTMLProcessor
from visitor import (
    HTMLStatisticsVisitor,
    HTMLValidationVisitor,
    HTMLTransformVisitor,
    HTMLSearchVisitor
)


def create_complex_document():
    root = LightElementNode("html", css_classes=["main-page"])

    head = LightElementNode("head")
    title = LightElementNode("title")
    title.add_child(LightTextNode("Демонстрація Відвідувача"))
    head.add_child(title)
    root.add_child(head)

    body = LightElementNode("body", css_classes=["container"])

    h1 = LightElementNode("h1", css_classes=["main-title"])
    h1.add_child(LightTextNode("Головна сторінка"))
    body.add_child(h1)

    nav = LightElementNode("nav", css_classes=["navigation"])
    nav_list = LightElementNode("ul")

    nav_items = ["Головна", "Про нас", "Контакти"]
    for item in nav_items:
        li = LightElementNode("li")
        link = LightElementNode("a", css_classes=["nav-link"])
        link.add_child(LightTextNode(item))
        li.add_child(link)
        nav_list.add_child(li)

    nav.add_child(nav_list)
    body.add_child(nav)

    main = LightElementNode("main", css_classes=["content"])

    p1 = LightElementNode("p")
    p1.add_child(LightTextNode("Це демонстрація патерну Відвідувач у HTML-дереві."))
    main.add_child(p1)

    table = create_sample_table()
    main.add_child(table)

    p2 = LightElementNode("p", css_classes=["highlight"])
    p2.add_child(LightTextNode("   Цей текст має зайві пробіли   "))
    main.add_child(p2)

    body.add_child(main)
    root.add_child(body)

    return root


def create_sample_table():
    table = LightElementNode("table", css_classes=["data-table"])

    thead = LightElementNode("thead")
    header_row = LightElementNode("tr")

    headers = ["ID", "Назва", "Статус"]
    for header_text in headers:
        th = LightElementNode("th", css_classes=["header-cell"])
        th.add_child(LightTextNode(header_text))
        header_row.add_child(th)

    thead.add_child(header_row)
    table.add_child(thead)

    tbody = LightElementNode("tbody")

    data = [
        ["1", "Елемент A", "Активний"],
        ["2", "Елемент B", "Неактивний"],
        ["3", "Елемент C", "Активний"]
    ]

    for row_data in data:
        tr = LightElementNode("tr")
        for cell_data in row_data:
            td = LightElementNode("td", css_classes=["data-cell"])
            td.add_child(LightTextNode(cell_data))
            tr.add_child(td)
        tbody.add_child(tr)

    table.add_child(tbody)
    return table


def create_flyweight_document():
    sample_text = [
        "Заголовок документа",
        "Короткий опис",
        "Це звичайний параграф тексту для демонстрації.",
        "    Цей рядок має відступ",
        "Ще один звичайний параграф.",
        "Фінал"
    ]

    return HTMLProcessor.process_text_flyweight(sample_text)


def demonstrate_statistics_visitor():
    print("1. СТАТИСТИЧНИЙ ВІДВІДУВАЧ")
    print("-" * 40)

    regular_doc = create_complex_document()
    flyweight_doc = create_flyweight_document()

    stats_visitor = HTMLStatisticsVisitor()
    regular_doc.accept(stats_visitor)

    print("Статистика звичайного документа:")
    print(stats_visitor.get_report())

    stats_visitor.reset()
    flyweight_doc.accept(stats_visitor)

    print("\nСтатистика документа з легковаговиками:")
    print(stats_visitor.get_report())


def demonstrate_validation_visitor():
    print("\n2. ВАЛІДАЦІЙНИЙ ВІДВІДУВАЧ")
    print("-" * 40)

    document = create_complex_document()

    script = LightElementNode("script")
    script.add_child(LightTextNode("alert('test');"))
    document.children[1].add_child(script)  # Додаємо до body

    validator = HTMLValidationVisitor()
    document.accept(validator)

    print(validator.get_report())


def demonstrate_transform_visitor():
    print("\n3. ТРАНСФОРМАЦІЙНИЙ ВІДВІДУВАЧ")
    print("-" * 40)

    document = create_complex_document()

    print("HTML до трансформації (фрагмент):")
    print(document.get_outer_html()[:200] + "...")

    transformations = {
        'add_css_class': 'transformed',
        'trim_whitespace': True
    }

    transformer = HTMLTransformVisitor(transformations)
    document.accept(transformer)

    print(f"\nВиконано змін: {transformer.get_changes_count()}")
    print("HTML після трансформації (фрагмент):")
    print(document.get_outer_html()[:200] + "...")


def demonstrate_search_visitor():
    print("\n4. ПОШУКОВИЙ ВІДВІДУВАЧ")
    print("-" * 40)

    document = create_complex_document()

    search_criteria = {'tag_name': 'p'}
    searcher = HTMLSearchVisitor(search_criteria)
    document.accept(searcher)

    p_elements = searcher.get_results()
    print(f"Знайдено елементів 'p': {len(p_elements)}")

    search_criteria = {'css_class': 'data-cell'}
    searcher = HTMLSearchVisitor(search_criteria)
    document.accept(searcher)

    data_cells = searcher.get_results()
    print(f"Знайдено елементів з класом 'data-cell': {len(data_cells)}")

    search_criteria = {'text_contains': 'демонстрація'}
    searcher = HTMLSearchVisitor(search_criteria)
    document.accept(searcher)

    text_nodes = searcher.get_results()
    print(f"Знайдено текстових вузлів з 'демонстрація': {len(text_nodes)}")

    for node in text_nodes:
        if isinstance(node, LightTextNode):
            print(f"  Текст: '{node.text}'")


def demonstrate_mixed_document():
    print("\n5. ЗМІШАНИЙ ДОКУМЕНТ (звичайні + легковагові)")
    print("-" * 50)

    root = LightElementNode("div", css_classes=["mixed-content"])

    regular_section = LightElementNode("section", css_classes=["regular"])
    regular_section.add_child(LightTextNode("Звичайна секція"))
    root.add_child(regular_section)

    flyweight_section = LightElementNodeFlyweight("section", css_classes=["flyweight"])
    flyweight_section.add_child(LightTextNode("Легковагова секція"))
    root.add_child(flyweight_section)

    stats_visitor = HTMLStatisticsVisitor()
    root.accept(stats_visitor)

    print("Статистика змішаного документа:")
    print(stats_visitor.get_report())


def demonstrate_visitor_pattern():
    print("ДЕМОНСТРАЦІЯ ПАТЕРНУ ВІДВІДУВАЧ")
    print("=" * 50)

    demonstrate_statistics_visitor()
    demonstrate_validation_visitor()
    demonstrate_transform_visitor()
    demonstrate_search_visitor()
    demonstrate_mixed_document()

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА")
    print("=" * 50)


if __name__ == "__main__":
    demonstrate_visitor_pattern()