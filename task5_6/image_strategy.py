from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os
import base64
from pathlib import Path


class ImageLoadingStrategy(ABC):
    """Абстрактна стратегія для завантаження зображень"""

    @abstractmethod
    def load_image(self, href: str) -> Dict[str, Any]:
        """
        Завантажує зображення за вказаним href

        Returns:
            Dict з ключами:
            - 'success': bool - чи успішно завантажено
            - 'data': str - дані зображення (base64 або URL)
            - 'content_type': str - MIME тип
            - 'size': int - розмір в байтах
            - 'error': str - опис помилки (якщо є)
        """
        pass

    @abstractmethod
    def can_handle(self, href: str) -> bool:
        """Перевіряє чи може ця стратегія обробити даний href"""
        pass


class FileSystemImageStrategy(ImageLoadingStrategy):
    """Стратегія завантаження зображень з файлової системи"""

    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
    MIME_TYPES = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml'
    }

    def can_handle(self, href: str) -> bool:
        """Перевіряє чи це локальний файл"""
        return not href.startswith(('http://', 'https://')) and \
            Path(href).suffix.lower() in self.SUPPORTED_EXTENSIONS

    def load_image(self, href: str) -> Dict[str, Any]:
        try:
            file_path = Path(href)

            if not file_path.exists():
                return {
                    'success': False,
                    'data': None,
                    'content_type': None,
                    'size': 0,
                    'error': f"Файл не знайдено: {href}"
                }

            if not file_path.is_file():
                return {
                    'success': False,
                    'data': None,
                    'content_type': None,
                    'size': 0,
                    'error': f"Шлях не є файлом: {href}"
                }

            extension = file_path.suffix.lower()
            content_type = self.MIME_TYPES.get(extension, 'application/octet-stream')

            # Читаємо файл
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Кодуємо в base64 для вбудовування в HTML
            base64_data = base64.b64encode(file_data).decode('utf-8')
            data_url = f"data:{content_type};base64,{base64_data}"

            return {
                'success': True,
                'data': data_url,
                'content_type': content_type,
                'size': len(file_data),
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'data': None,
                'content_type': None,
                'size': 0,
                'error': f"Помилка читання файлу: {str(e)}"
            }


class NetworkImageStrategy(ImageLoadingStrategy):
    """Стратегія завантаження зображень з мережі"""

    def can_handle(self, href: str) -> bool:
        """Перевіряє чи це URL"""
        return href.startswith(('http://', 'https://'))

    def load_image(self, href: str) -> Dict[str, Any]:
        try:
            # Симулюємо завантаження з мережі
            # В реальному додатку тут був би код для HTTP запиту

            # Перевіряємо чи URL виглядає валідно
            if not self._is_valid_image_url(href):
                return {
                    'success': False,
                    'data': None,
                    'content_type': None,
                    'size': 0,
                    'error': f"Неvalid URL для зображення: {href}"
                }

            # Симулюємо успішне завантаження
            # В реальності тут був би requests.get(href)
            return {
                'success': True,
                'data': href,  # Повертаємо URL як є для зовнішніх зображень
                'content_type': self._guess_content_type(href),
                'size': 0,  # Невідомий розмір для зовнішніх зображень
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'data': None,
                'content_type': None,
                'size': 0,
                'error': f"Помилка завантаження з мережі: {str(e)}"
            }

    def _is_valid_image_url(self, url: str) -> bool:
        """Перевіряє чи URL виглядає як зображення"""
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')
        return any(url.lower().endswith(ext) for ext in image_extensions) or \
            'image' in url.lower()

    def _guess_content_type(self, url: str) -> str:
        """Визначає MIME тип на основі URL"""
        url_lower = url.lower()
        if url_lower.endswith('.jpg') or url_lower.endswith('.jpeg'):
            return 'image/jpeg'
        elif url_lower.endswith('.png'):
            return 'image/png'
        elif url_lower.endswith('.gif'):
            return 'image/gif'
        elif url_lower.endswith('.webp'):
            return 'image/webp'
        elif url_lower.endswith('.svg'):
            return 'image/svg+xml'
        else:
            return 'image/jpeg'  # За замовчуванням


class ImageStrategyContext:
    """Контекст для вибору стратегії завантаження зображень"""

    def __init__(self):
        self._strategies = [
            FileSystemImageStrategy(),
            NetworkImageStrategy()
        ]

    def load_image(self, href: str) -> Dict[str, Any]:
        """Завантажує зображення, автоматично вибираючи стратегію"""

        for strategy in self._strategies:
            if strategy.can_handle(href):
                return strategy.load_image(href)

        return {
            'success': False,
            'data': None,
            'content_type': None,
            'size': 0,
            'error': f"Не знайдено підходящої стратегії для: {href}"
        }

    def add_strategy(self, strategy: ImageLoadingStrategy) -> None:
        """Додає нову стратегію"""
        self._strategies.append(strategy)

    def get_supported_strategies(self) -> list:
        """Повертає список підтримуваних стратегій"""
        return [type(strategy).__name__ for strategy in self._strategies]