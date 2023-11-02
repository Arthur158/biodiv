from classes.species import Species
from utility import calculate_stats_autotroph


class AutotrophSpecies(Species):
    def __init__(self, name: str, toxicity = 100, height = 100, depth_of_roots = 100, size_of_leaves = 100):
        super().__init__(name)

        self.toxicity = toxicity
        self.height = height
        self.depth_of_roots = depth_of_roots
        self.size_of_leaves = size_of_leaves

        self.unreachability: float = 0
        self.light_absorption: float = 0
        self.water_absorption: float = 0

        self.calculate_stats()
    
    def update_stats(self, toxicity = 100, height = 100, depth_of_roots = 100, size_of_leaves = 100):
        
        self.toxicity = toxicity
        self.height = height
        self.depth_of_roots = depth_of_roots
        self.size_of_leaves = size_of_leaves

        self.calculate_stats()

    def calculate_stats(self):

       self.toxicity, self.unreachability, self.depth_of_roots, self.size_of_leaves, self.calories_cost, self.provided_food = calculate_stats_autotroph(self.toxicity, self.height, self.depth_of_roots, self.size_of_leaves)