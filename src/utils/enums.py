from enum import Enum

class AnimalType(Enum):
    MAMMAL = "mammal"
    BIRD = "bird"
    REPTILE = "reptile"
    FISH = "fish"

class EnclosureType(Enum):
    CAGE = "cage"
    AQUARIUM = "aquarium"
    AVIARY = "aviary"
    OPEN_AREA = "open_area"