from typing import Dict
from ..models.animal import Animal
from ..models.food import Food
from ..models.enclosure import Enclosure

class FeedingService:
    @staticmethod
    def feed_animal(animal: Animal, food: Food) -> bool:
        return animal.feed(food)

    @staticmethod
    def feed_enclosure(enclosure: Enclosure, food: Food) -> Dict[str, bool]:
        results = {}
        for animal in enclosure.get_animals():
            results[animal.name] = FeedingService.feed_animal(animal, food)
        return results
    pass