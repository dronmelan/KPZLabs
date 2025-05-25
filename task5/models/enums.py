from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Build(Enum):
    SLIM = "slim"
    ATHLETIC = "athletic"
    MUSCULAR = "muscular"
    HEAVY = "heavy"
    PETITE = "petite"

class Alignment(Enum):
    GOOD = "good"
    NEUTRAL = "neutral"
    EVIL = "evil"