from abc import ABC, abstractmethod
from typing import List, Any, Optional
from light_html import LightNode, LightElementNode, LightTextNode


class Command(ABC):

    @abstractmethod
    def execute(self) -> Any:
        pass

    @abstractmethod
    def undo(self) -> Any:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class AddChildCommand(Command):

    def __init__(self, parent: LightElementNode, child: LightNode):
        self.parent = parent
        self.child = child
        self.executed = False

    def execute(self) -> None:
        if not self.executed:
            self.parent.add_child(self.child)
            self.executed = True

    def undo(self) -> None:
        if self.executed and self.child in self.parent.children:
            self.parent.children.remove(self.child)
            self.executed = False

    def get_description(self) -> str:
        child_type = type(self.child).__name__
        if isinstance(self.child, LightTextNode):
            content = self.child.text[:20] + "..."
        else:
            content = getattr(self.child, 'tag_name', 'unknown')
        return f"Add {child_type}({content}) to {self.parent.tag_name}"


class RemoveChildCommand(Command):

    def __init__(self, parent: LightElementNode, child: LightNode):
        self.parent = parent
        self.child = child
        self.child_index = None
        self.executed = False

    def execute(self) -> None:
        if not self.executed and self.child in self.parent.children:
            self.child_index = self.parent.children.index(self.child)
            self.parent.children.remove(self.child)
            self.executed = True

    def undo(self) -> None:
        if self.executed and self.child_index is not None:
            self.parent.children.insert(self.child_index, self.child)
            self.executed = False

    def get_description(self) -> str:
        child_type = type(self.child).__name__
        if isinstance(self.child, LightTextNode):
            content = self.child.text[:20] + "..."
        else:
            content = getattr(self.child, 'tag_name', 'unknown')
        return f"Remove {child_type}({content}) from {self.parent.tag_name}"


class ChangeTextCommand(Command):

    def __init__(self, text_node: LightTextNode, new_text: str):
        self.text_node = text_node
        self.new_text = new_text
        self.old_text = text_node.text
        self.executed = False

    def execute(self) -> None:
        if not self.executed:
            self.text_node.text = self.new_text
            self.executed = True

    def undo(self) -> None:
        if self.executed:
            self.text_node.text = self.old_text
            self.executed = False

    def get_description(self) -> str:
        old_preview = self.old_text[:15] + "..." if len(self.old_text) > 15 else self.old_text
        new_preview = self.new_text[:15] + "..." if len(self.new_text) > 15 else self.new_text
        return f"Change text from '{old_preview}' to '{new_preview}'"


class AddCssClassCommand(Command):

    def __init__(self, element: LightElementNode, css_class: str):
        self.element = element
        self.css_class = css_class
        self.executed = False

    def execute(self) -> None:
        if not self.executed and self.css_class not in self.element.css_classes:
            self.element.css_classes.append(self.css_class)
            self.executed = True

    def undo(self) -> None:
        if self.executed and self.css_class in self.element.css_classes:
            self.element.css_classes.remove(self.css_class)
            self.executed = False

    def get_description(self) -> str:
        return f"Add CSS class '{self.css_class}' to {self.element.tag_name}"


class RemoveCssClassCommand(Command):

    def __init__(self, element: LightElementNode, css_class: str):
        self.element = element
        self.css_class = css_class
        self.executed = False

    def execute(self) -> None:
        if not self.executed and self.css_class in self.element.css_classes:
            self.element.css_classes.remove(self.css_class)
            self.executed = True

    def undo(self) -> None:
        if self.executed:
            self.element.css_classes.append(self.css_class)
            self.executed = False

    def get_description(self) -> str:
        return f"Remove CSS class '{self.css_class}' from {self.element.tag_name}"


