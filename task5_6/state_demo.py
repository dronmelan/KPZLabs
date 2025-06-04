from state import StatefulLightElementNode, StateTransitionManager, StateFactory
from light_html import LightTextNode


def demonstrate_basic_states():
    print("1. БАЗОВІ СТАНИ ЕЛЕМЕНТІВ:")
    print("-" * 40)

    button = StatefulLightElementNode("button", css_classes=["btn"])
    button.add_child(LightTextNode("Натисни мене"))

    print(f"Початковий стан: {button.get_state()}")
    print(f"HTML: {button.get_outer_html()}")
    print()

    states_to_test = ["disabled", "hidden", "readonly", "highlighted"]

    for state in states_to_test:
        button.set_state(state)
        print(f"Стан '{state}':")
        print(f"HTML: {button.get_outer_html()}")
        print(f"Можна редагувати: {button.can_edit()}")
        print()

    button.enable()
    print(f"Повернення до нормального стану:")
    print(f"HTML: {button.get_outer_html()}")
    print()


def demonstrate_state_restrictions():
    print("2. ОБМЕЖЕННЯ У РІЗНИХ СТАНАХ:")
    print("-" * 40)

    form = StatefulLightElementNode("form", css_classes=["user-form"])

    print("Додавання елементів у нормальному стані:")
    input_field = StatefulLightElementNode("input", closing_type="self_closing")
    form.add_child(input_field)
    print(f"Дочірніх елементів: {form.get_children_count()}")

    print("\nПереведення у відключений стан:")
    form.disable()

    button = StatefulLightElementNode("button")
    button.add_child(LightTextNode("Submit"))
    form.add_child(button)  # Це не спрацює
    print(f"Дочірніх елементів після спроби додавання: {form.get_children_count()}")

    print("\nПереведення у прихований стан:")
    form.hide()
    print(f"HTML: {form.get_outer_html()}")

    form.show()
    print(f"Після показу: {form.get_outer_html()}")
    print()


def demonstrate_state_transitions():
    print("3. УПРАВЛІННЯ ПЕРЕХОДАМИ МІЖ СТАНАМИ:")
    print("-" * 40)

    manager = StateTransitionManager()
    element = StatefulLightElementNode("div", css_classes=["content"])
    element.add_child(LightTextNode("Контент"))

    print("Дозволені переходи з нормального стану:")
    allowed = manager.get_allowed_transitions("normal")
    print(f"  {', '.join(allowed)}")

    print("\nСпроба переходів:")
    success = manager.transition_element(element, "disabled")
    print(f"normal -> disabled: {'✓' if success else '✗'}")

    success = manager.transition_element(element, "readonly")
    print(f"disabled -> readonly: {'✓' if success else '✗'}")

    success = manager.transition_element(element, "normal")
    print(f"disabled -> normal: {'✓' if success else '✗'}")

    print(f"\nІсторія станів: {' -> '.join(element.get_state_history())}")
    print()


def demonstrate_complex_form():
    print("4. СКЛАДНА ФОРМА З РІЗНИМИ СТАНАМИ:")
    print("-" * 40)

    form = StatefulLightElementNode("form", css_classes=["registration-form"])

    title = StatefulLightElementNode("h2")
    title.add_child(LightTextNode("Реєстрація користувача"))
    form.add_child(title)

    name_field = StatefulLightElementNode("input", closing_type="self_closing",
                                          css_classes=["form-input"])
    form.add_child(name_field)

    email_field = StatefulLightElementNode("input", closing_type="self_closing",
                                           css_classes=["form-input"])
    email_field.make_readonly()
    form.add_child(email_field)

    submit_btn = StatefulLightElementNode("button", css_classes=["submit-btn"])
    submit_btn.add_child(LightTextNode("Зареєструватися"))
    submit_btn.disable()
    form.add_child(submit_btn)

    confirm_field = StatefulLightElementNode("input", closing_type="self_closing",
                                             css_classes=["form-input"])
    confirm_field.highlight()
    form.add_child(confirm_field)

    print("Форма з різними станами елементів:")
    print(form.get_outer_html())
    print()

    print("Симуляція валідації:")
    submit_btn.enable()
    print("✓ Кнопка активована")

    confirm_field.set_state("normal")
    print("✓ Підтвердження нормалізовано")

    print("\nФорма після валідації:")
    print(form.get_outer_html())
    print()


def demonstrate_state_methods():
    print("5. ЗРУЧНІ МЕТОДИ ДЛЯ РОБОТИ ЗІ СТАНАМИ:")
    print("-" * 40)

    panel = StatefulLightElementNode("div", css_classes=["control-panel"])
    panel.add_child(LightTextNode("Панель управління"))

    print("Доступні стани:", StateFactory.get_available_states())
    print()

    operations = [
        ("Відключення", lambda: panel.disable()),
        ("Приховування", lambda: panel.hide()),
        ("Показ", lambda: panel.show()),
        ("Режим тільки для читання", lambda: panel.make_readonly()),
        ("Виділення", lambda: panel.highlight()),
        ("Увімкнення", lambda: panel.enable())
    ]

    for description, operation in operations:
        operation()
        print(f"{description}: стан '{panel.get_state()}'")

    print(f"\nПовна історія: {' -> '.join(panel.get_state_history())}")
    print()

    print("Переключення між станами:")
    panel.toggle_state("normal", "highlighted")
    print(f"Після переключення: {panel.get_state()}")

    panel.toggle_state("normal", "highlighted")
    print(f"Після повторного переключення: {panel.get_state()}")
    print()


def demonstrate_state_pattern():
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ ПАТЕРНУ STATE")
    print("=" * 60)

    demonstrate_basic_states()
    demonstrate_state_restrictions()
    demonstrate_state_transitions()
    demonstrate_complex_form()
    demonstrate_state_methods()

    print("=" * 60)
    print("ЗАВЕРШЕННЯ ДЕМОНСТРАЦІЇ ПАТЕРНУ STATE")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_state_pattern()