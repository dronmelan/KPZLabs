from task4.utils.helpers import test_cloning, test_virus_factory, create_virus_family


def main():
    print("=== Демонстрація патерну Прототип для класу Virus ===")

    virus_family = create_virus_family()

    test_cloning(virus_family)

    test_virus_factory(virus_family)

    print("\n=== Додаткова інформація ===")
    all_descendants = virus_family.get_all_descendants()
    print(f"Всього нащадків у сімействі: {len(all_descendants)}")

    for virus in all_descendants:
        print(f"  - {virus.name} (Покоління {virus.get_generation()})")

    print(f"\nМаксимальне покоління: {max(v.get_generation() for v in [virus_family] + all_descendants)}")


if __name__ == "__main__":
    main()