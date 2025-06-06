from typing import Dict, Any
from event_listener import (EventType, Event, EventListener,
                            LoggingEventListener, CountingEventListener,
                            ConditionalEventListener, event_manager)
from task5_6.light_html import InteractiveButton, EventAwareLightElementNode, EventAwareLightTextNode, InteractiveForm


class CustomButtonEventListener(EventListener):

    def __init__(self, button_name: str):
        self.button_name = button_name
        self.last_click_time = 0

    def handle_event(self, event: Event) -> None:
        current_time = event.timestamp
        if event.type == EventType.CLICK:
            time_diff = current_time - self.last_click_time
            print(f"Custom handler for '{self.button_name}': "
                  f"Time since last click: {time_diff}ms")
            self.last_click_time = current_time
        elif event.type == EventType.MOUSEOVER:
            print(f"Mouse over '{self.button_name}' button")
        elif event.type == EventType.MOUSEOUT:
            print(f"🐭 Mouse left '{self.button_name}' button")


class FormValidationListener(EventListener):

    def handle_event(self, event: Event) -> None:
        if event.type == EventType.SUBMIT:
            print("Form validation started...")

            import random
            is_valid = random.choice([True, False])

            if is_valid:
                print("Form validation passed!")
            else:
                print("Form validation failed!")
                event.stop_propagation()
                print("Form submission stopped")


def demonstrate_basic_events():
    print("1. БАЗОВІ ПОДІЇ")
    print("-" * 40)

    button = InteractiveButton("Натисни мене", ["btn", "btn-primary"])

    button.add_event_listener(EventType.CLICK, CustomButtonEventListener("Primary Button"))
    button.add_event_listener(EventType.MOUSEOVER, LoggingEventListener("HOVER: "))
    button.add_event_listener(EventType.MOUSEOUT, LoggingEventListener("LEAVE: "))

    print("Симуляція взаємодії з кнопкою:")
    button.mouseover()
    button.click()
    button.click()
    button.mouseout()

    print(f"Кнопка була натиснута {button.get_click_count()} разів")
    print(f"Загальна кількість обробників: {button.get_all_listeners_count()}")


def demonstrate_event_propagation():
    print("\n2. ПОШИРЕННЯ ПОДІЙ")
    print("-" * 40)

    container = EventAwareLightElementNode("div", css_classes=["container"])
    button_wrapper = EventAwareLightElementNode("div", css_classes=["button-wrapper"])
    button = InteractiveButton("Кнопка з поширенням")

    container.add_child(button_wrapper)
    button_wrapper.add_child(button)

    container.add_event_listener(EventType.CLICK, LoggingEventListener("CONTAINER: "))
    button_wrapper.add_event_listener(EventType.CLICK, LoggingEventListener("WRAPPER: "))

    def stop_propagation_handler(event: Event):
        print("🛑 Stopping event propagation at button level")
        event.stop_propagation()

    button.add_event_listener_function(EventType.CLICK, stop_propagation_handler)

    print("Клік по кнопці (з зупинкою поширення):")
    button.click()

    print("\nКлік по wrapper (без зупинки):")
    button_wrapper.click()


def demonstrate_conditional_events():
    print("\n3. УМОВНІ ОБРОБНИКИ")
    print("-" * 40)

    button = InteractiveButton("Умовна кнопка")
    counter = CountingEventListener("Click Counter")

    def even_click_condition(event: Event) -> bool:
        return counter.get_count() % 2 == 0

    def even_click_action(event: Event):
        print(f"🎯 Even click #{counter.get_count()}!")

    conditional_listener = ConditionalEventListener(even_click_condition, even_click_action)

    button.add_event_listener(EventType.CLICK, counter)
    button.add_event_listener(EventType.CLICK, conditional_listener)

    print("Тестування умовного обробника (спрацьовує на парних кліках):")
    for i in range(5):
        print(f"Клік {i + 1}:")
        button.click()


def demonstrate_form_events():
    print("\n4. ПОДІЇ ФОРМИ")
    print("-" * 40)

    form = InteractiveForm(["contact-form"])

    name_field = form.add_input_field("name", "text", "Введіть ім'я")
    email_field = form.add_input_field("email", "email", "Введіть email")
    submit_button = form.add_submit_button("Відправити")

    form.add_event_listener(EventType.SUBMIT, FormValidationListener())

    def field_change_handler(event: Event):
        field_name = event.data.get('field', 'unknown')
        print(f"📝 Field '{field_name}' changed")

    name_field.add_event_listener_function(EventType.CHANGE, field_change_handler)
    email_field.add_event_listener_function(EventType.CHANGE, field_change_handler)

    print("Симуляція заповнення та відправки форми:")
    name_field.change({"field": "name", "value": "Іван Петренко"})
    email_field.change({"field": "email", "value": "ivan@example.com"})

    print("\nВідправка форми (спроба 1):")
    form.submit()

    print("\nВідправка форми (спроба 2):")
    form.submit()


