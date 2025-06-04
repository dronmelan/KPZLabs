from light_html import LightElementNode, LightTextNode
from flyweight import LightElementNodeFlyweight
from iterator import IteratorFactory, DepthFirstIterator, BreadthFirstIterator
from html_processor import HTMLProcessor


def create_complex_html_structure():
    """Створює складну HTML структуру для демонстрації ітераторів"""

    # Створюємо кореневий div
    root = LightElementNode("div", "block", "with_closing_tag", ["container"])

    # Додаємо заголовок
    header = LightElementNode("header", "block", "with_closing_tag", ["page-header"])
    h1 = LightElementNode("h1", "block", "with_closing_tag")
    h1.add_child(LightTextNode("Демонстрація ітераторів"))
    header.add_child(h1)

    nav = LightElementNode("nav", "block", "with_closing_tag")
    ul = LightElementNode("ul", "block", "with_closing_tag")

    for i, item in enumerate(["Головна", "Про нас", "Контакти"], 1):
        li = LightElementNode("li", "inline", "with_closing_tag")
        a = LightElementNode("a", "inline", "with_closing_tag", [f"nav-link-{i}"])
        a.add_child(LightTextNode(item))
        li.add_child(a)
        ul.add_child(li)

    nav.add_child(ul)
    header.add_child(nav)
    root.add_child(header)

    # Додаємо основний контент
    main = LightElementNode("main", "block", "with_closing_tag", ["main-content"])

    # Секція з артіклем
    article = LightElementNode("article", "block", "with_closing_tag", ["post"])
    article_title = LightElementNode("h2", "block", "with_closing_tag")
    article_title.add_child(LightTextNode("Стаття про ітератори"))
    article.add_child(article_title)

    for i in range(3):
        p = LightElementNode("p", "block", "with_closing_tag")
        p.add_child(LightTextNode(f"Це параграф номер {i + 1} у нашій статті про патерн Ітератор."))
        article.add_child(p)

    main.add_child(article)

    # Сайдбар
    aside = LightElementNode("aside", "block", "with_closing_tag", ["sidebar"])
    aside_title = LightElementNode("h3", "block", "with_closing_tag")
    aside_title.add_child(LightTextNode("Бічна панель"))
    aside.add_child(aside_title)

    sidebar_list = LightElementNode("ul", "block", "with_closing_tag")
    for i in range(2):
        li = LightElementNode("li", "block", "with_closing_tag")
        li.add_child(LightTextNode(f"Елемент сайдбару {i + 1}"))
        sidebar_list.add_child(li)
    aside.add_child(sidebar_list)

    main.add_child(aside)
    root.add_child(main)

    # Футер
    footer = LightElementNode("footer", "block", "with_closing_tag", ["page-footer"])
    footer_text = LightElementNode("p", "block", "with_closing_tag")
    footer_text.add_child(LightTextNode("© 2025 Демонстрація патернів проектування"))
    footer.add_child(footer_text)
    root.add_child(footer)

    return root


