from task5.models.enums import Build, Gender, Alignment
from typing import List, Dict



class Character:

    def __init__(self):
        self.name: str = ""
        self.gender: Gender = Gender.OTHER
        self.age: int = 0
        self.height: int = 0  # в см
        self.build: Build = Build.ATHLETIC

        self.hair_color: str = ""
        self.eye_color: str = ""
        self.skin_color: str = ""

        self.clothing: Dict[str, str] = {}
        self.weapons: List[str] = []
        self.armor: List[str] = []
        self.accessories: List[str] = []

        self.inventory: List[str] = []
        self.gold: int = 0

        self.skills: Dict[str, int] = {}
        self.special_abilities: List[str] = []

        self.alignment: Alignment = Alignment.NEUTRAL
        self.good_deeds: List[str] = []
        self.evil_deeds: List[str] = []

        self.backstory: str = ""
        self.personality_traits: List[str] = []
        self.fears: List[str] = []
        self.goals: List[str] = []

    def display_info(self) -> str:
        info = f"\n{'=' * 50}\n"
        info += f"CHARACTER: {self.name.upper()}\n"
        info += f"{'=' * 50}\n"

        info += f"Gender: {self.gender.value.title()}\n"
        info += f"Age: {self.age} years\n"
        info += f"Height: {self.height} cm\n"
        info += f"Build: {self.build.value.title()}\n"
        info += f"Alignment: {self.alignment.value.title()}\n\n"

        info += "APPEARANCE:\n"
        info += f"  Hair: {self.hair_color}\n"
        info += f"  Eyes: {self.eye_color}\n"
        info += f"  Skin: {self.skin_color}\n\n"

        if self.clothing:
            info += "CLOTHING:\n"
            for item_type, item in self.clothing.items():
                info += f"  {item_type.title()}: {item}\n"

        if self.weapons:
            info += f"\nWEAPONS: {', '.join(self.weapons)}\n"

        if self.armor:
            info += f"ARMOR: {', '.join(self.armor)}\n"

        if self.accessories:
            info += f"ACCESSORIES: {', '.join(self.accessories)}\n"

        if self.inventory:
            info += f"\nINVENTORY: {', '.join(self.inventory)}\n"

        if self.gold > 0:
            info += f"GOLD: {self.gold} coins\n"

        if self.skills:
            info += "\nSKILLS:\n"
            for skill, level in self.skills.items():
                info += f"  {skill}: {level}/100\n"

        if self.special_abilities:
            info += f"\nSPECIAL ABILITIES: {', '.join(self.special_abilities)}\n"

        if self.good_deeds:
            info += f"\nGOOD DEEDS:\n"
            for deed in self.good_deeds:
                info += f"  ✓ {deed}\n"

        if self.evil_deeds:
            info += f"\nEVIL DEEDS:\n"
            for deed in self.evil_deeds:
                info += f"  ✗ {deed}\n"

        if self.personality_traits:
            info += f"\nPERSONALITY: {', '.join(self.personality_traits)}\n"

        if self.fears:
            info += f"FEARS: {', '.join(self.fears)}\n"

        if self.goals:
            info += f"GOALS: {', '.join(self.goals)}\n"

        if self.backstory:
            info += f"\nBACKSTORY:\n{self.backstory}\n"

        info += f"{'=' * 50}\n"
        return info

    def __str__(self) -> str:
        return f"Character({self.name}, {self.alignment.value}, Age: {self.age})"