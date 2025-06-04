from abc import ABC, abstractmethod
from typing import List, Dict, Any
from light_html import LightNode, LightElementNode, LightTextNode
from flyweight import LightElementNodeFlyweight


class NodeVisitor(ABC):

    @abstractmethod
    def visit_element_node(self, node: LightElementNode) -> Any:
        pass

    @abstractmethod
    def visit_text_node(self, node: LightTextNode) -> Any:
        pass

    @abstractmethod
    def visit_flyweight_element_node(self, node: LightElementNodeFlyweight) -> Any:
        pass


class HTMLStatisticsVisitor(NodeVisitor):

    def __init__(self):
        self.reset()

    def reset(self):
        self.elements_count = 0
        self.text_nodes_count = 0
        self.flyweight_elements_count = 0
        self.total_text_length = 0
        self.tag_counts: Dict[str, int] = {}
        self.css_classes: set = set()
        self.max_depth = 0
        self.current_depth = 0

    def visit_element_node(self, node: LightElementNode) -> None:
        self.elements_count += 1
        self._process_element(node.tag_name, node.css_classes)
        self._visit_children(node.children)

    def visit_text_node(self, node: LightTextNode) -> None:
        self.text_nodes_count += 1
        self.total_text_length += len(node.text)

    def visit_flyweight_element_node(self, node: LightElementNodeFlyweight) -> None:
        self.flyweight_elements_count += 1
        self._process_element(node.flyweight.tag_name, node.css_classes)
        self._visit_children(node.children)

    def _process_element(self, tag_name: str, css_classes: List[str]):
        self.tag_counts[tag_name] = self.tag_counts.get(tag_name, 0) + 1
        self.css_classes.update(css_classes)

    def _visit_children(self, children: List[LightNode]):
        if children:
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)

            for child in children:
                child.accept(self)

            self.current_depth -= 1

    def get_report(self) -> str:
        report = []
        report.append("HTML СТАТИСТИКА:")
        report.append(f"  Звичайних елементів: {self.elements_count}")
        report.append(f"  Легковагових елементів: {self.flyweight_elements_count}")
        report.append(f"  Текстових вузлів: {self.text_nodes_count}")
        report.append(f"  Загальна довжина тексту: {self.total_text_length} символів")
        report.append(f"  Максимальна глибина: {self.max_depth}")

        if self.tag_counts:
            report.append("  Розподіл тегів:")
            for tag, count in sorted(self.tag_counts.items()):
                report.append(f"    {tag}: {count}")

        if self.css_classes:
            report.append(f"  Унікальних CSS класів: {len(self.css_classes)}")
            report.append(f"    {', '.join(sorted(self.css_classes))}")

        return '\n'.join(report)


