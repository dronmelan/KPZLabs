from typing import Optional
from typing import List
from task4.prototype.virus import Virus


class VirusFactory:

    def __init__(self):
        self._prototypes = {}

    def register_prototype(self, name: str, virus: Virus) -> None:
        self._prototypes[name] = virus
        print(f"Registered prototype: {name}")

    def create_virus(self, prototype_name: str, deep_clone: bool = True) -> Optional[Virus]:
        if prototype_name in self._prototypes:
            return self._prototypes[prototype_name].clone(deep_clone)
        print(f"Prototype {prototype_name} not found!")
        return None

    def list_prototypes(self) -> List[str]:
        return list(self._prototypes.keys())


def create_virus_family() -> Virus:
    print("\n=== Створення сімейства вірусів ===")

    ancestor = Virus(
        weight=10.5,
        age=100,
        name="Alpha_Ancestor",
        species="Coronaviridae"
    )
    print(f"Created ancestor: {ancestor}")

    child1 = Virus(
        weight=8.2,
        age=50,
        name="Beta_Child1",
        species="Coronaviridae"
    )

    child2 = Virus(
        weight=9.1,
        age=45,
        name="Beta_Child2",
        species="Coronaviridae"
    )

    ancestor.add_child(child1)
    ancestor.add_child(child2)

    grandchild1 = Virus(
        weight=6.5,
        age=25,
        name="Gamma_Grandchild1",
        species="Coronaviridae"
    )

    grandchild2 = Virus(
        weight=7.0,
        age=20,
        name="Gamma_Grandchild2",
        species="Coronaviridae"
    )

    grandchild3 = Virus(
        weight=6.8,
        age=22,
        name="Gamma_Grandchild3",
        species="Coronaviridae"
    )

    child1.add_child(grandchild1)
    child1.add_child(grandchild2)
    child2.add_child(grandchild3)

    great_grandchild1 = Virus(
        weight=5.2,
        age=10,
        name="Delta_GreatGrandchild1",
        species="Coronaviridae"
    )

    great_grandchild2 = Virus(
        weight=4.8,
        age=8,
        name="Delta_GreatGrandchild2",
        species="Coronaviridae"
    )

    grandchild1.add_child(great_grandchild1)
    grandchild2.add_child(great_grandchild2)

    return ancestor