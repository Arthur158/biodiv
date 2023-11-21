from classes.species import Species
from math_utils import calculate_stats_heterotroph


class HeterotrophSpecies(Species):
    def __init__(self, name: str, heterotroph_level: int) -> None:
        super().__init__(name)

        self.heterotroph_level = heterotroph_level

        self.armor = 0
        self.speed = 0
        self.strength = 0
        self.digestive_strength: float = 0
        self.size: float = 0

        self.evasion: float = 0
        self.anti_evasion: float = 0
        self.attack: float = 0
        self.defense: float = 0
        self.reach: float = 0

        self.calculate_stats()

    def update_stats(self, armor, speed, strength, digestive_strength, size):

        self.armor = armor
        self.speed = speed
        self.strength = strength
        self.digestive_strength = digestive_strength
        self.size = size
        self.calculate_stats()

    def calculate_stats(self):
        self.evasion, self.anti_evasion, self.attack, self.defense, self.calories_cost, self.provided_food, self.reach = calculate_stats_heterotroph(self.armor, self.speed, self.strength, self.digestive_strength, self.size)
