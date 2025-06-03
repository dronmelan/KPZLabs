from task2.hero_interface import Hero


class Warrior(Hero):

    def __init__(self, name="Warrior"):
        self.name = name
        self.base_health = 120
        self.base_mana = 20
        self.base_attack = 25
        self.base_defense = 15
        self.base_magic_power = 5

    def get_name(self):
        return self.name

    def get_health(self):
        return self.base_health

    def get_mana(self):
        return self.base_mana

    def get_attack(self):
        return self.base_attack

    def get_defense(self):
        return self.base_defense

    def get_magic_power(self):
        return self.base_magic_power

    def get_description(self):
        return f"{self.name} (Warrior)"


class Mage(Hero):

    def __init__(self, name="Mage"):
        self.name = name
        self.base_health = 70
        self.base_mana = 100
        self.base_attack = 10
        self.base_defense = 8
        self.base_magic_power = 30

    def get_name(self):
        return self.name

    def get_health(self):
        return self.base_health

    def get_mana(self):
        return self.base_mana

    def get_attack(self):
        return self.base_attack

    def get_defense(self):
        return self.base_defense

    def get_magic_power(self):
        return self.base_magic_power

    def get_description(self):
        return f"{self.name} (Mage)"


class Paladin(Hero):

    def __init__(self, name="Paladin"):
        self.name = name
        self.base_health = 100
        self.base_mana = 60
        self.base_attack = 18
        self.base_defense = 20
        self.base_magic_power = 15

    def get_name(self):
        return self.name

    def get_health(self):
        return self.base_health

    def get_mana(self):
        return self.base_mana

    def get_attack(self):
        return self.base_attack

    def get_defense(self):
        return self.base_defense

    def get_magic_power(self):
        return self.base_magic_power

    def get_description(self):
        return f"{self.name} (Paladin)"