def demonstrate_iterators():
    """Демонстрація різних типів ітераторів"""
    print("=" * 70)
    print("ЗАВДАННЯ 7: ПАТЕРН ІТЕРАТОР")
    print("=" * 70)

    # Створюємо складну HTML структуру
    html_tree = create_complex_html_structure()

    print("Створено HTML дерево для демонстрації ітераторів\n")

    # 1. Демонстрація обходу в глибину (DFS)
    print("1. ОБХІД В ГЛИБИНУ (Depth-First Search)")
    print("-" * 50)
    dfs_iterator = html_tree.create_depth_first_iterator()
    dfs_nodes = []

    for node in dfs_iterator:
        if hasattr(node, 'tag_name'):
            dfs_nodes.append(node.tag_name)
        elif hasattr(node, 'flyweight'):
            dfs_nodes.append(node.flyweight.tag_name)
        else:
            dfs_nodes.append("TextNode")

    print(f"Порядок обходу: {' -> '.join(dfs_nodes[:15])}...")
    print(f"Загальна кількість вузлів: {len(dfs_nodes)}")

    # 2. Демонстрація обходу в ширину (BFS)
    print("\n2. ОБХІД В ШИРИНУ (Breadth-First Search)")
    print("-" * 50)
    bfs_iterator = html_tree.create_breadth_first_iterator()
    bfs_nodes = []

    for node in bfs_iterator:
        if hasattr(node, 'tag_name'):
            bfs_nodes.append(node.tag_name)
        elif hasattr(node, 'flyweight'):
            bfs_nodes.append(node.flyweight.tag_name)
        else:
            bfs_nodes.append("TextNode")

    print(f"Порядок обходу: {' -> '.join(bfs_nodes[:15])}...")
    print(f"Загальна кількість вузлів: {len(bfs_nodes)}")

    # 3. Ітератор за типом елементів
    print("\n3. ІТЕРАТОР ЗА ТИПОМ ЕЛЕМЕНТІВ")
    print("-" * 50)
    text_nodes = []
    for node in html_tree.create_element_type_iterator(LightTextNode):
        text_nodes.append(node.text[:30] + "..." if len(node.text) > 30 else node.text)

    print(f"Знайдено {len(text_nodes)} текстових вузлів:")
    for i, text in enumerate(text_nodes[:5], 1):
        print(f"  {i}. {text}")
    if len(text_nodes) > 5:
        print(f"  ... та ще {len(text_nodes) - 5} вузлів")

    # 4. Ітератор за тегом
    print("\n4. ІТЕРАТОР ЗА ТЕГОМ")
    print("-" * 50)

    # Шукаємо всі параграфи
    paragraphs = html_tree.find_elements_by_tag("p")
    print(f"Знайдено {len(paragraphs)} елементів <p>:")
    for i, p in enumerate(paragraphs, 1):
        inner_text = p.get_inner_html()[:50] + "..." if len(p.get_inner_html()) > 50 else p.get_inner_html()
        print(f"  {i}. {inner_text}")

    # Шукаємо всі списки
    lists = html_tree.find_elements_by_tag("ul")
    print(f"\nЗнайдено {len(lists)} елементів <ul>:")
    for i, ul in enumerate(lists, 1):
        children_count = ul.get_children_count()
        print(f"  {i}. Список з {children_count} дочірніми елементами")

    # 5. Використання вбудованого ітератора для дочірніх елементів
    print("\n5. ПЕРЕБІР ДОЧІРНІХ ЕЛЕМЕНТІВ")
    print("-" * 50)
    print("Дочірні елементи кореневого div:")
    for i, child in enumerate(html_tree, 1):
        tag_name = getattr(child, 'tag_name', 'TextNode')
        css_classes = getattr(child, 'css_classes', [])
        classes_str = f" (класи: {', '.join(css_classes)})" if css_classes else ""
        print(f"  {i}. <{tag_name}>{classes_str}")


def demonstrate_with_flyweight():
    """Демонстрація ітераторів з flyweight структурою"""
    print("\n" + "=" * 70)
    print("ІТЕРАТОРИ З FLYWEIGHT СТРУКТУРОЮ")
    print("=" * 70)

    # Створюємо flyweight структуру з тексту
    sample_text = [
        "Заголовок документа",
        "Перший параграф тексту для демонстрації.",
        "    Цей рядок має відступ - буде в <pre>",
        "Короткий рядок",  # Буде в h2
        "Ще один звичайний параграф з текстом.",
        "    Ще один рядок з відступом",
    ]

    flyweight_tree = HTMLProcessor.process_text_flyweight(sample_text)

    print("Створено flyweight HTML дерево")
    print(f"Кількість flyweight об'єктів: {len(sample_text) + 1}")  # +1 для root div

    # Демонстрація пошуку по тегам у flyweight структурі
    print("\nПошук елементів за тегами:")

    h1_elements = flyweight_tree.find_elements_by_tag("h1")
    print(f"Елементи <h1>: {len(h1_elements)}")

    h2_elements = flyweight_tree.find_elements_by_tag("h2")
    print(f"Елементи <h2>: {len(h2_elements)}")

    p_elements = flyweight_tree.find_elements_by_tag("p")
    print(f"Елементи <p>: {len(p_elements)}")

    pre_elements = flyweight_tree.find_elements_by_tag("pre")
    print(f"Елементи <pre>: {len(pre_elements)}")

    # Демонстрація DFS обходу flyweight структури
    print("\nОбхід flyweight структури в глибину:")
    count = 0
    for node in flyweight_tree.create_depth_first_iterator():
        count += 1
        if hasattr(node, 'flyweight') and hasattr(node.flyweight, 'tag_name'):
            print(f"  {count}. Flyweight елемент: <{node.flyweight.tag_name}>")
        elif hasattr(node, 'tag_name'):
            print(f"  {count}. Звичайний елемент: <{node.tag_name}>")
        else:
            text_preview = node.text[:40] + "..." if len(node.text) > 40 else node.text
            print(f"  {count}. Текстовий вузол: {text_preview}")


if __name__ == "__main__":
    demonstrate_iterators()
    demonstrate_with_flyweight()

    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦІЯ ПАТЕРНУ ІТЕРАТОР ЗАВЕРШЕНА")
    print("=" * 70)