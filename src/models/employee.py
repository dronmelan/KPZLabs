from typing import List, Dict, Any
from ..interfaces.base_interfaces import Observable

class Employee(Observable):
    def __init__(self, employee_id: str, name: str, position: str, salary: float):
        if not all([employee_id, name, position]):
            raise ValueError("Employee ID, name, and position cannot be empty")
        if salary < 0:
            raise ValueError("Salary cannot be negative")

        self._id = employee_id
        self._name = name
        self._position = position
        self._salary = salary
        self._assigned_enclosures: List[str] = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> str:
        return self._position

    def assign_enclosure(self, enclosure_id: str) -> None:
        if enclosure_id not in self._assigned_enclosures:
            self._assigned_enclosures.append(enclosure_id)

    def get_status(self) -> Dict[str, Any]:
        return {
            "id": self._id,
            "name": self._name,
            "position": self._position,
            "salary": self._salary,
            "assigned_enclosures": self._assigned_enclosures.copy()
        }
    pass