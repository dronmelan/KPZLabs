from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from light_html import LightElementNode


class ElementState(ABC):

    @abstractmethod
    def get_state_name(self) -> str:
        pass

    @abstractmethod
    def render(self, element: 'StatefulLightElementNode') -> str:
        pass

    @abstractmethod
    def can_add_child(self, element: 'StatefulLightElementNode') -> bool:
        pass

    @abstractmethod
    def can_edit(self, element: 'StatefulLightElementNode') -> bool:
        pass

    @abstractmethod
    def get_css_modifier(self) -> str:
        pass


class NormalState(ElementState):

    def get_state_name(self) -> str:
        return "normal"

    def render(self, element: 'StatefulLightElementNode') -> str:
        return element._render_base()

    def can_add_child(self, element: 'StatefulLightElementNode') -> bool:
        return True

    def can_edit(self, element: 'StatefulLightElementNode') -> bool:
        return True

    def get_css_modifier(self) -> str:
        return ""


class DisabledState(ElementState):

    def get_state_name(self) -> str:
        return "disabled"

    def render(self, element: 'StatefulLightElementNode') -> str:
        html = element._render_base()
        if element.closing_type == element.SELF_CLOSING:
            html = html.replace(' />', ' disabled />')
        else:
            tag_end = html.find('>')
            if tag_end != -1:
                html = html[:tag_end] + ' disabled' + html[tag_end:]
        return html

    def can_add_child(self, element: 'StatefulLightElementNode') -> bool:
        return False

    def can_edit(self, element: 'StatefulLightElementNode') -> bool:
        return False

    def get_css_modifier(self) -> str:
        return "disabled"


class HiddenState(ElementState):

    def get_state_name(self) -> str:
        return "hidden"

    def render(self, element: 'StatefulLightElementNode') -> str:
        return "<!-- Hidden element -->"

    def can_add_child(self, element: 'StatefulLightElementNode') -> bool:
        return True  # Можна додавати, але вони не будуть відображатися

    def can_edit(self, element: 'StatefulLightElementNode') -> bool:
        return True

    def get_css_modifier(self) -> str:
        return "hidden"


class ReadOnlyState(ElementState):
    def get_state_name(self) -> str:
        return "readonly"

    def render(self, element: 'StatefulLightElementNode') -> str:
        html = element._render_base()
        if element.closing_type == element.SELF_CLOSING:
            html = html.replace(' />', ' readonly />')
        else:
            tag_end = html.find('>')
            if tag_end != -1:
                html = html[:tag_end] + ' readonly' + html[tag_end:]
        return html

    def can_add_child(self, element: 'StatefulLightElementNode') -> bool:
        return False

    def can_edit(self, element: 'StatefulLightElementNode') -> bool:
        return False

    def get_css_modifier(self) -> str:
        return "readonly"


class HighlightedState(ElementState):

    def get_state_name(self) -> str:
        return "highlighted"

    def render(self, element: 'StatefulLightElementNode') -> str:
        html = element._render_base()
        if element.closing_type == element.SELF_CLOSING:
            html = html.replace(' />', ' style="background-color: yellow;" />')
        else:
            tag_end = html.find('>')
            if tag_end != -1:
                html = html[:tag_end] + ' style="background-color: yellow;"' + html[tag_end:]
        return html

    def can_add_child(self, element: 'StatefulLightElementNode') -> bool:
        return True

    def can_edit(self, element: 'StatefulLightElementNode') -> bool:
        return True

    def get_css_modifier(self) -> str:
        return "highlighted"


class StateFactory:

    _states = {
        "normal": NormalState(),
        "disabled": DisabledState(),
        "hidden": HiddenState(),
        "readonly": ReadOnlyState(),
        "highlighted": HighlightedState()
    }

    @classmethod
    def get_state(cls, state_name: str) -> ElementState:
        if state_name not in cls._states:
            raise ValueError(f"Unknown state: {state_name}")
        return cls._states[state_name]

    @classmethod
    def get_available_states(cls) -> list:
        return list(cls._states.keys())


from light_html import LightElementNode, LightNode
from typing import List


class StatefulLightElementNode(LightElementNode):

    def __init__(self, tag_name: str, display_type: str = "block",
                 closing_type: str = "with_closing_tag", css_classes: List[str] = None,
                 initial_state: str = "normal"):
        super().__init__(tag_name, display_type, closing_type, css_classes)
        self._state: ElementState = StateFactory.get_state(initial_state)
        self._state_history: List[str] = [initial_state]

    def set_state(self, state_name: str) -> None:
        if state_name not in StateFactory.get_available_states():
            raise ValueError(f"Invalid state: {state_name}")

        old_state = self._state.get_state_name()
        self._state = StateFactory.get_state(state_name)
        self._state_history.append(state_name)

        print(f"Element {self.tag_name} state changed: {old_state} -> {state_name}")

    def get_state(self) -> str:
        return self._state.get_state_name()

    def get_state_history(self) -> List[str]:
        return self._state_history.copy()

    def add_child(self, child: LightNode) -> None:
        if not self._state.can_add_child(self):
            print(f"Cannot add child to {self.tag_name} in {self.get_state()} state")
            return
        super().add_child(child)

    def get_outer_html(self) -> str:
        return self._state.render(self)

    def _render_base(self) -> str:
        css_classes = self.css_classes.copy()
        css_modifier = self._state.get_css_modifier()
        if css_modifier and css_modifier not in css_classes:
            css_classes.append(css_modifier)

        class_attr = f' class="{" ".join(css_classes)}"' if css_classes else ""

        if self.closing_type == self.SELF_CLOSING:
            return f'<{self.tag_name}{class_attr} />'
        else:
            inner_html = self.get_inner_html()
            return f'<{self.tag_name}{class_attr}>{inner_html}</{self.tag_name}>'

    def can_edit(self) -> bool:
        return self._state.can_edit(self)

    def enable(self) -> None:
        self.set_state("normal")

    def disable(self) -> None:
        self.set_state("disabled")

    def hide(self) -> None:
        self.set_state("hidden")

    def show(self) -> None:
        self.set_state("normal")

    def make_readonly(self) -> None:
        self.set_state("readonly")

    def highlight(self) -> None:
        self.set_state("highlighted")

    def toggle_state(self, state1: str, state2: str) -> None:
        current_state = self.get_state()
        if current_state == state1:
            self.set_state(state2)
        else:
            self.set_state(state1)


class StateTransitionManager:

    def __init__(self):
        self._allowed_transitions = {
            "normal": ["disabled", "hidden", "readonly", "highlighted"],
            "disabled": ["normal", "hidden"],
            "hidden": ["normal", "disabled", "readonly", "highlighted"],
            "readonly": ["normal", "hidden", "highlighted"],
            "highlighted": ["normal", "disabled", "hidden", "readonly"]
        }

    def can_transition(self, from_state: str, to_state: str) -> bool:
        return to_state in self._allowed_transitions.get(from_state, [])

    def get_allowed_transitions(self, from_state: str) -> List[str]:
        return self._allowed_transitions.get(from_state, []).copy()

    def transition_element(self, element: StatefulLightElementNode, to_state: str) -> bool:
        current_state = element.get_state()

        if not self.can_transition(current_state, to_state):
            print(f"Transition from {current_state} to {to_state} is not allowed")
            return False

        element.set_state(to_state)
        return True