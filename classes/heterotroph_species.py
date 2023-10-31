from classes.species import Species


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

        self.evasion = 1.0 * self.speed
        self.anti_evasion =  1.0 * self.speed

        self.attack = 0.2 * self.armor + 0.8 * self.strength
        self.defense = 0.8 * self.armor + 0.2 * self.strength

        self.calories_cost = 1.5 * self.speed + 1.0 * self.armor + 1.0 * self.strength + 1.0 * self.digestive_strength + 1.0 * self.height

        self.provided_food = 1.5 * self.speed + 2.0 * self.strength + 2.5 * self.height

        # equations will be changed once we have a working system.