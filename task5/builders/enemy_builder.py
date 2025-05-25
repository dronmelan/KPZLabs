from task5.builders.base_builder import CharacterBuilder
from task5.models.enums import Alignment


class EnemyBuilder(CharacterBuilder):

    def build_moral_alignment(self) -> 'EnemyBuilder':
        self.character.alignment = Alignment.EVIL
        return self

    def add_moral_deed(self, deed: str) -> 'EnemyBuilder':
        self.character.evil_deeds.append(deed)
        return self

    def add_dark_ability(self, ability: str) -> 'EnemyBuilder':
        return self.add_special_ability(f"Dark: {ability}")

    def set_dark_backstory(self, story: str) -> 'EnemyBuilder':
        dark_story = f"Dark Origin: {story}"
        return self.set_backstory(dark_story)

    def add_vice(self, vice: str) -> 'EnemyBuilder':
        return self.add_personality_trait(f"Vice: {vice}")

    def add_evil_scheme(self, scheme: str) -> 'EnemyBuilder':
        return self.add_goal(f"Evil Scheme: {scheme}")