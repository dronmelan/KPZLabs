from task5.builders.base_builder import CharacterBuilder
from task5.models.enums import Alignment


class HeroBuilder(CharacterBuilder):

    def build_moral_alignment(self) -> 'HeroBuilder':
        self.character.alignment = Alignment.GOOD
        return self

    def add_moral_deed(self, deed: str) -> 'HeroBuilder':
        self.character.good_deeds.append(deed)
        return self

    def add_heroic_ability(self, ability: str) -> 'HeroBuilder':
        return self.add_special_ability(f"Heroic: {ability}")

    def set_noble_backstory(self, story: str) -> 'HeroBuilder':
        noble_story = f"Noble Origin: {story}"
        return self.set_backstory(noble_story)

    def add_virtue(self, virtue: str) -> 'HeroBuilder':
        return self.add_personality_trait(f"Virtue: {virtue}")