from task2.decorators import SwordDecorator, PlateArmorDecorator, DefenseShieldDecorator, StrengthRingDecorator, \
    MagicStaffDecorator, ManaPotionDecorator, WisdomAmuletDecorator, HealthPotionDecorator, LeatherArmorDecorator, \
    RobeDecorator
from task2.heroes import Mage, Warrior, Paladin
from task2.utils import print_hero_stats


def main():
    print("=== РПГ Гра з патерном Декоратор ===\n")

    # Створення базових героїв
    print("1. Базові герої без екіпіровки:")

    warrior = Warrior("Aragorn")
    mage = Mage("Gandalf")
    paladin = Paladin("Arthas")

    print_hero_stats(warrior)
    print_hero_stats(mage)
    print_hero_stats(paladin)

    print("\n" + "=" * 60 + "\n")

    # Екіпіровка воїна
    print("2. Екіпіровка Воїна:")
    equipped_warrior = warrior
    equipped_warrior = SwordDecorator(equipped_warrior)
    equipped_warrior = PlateArmorDecorator(equipped_warrior)
    equipped_warrior = DefenseShieldDecorator(equipped_warrior)
    equipped_warrior = HealthPotionDecorator(equipped_warrior)
    equipped_warrior = StrengthRingDecorator(equipped_warrior)

    print_hero_stats(equipped_warrior)

    # Екіпіровка мага
    print("3. Екіпіровка Мага:")
    equipped_mage = mage
    equipped_mage = MagicStaffDecorator(equipped_mage)
    equipped_mage = RobeDecorator(equipped_mage)
    equipped_mage = ManaPotionDecorator(equipped_mage)
    equipped_mage = WisdomAmuletDecorator(equipped_mage)
    equipped_mage = HealthPotionDecorator(equipped_mage)  # Маг теж може мати зілля здоров'я

    print_hero_stats(equipped_mage)

    # Екіпіровка паладина (гібридна збірка)
    print("4. Екіпіровка Паладина (гібридна збірка):")
    equipped_paladin = paladin
    equipped_paladin = SwordDecorator(equipped_paladin)
    equipped_paladin = LeatherArmorDecorator(equipped_paladin)
    equipped_paladin = DefenseShieldDecorator(equipped_paladin)
    equipped_paladin = ManaPotionDecorator(equipped_paladin)
    equipped_paladin = StrengthRingDecorator(equipped_paladin)
    equipped_paladin = WisdomAmuletDecorator(equipped_paladin)

    print_hero_stats(equipped_paladin)

    # Демонстрація множинного використання декораторів
    print("5. Супер-екіпірований маг (множинні артефакти):")
    super_mage = mage
    super_mage = MagicStaffDecorator(super_mage)
    super_mage = RobeDecorator(super_mage)
    super_mage = ManaPotionDecorator(super_mage)
    super_mage = ManaPotionDecorator(super_mage)  # Друге зілля мани
    super_mage = WisdomAmuletDecorator(super_mage)
    super_mage = HealthPotionDecorator(super_mage)
    super_mage = HealthPotionDecorator(super_mage)  # Друге зілля здоров'я

    print_hero_stats(super_mage)

    # Демонстрація універсальності декораторів
    print("6. Маг з воїнським спорядженням (демонстрація універсальності):")
    warrior_mage = mage
    warrior_mage = SwordDecorator(warrior_mage)  # Маг з мечем
    warrior_mage = PlateArmorDecorator(warrior_mage)  # Маг в броні
    warrior_mage = MagicStaffDecorator(warrior_mage)  # І з посохом теж
    warrior_mage = StrengthRingDecorator(warrior_mage)

    print_hero_stats(warrior_mage)

    print("=== Демонстрація завершена ===")


if __name__ == "__main__":
    main()