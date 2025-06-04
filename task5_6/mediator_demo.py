from mediator import (
    HTMLDocumentMediator,
    HTMLComponentFactory,
    MediatedElementNode,
    MediatedTextNode,
    HTMLValidationRules
)
from light_html import LightElementNode, LightTextNode


def demonstrate_mediator_pattern():

    print("Створюємо HTML документ з медіатором...")
    mediator, root = HTMLComponentFactory.create_document_with_mediator()

    head = HTMLComponentFactory.create_mediated_element('head', 'head')
    body = HTMLComponentFactory.create_mediated_element('body', 'body')

    mediator.register_component('head', head)
    mediator.register_component('body', body)

    print("\n1. ДОДАВАННЯ ЕЛЕМЕНТІВ:")
    print("=" * 40)

    root.get_element().add_child(head.get_element())
    root.get_element().add_child(body.get_element())

    title_element = HTMLComponentFactory.create_mediated_element('title', 'title')
    title_text = HTMLComponentFactory.create_mediated_text('title-text', 'Демо Медіатора')

    mediator.register_component('title', title_element)
    mediator.register_component('title-text', title_text)

    title_element.get_element().add_child(title_text.get_text_node())
    head.get_element().add_child(title_element.get_element())

    print("\n2. ДОДАВАННЯ КОНТЕНТУ В BODY:")
    print("=" * 40)

    header = HTMLComponentFactory.create_mediated_element('header', 'h1', ['main-header'])
    header_text = HTMLComponentFactory.create_mediated_text('header-text', 'Головна сторінка')

    mediator.register_component('header', header)
    mediator.register_component('header-text', header_text)

    header.get_element().add_child(header_text.get_text_node())
    body.get_element().add_child(header.get_element())

    paragraph = HTMLComponentFactory.create_mediated_element('paragraph', 'p')
    para_text = HTMLComponentFactory.create_mediated_text('para-text', 'Це звичайний параграф.')

    mediator.register_component('paragraph', paragraph)
    mediator.register_component('para-text', para_text)

    paragraph.get_element().add_child(para_text.get_text_node())
    body.get_element().add_child(paragraph.get_element())

    print("\n3. ДОДАВАННЯ EVENT LISTENERS:")
    print("=" * 40)

    # Додаємо слухачі подій
    def on_element_added(sender, data):
        print(f"  → Event Listener: Element added by {sender.get_name()}")

    def on_css_changed(sender, data):
        print(f"  → Event Listener: CSS changed in {sender.get_name()}: {data}")

    def on_text_changed(sender, data):
        print(f"  → Event Listener: Text changed in {sender.get_name()}")

    mediator.add_event_listener('element_added', on_element_added)
    mediator.add_event_listener('css_class_changed', on_css_changed)
    mediator.add_event_listener('text_changed', on_text_changed)

    print("\n4. ТЕСТУВАННЯ ВЗАЄМОДІЇ ЧЕРЕЗ МЕДІАТОР:")
    print("=" * 40)

    # Тестуємо зміну CSS класів
    print("\nДодаємо CSS клас 'highlight' до заголовка:")
    header.add_css_class('highlight')

    print("\nЗмінюємо текст параграфа на TODO:")
    para_text.change_text('TODO: Додати більше контенту тут')

    print("\nСтворюємо новий елемент списку:")
    list_element = HTMLComponentFactory.create_mediated_element('list', 'ul')
    mediator.register_component('list', list_element)

    list_item = HTMLComponentFactory.create_mediated_element('list-item', 'li')
    item_text = HTMLComponentFactory.create_mediated_text('item-text', 'Пункт списку')

    mediator.register_component('list-item', list_item)
    mediator.register_component('item-text', item_text)

    list_item.get_element().add_child(item_text.get_text_node())
    list_element.get_element().add_child(list_item.get_element())
    body.get_element().add_child(list_element.get_element())

    print("\n5. СТАТИСТИКА КОМПОНЕНТІВ:")
    print("=" * 40)

    stats = mediator.get_component_stats()
    for name, stat in stats.items():
        print(f"{name}: {stat}")

    print("\n6. ІСТОРІЯ ЗМІН:")
    print("=" * 40)

    history = mediator.get_change_history()
    for i, change in enumerate(history[-5:], 1):
        print(f"{i}. {change}")

    print("\n7. ТЕСТУВАННЯ ВАЛІДАЦІЇ:")
    print("=" * 40)

    print("\nСпробуємо додати порожній параграф:")
    empty_para = HTMLComponentFactory.create_mediated_element('empty-para', 'p')
    mediator.register_component('empty-para', empty_para)

    body.get_element().add_child(empty_para.get_element())

    print("\n8. ГЕНЕРАЦІЯ ФІНАЛЬНОГО HTML:")
    print("=" * 40)

    final_html = root.get_element().get_outer_html()
    print("Згенерований HTML:")
    print(final_html)

    return mediator, root


