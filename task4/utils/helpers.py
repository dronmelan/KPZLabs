from task4.prototype.virus import Virus
from task4.prototype.virus_factory import VirusFactory


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


def test_cloning(original_family: Virus) -> None:
    print("\n=== Тестування клонування ===")

    print("\n1. Глибоке клонування всього сімейства:")
    cloned_family = original_family.clone(deep=True)

    print(f"\nОригінальне сімейство (нащадків: {original_family.count_descendants()}):")
    print(original_family.get_family_tree())

    print(f"Клоноване сімейство (нащадків: {cloned_family.count_descendants()}):")
    print(cloned_family.get_family_tree())

    print("\n2. Поверхневе клонування (тільки корінь):")
    shallow_clone = original_family.clone(deep=False)
    print(f"Поверхневий клон (нащадків: {shallow_clone.count_descendants()}):")
    print(shallow_clone.get_family_tree())

    print("\n3. Тестування незалежності клонів:")
    print("Мутація оригінального вірусу...")
    original_family.mutate(weight_change=2.0, age_change=10)

    print("Мутація клонованого вірусу...")
    cloned_family.mutate(weight_change=-1.0, age_change=5)

    print(f"\nПісля мутації:")
    print(f"Оригінал: {original_family}")
    print(f"Клон: {cloned_family}")


def test_virus_factory(original_family: Virus) -> None:
    print("\n=== Тестування фабрики вірусів ===")

    factory = VirusFactory()

    factory.register_prototype("corona_family", original_family)

    simple_virus = Virus(
        weight=3.0,
        age=15,
        name="Simple_Virus",
        species="Adenoviridae"
    )
    factory.register_prototype("simple_virus", simple_virus)

    print(f"Зареєстровані прототипи: {factory.list_prototypes()}")

    print("\nСтворення вірусів з прототипів:")
    new_corona_family = factory.create_virus("corona_family")
    new_simple_virus = factory.create_virus("simple_virus")

    if new_corona_family:
        print(f"Створено нове сімейство з {new_corona_family.count_descendants()} нащадків")

    if new_simple_virus:
        print(f"Створено простий вірус: {new_simple_virus}")