from task2.hero_interface import Hero


class HeroDecorator(Hero):

    def __init__(self, hero):
        self.hero = hero

    def get_name(self):
        return self.hero.get_name()

    def get_health(self):
        return self.hero.get_health()

    def get_mana(self):
        return self.hero.get_mana()

    def get_attack(self):
        return self.hero.get_attack()

    def get_defense(self):
        return self.hero.get_defense()

    def get_magic_power(self):
        return self.hero.get_magic_power()

    def get_description(self):
        return self.hero.get_description()


# Декоратори зброї
class SwordDecorator(HeroDecorator):

    def get_attack(self):
        return self.hero.get_attack() + 15

    def get_description(self):
        return f"{self.hero.get_description()} + Iron Sword"


class MagicStaffDecorator(HeroDecorator):

    def get_magic_power(self):
        return self.hero.get_magic_power() + 20

    def get_mana(self):
        return self.hero.get_mana() + 30

    def get_description(self):
        return f"{self.hero.get_description()} + Magic Staff"


class BowDecorator(HeroDecorator):
    """Декоратор лука - збільшує атаку менше ніж меч"""

    def get_attack(self):
        return self.hero.get_attack() + 12

    def get_description(self):
        return f"{self.hero.get_description()} + Elven Bow"


# Декоратори броні
class LeatherArmorDecorator(HeroDecorator):


    def get_defense(self):
        return self.hero.get_defense() + 8

    def get_health(self):
        return self.hero.get_health() + 15

    def get_description(self):
        return f"{self.hero.get_description()} + Leather Armor"


class PlateArmorDecorator(HeroDecorator):

    def get_defense(self):
        return self.hero.get_defense() + 20

    def get_health(self):
        return self.hero.get_health() + 40

    def get_description(self):
        return f"{self.hero.get_description()} + Plate Armor"


class RobeDecorator(HeroDecorator):

    def get_mana(self):
        return self.hero.get_mana() + 25

    def get_magic_power(self):
        return self.hero.get_magic_power() + 10

    def get_defense(self):
        return self.hero.get_defense() + 3

    def get_description(self):
        return f"{self.hero.get_description()} + Mystic Robe"


# Декоратори артефактів
class HealthPotionDecorator(HeroDecorator):

    def get_health(self):
        return self.hero.get_health() + 50

    def get_description(self):
        return f"{self.hero.get_description()} + Health Potion"


class ManaPotionDecorator(HeroDecorator):


    def get_mana(self):
        return self.hero.get_mana() + 40

    def get_description(self):
        return f"{self.hero.get_description()} + Mana Potion"


class StrengthRingDecorator(HeroDecorator):

    def get_attack(self):
        return self.hero.get_attack() + 8

    def get_health(self):
        return self.hero.get_health() + 20

    def get_description(self):
        return f"{self.hero.get_description()} + Ring of Strength"


class WisdomAmuletDecorator(HeroDecorator):

    def get_magic_power(self):
        return self.hero.get_magic_power() + 15

    def get_mana(self):
        return self.hero.get_mana() + 35

    def get_description(self):
        return f"{self.hero.get_description()} + Amulet of Wisdom"


class DefenseShieldDecorator(HeroDecorator):

    def get_defense(self):
        return self.hero.get_defense() + 12

    def get_health(self):
        return self.hero.get_health() + 25

    def get_description(self):
        return f"{self.hero.get_description()} + Defense Shield"