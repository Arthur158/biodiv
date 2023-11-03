
from classes.autotroph_species import AutotrophSpecies
from classes.heterotroph_species import HeterotrophSpecies
from math_utils import gaussian


def matchup_plant_to_herbivore(plant_species: AutotrophSpecies, herbivore_species: HeterotrophSpecies):

    matchup_digestibility = gaussian(plant_species.toxicity, herbivore_species.digestive_strength)
    matchup_reachability = gaussian(plant_species.unreachability, herbivore_species.height)

def matchup_prey_to_carnivore(plant_species: AutotrophSpecies, herbivore_species: HeterotrophSpecies):
    pass

