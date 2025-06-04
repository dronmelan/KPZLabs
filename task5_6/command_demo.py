from light_html import LightElementNode, LightTextNode
from command import (
    HTMLEditorInvoker, HTMLCommandFactory, MacroCommand,
    AddChildCommand, RemoveChildCommand, ChangeTextCommand,
    AddCssClassCommand, RemoveCssClassCommand
)


def demonstrate_basic_commands():
    print("1. БАЗОВІ КОМАНДИ:")
    print("-" * 40)

    div = LightElementNode("div", "block", "with_closing_tag", ["container"])
    p = LightElementNode("p", "block", "with_closing_tag")
    text = LightTextNode("Початковий текст")

    editor = HTMLEditorInvoker()

    print("Початкова структура:")
    print(f"div.css_classes: {div.css_classes}")
    print(f"div.children: {len(div.children)}")
    print(f"text.text: '{text.text}'")

    print("\nВиконуємо команди:")

    add_p_cmd = HTMLCommandFactory.create_add_child_command(div, p)
    editor.execute_command(add_p_cmd)
    print(f"✓ {add_p_cmd.get_description()}")

    add_text_cmd = HTMLCommandFactory.create_add_child_command(p, text)
    editor.execute_command(add_text_cmd)
    print(f"✓ {add_text_cmd.get_description()}")

    add_class_cmd = HTMLCommandFactory.create_add_css_class_command(div, "highlighted")
    editor.execute_command(add_class_cmd)
    print(f"✓ {add_class_cmd.get_description()}")

    change_text_cmd = HTMLCommandFactory.create_change_text_command(text, "Змінений текст!")
    editor.execute_command(change_text_cmd)
    print(f"✓ {change_text_cmd.get_description()}")

    print("\nРезультат після виконання команд:")
    print(f"div.css_classes: {div.css_classes}")
    print(f"div.children: {len(div.children)}")
    print(f"text.text: '{text.text}'")
    print(f"HTML: {div.get_outer_html()}")

    return editor, div, p, text


def demonstrate_undo_redo(editor, div, p, text):
    print("\n\n2. СКАСУВАННЯ ТА ПОВТОР КОМАНД:")
    print("-" * 40)

    print("Історія команд:")
    for i, desc in enumerate(editor.get_history()):
        marker = " ← current" if i == len(editor.get_history()) - 1 else ""
        print(f"  {i + 1}. {desc}{marker}")

    print(f"\nМожна скасувати: {editor.can_undo()}")
    print(f"Можна повторити: {editor.can_redo()}")

    print("\nСкасовуємо останні 2 команди:")
    for i in range(2):
        if editor.undo():
            print(f"✓ Скасовано команду {len(editor.history) - editor.current_position}")

    print(f"\nСтан після скасування:")
    print(f"text.text: '{text.text}'")
    print(f"div.css_classes: {div.css_classes}")

    print("\nПовторюємо одну команду:")
    if editor.redo():
        print("✓ Повторено команду")

    print(f"\nСтан після повтору:")
    print(f"div.css_classes: {div.css_classes}")

    print(f"\nМожна скасувати: {editor.can_undo()}")
    print(f"Можна повторити: {editor.can_redo()}")


def demonstrate_macro_commands():
    """Демонстрація макрокоманд"""
    print("\n\n3. МАКРОКОМАНДИ:")
    print("-" * 40)

    article = LightElementNode("article", "block", "with_closing_tag")
    header = LightElementNode("header", "block", "with_closing_tag")
    h1 = LightElementNode("h1", "block", "with_closing_tag")
    title_text = LightTextNode("Заголовок статті")

    editor = HTMLEditorInvoker()

    print("Створюємо макрокоманду для побудови структури статті...")

    commands = [
        HTMLCommandFactory.create_add_child_command(article, header),
        HTMLCommandFactory.create_add_child_command(header, h1),
        HTMLCommandFactory.create_add_child_command(h1, title_text),
        HTMLCommandFactory.create_add_css_class_command(article, "article"),
        HTMLCommandFactory.create_add_css_class_command(header, "article-header"),
        HTMLCommandFactory.create_add_css_class_command(h1, "main-title")
    ]

    macro = HTMLCommandFactory.create_macro_command(
        commands,
        "Create article structure"
    )

    print(f"Макрокоманда: {macro.get_description()}")

    editor.execute_command(macro)
    print("Макрокоманда виконана")

    print(f"\nРезультат:")
    print(f"HTML: {article.get_outer_html()}")

    print("\nСкасовуємо макрокоманду...")
    editor.undo()
    print("Макрокоманда скасована")

    print(f"\nСтан після скасування:")
    print(f"article.children: {len(article.children)}")
    print(f"article.css_classes: {article.css_classes}")