def demonstrate_advanced_mediator_features():

    print("\n" + "=" * 60)
    print("ПРОСУНУТІ МОЖЛИВОСТІ МЕДІАТОРА")
    print("=" * 60)

    mediator = HTMLDocumentMediator()

    def custom_validation_rule(sender, event, data):
        if (event == 'text_changed' and
                isinstance(data, dict) and
                'FORBIDDEN' in data.get('new_text', '').upper()):
            print("  ⚠️  Validation failed: Forbidden word detected!")
            return False
        return True

    mediator.add_validation_rule(custom_validation_rule)

    container = HTMLComponentFactory.create_mediated_element('container', 'div', ['container'])
    mediator.register_component('container', container)

    text_node = HTMLComponentFactory.create_mediated_text('text', 'Початковий текст')
    mediator.register_component('text', text_node)

    container.get_element().add_child(text_node.get_text_node())

    print("\n1. ТЕСТУВАННЯ КАСТОМНОЇ ВАЛІДАЦІЇ:")
    print("Спробуємо змінити текст на заборонений:")
    text_node.change_text('Цей текст містить FORBIDDEN слово')

    print("\n2. МНОЖИННІ СЛУХАЧІ ПОДІЙ:")

    event_counter = {'count': 0}

    def counter_listener(sender, data):
        event_counter['count'] += 1
        print(f"  📊 Event counter: {event_counter['count']}")

    def logger_listener(sender, data):
        print(f"  📝 Logger: Event in {sender.get_name()}")

    mediator.add_event_listener('css_class_changed', counter_listener)
    mediator.add_event_listener('css_class_changed', logger_listener)

    for i in range(3):
        container.add_css_class(f'dynamic-class-{i}')
        container.remove_css_class(f'dynamic-class-{i}')

    print(f"\nЗагальна кількість подій: {event_counter['count']}")

    print("\n3. МЕДІАТОР ЯК КООРДИНАТОР:")

    form = HTMLComponentFactory.create_mediated_element('form', 'form')
    input_field = HTMLComponentFactory.create_mediated_element('input', 'input')
    submit_button = HTMLComponentFactory.create_mediated_element('submit', 'button')

    mediator.register_component('form', form)
    mediator.register_component('input', input_field)
    mediator.register_component('submit', submit_button)

    def form_coordination_listener(sender, data):
        if sender.get_name() == 'input' and data.get('action') == 'added':
            if data.get('class') == 'error':
                # Автоматично деактивуємо кнопку при помилці
                submit_comp = mediator._components.get('submit')
                if submit_comp:
                    submit_comp.add_css_class('disabled')
                    print("  🔒 Submit button disabled due to input error")

    mediator.add_event_listener('css_class_changed', form_coordination_listener)

    print("Додаємо клас 'error' до input поля:")
    input_field.add_css_class('error')

    print("\n4. ФІНАЛЬНИЙ СТАН:")
    history = mediator.get_change_history()
    print(f"Всього змін: {len(history)}")
    print(f"Зареєстровано компонентів: {len(mediator._components)}")

    return mediator


if __name__ == "__main__":
    demonstrate_mediator_pattern()
    demonstrate_advanced_mediator_features()