# Lab 1 - Code Principles Demonstration


## SOLID Principles

**S - Single Responsibility Principle (SRP)**
- Each class in the project has a single responsibility. For example,
  - [`animal.py`](./src/models/animal.py): Handles only animal-related data and behaviors.
  - [`feeding_service.py`](./src/services/feeding_service.py): Manages feeding logic.

**O - Open/Closed Principle (OCP)**
- Code is open for extension but closed for modification. You can add new animal types by extending base interfaces without changing existing code.
  - [`base_interfaces.py`](./src/interfaces/base_interfaces.py): Abstract interfaces support this.

**L - Liskov Substitution Principle (LSP)**
- Subclasses can replace their base classes without affecting functionality.
  - Any class implementing `Feedable` or `Reportable` in [`base_interfaces.py`](./src/interfaces/base_interfaces.py) can be used interchangeably.

**I - Interface Segregation Principle (ISP)**
- Interfaces are small and specific. For example, `Feedable` and `Reportable` are separate.
  - [`base_interfaces.py`](./src/interfaces/base_interfaces.py): Defines multiple focused interfaces.

**D - Dependency Inversion Principle (DIP)**
- High-level modules depend on abstractions.
  - Services rely on interfaces like `Feedable` rather than concrete implementations.

## DRY - Don't Repeat Yourself
- Shared logic is abstracted into services and utility classes.
  - [`feeding_service.py`](./src/services/feeding_service.py): Centralizes animal feeding logic.

## KISS - Keep It Simple, Stupid
- Functions and classes are kept small and focused.
  - [`inventory_service.py`](./src/services/inventory_service.py): Simple inventory tracking logic.

## YAGNI - You Aren’t Gonna Need It
- Code avoids unnecessary complexity or unused features.
- Focus is on minimal functionality required for a zoo management system.

## Enumerations
- Enumerations are used to ensure consistent type usage.
  - [`enums.py`](./src/utils/enums.py): Defines enums like `AnimalType`, `FoodType`, etc.

## UML Diagram
- See the generated UML diagram: [uml_diagram.png](./uml_diagram.png)