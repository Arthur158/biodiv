from classes.species import Species
from math_utils import calculate_stats_autotroph


class AutotrophSpecies(Species):
    def __init__(self, name: str):
        super().__init__(name)

        self.toxicity: float = 0
        self.height = 0
        self.depth_of_roots = 0
        self.size_of_leaves = 0

        self.unreachability: float = 0
        self.light_absorption: float = 0
        self.water_absorption: float = 0

    
    def update_stats(self, toxicity, height, depth_of_roots, size_of_leaves):
        
        self.toxicity = toxicity
        self.height = height
        self.depth_of_roots = depth_of_roots
        self.size_of_leaves = size_of_leaves

        self.calculate_stats()

    def calculate_stats(self):
        self.toxicity, self.unreachability, self.light_absorption, self.water_absorption, self.calories_cost, self.provided_food = calculate_stats_autotroph(self.toxicity, self.height, self.depth_of_roots, self.size_of_leaves)