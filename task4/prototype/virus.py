from typing import List
import copy
import uuid
from typing import Optional

from task4.prototype.base_prototype import Prototype


class Virus(Prototype):

    def __init__(self, weight: float, age: int, name: str, species: str,
                 parent: Optional['Virus'] = None):

        self._id = str(uuid.uuid4())[:8]  # Унікальний ідентифікатор
        self.weight = weight
        self.age = age
        self.name = name
        self.species = species
        self.children: List['Virus'] = []
        self.parent = parent
        self._generation = 1 if parent is None else parent._generation + 1

    def add_child(self, child: 'Virus') -> None:
        child.parent = self
        child._generation = self._generation + 1
        self.children.append(child)
        print(f"Added child {child.name} to {self.name}")

    def remove_child(self, child: 'Virus') -> bool:
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            print(f"Removed child {child.name} from {self.name}")
            return True
        return False

    def clone(self, deep: bool = True) -> 'Virus':

        print(f"Cloning virus {self.name} (ID: {self._id})")

        if deep:
            cloned_virus = copy.deepcopy(self)
            cloned_virus._update_ids_recursively()
        else:
            cloned_virus = Virus(
                weight=self.weight,
                age=self.age,
                name=f"{self.name}_clone",
                species=self.species
            )

        print(f"Cloned virus created: {cloned_virus.name} (ID: {cloned_virus._id})")
        return cloned_virus

    def _update_ids_recursively(self) -> None:
        old_id = self._id
        self._id = str(uuid.uuid4())[:8]
        self.name = f"{self.name}_clone"

        print(f"Updated ID from {old_id} to {self._id} for {self.name}")

        for child in self.children:
            child.parent = self
            child._update_ids_recursively()

    def mutate(self, weight_change: float = 0, age_change: int = 0) -> None:
        old_weight = self.weight
        old_age = self.age

        self.weight += weight_change
        self.age += age_change

        self.weight = max(0.1, self.weight)
        self.age = max(0, self.age)

        print(f"Virus {self.name} mutated: weight {old_weight} -> {self.weight}, "
              f"age {old_age} -> {self.age}")

    def get_family_tree(self, level: int = 0) -> str:
        indent = "  " * level
        tree = f"{indent}{self.name} (Gen {self._generation}, ID: {self._id}, "
        tree += f"Weight: {self.weight}, Age: {self.age}, Species: {self.species})\n"

        for child in self.children:
            tree += child.get_family_tree(level + 1)

        return tree

    def count_descendants(self) -> int:
        count = len(self.children)
        for child in self.children:
            count += child.count_descendants()
        return count

    def get_generation(self) -> int:
        return self._generation

    def get_all_descendants(self) -> List['Virus']:
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants

    def __str__(self) -> str:
        return (f"Virus(name={self.name}, id={self._id}, weight={self.weight}, "
                f"age={self.age}, species={self.species}, generation={self._generation}, "
                f"children={len(self.children)})")

    def __repr__(self) -> str:
        return self.__str__()