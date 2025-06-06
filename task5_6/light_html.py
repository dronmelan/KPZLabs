from abc import ABC, abstractmethod
from typing import List, Optional


class LightNode(ABC):

    @abstractmethod
    def get_outer_html(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    def accept(self, visitor):
        pass

    def create_depth_first_iterator(self):
        from iterator import IteratorFactory
        return IteratorFactory.create_depth_first_iterator(self)

    def create_breadth_first_iterator(self):
        from iterator import IteratorFactory
        return IteratorFactory.create_breadth_first_iterator(self)

    def create_element_type_iterator(self, element_type: type):
        from iterator import IteratorFactory
        return IteratorFactory.create_element_type_iterator(self, element_type)

    def create_tag_name_iterator(self, tag_name: str):
        from iterator import IteratorFactory
        return IteratorFactory.create_tag_name_iterator(self, tag_name)


class LightTextNode(LightNode):

    def __init__(self, text: str):
        self.text = text

    def get_outer_html(self) -> str:
        return self.text

    def get_size(self) -> int:
        return 48 + len(self.text.encode('utf-8'))

    def accept(self, visitor):
        return visitor.visit_text_node(self)


class LightElementNode(LightNode):
    BLOCK = "block"
    INLINE = "inline"

    SELF_CLOSING = "self_closing"
    WITH_CLOSING_TAG = "with_closing_tag"

    def __init__(self, tag_name: str, display_type: str = BLOCK,
                 closing_type: str = WITH_CLOSING_TAG, css_classes: List[str] = None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
        self.css_classes = css_classes or []
        self.children: List[LightNode] = []

    def add_child(self, child: LightNode):
        self.children.append(child)

    def get_children_count(self) -> int:
        return len(self.children)

    def get_inner_html(self) -> str:
        return "".join(child.get_outer_html() for child in self.children)

    def get_outer_html(self) -> str:
        class_attr = f' class="{" ".join(self.css_classes)}"' if self.css_classes else ""

        if self.closing_type == self.SELF_CLOSING:
            return f'<{self.tag_name}{class_attr} />'
        else:
            inner_html = self.get_inner_html()
            return f'<{self.tag_name}{class_attr}>{inner_html}</{self.tag_name}>'

    def get_size(self) -> int:
        size = 120
        size += len(self.tag_name.encode('utf-8'))
        size += len(self.display_type.encode('utf-8'))
        size += len(self.closing_type.encode('utf-8'))
        for css_class in self.css_classes:
            size += len(css_class.encode('utf-8')) + 24
        size += len(self.children) * 8
        for child in self.children:
            size += child.get_size()
        return size

    def accept(self, visitor):
        return visitor.visit_element_node(self)

    def __iter__(self):
        return iter(self.children)

    def find_elements_by_tag(self, tag_name: str) -> List['LightNode']:
        result = []
        for node in self.create_tag_name_iterator(tag_name):
            result.append(node)
        return result

    def find_elements_by_type(self, element_type: type) -> List['LightNode']:
        result = []
        for node in self.create_element_type_iterator(element_type):
            result.append(node)
        return result


# Розширені класи з підтримкою команд
class CommandMixin:

    def __init__(self):
        self._editor = None

    def set_editor(self, editor):
        self._editor = editor

    def add_child_with_command(self, child: LightNode):
        if self._editor:
            from command import HTMLCommandFactory
            command = HTMLCommandFactory.create_add_child_command(self, child)
            self._editor.execute_command(command)

    def remove_child_with_command(self, child: LightNode):
        if self._editor:
            from command import HTMLCommandFactory
            command = HTMLCommandFactory.create_remove_child_command(self, child)
            self._editor.execute_command(command)

    def add_css_class_with_command(self, css_class: str):
        if self._editor:
            from command import HTMLCommandFactory
            command = HTMLCommandFactory.create_add_css_class_command(self, css_class)
            self._editor.execute_command(command)

    def remove_css_class_with_command(self, css_class: str):
        if self._editor:
            from command import HTMLCommandFactory
            command = HTMLCommandFactory.create_remove_css_class_command(self, css_class)
            self._editor.execute_command(command)


class EnhancedLightElementNode(LightElementNode, CommandMixin):

    def __init__(self, tag_name: str, display_type: str = "block",
                 closing_type: str = "with_closing_tag", css_classes: List[str] = None,
                 editor: Optional = None):
        LightElementNode.__init__(self, tag_name, display_type, closing_type, css_classes)
        CommandMixin.__init__(self)
        if editor:
            self.set_editor(editor)

    def set_editor_recursive(self, editor) -> None:
        self.set_editor(editor)
        for child in self.children:
            if isinstance(child, EnhancedLightElementNode):
                child.set_editor_recursive(editor)

    def smart_add_child(self, child: LightNode) -> None:
        if self._editor:
            self.add_child_with_command(child)
        else:
            self.add_child(child)

    def smart_remove_child(self, child: LightNode) -> None:
        if self._editor:
            self.remove_child_with_command(child)
        else:
            if child in self.children:
                self.children.remove(child)

    def smart_add_css_class(self, css_class: str) -> None:
        if self._editor:
            self.add_css_class_with_command(css_class)
        else:
            if css_class not in self.css_classes:
                self.css_classes.append(css_class)

    def smart_remove_css_class(self, css_class: str) -> None:
        if self._editor:
            self.remove_css_class_with_command(css_class)
        else:
            if css_class in self.css_classes:
                self.css_classes.remove(css_class)


class EnhancedLightTextNode(LightTextNode):

    def __init__(self, text: str, editor: Optional = None):
        super().__init__(text)
        self._editor = editor

    def set_editor(self, editor) -> None:
        self._editor = editor

    def smart_change_text(self, new_text: str) -> None:
        if self._editor:
            from command import HTMLCommandFactory
            command = HTMLCommandFactory.create_change_text_command(self, new_text)
            self._editor.execute_command(command)
        else:
            self.text = new_text


class HTMLDocumentBuilder:

    def __init__(self, editor: Optional = None):
        self.editor = editor
        if not self.editor:
            from command import HTMLEditorInvoker
            self.editor = HTMLEditorInvoker()
        self.root: Optional[EnhancedLightElementNode] = None

    def create_document(self, root_tag: str = "html") -> 'HTMLDocumentBuilder':
        self.root = EnhancedLightElementNode(root_tag, editor=self.editor)
        return self

    def add_element(self, parent: EnhancedLightElementNode, tag_name: str,
                    css_classes: List[str] = None) -> EnhancedLightElementNode:
        element = EnhancedLightElementNode(tag_name, css_classes=css_classes, editor=self.editor)
        parent.smart_add_child(element)
        return element

    def add_text(self, parent: EnhancedLightElementNode, text: str) -> EnhancedLightTextNode:
        text_node = EnhancedLightTextNode(text, editor=self.editor)
        parent.smart_add_child(text_node)
        return text_node

    def add_table(self, parent: EnhancedLightElementNode,
                  headers: List[str], rows: List[List[str]]) -> EnhancedLightElementNode:
        table = self.add_element(parent, "table", ["data-table"])

        commands = []

        if headers:
            thead = EnhancedLightElementNode("thead", editor=self.editor)
            from command import HTMLCommandFactory
            commands.append(HTMLCommandFactory.create_add_child_command(table, thead))

            header_row = EnhancedLightElementNode("tr", editor=self.editor)
            commands.append(HTMLCommandFactory.create_add_child_command(thead, header_row))

            for header_text in headers:
                th = EnhancedLightElementNode("th", css_classes=["header-cell"], editor=self.editor)
                commands.append(HTMLCommandFactory.create_add_child_command(header_row, th))

                text_node = EnhancedLightTextNode(header_text, editor=self.editor)
                commands.append(HTMLCommandFactory.create_add_child_command(th, text_node))

        if rows:
            tbody = EnhancedLightElementNode("tbody", editor=self.editor)
            commands.append(HTMLCommandFactory.create_add_child_command(table, tbody))

            for row_data in rows:
                tr = EnhancedLightElementNode("tr", editor=self.editor)
                commands.append(HTMLCommandFactory.create_add_child_command(tbody, tr))

                for cell_data in row_data:
                    td = EnhancedLightElementNode("td", css_classes=["data-cell"], editor=self.editor)
                    commands.append(HTMLCommandFactory.create_add_child_command(tr, td))

                    text_node = EnhancedLightTextNode(str(cell_data), editor=self.editor)
                    commands.append(HTMLCommandFactory.create_add_child_command(td, text_node))

        if commands:
            from command import HTMLCommandFactory
            macro = HTMLCommandFactory.create_macro_command(
                commands, f"Create table with {len(headers)} headers and {len(rows)} rows"
            )
            self.editor.execute_command(macro)

        return table

    def undo(self) -> bool:
        return self.editor.undo()

    def redo(self) -> bool:
        return self.editor.redo()

    def get_history(self) -> List[str]:
        return self.editor.get_history()

    def get_document(self) -> Optional[EnhancedLightElementNode]:
        return self.root


class CommandLogger:

    def __init__(self, editor):
        self.editor = editor
        self.original_execute = editor.execute_command
        editor.execute_command = self._logged_execute

    def _logged_execute(self, command):
        print(f"[LOG] Executing: {command.get_description()}")
        result = self.original_execute(command)
        print(f"[LOG] Completed: {command.get_description()}")
        return result


from typing import List, Dict, Any, Callable
from light_html import LightNode, LightElementNode, LightTextNode
from event_listener import EventTarget, EventType, Event, EventListener, event_manager


class EventAwareLightElementNode(LightElementNode, EventTarget):

    def __init__(self, tag_name: str, display_type: str = "block",
                 closing_type: str = "with_closing_tag", css_classes: List[str] = None):
        LightElementNode.__init__(self, tag_name, display_type, closing_type, css_classes)
        EventTarget.__init__(self)
        self._event_attributes: Dict[str, str] = {}

    def add_child(self, child: LightNode):
        super().add_child(child)
        if isinstance(child, EventTarget):
            child.set_parent_target(self)

    def click(self, data: Dict[str, Any] = None) -> None:
        self.trigger_event(EventType.CLICK, data)
        event_manager.process_global_event(Event(EventType.CLICK, self, data))

    def mouseover(self, data: Dict[str, Any] = None) -> None:
        self.trigger_event(EventType.MOUSEOVER, data)
        event_manager.process_global_event(Event(EventType.MOUSEOVER, self, data))

    def mouseout(self, data: Dict[str, Any] = None) -> None:
        self.trigger_event(EventType.MOUSEOUT, data)
        event_manager.process_global_event(Event(EventType.MOUSEOUT, self, data))

    def focus(self, data: Dict[str, Any] = None) -> None:
        self.trigger_event(EventType.FOCUS, data)
        event_manager.process_global_event(Event(EventType.FOCUS, self, data))

    def blur(self, data: Dict[str, Any] = None) -> None:
        self.trigger_event(EventType.BLUR, data)
        event_manager.process_global_event(Event(EventType.BLUR, self, data))

    def change(self, data: Dict[str, Any] = None) -> None:
        self.trigger_event(EventType.CHANGE, data)
        event_manager.process_global_event(Event(EventType.CHANGE, self, data))

    def keydown(self, key: str, data: Dict[str, Any] = None) -> None:
        event_data = data or {}
        event_data['key'] = key
        self.trigger_event(EventType.KEYDOWN, event_data)
        event_manager.process_global_event(Event(EventType.KEYDOWN, self, event_data))

    def keyup(self, key: str, data: Dict[str, Any] = None) -> None:
        event_data = data or {}
        event_data['key'] = key
        self.trigger_event(EventType.KEYUP, event_data)
        event_manager.process_global_event(Event(EventType.KEYUP, self, event_data))

    def submit(self, data: Dict[str, Any] = None) -> None:
        self.trigger_event(EventType.SUBMIT, data)
        event_manager.process_global_event(Event(EventType.SUBMIT, self, data))

    def set_event_attribute(self, event_type: EventType, handler_code: str) -> None:
        self._event_attributes[f"on{event_type.value}"] = handler_code

    def get_outer_html(self) -> str:
        class_attr = f' class="{" ".join(self.css_classes)}"' if self.css_classes else ""

        event_attrs = ""
        for attr_name, attr_value in self._event_attributes.items():
            event_attrs += f' {attr_name}="{attr_value}"'

        if self.closing_type == self.SELF_CLOSING:
            return f'<{self.tag_name}{class_attr}{event_attrs} />'
        else:
            inner_html = self.get_inner_html()
            return f'<{self.tag_name}{class_attr}{event_attrs}>{inner_html}</{self.tag_name}>'

    def get_size(self) -> int:
        base_size = super().get_size()

        events_size = 0
        for event_listeners in self._event_listeners.values():
            events_size += len(event_listeners) * 32  # Приблизний розмір обробника

        for attr_name, attr_value in self._event_attributes.items():
            events_size += len(attr_name.encode('utf-8')) + len(attr_value.encode('utf-8')) + 16

        return base_size + events_size

    def get_event_info(self) -> Dict[str, Any]:
        return {
            'listeners_count': self.get_all_listeners_count(),
            'event_types': list(self._event_listeners.keys()),
            'event_attributes': self._event_attributes.copy()
        }


class EventAwareLightTextNode(LightTextNode, EventTarget):

    def __init__(self, text: str):
        LightTextNode.__init__(self, text)
        EventTarget.__init__(self)

    def get_size(self) -> int:
        base_size = super().get_size()

        events_size = 0
        for event_listeners in self._event_listeners.values():
            events_size += len(event_listeners) * 32

        return base_size + events_size


class InteractiveButton(EventAwareLightElementNode):

    def __init__(self, text: str, css_classes: List[str] = None):
        super().__init__("button", "inline", "with_closing_tag", css_classes or ["btn"])
        self.add_child(EventAwareLightTextNode(text))
        self._click_count = 0
        self._enabled = True

        self.add_event_listener_function(EventType.CLICK, self._default_click_handler)

    def _default_click_handler(self, event: Event) -> None:
        if self._enabled:
            self._click_count += 1
            print(f"Button '{self.get_text()}' clicked {self._click_count} times")

    def get_text(self) -> str:
        if self.children and isinstance(self.children[0], EventAwareLightTextNode):
            return self.children[0].text
        return ""

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        if enabled:
            self.css_classes = [cls for cls in self.css_classes if cls != "disabled"]
        else:
            if "disabled" not in self.css_classes:
                self.css_classes.append("disabled")

    def get_click_count(self) -> int:
        return self._click_count

    def reset_click_count(self) -> None:
        self._click_count = 0


class InteractiveForm(EventAwareLightElementNode):

    def __init__(self, css_classes: List[str] = None):
        super().__init__("form", "block", "with_closing_tag", css_classes or ["form"])
        self._fields: Dict[str, EventAwareLightElementNode] = {}
        self._validation_rules: Dict[str, Callable[[str], bool]] = {}

        self.add_event_listener_function(EventType.SUBMIT, self._handle_submit)

    def add_input_field(self, name: str, input_type: str = "text",
                        placeholder: str = "", validation: Callable[[str], bool] = None) -> EventAwareLightElementNode:
        input_field = EventAwareLightElementNode("input", "inline", "self_closing", ["form-input"])
        input_field.set_event_attribute(EventType.CHANGE, f"validateField('{name}')")

        self._fields[name] = input_field
        if validation:
            self._validation_rules[name] = validation

        self.add_child(input_field)
        return input_field

    def add_submit_button(self, text: str = "Submit") -> InteractiveButton:
        button = InteractiveButton(text, ["btn", "btn-submit"])
        button.add_event_listener_function(EventType.CLICK, lambda e: self.submit())
        self.add_child(button)
        return button

    def _handle_submit(self, event: Event) -> None:
        print(f"Form submitted with {len(self._fields)} fields")

        valid = True
        for field_name, validation_rule in self._validation_rules.items():
            print(f"Validating field: {field_name}")

        if valid:
            print("Form validation passed!")
        else:
            print("Form validation failed!")
            event.stop_propagation()

    def get_fields_count(self) -> int:
        return len(self._fields)