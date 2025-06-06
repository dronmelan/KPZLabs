import os
from pathlib import Path
from image_element import LightImageNode, ImageGallery
from image_strategy import FileSystemImageStrategy, NetworkImageStrategy


def create_test_image_file():
    """Створює тестовий файл зображення для демонстрації"""
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)

    # Створюємо простий SVG файл для тестування
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" fill="#4CAF50"/>
  <text x="50" y="50" text-anchor="middle" dy=".3em" fill="white" font-family="Arial" font-size="12">
    Тест SVG
  </text>
</svg>'''

    test_file = test_dir / "test_image.svg"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    return str(test_file)


def demonstrate_image_strategy():
    """Демонструє роботу паттерну Стратегія для завантаження зображень"""

    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ: ЕЛЕМЕНТ IMAGE З ПАТТЕРНОМ СТРАТЕГІЯ")
    print("=" * 60)

    # 1. Створюємо тестовий файл
    print("1. ПІДГОТОВКА ТЕСТОВИХ ДАНИХ")
    test_image_path = create_test_image_file()
    print(f"   ✓ Створено тестовий файл: {test_image_path}")

    # 2. Тестуємо завантаження з файлової системи
    print("\n2. ТЕСТУВАННЯ СТРАТЕГІЇ ФАЙЛОВОЇ СИСТЕМИ")

    # Успішне завантаження
    local_image = LightImageNode(test_image_path, "Тестове SVG зображення", ["local-image"])
    print(f"   Джерело: {local_image.src}")
    print(f"   Завантажено: {'✓' if local_image.is_loaded() else '✗'}")

    if local_image.is_loaded():
        info = local_image.get_image_info()
        print(f"   MIME тип: {info['content_type']}")
        print(f"   Розмір: {info['size']} байт")
        print(f"   Стратегія: FileSystemImageStrategy")

    # Неіснуючий файл
    missing_image = LightImageNode("nonexistent/image.jpg", "Неіснуюче зображення")
    print(f"\n   Тест неіснуючого файлу: {'✗' if not missing_image.is_loaded() else '✓'}")
    if not missing_image.is_loaded():
        error_info = missing_image.get_image_info()
        print(f"   Помилка: {error_info['error']}")

    # 3. Тестуємо завантаження з мережі
    print("\n3. ТЕСТУВАННЯ МЕРЕЖЕВОЇ СТРАТЕГІЇ")

    network_urls = [
        "https://example.com/image.jpg",
        "https://picsum.photos/200/300.jpg",
        "https://via.placeholder.com/150x150.png"
    ]

    for url in network_urls:
        network_image = LightImageNode(url, f"Зображення з {url}")
        print(f"   URL: {url}")
        print(f"   Завантажено: {'✓' if network_image.is_loaded() else '✗'}")

        if network_image.is_loaded():
            info = network_image.get_image_info()
            print(f"   MIME тип: {info['content_type']}")
            print(f"   Стратегія: NetworkImageStrategy")
        print()

    # 4. Демонстрація галереї зображень
    print("4. ДЕМОНСТРАЦІЯ ГАЛЕРЕЇ ЗОБРАЖЕНЬ")

    gallery = ImageGallery(["main-gallery", "responsive"])

    # Додаємо зображення пакетом
    image_data = [
        {"src": test_image_path, "alt": "Локальне SVG"},
        {"src": "https://picsum.photos/200/200.jpg", "alt": "Випадкове зображення"},
        {"src": "nonexistent.png", "alt": "Неіснуюче зображення"},
        {"src": "https://via.placeholder.com/100x100.gif", "alt": "Placeholder GIF"}
    ]

    added_images = gallery.add_images_batch(image_data)

    # Виводимо статистику галереї
    gallery_info = gallery.get_gallery_info()
    print(f"   Загальна кількість зображень: {gallery_info['total_images']}")
    print(f"   Успішно завантажених: {gallery_info['loaded_images']}")
    print(f"   Помилок завантаження: {gallery_info['failed_images']}")
    print(f"   Загальний розмір: {gallery_info['total_size_bytes']} байт")
    print(f"   Підтримувані стратегії: {', '.join(gallery_info['supported_strategies'])}")

    # 5. Генерація HTML
    print("\n5. ЗГЕНЕРОВАНИЙ HTML")

    print("\n   Окремі зображення:")
    print(f"   {local_image.get_outer_html()}")

    print(f"\n   Перші 500 символів галереї:")
    gallery_html = gallery.get_outer_html()
    print(f"   {gallery_html[:500]}")
    if len(gallery_html) > 500:
        print("   ...")

    # 6. Тестування динамічної зміни джерела
    print("\n6. ТЕСТУВАННЯ ДИНАМІЧНОЇ ЗМІНИ ДЖЕРЕЛА")

    dynamic_image = LightImageNode("initial_nonexistent.jpg", "Динамічне зображення")
    print(f"   Початковий стан: {'✓' if dynamic_image.is_loaded() else '✗'}")

    # Змінюємо на валідний файл
    success = dynamic_image.set_src(test_image_path)
    print(f"   Після зміни на локальний файл: {'✓' if success else '✗'}")

    # Змінюємо на мережевий URL
    success = dynamic_image.set_src("https://picsum.photos/50/50.jpg")
    print(f"   Після зміни на мережевий URL: {'✓' if success else '✗'}")

    # 7. Розміри в пам'яті
    print("\n7. АНАЛІЗ ПАМ'ЯТІ")

    print(f"   Локальне зображення: {local_image.get_size()} байт")
    print(f"   Мережеве зображення: {network_image.get_size()} байт")
    print(f"   Вся галерея: {gallery.get_size()} байт")

    # 8. Очищення тестових файлів
    print("\n8. ОЧИЩЕННЯ")
    try:
        os.remove(test_image_path)
        os.rmdir("test_images")
        print("   ✓ Тестові файли видалено")
    except:
        print("   ⚠ Не вдалося видалити тестові файли")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА")
    print("=" * 60)


def demonstrate_strategy_extensibility():
    """Демонструє розширюваність стратегій"""

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦІЯ: РОЗШИРЮВАНІСТЬ СТРАТЕГІЙ")
    print("=" * 60)

    from image_strategy import ImageLoadingStrategy

    # Створюємо власну стратегію
    class Base64ImageStrategy(ImageLoadingStrategy):
        """Стратегія для завантаження зображень з base64 рядків"""

        def can_handle(self, href: str) -> bool:
            return href.startswith('data:image/')

        def load_image(self, href: str) -> dict:
            try:
                # Перевіряємо формат data:image/type;base64,data
                if not href.startswith('data:image/') or ';base64,' not in href:
                    return {
                        'success': False,
                        'data': None,
                        'content_type': None,
                        'size': 0,
                        'error': 'Невірний формат Base64 зображення'
                    }

                # Витягуємо MIME тип та дані
                header, data = href.split(';base64,', 1)
                content_type = header.replace('data:', '')

                # Оцінюємо розмір (приблизно)
                estimated_size = len(data) * 3 // 4  # Base64 збільшує розмір на ~33%

                return {
                    'success': True,
                    'data': href,  # Повертаємо as is для data URLs
                    'content_type': content_type,
                    'size': estimated_size,
                    'error': None
                }

            except Exception as e:
                return {
                    'success': False,
                    'data': None,
                    'content_type': None,
                    'size': 0,
                    'error': f'Помилка обробки Base64: {str(e)}'
                }

    # Тестуємо нову стратегію
    base64_data = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzIxOTZGMyIvPgogIDx0ZXh0IHg9IjUwIiB5PSI1MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZpbGw9IndoaXRlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTAiPgogICAgQmFzZTY0CiAgPC90ZXh0Pgo8L3N2Zz4K"

    image_with_base64 = LightImageNode(base64_data, "Base64 зображення")

    # Додаємо нову стратегію
    image_with_base64.add_image_strategy(Base64ImageStrategy())

    # Перезавантажуємо з новою стратегією
    image_with_base64.reload_image()

    print("   Створено власну стратегію: Base64ImageStrategy")
    print(f"   Base64 зображення завантажено: {'✓' if image_with_base64.is_loaded() else '✗'}")

    if image_with_base64.is_loaded():
        info = image_with_base64.get_image_info()
        print(f"   MIME тип: {info['content_type']}")
        print(f"   Оцінений розмір: {info['size']} байт")

    strategies = image_with_base64.get_supported_strategies()
    print(f"   Підтримувані стратегії: {', '.join(strategies)}")

    print(f"\n   Згенерований HTML:")
    print(f"   {image_with_base64.get_outer_html()[:100]}...")


if __name__ == "__main__":
    create_test_image_file()
    demonstrate_image_strategy()
    demonstrate_strategy_extensibility()

    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦІЯ ПАТЕРНУ СТРАТЕГІЯ ЗАВЕРШЕНА")
    print("=" * 70)