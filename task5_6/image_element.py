from typing import List, Optional, Dict, Any
from light_html import LightElementNode
from image_strategy import ImageStrategyContext


class LightImageNode(LightElementNode):
    """
    Елемент зображення з підтримкою стратегій завантаження
    """

    def __init__(self, src: str, alt: str = "", css_classes: List[str] = None):
        super().__init__("img", "inline", "self_closing", css_classes)

        self.src = src
        self.alt = alt
        self._strategy_context = ImageStrategyContext()
        self._image_info: Optional[Dict[str, Any]] = None
        self._loaded = False

        # Автоматично завантажуємо зображення при створенні
        self.load_image()

    def load_image(self) -> bool:
        """
        Завантажує зображення використовуючи відповідну стратегію

        Returns:
            bool: True якщо завантаження успішне
        """
        self._image_info = self._strategy_context.load_image(self.src)
        self._loaded = self._image_info['success']

        if not self._loaded:
            print(f"[WARNING] Помилка завантаження зображення: {self._image_info['error']}")

        return self._loaded

    def get_outer_html(self) -> str:
        """Генерує HTML для img тега"""
        class_attr = f' class="{" ".join(self.css_classes)}"' if self.css_classes else ""
        alt_attr = f' alt="{self.alt}"' if self.alt else ""

        # Використовуємо завантажені дані або оригінальний src
        src_value = self.src
        if self._loaded and self._image_info:
            src_value = self._image_info['data']

        return f'<img src="{src_value}"{alt_attr}{class_attr} />'

    def get_size(self) -> int:
        """Розраховує розмір елемента в пам'яті"""
        base_size = 80  # Базовий розмір img елемента
        base_size += len(self.src.encode('utf-8'))
        base_size += len(self.alt.encode('utf-8'))

        # Додаємо розмір CSS класів
        for css_class in self.css_classes:
            base_size += len(css_class.encode('utf-8')) + 24

        # Додаємо розмір завантажених даних
        if self._loaded and self._image_info and self._image_info['size']:
            base_size += self._image_info['size']

        return base_size

    def is_loaded(self) -> bool:
        """Повертає стан завантаження зображення"""
        return self._loaded

    def get_image_info(self) -> Optional[Dict[str, Any]]:
        """Повертає інформацію про завантажене зображення"""
        return self._image_info.copy() if self._image_info else None

    def get_content_type(self) -> Optional[str]:
        """Повертає MIME тип зображення"""
        return self._image_info['content_type'] if self._loaded else None

    def get_image_size_bytes(self) -> int:
        """Повертає розмір зображення в байтах"""
        return self._image_info['size'] if self._loaded else 0

    def reload_image(self) -> bool:
        """
        Перезавантажує зображення

        Returns:
            bool: True якщо перезавантаження успішне
        """
        return self.load_image()

    def set_src(self, new_src: str) -> bool:
        """
        Змінює джерело зображення та перезавантажує його

        Args:
            new_src: Новий URL/шлях до зображення

        Returns:
            bool: True якщо завантаження успішне
        """
        self.src = new_src
        return self.load_image()

    def set_alt(self, new_alt: str) -> None:
        """Встановлює альтернативний текст"""
        self.alt = new_alt

    def add_image_strategy(self, strategy) -> None:
        """Додає нову стратегію завантаження"""
        self._strategy_context.add_strategy(strategy)

    def get_supported_strategies(self) -> List[str]:
        """Повертає список підтримуваних стратегій"""
        return self._strategy_context.get_supported_strategies()

    def accept(self, visitor):
        """Підтримка паттерну Відвідувач"""
        if hasattr(visitor, 'visit_image_node'):
            return visitor.visit_image_node(self)
        else:
            return visitor.visit_element_node(self)


class ImageGallery(LightElementNode):
    """
    Контейнер для галереї зображень
    """

    def __init__(self, css_classes: List[str] = None):
        super().__init__("div", "block", "with_closing_tag",
                         css_classes or ["image-gallery"])
        self._images: List[LightImageNode] = []

    def add_image(self, src: str, alt: str = "", css_classes: List[str] = None) -> LightImageNode:
        """Додає зображення до галереї"""
        image_classes = css_classes or ["gallery-image"]
        image = LightImageNode(src, alt, image_classes)

        self._images.append(image)
        self.add_child(image)

        return image

    def add_images_batch(self, image_data: List[Dict[str, str]]) -> List[LightImageNode]:
        """
        Додає кілька зображень одночасно

        Args:
            image_data: Список словників з ключами 'src', 'alt' (опціонально)
        """
        added_images = []

        for data in image_data:
            src = data['src']
            alt = data.get('alt', '')
            image = self.add_image(src, alt)
            added_images.append(image)

        return added_images

    def get_images_count(self) -> int:
        """Повертає кількість зображень у галереї"""
        return len(self._images)

    def get_loaded_images_count(self) -> int:
        """Повертає кількість успішно завантажених зображень"""
        return sum(1 for img in self._images if img.is_loaded())

    def get_failed_images_count(self) -> int:
        """Повертає кількість зображень, які не вдалося завантажити"""
        return sum(1 for img in self._images if not img.is_loaded())

    def get_total_size_bytes(self) -> int:
        """Повертає загальний розмір всіх зображень у байтах"""
        return sum(img.get_image_size_bytes() for img in self._images)

    def reload_all_images(self) -> Dict[str, int]:
        """
        Перезавантажує всі зображення в галереї

        Returns:
            Dict з результатами: {'success': count, 'failed': count}
        """
        success_count = 0
        failed_count = 0

        for image in self._images:
            if image.reload_image():
                success_count += 1
            else:
                failed_count += 1

        return {'success': success_count, 'failed': failed_count}

    def get_gallery_info(self) -> Dict[str, Any]:
        """Повертає детальну інформацію про галерею"""
        return {
            'total_images': self.get_images_count(),
            'loaded_images': self.get_loaded_images_count(),
            'failed_images': self.get_failed_images_count(),
            'total_size_bytes': self.get_total_size_bytes(),
            'supported_strategies': self._images[0].get_supported_strategies() if self._images else []
        }