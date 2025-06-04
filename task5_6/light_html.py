from abc import ABC, abstractmethod
from typing import List


class LightNode(ABC):

    @abstractmethod
    def get_outer_html(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
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


from light_html import LightElementNode, LightTextNode, LightNode
from command import HTMLEditorInvoker, HTMLCommandFactory, CommandMixin
from typing import List, Optional


class EnhancedLightElementNode(LightElementNode, CommandMixin):

    def __init__(self, tag_name: str, display_type: str = "block",
                 closing_type: str = "with_closing_tag", css_classes: List[str] = None,
                 editor: Optional[HTMLEditorInvoker] = None):
        LightElementNode.__init__(self, tag_name, display_type, closing_type, css_classes)
        CommandMixin.__init__(self)
        if editor:
            self.set_editor(editor)

    def set_editor_recursive(self, editor: HTMLEditorInvoker) -> None:
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

    def __init__(self, text: str, editor: Optional[HTMLEditorInvoker] = None):
        super().__init__(text)
        self._editor = editor

    def set_editor(self, editor: HTMLEditorInvoker) -> None:
        self._editor = editor

    def smart_change_text(self, new_text: str) -> None:
        if self._editor:
            command = HTMLCommandFactory.create_change_text_command(self, new_text)
            self._editor.execute_command(command)
        else:
            self.text = new_text


class HTMLDocumentBuilder:

    def __init__(self, editor: Optional[HTMLEditorInvoker] = None):
        self.editor = editor or HTMLEditorInvoker()
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

    def __init__(self, editor: HTMLEditorInvoker):
        self.editor = editor
        self.original_execute = editor.execute_command
        editor.execute_command = self._logged_execute

    def _logged_execute(self, command):
        print(f"[LOG] Executing: {command.get_description()}")
        result = self.original_execute(command)
        print(f"[LOG] Completed: {command.get_description()}")
        return result