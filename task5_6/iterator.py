from abc import ABC, abstractmethod
from typing import Iterator, List, Optional
from light_html import LightNode, LightElementNode, LightTextNode
from flyweight import LightElementNodeFlyweight


class TreeIterator(ABC):
    """Абстрактний клас для ітераторів дерева HTML"""

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self) -> LightNode:
        pass


class DepthFirstIterator(TreeIterator):
    """Ітератор для обходу дерева в глибину (DFS)"""

    def __init__(self, root: LightNode):
        self.root = root
        self.stack: List[LightNode] = []
        self.visited = set()
        self.current_index = 0

    def __iter__(self):
        # Скидаємо стан ітератора
        self.stack = [self.root] if self.root else []
        self.visited.clear()
        return self

    def __next__(self) -> LightNode:
        if not self.stack:
            raise StopIteration

        current = self.stack.pop()

        # Додаємо дочірні елементи в стек (у зворотному порядку для правильного обходу)
        if hasattr(current, 'children'):
            for child in reversed(current.children):
                self.stack.append(child)

        return current


class BreadthFirstIterator(TreeIterator):
    """Ітератор для обходу дерева в ширину (BFS)"""

    def __init__(self, root: LightNode):
        self.root = root
        self.queue: List[LightNode] = []

    def __iter__(self):
        # Скидаємо стан ітератора
        self.queue = [self.root] if self.root else []
        return self

    def __next__(self) -> LightNode:
        if not self.queue:
            raise StopIteration

        current = self.queue.pop(0)  # Беремо перший елемент (FIFO)

        # Додаємо дочірні елементи в кінець черги
        if hasattr(current, 'children'):
            self.queue.extend(current.children)

        return current


class ElementTypeIterator(TreeIterator):
    """Ітератор для обходу лише елементів певного типу"""

    def __init__(self, root: LightNode, element_type: type):
        self.root = root
        self.element_type = element_type
        self.all_nodes: List[LightNode] = []
        self.current_index = 0

    def __iter__(self):
        # Збираємо всі вузли потрібного типу
        self.all_nodes = []
        self.current_index = 0
        self._collect_nodes(self.root)
        return self

    def _collect_nodes(self, node: LightNode):
        """Рекурсивно збираємо всі вузли потрібного типу"""
        if isinstance(node, self.element_type):
            self.all_nodes.append(node)

        if hasattr(node, 'children'):
            for child in node.children:
                self._collect_nodes(child)

    def __next__(self) -> LightNode:
        if self.current_index >= len(self.all_nodes):
            raise StopIteration

        node = self.all_nodes[self.current_index]
        self.current_index += 1
        return node


class TagNameIterator(TreeIterator):
    """Ітератор для обходу елементів з певним тегом"""

    def __init__(self, root: LightNode, tag_name: str):
        self.root = root
        self.tag_name = tag_name.lower()
        self.all_nodes: List[LightNode] = []
        self.current_index = 0

    def __iter__(self):
        self.all_nodes = []
        self.current_index = 0
        self._collect_nodes(self.root)
        return self

    def _collect_nodes(self, node: LightNode):
        """Рекурсивно збираємо всі вузли з потрібним тегом"""
        # Перевіряємо чи є це елемент з потрібним тегом
        if hasattr(node, 'tag_name') and node.tag_name.lower() == self.tag_name:
            self.all_nodes.append(node)
        elif hasattr(node, 'flyweight') and hasattr(node.flyweight, 'tag_name') and \
                node.flyweight.tag_name.lower() == self.tag_name:
            self.all_nodes.append(node)

        if hasattr(node, 'children'):
            for child in node.children:
                self._collect_nodes(child)

    def __next__(self) -> LightNode:
        if self.current_index >= len(self.all_nodes):
            raise StopIteration

        node = self.all_nodes[self.current_index]
        self.current_index += 1
        return node


class IteratorFactory:
    """Фабрика для створення різних типів ітераторів"""

    @staticmethod
    def create_depth_first_iterator(root: LightNode) -> DepthFirstIterator:
        """Створює ітератор для обходу в глибину"""
        return DepthFirstIterator(root)

    @staticmethod
    def create_breadth_first_iterator(root: LightNode) -> BreadthFirstIterator:
        """Створює ітератор для обходу в ширину"""
        return BreadthFirstIterator(root)

    @staticmethod
    def create_element_type_iterator(root: LightNode, element_type: type) -> ElementTypeIterator:
        """Створює ітератор для елементів певного типу"""
        return ElementTypeIterator(root, element_type)

    @staticmethod
    def create_tag_name_iterator(root: LightNode, tag_name: str) -> TagNameIterator:
        """Створює ітератор для елементів з певним тегом"""
        return TagNameIterator(root, tag_name)