def demonstrate_global_events():
    print("\n5. ГЛОБАЛЬНІ ПОДІЇ")
    print("-" * 40)

    event_manager.enable_logging(True)

    global_logger = LoggingEventListener("GLOBAL: ")
    event_manager.add_global_listener(EventType.CLICK, global_logger)

    button1 = InteractiveButton("Кнопка 1")
    button2 = InteractiveButton("Кнопка 2")

    print("Кліки по різних кнопках (з глобальним обробником):")
    button1.click()
    button2.click()
    button1.click()

    event_log = event_manager.get_event_log()
    print(f"\nЗафіксовано {len(event_log)} подій у глобальному логі")

    event_manager.clear_event_log()


def demonstrate_keyboard_events():
    print("\n6. ПОДІЇ КЛАВІАТУРИ")
    print("-" * 40)

    input_field = EventAwareLightElementNode("input", "inline", "self_closing", ["text-input"])

    def keyboard_handler(event: Event):
        key = event.data.get('key', 'unknown')
        event_type = event.type.value
        print(f"⌨️  {event_type}: key '{key}'")

    input_field.add_event_listener_function(EventType.KEYDOWN, keyboard_handler)
    input_field.add_event_listener_function(EventType.KEYUP, keyboard_handler)

    print("Симуляція введення тексту:")
    keys = ['H', 'e', 'l', 'l', 'o']
    for key in keys:
        input_field.keydown(key)
        input_field.keyup(key)


def demonstrate_html_output():
    print("\n7. HTML ВИВІД З ПОДІЯМИ")
    print("-" * 40)

    button = EventAwareLightElementNode("button", "inline", "with_closing_tag", ["interactive-btn"])
    button.add_child(EventAwareLightTextNode("Інтерактивна кнопка"))
    button.set_event_attribute(EventType.CLICK, "handleButtonClick(this)")
    button.set_event_attribute(EventType.MOUSEOVER, "showTooltip(this)")

    div = EventAwareLightElementNode("div", "block", "with_closing_tag", ["event-container"])
    div.set_event_attribute(EventType.CLICK, "handleContainerClick(event)")
    div.add_child(button)

    input_elem = EventAwareLightElementNode("input", "inline", "self_closing", ["form-control"])
    input_elem.set_event_attribute(EventType.CHANGE, "validateInput(this.value)")
    input_elem.set_event_attribute(EventType.FOCUS, "highlightField(this)")

    div.add_child(input_elem)

    print("Згенерований HTML з атрибутами подій:")
    print(div.get_outer_html())

    print(f"\nІнформація про події:")
    print(f"- Кнопка: {button.get_event_info()}")
    print(f"- Контейнер: {div.get_event_info()}")
    print(f"- Поле вводу: {input_elem.get_event_info()}")


def demonstrate_memory_usage():
    print("\n8. ВИКОРИСТАННЯ ПАМ'ЯТІ")
    print("-" * 40)

    simple_button = EventAwareLightElementNode("button")
    simple_button.add_child(EventAwareLightTextNode("Проста кнопка"))

    complex_button = EventAwareLightElementNode("button")
    complex_button.add_child(EventAwareLightTextNode("Складна кнопка"))

    for i in range(5):
        complex_button.add_event_listener(EventType.CLICK, LoggingEventListener(f"Handler{i}: "))
        complex_button.add_event_listener(EventType.MOUSEOVER, CountingEventListener(f"Counter{i}"))

    complex_button.set_event_attribute(EventType.CLICK, "complexHandler()")
    complex_button.set_event_attribute(EventType.MOUSEOVER, "showComplexTooltip()")
    complex_button.set_event_attribute(EventType.MOUSEOUT, "hideComplexTooltip()")

    print(f"Розмір простої кнопки: {simple_button.get_size()} байт")
    print(f"Розмір складної кнопки: {complex_button.get_size()} байт")
    print(f"Різниця: {complex_button.get_size() - simple_button.get_size()} байт")

    print(f"\nКількість обробників у складної кнопки: {complex_button.get_all_listeners_count()}")


def demonstrate_event_system():
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ СИСТЕМИ ПОДІЙ LIGHTHTML")
    print("=" * 60)

    demonstrate_basic_events()
    demonstrate_event_propagation()
    demonstrate_conditional_events()
    demonstrate_form_events()
    demonstrate_global_events()
    demonstrate_keyboard_events()
    demonstrate_html_output()
    demonstrate_memory_usage()

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦІЯ СИСТЕМИ ПОДІЙ ЗАВЕРШЕНА")
    print("=" * 60)