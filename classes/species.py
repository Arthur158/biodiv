from abc import abstractmethod

class Species:
    def __init__(self, name: str) -> None:
        self.name = name

        self.calories_cost: float = 0

        self.provided_food: float = 0

    @abstractmethod
    def update_stats(self):
        pass

    @abstractmethod
    def calculate_stats(self):
        pass
