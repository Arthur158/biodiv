from classes.species import Species


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

        self.unreachability = 1.0 * self.height
        self.light_absorption = 0.4 * self.height + 0.6 * self.size_of_leaves
        self.water_absorption = 1.0 * self.depth_of_roots

        self.calories_cost = 1.0 * self.toxicity + 1.5 * self.height + 1.0 * self.depth_of_roots + 0.6 * self.size_of_leaves
        self.provided_food = 1.5 * self.height + 0.8 * self.depth_of_roots + 1.0 * self.size_of_leaves