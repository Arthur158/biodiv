from classes.diet import Diet 
from typing import Set

class Species:
    def __init__(self, name: str, trophic_type: Set[Diet]) -> None:
       self.name = name
       self.trophic_type = trophic_type 