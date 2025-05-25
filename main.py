from src import (
    Zoo, InventoryService, FeedingService, ReportingService,
    Mammal, Bird, Reptile, Enclosure, Employee, Food,
    AnimalType, EnclosureType
)


def main():
    print("=== ZOO MANAGEMENT SYSTEM DEMO ===\n")

    # Create inventory service
    inventory = InventoryService()

    # Create zoo
    zoo = Zoo("Safari Adventure Park", inventory)

    # Create and add animals
    print("Creating animals...")
    lion = Mammal("Simba", "African Lion", 5, "golden")
    eagle = Bird("Eddie", "Bald Eagle", 3, True)
    snake = Reptile("Slither", "Python", 2, False)

    inventory.add_animal(lion)
    inventory.add_animal(eagle)
    inventory.add_animal(snake)

    # Create food
    meat = Food("Raw Meat", 30, [AnimalType.MAMMAL, AnimalType.REPTILE])
    fish = Food("Fresh Fish", 25, [AnimalType.BIRD])

    inventory.add_food(meat)
    inventory.add_food(fish)

    # Create enclosures
    print("Creating enclosures...")
    mammal_cage = Enclosure("M001", EnclosureType.CAGE, 3, 100.0)
    bird_aviary = Enclosure("B001", EnclosureType.AVIARY, 5, 50.0)

    inventory.add_enclosure(mammal_cage)
    inventory.add_enclosure(bird_aviary)

    # Create employees
    print("Adding employees...")
    keeper = Employee("E001", "John Smith", "Animal Keeper", 35000.0)
    vet = Employee("E002", "Dr. Jane Doe", "Veterinarian", 65000.0)

    inventory.add_employee(keeper)
    inventory.add_employee(vet)

    # Add animals to enclosures
    print("Placing animals in enclosures...")
    mammal_cage.add_animal(lion)
    bird_aviary.add_animal(eagle)

    # Test feeding
    print("\nFeeding animals...")
    feeding_service = FeedingService()
    lion_fed = feeding_service.feed_animal(lion, meat)
    eagle_fed = feeding_service.feed_animal(eagle, fish)

    print(f"Lion fed successfully: {lion_fed}")
    print(f"Eagle fed successfully: {eagle_fed}")

    # Generate reports
    print("\n" + "=" * 50)
    reporting = ReportingService(inventory)
    reporting.print_full_report()

    # Show zoo status
    print("\n" + "=" * 50)
    print("ZOO STATUS:")
    zoo_status = zoo.get_zoo_status()
    for key, value in zoo_status.items():
        print(f"{key}: {value}")

    # Test bird flying (specific behavior)
    print(f"\n{eagle.fly()}")

    # Show enclosure status
    print(f"\nMammal cage status: {mammal_cage.get_status()}")
    print(f"Bird aviary status: {bird_aviary.get_status()}")


if __name__ == "__main__":
    main()