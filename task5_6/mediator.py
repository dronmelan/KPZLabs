from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from light_html import LightNode, LightElementNode, LightTextNode


class HTMLMediator(ABC):

    @abstractmethod
    def notify(self, sender: 'HTMLComponent', event: str, data: Any = None) -> None:
        pass


class HTMLDocumentMediator(HTMLMediator):

    def __init__(self):
        self._components: Dict[str, 'HTMLComponent'] = {}
        self._event_listeners: Dict[str, List[callable]] = {}
        self._validation_rules: List[callable] = []
        self._change_history: List[str] = []

    def register_component(self, name: str, component: 'HTMLComponent') -> None:
        self._components[name] = component
        component.set_mediator(self)

    def add_event_listener(self, event_type: str, callback: callable) -> None:
        if event_type not in self._event_listeners:
            self._event_listeners[event_type] = []
        self._event_listeners[event_type].append(callback)

    def add_validation_rule(self, rule: callable) -> None:
        self._validation_rules.append(rule)

    def notify(self, sender: 'HTMLComponent', event: str, data: Any = None) -> None:
        print(f"[MEDIATOR] Event '{event}' from {sender.get_name()}")

        self._change_history.append(f"{event} in {sender.get_name()}: {data}")

        if event in ['element_added', 'element_removed', 'text_changed']:
            self._validate_change(sender, event, data)

        if event == 'element_added':
            self._handle_element_added(sender, data)
        elif event == 'element_removed':
            self._handle_element_removed(sender, data)
        elif event == 'css_class_changed':
            self._handle_css_class_changed(sender, data)
        elif event == 'text_changed':
            self._handle_text_changed(sender, data)
        elif event == 'structure_changed':
            self._handle_structure_changed(sender, data)

        if event in self._event_listeners:
            for callback in self._event_listeners[event]:
                callback(sender, data)

    def _validate_change(self, sender: 'HTMLComponent', event: str, data: Any) -> bool:
        for rule in self._validation_rules:
            if not rule(sender, event, data):
                print(f"[MEDIATOR] Validation failed for {event} in {sender.get_name()}")
                return False
        return True

    def _handle_element_added(self, sender: 'HTMLComponent', element: LightNode) -> None:
        if isinstance(element, LightElementNode) and hasattr(element, 'css_classes'):
            if not any(cls.startswith('id-') for cls in element.css_classes):
                element.css_classes.append(f'id-{len(self._change_history)}')

        for name, component in self._components.items():
            if component != sender:
                component.on_structure_changed('element_added', element)

    def _handle_element_removed(self, sender: 'HTMLComponent', element: LightNode) -> None:
        for name, component in self._components.items():
            if component != sender:
                component.on_structure_changed('element_removed', element)

    def _handle_css_class_changed(self, sender: 'HTMLComponent', data: Dict) -> None:
        css_class = data.get('class')
        action = data.get('action')  # 'added' or 'removed'

        if css_class == 'highlight':
            self._update_highlighting(sender, action == 'added')

    def _handle_text_changed(self, sender: 'HTMLComponent', data: Dict) -> None:
        old_text = data.get('old_text')
        new_text = data.get('new_text')

        if 'TODO' in new_text.upper():
            self._mark_as_todo(sender)

    def _handle_structure_changed(self, sender: 'HTMLComponent', data: Any) -> None:
        # Оновлюємо індекси та кеш
        self._rebuild_indexes()

    def _update_highlighting(self, sender: 'HTMLComponent', highlight: bool) -> None:
        for name, component in self._components.items():
            if hasattr(component, 'update_highlight'):
                component.update_highlight(sender, highlight)

    def _mark_as_todo(self, sender: 'HTMLComponent') -> None:
        if hasattr(sender, 'add_css_class'):
            sender.add_css_class('todo-item')

    def _rebuild_indexes(self) -> None:
        print("[MEDIATOR] Rebuilding indexes after structure change")

    def get_change_history(self) -> List[str]:
        return self._change_history.copy()

    def get_component_stats(self) -> Dict[str, Any]:
        stats = {}
        for name, component in self._components.items():
            if hasattr(component, 'get_stats'):
                stats[name] = component.get_stats()
        return stats


class HTMLComponent(ABC):

    def __init__(self, name: str):
        self._name = name
        self._mediator: Optional[HTMLMediator] = None

    def set_mediator(self, mediator: HTMLMediator) -> None:
        self._mediator = mediator

    def get_name(self) -> str:
        return self._name

    @abstractmethod
    def on_structure_changed(self, change_type: str, data: Any) -> None:
        pass


