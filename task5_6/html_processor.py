from typing import List
from light_html import LightNode, LightElementNode, LightTextNode
from flyweight import LightElementNodeFlyweight


class HTMLProcessor:

    @staticmethod
    def process_text_simple(lines: List[str]) -> LightElementNode:
        root = LightElementNode("div", "block", "with_closing_tag", ["content"])

        for i, line in enumerate(lines):
            line = line.rstrip('\n\r')

            if i == 0:
                h1 = LightElementNode("h1", "block", "with_closing_tag")
                h1.add_child(LightTextNode(line))
                root.add_child(h1)
            elif len(line) < 20:
                h2 = LightElementNode("h2", "block", "with_closing_tag")
                h2.add_child(LightTextNode(line))
                root.add_child(h2)
            elif line.startswith(' ') or line.startswith('\t'):
                pre = LightElementNode("pre", "block", "with_closing_tag")
                pre.add_child(LightTextNode(line))
                root.add_child(pre)
            else:
                p = LightElementNode("p", "block", "with_closing_tag")
                p.add_child(LightTextNode(line))
                root.add_child(p)

        return root

    @staticmethod
    def process_text_flyweight(lines: List[str]) -> LightElementNodeFlyweight:
        root = LightElementNodeFlyweight("div", "block", "with_closing_tag", ["content"])

        for i, line in enumerate(lines):
            line = line.rstrip('\n\r')

            if i == 0:
                h1 = LightElementNodeFlyweight("h1", "block", "with_closing_tag")
                h1.add_child(LightTextNode(line))
                root.add_child(h1)
            elif len(line) < 20:
                h2 = LightElementNodeFlyweight("h2", "block", "with_closing_tag")
                h2.add_child(LightTextNode(line))
                root.add_child(h2)
            elif line.startswith(' ') or line.startswith('\t'):  # Починається з пробілу - pre
                pre = LightElementNodeFlyweight("pre", "block", "with_closing_tag")
                pre.add_child(LightTextNode(line))
                root.add_child(pre)
            else:
                p = LightElementNodeFlyweight("p", "block", "with_closing_tag")
                p.add_child(LightTextNode(line))
                root.add_child(p)

        return root