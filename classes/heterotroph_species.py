from classes.species import Species


class HeterotrophSpecies(Species):
    def __init__(self, name: str, heterotroph_level: int, armor=100, speed=100, strength=100) -> None:
        super().__init__(name)

        self.heterotroph_level = heterotroph_level