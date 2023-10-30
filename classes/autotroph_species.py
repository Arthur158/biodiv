from classes.species import Species


class AutotrophSpecies(Species):
    def __init__(self, name: str) -> None:
        super().__init__(name)