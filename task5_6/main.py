from light_html import LightElementNode, LightTextNode
from flyweight import ElementFlyweightFactory
from html_processor import HTMLProcessor
from iterator_demo import demonstrate_iterators, demonstrate_with_flyweight


def create_sample_table():
    table = LightElementNode("table", "block", "with_closing_tag", ["data-table"])

    thead = LightElementNode("thead", "block", "with_closing_tag")
    header_row = LightElementNode("tr", "block", "with_closing_tag")

    headers = ["Ім'я", "Вік", "Місто"]
    for header_text in headers:
        th = LightElementNode("th", "inline", "with_closing_tag", ["header-cell"])
        th.add_child(LightTextNode(header_text))
        header_row.add_child(th)

    thead.add_child(header_row)
    table.add_child(thead)

    tbody = LightElementNode("tbody", "block", "with_closing_tag")

    data = [
        ["Олексій", "25", "Київ"],
        ["Марія", "30", "Львів"],
        ["Петро", "22", "Одеса"]
    ]

    for row_data in data:
        tr = LightElementNode("tr", "block", "with_closing_tag")
        for cell_data in row_data:
            td = LightElementNode("td", "inline", "with_closing_tag", ["data-cell"])
            td.add_child(LightTextNode(cell_data))
            tr.add_child(td)
        tbody.add_child(tr)

    table.add_child(tbody)
    return table


def create_sample_text():
    return [
        "Пригоди Аліси в Країні Чудес",
        "",
        "Розділ 1",
        "Аліса почала відчувати, що їй дуже набридло сидіти біля сестри на березі і нічого не робити.",
        "    Раз чи двічі вона зазирнула в книгу, яку читала сестра, але там не було ні картинок, ні розмов.",
        "— А що толку в книзі, — подумала Аліса, — коли в ній немає ні картинок, ні розмов?",
        "",
        "Розділ 2",
        "    І тут Білий Кролик витяг із кишені годинник і, глянувши на нього, поспішив далі.",
        "Аліса стрибнула на ноги: до цієї миті їй ніколи не доводилося бачити кролика із кишенею,",
        "а тим більше з годинником у ній."
    ]


def demonstrate_task5():
    print("=" * 60)
    print("ЗАВДАННЯ 5: КОМПОНУВАЛЬНИК (LightHTML)")
    print("=" * 60)

    table = create_sample_table()

    print(f"Створено таблицю з {table.get_children_count()} дочірніми елементами")
    print(f"Тип відображення: {table.display_type}")
    print(f"Тип закриття: {table.closing_type}")
    print(f"CSS класи: {', '.join(table.css_classes)}")
    print(f"Розмір в пам'яті: {table.get_size()} байт")

    print("\nouterHTML таблиці:")
    print(table.get_outer_html())

    print("\ninnerHTML заголовка таблиці:")
    thead = table.children[0]
    print(thead.get_inner_html())


def demonstrate_task6():
    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 6: ЛЕГКОВАГОВИК")
    print("=" * 60)

    sample_text = create_sample_text()
    print(f"Обробляємо текст з {len(sample_text)} рядків\n")

    print("1. БЕЗ ЛЕГКОВАГОВИКА:")
    simple_tree = HTMLProcessor.process_text_simple(sample_text)
    simple_size = simple_tree.get_size()
    print(f"Розмір дерева: {simple_size} байт")

    print("\n2. З ЛЕГКОВАГОВИКОМ:")
    flyweight_tree = HTMLProcessor.process_text_flyweight(sample_text)
    flyweight_size = flyweight_tree.get_size()
    flyweights_size = ElementFlyweightFactory.get_total_flyweights_size()
    total_flyweight_size = flyweight_size + flyweights_size

    print(f"Кількість унікальних легковаговиків: {ElementFlyweightFactory.get_flyweights_count()}")
    print(f"Розмір дерева (без легковаговиків): {flyweight_size} байт")
    print(f"Розмір всіх легковаговиків: {flyweights_size} байт")
    print(f"Загальний розмір: {total_flyweight_size} байт")

    print("\n3. ПОРІВНЯННЯ:")
    savings = simple_size - total_flyweight_size
    percentage = (savings / simple_size) * 100 if simple_size > 0 else 0
    print(f"Економія пам'яті: {savings} байт ({percentage:.1f}%)")

    print("\n4. ПРИКЛАД ЗГЕНЕРОВАНОГО HTML:")
    html_output = flyweight_tree.get_outer_html()
    print(html_output[:500] + "..." if len(html_output) > 500 else html_output)


def demonstrate_task7():
    print("\n")
    demonstrate_iterators()
    demonstrate_with_flyweight()


from command_demo import demonstrate_command_pattern

def demonstrate_task8():
    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 8: КОМАНДА")
    print("=" * 60)
    demonstrate_command_pattern()

if __name__ == "__main__":
    demonstrate_task5()
    demonstrate_task6()
    demonstrate_task7()
    demonstrate_task8()

    print("\n" + "=" * 60)
    print("ПРОГРАМА ЗАВЕРШЕНА УСПІШНО")
    print("=" * 60)
