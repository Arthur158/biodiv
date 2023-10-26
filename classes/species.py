from classes.diet import Trophic_type 
from typing import Set

class Species:
    def __init__(self, name: str, trophic_type: Trophic_type, heterotroph_level: int | None) -> None:
       self.name = name
       self.trophic_type = trophic_type 
       self.heterotroph_level = heterotroph_level