class HTMLValidationVisitor(NodeVisitor):

    def __init__(self):
        self.reset()

    def reset(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.path_stack: List[str] = []

    def visit_element_node(self, node: LightElementNode) -> None:
        self._validate_element(node.tag_name, node.css_classes, node.children)
        self._visit_children_with_path(node.tag_name, node.children)

    def visit_text_node(self, node: LightTextNode) -> None:
        self._validate_text(node.text)

    def visit_flyweight_element_node(self, node: LightElementNodeFlyweight) -> None:
        self._validate_element(node.flyweight.tag_name, node.css_classes, node.children)
        self._visit_children_with_path(node.flyweight.tag_name, node.children)

    def _validate_element(self, tag_name: str, css_classes: List[str], children: List[LightNode]):
        current_path = ' > '.join(self.path_stack + [tag_name])

        if tag_name.lower() in ['script', 'iframe', 'object', 'embed']:
            self.warnings.append(f"Потенційно небезпечний тег '{tag_name}' в {current_path}")

        if tag_name == 'table':
            self._validate_table_structure(children, current_path)

        for css_class in css_classes:
            if not css_class.replace('-', '').replace('_', '').isalnum():
                self.warnings.append(f"Підозрілий CSS клас '{css_class}' в {current_path}")

    def _validate_text(self, text: str):
        if len(text.strip()) == 0 and len(text) > 10:
            self.warnings.append("Знайдено текстовий вузол з великою кількістю пробілів")

        if '<' in text or '>' in text:
            self.warnings.append("Текстовий вузол містить HTML-подібні символи")

    def _validate_table_structure(self, children: List[LightNode], path: str):
        has_thead = any(self._get_tag_name(child) == 'thead' for child in children)
        has_tbody = any(self._get_tag_name(child) == 'tbody' for child in children)

        if not has_thead:
            self.warnings.append(f"Таблиця без thead в {path}")
        if not has_tbody:
            self.warnings.append(f"Таблиця без tbody в {path}")

    def _get_tag_name(self, node: LightNode) -> str:
        if isinstance(node, LightElementNode):
            return node.tag_name
        elif isinstance(node, LightElementNodeFlyweight):
            return node.flyweight.tag_name
        return ""

    def _visit_children_with_path(self, tag_name: str, children: List[LightNode]):
        self.path_stack.append(tag_name)

        for child in children:
            child.accept(self)

        self.path_stack.pop()

    def get_report(self) -> str:
        report = []
        report.append("РЕЗУЛЬТАТИ ВАЛІДАЦІЇ:")

        if not self.errors and not self.warnings:
            report.append("  ✓ Помилок не знайдено")
        else:
            if self.errors:
                report.append(f"  ПОМИЛКИ ({len(self.errors)}):")
                for error in self.errors:
                    report.append(f"    ✗ {error}")

            if self.warnings:
                report.append(f"  ПОПЕРЕДЖЕННЯ ({len(self.warnings)}):")
                for warning in self.warnings:
                    report.append(f"    ⚠ {warning}")

        return '\n'.join(report)


class HTMLTransformVisitor(NodeVisitor):

    def __init__(self, transformations: Dict[str, Any] = None):
        self.transformations = transformations or {}
        self.changes_made = 0

    def visit_element_node(self, node: LightElementNode) -> None:
        self._transform_element(node)
        self._visit_children(node.children)

    def visit_text_node(self, node: LightTextNode) -> None:
        self._transform_text(node)

    def visit_flyweight_element_node(self, node: LightElementNodeFlyweight) -> None:
        if 'add_css_class' in self.transformations:
            css_class = self.transformations['add_css_class']
            if css_class not in node.css_classes:
                node.css_classes.append(css_class)
                self.changes_made += 1

        self._visit_children(node.children)

    def _transform_element(self, node: LightElementNode):
        if 'add_css_class' in self.transformations:
            css_class = self.transformations['add_css_class']
            if css_class not in node.css_classes:
                node.css_classes.append(css_class)
                self.changes_made += 1

        if 'set_display_type' in self.transformations:
            new_display = self.transformations['set_display_type']
            if node.display_type != new_display:
                node.display_type = new_display
                self.changes_made += 1

    def _transform_text(self, node: LightTextNode):
        if 'uppercase_text' in self.transformations and self.transformations['uppercase_text']:
            if node.text != node.text.upper():
                node.text = node.text.upper()
                self.changes_made += 1

        if 'trim_whitespace' in self.transformations and self.transformations['trim_whitespace']:
            original_text = node.text
            node.text = node.text.strip()
            if original_text != node.text:
                self.changes_made += 1

    def _visit_children(self, children: List[LightNode]):
        for child in children:
            child.accept(self)

    def get_changes_count(self) -> int:
        return self.changes_made


class HTMLSearchVisitor(NodeVisitor):

    def __init__(self, search_criteria: Dict[str, Any]):
        self.search_criteria = search_criteria
        self.found_nodes: List[LightNode] = []

    def visit_element_node(self, node: LightElementNode) -> None:
        if self._matches_criteria(node.tag_name, node.css_classes, "element"):
            self.found_nodes.append(node)

        self._visit_children(node.children)

    def visit_text_node(self, node: LightTextNode) -> None:
        if self._matches_text_criteria(node.text):
            self.found_nodes.append(node)

    def visit_flyweight_element_node(self, node: LightElementNodeFlyweight) -> None:
        if self._matches_criteria(node.flyweight.tag_name, node.css_classes, "flyweight"):
            self.found_nodes.append(node)

        self._visit_children(node.children)

    def _matches_criteria(self, tag_name: str, css_classes: List[str], node_type: str) -> bool:
        if 'tag_name' in self.search_criteria:
            if tag_name != self.search_criteria['tag_name']:
                return False

        if 'css_class' in self.search_criteria:
            if self.search_criteria['css_class'] not in css_classes:
                return False

        if 'node_type' in self.search_criteria:
            if node_type != self.search_criteria['node_type']:
                return False

        return True

    def _matches_text_criteria(self, text: str) -> bool:
        if 'text_contains' in self.search_criteria:
            if self.search_criteria['text_contains'].lower() not in text.lower():
                return False

        if 'text_min_length' in self.search_criteria:
            if len(text) < self.search_criteria['text_min_length']:
                return False

        return True

    def _visit_children(self, children: List[LightNode]):
        for child in children:
            child.accept(self)

    def get_results(self) -> List[LightNode]:
        return self.found_nodes.copy()