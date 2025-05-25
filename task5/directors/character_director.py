from task5.builders.base_builder import CharacterBuilder
from task5.models.character import Character
from task5.models.enums import Gender, Build


class CharacterDirector:

    def __init__(self, builder: CharacterBuilder):
        self.builder = builder

    def set_builder(self, builder: CharacterBuilder):
        self.builder = builder

    def build_basic_character(self, name: str, gender: Gender, age: int) -> Character:
        return (self.builder
                .reset()
                .set_name(name)
                .set_gender(gender)
                .set_age(age)
                .build_moral_alignment()
                .get_character())

    def build_fantasy_hero(self) -> Character:
        return (self.builder
                .reset()
                .set_name("Elara Moonwhisper")
                .set_gender(Gender.FEMALE)
                .set_age(125)
                .set_height(170)
                .set_build(Build.ATHLETIC)
                .set_hair_color("Silver with blue highlights")
                .set_eye_color("Emerald green")
                .set_skin_color("Pale with mystical glow")
                .add_clothing("robe", "Enchanted Elven Robe of Starlight")
                .add_clothing("boots", "Boots of Silent Steps")
                .add_clothing("cloak", "Cloak of Elvish Nobility")
                .add_weapon("Moonblade - Ancient Elven Sword")
                .add_weapon("Bow of the Eternal Hunt")
                .add_armor("Mithril Chain Mail")
                .add_accessory("Amulet of Nature's Protection")
                .add_accessory("Ring of Wisdom")
                .add_inventory_item("Healing Potions x5")
                .add_inventory_item("Mana Crystals x3")
                .add_inventory_item("Ancient Spellbook")
                .set_gold(2500)
                .add_skill("Archery", 95)
                .add_skill("Magic", 90)
                .add_skill("Stealth", 85)
                .add_skill("Herbalism", 80)
                .add_heroic_ability("Light Magic Mastery")
                .add_heroic_ability("Nature Communication")
                .add_heroic_ability("Prophecy Vision")
                .build_moral_alignment()
                .add_moral_deed("Saved the Ancient Forest from corruption")
                .add_moral_deed("Rescued villages from dragon attacks")
                .add_moral_deed("Restored peace between warring kingdoms")
                .add_virtue("Compassion")
                .add_virtue("Wisdom")
                .add_virtue("Courage")
                .add_personality_trait("Mystical")
                .add_personality_trait("Protective")
                .add_personality_trait("Wise")
                .add_fear("Loss of nature's balance")
                .add_fear("Corruption of innocent souls")
                .add_goal("Protect the realm from darkness")
                .add_goal("Restore ancient elven magic")
                .add_goal("Train new generation of heroes")
                .set_noble_backstory("Born under a rare celestial alignment, "
                                     "chosen by the Elven Council as Guardian of Light")
                .get_character())

    def build_dark_enemy(self) -> Character:
        return (self.builder
                .reset()
                .set_name("Malachar the Shadowlord")
                .set_gender(Gender.MALE)
                .set_age(800)
                .set_height(195)
                .set_build(Build.MUSCULAR)
                .set_hair_color("Black as the void")
                .set_eye_color("Glowing red")
                .set_skin_color("Ashen grey with dark veins")
                .add_clothing("armor", "Cursed Plate Armor of Souls")
                .add_clothing("cloak", "Cloak of Eternal Darkness")
                .add_clothing("crown", "Crown of the Damned")
                .add_weapon("Soulreaper - Cursed Greatsword")
                .add_weapon("Shadow Orb of Destruction")
                .add_armor("Full Plate of the Abyss")
                .add_accessory("Amulet of Soul Binding")
                .add_accessory("Ring of Dark Power")
                .add_inventory_item("Vials of Corrupted Blood x10")
                .add_inventory_item("Cursed Grimoires x3")
                .add_inventory_item("Souls of the Innocent x50")
                .set_gold(50000)
                .add_skill("Dark Magic", 100)
                .add_skill("Necromancy", 95)
                .add_skill("Intimidation", 90)
                .add_skill("Sword Combat", 85)
                .add_dark_ability("Soul Drain")
                .add_dark_ability("Shadow Manipulation")
                .add_dark_ability("Undead Army Summoning")
                .build_moral_alignment()
                .add_moral_deed("Destroyed entire kingdoms for power")
                .add_moral_deed("Corrupted sacred temples")
                .add_moral_deed("Enslaved thousands of souls")
                .add_vice("Wrath")
                .add_vice("Pride")
                .add_vice("Greed")
                .add_personality_trait("Ruthless")
                .add_personality_trait("Cunning")
                .add_personality_trait("Merciless")
                .add_fear("Loss of power")
                .add_fear("The return of ancient light")
                .add_evil_scheme("Plunge the world into eternal darkness")
                .add_evil_scheme("Corrupt all pure magic")
                .add_evil_scheme("Rule over all realms as Shadow Emperor")
                .set_dark_backstory("Once a noble paladin who fell to darkness "
                                    "after losing everything he loved, now seeks "
                                    "to make the world suffer as he has suffered")
                .get_character())