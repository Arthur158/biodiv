from typing import List, Set
from abc import ABC, abstractmethod

class Species:
    def __init__(self, name: str) -> None:
        self.name = name

        self.calories_cost = 0

        self.provided_food = 0

    @abstractmethod
    def update_stats(self):
        pass

    @abstractmethod
    def calculate_stats(self):
        pass
