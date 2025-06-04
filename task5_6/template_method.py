from abc import ABC, abstractmethod
from typing import List, Optional
from light_html import LightNode, LightElementNode, LightTextNode
from flyweight import LightElementNodeFlyweight


class HTMLDocumentTemplate(ABC):


    def create_document(self, content: List[str], title: str = "Document") -> LightNode:

        print(f"[TEMPLATE] Створення документу: {title}")

        root = self._create_root()

        if self._should_add_metadata():
            self._add_metadata(root, title)

        container = self._create_content_container(root)

        self._process_title(container, title)

        self._process_content(container, content)

        if self._should_add_footer():
            self._add_footer(root)

        self._post_process(root)

        print(f"[TEMPLATE] Документ створено успішно")
        return root

    @abstractmethod
    def _create_root(self) -> LightNode:
        pass

    @abstractmethod
    def _create_content_container(self, root: LightNode) -> LightNode:
        pass

    @abstractmethod
    def _process_title(self, container: LightNode, title: str) -> None:
        pass

    @abstractmethod
    def _process_content(self, container: LightNode, content: List[str]) -> None:
        pass

    def _should_add_metadata(self) -> bool:
        return False

    def _add_metadata(self, root: LightNode, title: str) -> None:
        pass

    def _should_add_footer(self) -> bool:
        return False

    def _add_footer(self, root: LightNode) -> None:
        pass

    def _post_process(self, root: LightNode) -> None:
        pass


class ArticleDocumentTemplate(HTMLDocumentTemplate):

    def _create_root(self) -> LightNode:
        return LightElementNode("article", "block", "with_closing_tag", ["article-document"])

    def _create_content_container(self, root: LightNode) -> LightNode:
        container = LightElementNode("div", "block", "with_closing_tag", ["article-content"])
        root.add_child(container)
        return container

    def _process_title(self, container: LightNode, title: str) -> None:
        h1 = LightElementNode("h1", "block", "with_closing_tag", ["article-title"])
        h1.add_child(LightTextNode(title))
        container.add_child(h1)

    def _process_content(self, container: LightNode, content: List[str]) -> None:
        for line in content:
            line = line.strip()
            if not line:
                continue

            if len(line) < 30 and not line.startswith(' '):
                # Короткі рядки - підзаголовки
                h2 = LightElementNode("h2", "block", "with_closing_tag", ["article-subtitle"])
                h2.add_child(LightTextNode(line))
                container.add_child(h2)
            elif line.startswith(' ') or line.startswith('\t'):
                # Код або цитати
                pre = LightElementNode("pre", "block", "with_closing_tag", ["code-block"])
                pre.add_child(LightTextNode(line.strip()))
                container.add_child(pre)
            else:
                # Звичайні параграфи
                p = LightElementNode("p", "block", "with_closing_tag", ["article-paragraph"])
                p.add_child(LightTextNode(line))
                container.add_child(p)

    def _should_add_metadata(self) -> bool:
        return True

    def _add_metadata(self, root: LightNode, title: str) -> None:
        header = LightElementNode("header", "block", "with_closing_tag", ["article-header"])

        time_elem = LightElementNode("time", "inline", "with_closing_tag", ["publish-date"])
        time_elem.add_child(LightTextNode("2024-01-01"))
        header.add_child(time_elem)

        author = LightElementNode("span", "inline", "with_closing_tag", ["author"])
        author.add_child(LightTextNode("Автор статті"))
        header.add_child(author)

        root.add_child(header)

    def _should_add_footer(self) -> bool:
        return True

    def _add_footer(self, root: LightNode) -> None:
        footer = LightElementNode("footer", "block", "with_closing_tag", ["article-footer"])
        footer.add_child(LightTextNode("© 2024 Всі права захищені"))
        root.add_child(footer)


class ReportDocumentTemplate(HTMLDocumentTemplate):


    def _create_root(self) -> LightNode:
        return LightElementNode("div", "block", "with_closing_tag", ["report-document"])

    def _create_content_container(self, root: LightNode) -> LightNode:
        main = LightElementNode("main", "block", "with_closing_tag", ["report-main"])
        root.add_child(main)
        return main

    def _process_title(self, container: LightNode, title: str) -> None:
        header = LightElementNode("header", "block", "with_closing_tag", ["report-header"])
        h1 = LightElementNode("h1", "block", "with_closing_tag", ["report-title"])
        h1.add_child(LightTextNode(f"ЗВІТ: {title}"))
        header.add_child(h1)
        container.add_child(header)

    def _process_content(self, container: LightNode, content: List[str]) -> None:
        section = LightElementNode("section", "block", "with_closing_tag", ["report-section"])

        current_list = None

        for line in content:
            line = line.strip()
            if not line:
                continue

            if line.startswith('•') or line.startswith('-'):
                if current_list is None:
                    current_list = LightElementNode("ul", "block", "with_closing_tag", ["report-list"])
                    section.add_child(current_list)

                li = LightElementNode("li", "block", "with_closing_tag")
                li.add_child(LightTextNode(line[1:].strip()))
                current_list.add_child(li)
            else:
                current_list = None

                if len(line) < 40 and line.isupper():
                    # Заголовки секцій
                    h2 = LightElementNode("h2", "block", "with_closing_tag", ["section-title"])
                    h2.add_child(LightTextNode(line))
                    section.add_child(h2)
                else:
                    p = LightElementNode("p", "block", "with_closing_tag", ["report-text"])
                    p.add_child(LightTextNode(line))
                    section.add_child(p)

        container.add_child(section)

    def _should_add_metadata(self) -> bool:
        return True

    def _add_metadata(self, root: LightNode, title: str) -> None:
        metadata = LightElementNode("div", "block", "with_closing_tag", ["report-metadata"])


        report_id = LightElementNode("span", "inline", "with_closing_tag", ["report-id"])
        report_id.add_child(LightTextNode("ID: RPT-001"))
        metadata.add_child(report_id)


        date = LightElementNode("span", "inline", "with_closing_tag", ["report-date"])
        date.add_child(LightTextNode("Дата: 2024-01-01"))
        metadata.add_child(date)

        root.add_child(metadata)


