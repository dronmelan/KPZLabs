from task2.Services.TechManufacturer import TechManufacturer


def main():
    print("🏭 === ФАБРИКА ВИРОБНИЦТВА ТЕХНІКИ ===")
    print("Використання патерну 'Абстрактна фабрика'\n")

    manufacturer = TechManufacturer()

    # Демонстрація 1: Виробництво всіх девайсів по брендах
    print("📱 === ПОВНА ЛІНІЙКА ПРОДУКТІВ ===\n")

    for brand in manufacturer.get_available_brands():
        print(f"🏷️  БРЕНД: {brand.upper()}")
        print("-" * 50)

        devices = manufacturer.produce_full_line(brand)
        for device in devices:
            device.display_info()

    # Демонстрація 2: Виробництво конкретних девайсів
    print("\n🎯 === ВИРОБНИЦТВО КОНКРЕТНИХ ДЕВАЙСІВ ===\n")

    specific_orders = [
        ("iprone", "laptop"),
        ("kiaomi", "smartphone"),
        ("balaxy", "ebook"),
        ("iprone", "smartphone"),
        ("kiaomi", "netbook")
    ]

    print("📋 Замовлення на виробництво:")
    for brand, device_type in specific_orders:
        print(f"   • {brand} {device_type}")
    print()

    for brand, device_type in specific_orders:
        print(f"🔧 Виробництво {device_type} бренду {brand}:")
        device = manufacturer.produce_device(brand, device_type)
        device.display_info()

    # Демонстрація 3: Порівняння девайсів одного типу
    print("⚖️  === ПОРІВНЯННЯ СМАРТФОНІВ РІЗНИХ БРЕНДІВ ===\n")

    smartphones = []
    for brand in manufacturer.get_available_brands():
        smartphone = manufacturer.produce_device(brand, "smartphone")
        smartphones.append(smartphone)

    # Сортування за ціною
    smartphones.sort(key=lambda x: x.price)

    print("📊 Смартфони відсортовані за ціною:")
    for smartphone in smartphones:
        smartphone.display_info()

    # Статистика
    print("📈 === СТАТИСТИКА ВИРОБНИЦТВА ===")
    total_devices = len(manufacturer.get_available_brands()) * 4  # 4 типи девайсів
    print(f"   • Всього брендів: {len(manufacturer.get_available_brands())}")
    print(f"   • Типів девайсів: 4 (Laptop, Netbook, EBook, Smartphone)")
    print(f"   • Всього моделей: {total_devices}")

    avg_price = sum(device.price for brand in manufacturer.get_available_brands()
                    for device in manufacturer.produce_full_line(brand)) / total_devices
    print(f"   • Середня ціна: ${avg_price:.2f}")


if __name__ == "__main__":
    main()