class MediatedElementNode(HTMLComponent):

    def __init__(self, name: str, element: LightElementNode):
        super().__init__(name)
        self._element = element
        self._original_add_child = element.add_child
        self._original_remove_child = getattr(element, 'remove_child', None)

        element.add_child = self._mediated_add_child

    def _mediated_add_child(self, child: LightNode) -> None:
        self._original_add_child(child)
        if self._mediator:
            self._mediator.notify(self, 'element_added', child)

    def remove_child(self, child: LightNode) -> None:
        if child in self._element.children:
            self._element.children.remove(child)
            if self._mediator:
                self._mediator.notify(self, 'element_removed', child)

    def add_css_class(self, css_class: str) -> None:
        if css_class not in self._element.css_classes:
            self._element.css_classes.append(css_class)
            if self._mediator:
                self._mediator.notify(self, 'css_class_changed', {
                    'class': css_class,
                    'action': 'added'
                })

    def remove_css_class(self, css_class: str) -> None:
        if css_class in self._element.css_classes:
            self._element.css_classes.remove(css_class)
            if self._mediator:
                self._mediator.notify(self, 'css_class_changed', {
                    'class': css_class,
                    'action': 'removed'
                })

    def on_structure_changed(self, change_type: str, data: Any) -> None:
        print(f"[{self._name}] Structure changed: {change_type}")

    def update_highlight(self, sender: 'HTMLComponent', highlight: bool) -> None:
        if highlight:
            self.add_css_class('related-highlight')
        else:
            self.remove_css_class('related-highlight')

    def get_stats(self) -> Dict[str, Any]:
        return {
            'tag_name': self._element.tag_name,
            'children_count': len(self._element.children),
            'css_classes': len(self._element.css_classes),
            'size': self._element.get_size()
        }

    def get_element(self) -> LightElementNode:
        return self._element


class MediatedTextNode(HTMLComponent):

    def __init__(self, name: str, text_node: LightTextNode):
        super().__init__(name)
        self._text_node = text_node
        self._original_text = text_node.text

    def change_text(self, new_text: str) -> None:
        old_text = self._text_node.text
        self._text_node.text = new_text
        if self._mediator:
            self._mediator.notify(self, 'text_changed', {
                'old_text': old_text,
                'new_text': new_text
            })

    def on_structure_changed(self, change_type: str, data: Any) -> None:
        print(f"[{self._name}] Structure changed: {change_type}")

    def get_stats(self) -> Dict[str, Any]:
        return {
            'text_length': len(self._text_node.text),
            'size': self._text_node.get_size()
        }

    def get_text_node(self) -> LightTextNode:
        return self._text_node


class HTMLValidationRules:

    @staticmethod
    def no_empty_paragraphs(sender: HTMLComponent, event: str, data: Any) -> bool:
        if (event == 'element_added' and
                isinstance(data, LightElementNode) and
                data.tag_name == 'p' and
                len(data.children) == 0):
            return False
        return True

    @staticmethod
    def max_nesting_level(max_level: int = 10):

        def rule(sender: HTMLComponent, event: str, data: Any) -> bool:
            if event == 'element_added' and isinstance(data, LightElementNode):
                level = 0
                current = data
                while hasattr(current, 'children') and current.children:
                    level += 1
                    if level > max_level:
                        return False
                    current = current.children[0] if current.children else None
            return True

        return rule

    @staticmethod
    def required_attributes(sender: HTMLComponent, event: str, data: Any) -> bool:
        if (event == 'element_added' and
                isinstance(data, LightElementNode) and
                data.tag_name == 'img'):
            # img теги повинні мати alt текст (симулюємо через CSS клас)
            return any('alt-' in cls for cls in data.css_classes)
        return True


class HTMLComponentFactory:

    @staticmethod
    def create_mediated_element(name: str, tag_name: str,
                                css_classes: List[str] = None) -> MediatedElementNode:
        element = LightElementNode(tag_name, css_classes=css_classes or [])
        return MediatedElementNode(name, element)

    @staticmethod
    def create_mediated_text(name: str, text: str) -> MediatedTextNode:
        text_node = LightTextNode(text)
        return MediatedTextNode(name, text_node)

    @staticmethod
    def create_document_with_mediator() -> tuple[HTMLDocumentMediator, MediatedElementNode]:
        mediator = HTMLDocumentMediator()

        mediator.add_validation_rule(HTMLValidationRules.no_empty_paragraphs)
        mediator.add_validation_rule(HTMLValidationRules.max_nesting_level(8))
        mediator.add_validation_rule(HTMLValidationRules.required_attributes)

        root = HTMLComponentFactory.create_mediated_element('document-root', 'html')
        mediator.register_component('document', root)

        return mediator, root