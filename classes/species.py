from classes.diet import Trophic_type 
from typing import List, Set

class Species:
    def __init__(self, name: str, trophic_type: Trophic_type, heterotroph_level: int | None) -> None:
       self.name = name
       self.trophic_type = trophic_type 
       self.heterotroph_level = heterotroph_level
       self.cost: float = 1.0
       self.food_content:float = 1.0
       self.effectiveness: List[float] = [1.0, 1.0, 1.0] 
       # these are the weights that represent the cost of maintaining as well as the effectiveness of the species at gathering food
       # they will later be replaced to represent different species.