class FlyweightDocumentTemplate(HTMLDocumentTemplate):

    def _create_root(self) -> LightNode:
        return LightElementNodeFlyweight("div", "block", "with_closing_tag", ["flyweight-document"])

    def _create_content_container(self, root: LightNode) -> LightNode:
        container = LightElementNodeFlyweight("div", "block", "with_closing_tag", ["content"])
        root.add_child(container)
        return container

    def _process_title(self, container: LightNode, title: str) -> None:
        h1 = LightElementNodeFlyweight("h1", "block", "with_closing_tag", ["main-title"])
        h1.add_child(LightTextNode(title))
        container.add_child(h1)

    def _process_content(self, container: LightNode, content: List[str]) -> None:
        for i, line in enumerate(content):
            line = line.strip()
            if not line:
                continue

            if i == 0:
                continue
            elif len(line) < 20:
                h2 = LightElementNodeFlyweight("h2", "block", "with_closing_tag")
                h2.add_child(LightTextNode(line))
                container.add_child(h2)
            elif line.startswith(' ') or line.startswith('\t'):
                pre = LightElementNodeFlyweight("pre", "block", "with_closing_tag")
                pre.add_child(LightTextNode(line))
                container.add_child(pre)
            else:
                p = LightElementNodeFlyweight("p", "block", "with_closing_tag")
                p.add_child(LightTextNode(line))
                container.add_child(p)

    def _post_process(self, root: LightNode) -> None:
        from flyweight import ElementFlyweightFactory
        print(f"[FLYWEIGHT] Створено {ElementFlyweightFactory.get_flyweights_count()} flyweight об'єктів")


class DocumentFactory:


    @staticmethod
    def create_article_processor() -> HTMLDocumentTemplate:
        return ArticleDocumentTemplate()

    @staticmethod
    def create_report_processor() -> HTMLDocumentTemplate:
        return ReportDocumentTemplate()

    @staticmethod
    def create_flyweight_processor() -> HTMLDocumentTemplate:
        return FlyweightDocumentTemplate()


def demonstrate_template_method():


    sample_content = [
        "Програмування в Python",
        "",
        "ВСТУП",
        "Python - це високорівнева мова програмування.",
        "• Простий синтаксис",
        "• Велика кількість бібліотек",
        "• Активна спільнота",
        "",
        "ОСНОВИ",
        "    print('Hello, World!')",
        "    x = 10",
        "Змінні в Python створюються динамічно.",
        "",
        "ВИСНОВКИ",
        "Python підходить для різних задач."
    ]

    print("=== ДЕМОНСТРАЦІЯ TEMPLATE METHOD ПАТТЕРНУ ===\n")

    print("1. СТВОРЕННЯ СТАТТІ:")
    article_processor = DocumentFactory.create_article_processor()
    article = article_processor.create_document(sample_content, "Основи Python")
    print(f"Розмір статті: {article.get_size()} байт")
    print("HTML preview:")
    html = article.get_outer_html()
    print(html[:200] + "..." if len(html) > 200 else html)
    print()

    print("2. СТВОРЕННЯ ЗВІТУ:")
    report_processor = DocumentFactory.create_report_processor()
    report = report_processor.create_document(sample_content, "Аналіз мови Python")
    print(f"Розмір звіту: {report.get_size()} байт")
    print("HTML preview:")
    html = report.get_outer_html()
    print(html[:200] + "..." if len(html) > 200 else html)
    print()

    print("3. СТВОРЕННЯ З FLYWEIGHT:")
    flyweight_processor = DocumentFactory.create_flyweight_processor()
    flyweight_doc = flyweight_processor.create_document(sample_content, "Python Guide")
    print(f"Розмір документу: {flyweight_doc.get_size()} байт")
    print("HTML preview:")
    html = flyweight_doc.get_outer_html()
    print(html[:200] + "..." if len(html) > 200 else html)
    print()

    print("4. ПОРІВНЯННЯ РОЗМІРІВ:")
    print(f"Стаття: {article.get_size()} байт")
    print(f"Звіт: {report.get_size()} байт")
    print(f"Flyweight: {flyweight_doc.get_size()} байт")


if __name__ == "__main__":
    demonstrate_template_method()