def demonstrate_command_factory():
    print("\n\n4. ФАБРИКА КОМАНД:")
    print("-" * 40)

    div = LightElementNode("div", "block", "with_closing_tag")
    span = LightElementNode("span", "inline", "with_closing_tag")
    text = LightTextNode("Текст")

    print("Створюємо команди через фабрику:")

    commands = [
        HTMLCommandFactory.create_add_child_command(div, span),
        HTMLCommandFactory.create_add_child_command(span, text),
        HTMLCommandFactory.create_add_css_class_command(div, "wrapper"),
        HTMLCommandFactory.create_add_css_class_command(span, "highlight"),
        HTMLCommandFactory.create_change_text_command(text, "Новий текст")
    ]

    for cmd in commands:
        print(f"✓ {type(cmd).__name__}: {cmd.get_description()}")

    editor = HTMLEditorInvoker()
    print(f"\nВиконуємо {len(commands)} команд...")

    for cmd in commands:
        editor.execute_command(cmd)

    print(f"Результат: {div.get_outer_html()}")

    print(f"\nІсторія команд ({len(editor.get_history())} записів):")
    for i, desc in enumerate(editor.get_history(), 1):
        print(f"  {i}. {desc}")


def demonstrate_complex_scenario():
    print("\n\n5. КОМПЛЕКСНИЙ СЦЕНАРІЙ:")
    print("-" * 40)

    # Створюємо таблицю
    table = LightElementNode("table", "block", "with_closing_tag")
    thead = LightElementNode("thead", "block", "with_closing_tag")
    tbody = LightElementNode("tbody", "block", "with_closing_tag")

    editor = HTMLEditorInvoker()

    print("Сценарій: Створення та редагування таблиці")

    print("\nЕтап 1: Створення базової структури")
    structure_commands = [
        HTMLCommandFactory.create_add_child_command(table, thead),
        HTMLCommandFactory.create_add_child_command(table, tbody),
        HTMLCommandFactory.create_add_css_class_command(table, "data-table")
    ]

    structure_macro = HTMLCommandFactory.create_macro_command(
        structure_commands, "Create table structure"
    )
    editor.execute_command(structure_macro)
    print(f"✓ {structure_macro.get_description()}")

    print("\nЕтап 2: Додавання заголовків")
    header_row = LightElementNode("tr", "block", "with_closing_tag")
    th1 = LightElementNode("th", "inline", "with_closing_tag")
    th2 = LightElementNode("th", "inline", "with_closing_tag")

    header_commands = [
        HTMLCommandFactory.create_add_child_command(thead, header_row),
        HTMLCommandFactory.create_add_child_command(header_row, th1),
        HTMLCommandFactory.create_add_child_command(header_row, th2),
        HTMLCommandFactory.create_add_child_command(th1, LightTextNode("Назва")),
        HTMLCommandFactory.create_add_child_command(th2, LightTextNode("Значення"))
    ]

    for cmd in header_commands:
        editor.execute_command(cmd)
        print(f"✓ {cmd.get_description()}")

    print(f"\nПроміжний результат ({table.get_children_count()} дочірніх елементів):")
    print(f"HTML: {table.get_outer_html()[:100]}...")

    print("\nЕтап 3: Додавання стилів (з помилкою)")
    editor.execute_command(
        HTMLCommandFactory.create_add_css_class_command(table, "wrong-style")
    )
    editor.execute_command(
        HTMLCommandFactory.create_add_css_class_command(thead, "header-style")
    )
    print("Додано стилі (один з них помилковий)")

    print("\nЕтап 4: Виправлення помилки")
    print("Скасовуємо останні 2 команди...")
    editor.undo()  # Скасовуємо header-style
    editor.undo()  # Скасовуємо wrong-style

    editor.execute_command(
        HTMLCommandFactory.create_add_css_class_command(table, "correct-style")
    )
    print("Додано правильний стиль")

    print(f"\nФінальний результат:")
    print(f"CSS класи таблиці: {table.css_classes}")
    print(f"Кількість команд в історії: {len(editor.get_history())}")
    print(f"Поточна позиція: {editor.current_position + 1}")

    print(f"\nФінальний HTML:")
    print(table.get_outer_html())


def demonstrate_command_pattern():
    print("=" * 60)
    print("ПАТТЕРН КОМАНДА - ДЕМОНСТРАЦІЯ")
    print("=" * 60)

    editor, div, p, text = demonstrate_basic_commands()

    demonstrate_undo_redo(editor, div, p, text)

    demonstrate_macro_commands()

    demonstrate_command_factory()

    demonstrate_complex_scenario()

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦІЯ ПАТЕРНУ КОМАНДА ЗАВЕРШЕНА")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_command_pattern()