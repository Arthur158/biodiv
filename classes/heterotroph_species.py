from classes.species import Species
from utility import calculate_stats_heterotroph


class HeterotrophSpecies(Species):
    def __init__(self, name: str, heterotroph_level: int, armor=100, speed=100, strength=100, digestive_strength = 100, height = 100) -> None:
        super().__init__(name)

        self.heterotroph_level = heterotroph_level

        self.armor = armor
        self.speed = speed
        self.strength = strength
        self.digestive_strength = digestive_strength
        self.height = height

        self.evasion: float = 0
        self.anti_evasion: float = 0
        self.attack: float = 0
        self.defense: float = 0

        self.calculate_stats()

    def update_stats(self, armor=100, speed=100, strength=100, digestive_strength = 100, height = 100):

        self.armor = armor
        self.speed = speed
        self.strength = strength
        self.digestive_strength = digestive_strength
        self.height = height
        self.calculate_stats()

    def calculate_stats(self):
        self.evasion, self.anti_evasion, self.attack, self.defense, self.calories_cost, self.provided_food = calculate_stats_heterotroph(self.armor, self.speed, self.strength, self.digestive_strength, self.height)
