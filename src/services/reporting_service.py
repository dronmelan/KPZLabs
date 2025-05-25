from .inventory_service import InventoryService
from ..utils.enums import AnimalType

class ReportingService:
    def __init__(self, inventory: InventoryService):
        self._inventory = inventory

    def print_animals_report(self) -> None:
        print("=== ANIMALS REPORT ===")
        print(f"Total animals: {self._inventory.get_animal_count()}")

        for animal_type in AnimalType:
            animals = self._inventory.get_animals_by_type(animal_type)
            print(f"\n{animal_type.value.upper()}S ({len(animals)}):")
            for animal in animals:
                status = animal.get_status()
                print(
                    f"  - {status['name']} ({status['species']}) - Age: {status['age']}, Hunger: {status['hunger_level']}")

    def print_employees_report(self) -> None:
        print("\n=== EMPLOYEES REPORT ===")
        print(f"Total employees: {self._inventory.get_employee_count()}")
        # Implementation would iterate through employees

    def print_enclosures_report(self) -> None:
        print("\n=== ENCLOSURES REPORT ===")
        print(f"Total enclosures: {self._inventory.get_enclosure_count()}")
        # Implementation would iterate through enclosures

    def print_full_report(self) -> None:
        self.print_animals_report()
        self.print_employees_report()
        self.print_enclosures_report()