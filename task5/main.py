from task5.builders.enemy_builder import EnemyBuilder
from task5.builders.hero_builder import HeroBuilder
from task5.directors.character_director import CharacterDirector
from task5.models.enums import Gender, Alignment


def main():
    print("=== Демонстрація патерну Будівельник (Builder) ===")
    print("Створення персонажів гри з використанням текучого інтерфейсу\n")

    print("1. Створення героя мрії...")
    hero_builder = HeroBuilder()
    director = CharacterDirector(hero_builder)

    dream_hero = director.build_fantasy_hero()
    print(dream_hero.display_info())

    print("\n2. Створення найзапеклішого ворога...")
    enemy_builder = EnemyBuilder()
    director.set_builder(enemy_builder)

    arch_enemy = director.build_dark_enemy()
    print(arch_enemy.display_info())

    print("\n3. Демонстрація текучого інтерфейсу (Fluent Interface)...")
    print("Створення простого персонажа за допомогою ланцюжка методів:")

    simple_character = (HeroBuilder()
                        .set_name("Simple Hero")
                        .set_gender(Gender.MALE)
                        .set_age(25)
                        .set_height(180)
                        .set_hair_color("Brown")
                        .set_eye_color("Blue")
                        .add_weapon("Steel Sword")
                        .add_skill("Swordsmanship", 70)
                        .build_moral_alignment()
                        .add_moral_deed("Helped villagers")
                        .get_character())

    print(simple_character.display_info())

    print("\n4. Порівняння створених персонажів:")
    characters = [dream_hero, arch_enemy, simple_character]

    for char in characters:
        print(f"- {char.name}: {char.alignment.value}, "
              f"{len(char.skills)} навичок, {char.gold} золота")

    print("\n5. Створення кастомного персонажа:")
    custom_builder = EnemyBuilder()

    custom_character = (custom_builder
                        .set_name("Grey Wanderer")
                        .set_gender(Gender.OTHER)
                        .set_age(200)
                        .add_personality_trait("Mysterious")
                        .add_personality_trait("Neutral")
                        .add_skill("Ancient Knowledge", 95)
                        .add_special_ability("Time Manipulation")
                        .set_backstory("A being from another dimension")
                        .get_character())

    custom_character.alignment = Alignment.NEUTRAL

    print(f"Створено: {custom_character}")
    print(f"Alignment: {custom_character.alignment.value}")
    print(f"Special Abilities: {custom_character.special_abilities}")


if __name__ == "__main__":
    main()