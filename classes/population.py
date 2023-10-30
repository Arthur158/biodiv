from classes.species import Species


class Population:
    def __init__(self, species: Species, population_size : int) -> None:
        self.species = species
        self.population_size: int = population_size

        self.grass_collected: float = 0
        self.meat_collected: float = 0
        self.food_collected: float = 0
        self.losse_to_predation: float = 0

        self.grass_debts = dict()
        self.meat_debts = dict()

        self.growth_factor: float = 1

    def __str__(self):
        return (f"Population(species={self.species}, population_size={self.population_size}, "
                f"grass_collected={self.grass_collected}, meat_collected={self.meat_collected}, "
                f"food_collected={self.food_collected}, losse_to_predation={self.losse_to_predation}, "
                f"grass_debts={self.grass_debts}, meat_debts={self.meat_debts}, "
                f"growth_factor={self.growth_factor})")
    
    def grow(self):
        print(f"population of{self.species.name} from {self.population_size}")
        self.population_size = round(self.population_size * self.growth_factor)
        print(f"to {self.population_size}")

 