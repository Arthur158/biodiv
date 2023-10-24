from classes.region import Region
from classes.species import Species


class Population:
    def __init__(self, species: Species, population_size : int, region: Region) -> None:
        self.species = species
        self.population_size = population_size
        self.region = Region
 