class MacroCommand(Command):

    def __init__(self, commands: List[Command], description: str = "Macro command"):
        self.commands = commands
        self.description = description
        self.executed = False

    def execute(self) -> None:
        if not self.executed:
            for command in self.commands:
                command.execute()
            self.executed = True

    def undo(self) -> None:
        if self.executed:
            for command in reversed(self.commands):
                command.undo()
            self.executed = False

    def get_description(self) -> str:
        return f"{self.description} ({len(self.commands)} operations)"


class HTMLEditorInvoker:

    def __init__(self, max_history: int = 50):
        self.history: List[Command] = []
        self.current_position = -1
        self.max_history = max_history

    def execute_command(self, command: Command) -> Any:
        result = command.execute()

        if self.current_position < len(self.history) - 1:
            self.history = self.history[:self.current_position + 1]

        self.history.append(command)
        self.current_position += 1

        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_position -= 1

        return result

    def undo(self) -> bool:
        if self.can_undo():
            command = self.history[self.current_position]
            command.undo()
            self.current_position -= 1
            return True
        return False

    def redo(self) -> bool:
        if self.can_redo():
            self.current_position += 1
            command = self.history[self.current_position]
            command.execute()
            return True
        return False

    def can_undo(self) -> bool:
        return self.current_position >= 0

    def can_redo(self) -> bool:
        return self.current_position < len(self.history) - 1

    def get_history(self) -> List[str]:
        return [cmd.get_description() for cmd in self.history]

    def clear_history(self) -> None:
        self.history.clear()
        self.current_position = -1


class HTMLCommandFactory:

    @staticmethod
    def create_add_child_command(parent: LightElementNode, child: LightNode) -> AddChildCommand:
        return AddChildCommand(parent, child)

    @staticmethod
    def create_remove_child_command(parent: LightElementNode, child: LightNode) -> RemoveChildCommand:
        return RemoveChildCommand(parent, child)

    @staticmethod
    def create_change_text_command(text_node: LightTextNode, new_text: str) -> ChangeTextCommand:
        return ChangeTextCommand(text_node, new_text)

    @staticmethod
    def create_add_css_class_command(element: LightElementNode, css_class: str) -> AddCssClassCommand:
        return AddCssClassCommand(element, css_class)

    @staticmethod
    def create_remove_css_class_command(element: LightElementNode, css_class: str) -> RemoveCssClassCommand:
        return RemoveCssClassCommand(element, css_class)

    @staticmethod
    def create_macro_command(commands: List[Command], description: str = "Macro command") -> MacroCommand:
        return MacroCommand(commands, description)


class CommandMixin:

    def __init__(self):
        self._editor: Optional[HTMLEditorInvoker] = None

    def set_editor(self, editor: HTMLEditorInvoker) -> None:
        self._editor = editor

    def add_child_with_command(self, child: LightNode) -> None:
        if self._editor and hasattr(self, 'add_child'):
            command = HTMLCommandFactory.create_add_child_command(self, child)
            self._editor.execute_command(command)
        else:
            if hasattr(self, 'add_child'):
                self.add_child(child)

    def remove_child_with_command(self, child: LightNode) -> None:
        if self._editor and hasattr(self, 'children'):
            command = HTMLCommandFactory.create_remove_child_command(self, child)
            self._editor.execute_command(command)
        else:
            if hasattr(self, 'children') and child in self.children:
                self.children.remove(child)

    def add_css_class_with_command(self, css_class: str) -> None:
        if self._editor and hasattr(self, 'css_classes'):
            command = HTMLCommandFactory.create_add_css_class_command(self, css_class)
            self._editor.execute_command(command)
        else:
            if hasattr(self, 'css_classes') and css_class not in self.css_classes:
                self.css_classes.append(css_class)

    def remove_css_class_with_command(self, css_class: str) -> None:
        if self._editor and hasattr(self, 'css_classes'):
            command = HTMLCommandFactory.create_remove_css_class_command(self, css_class)
            self._editor.execute_command(command)
        else:
            if hasattr(self, 'css_classes') and css_class in self.css_classes:
                self.css_classes.remove(css_class)