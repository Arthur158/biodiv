
from classes.autotroph_species import AutotrophSpecies
from classes.heterotroph_species import HeterotrophSpecies
from constants import AMOUNT_OF_POOLS
from math_utils import gaussian


def matchup_plant_to_herbivore(plant_species: AutotrophSpecies, herbivore_species: HeterotrophSpecies):

    matchup_digestibility = gaussian(plant_species.toxicity, herbivore_species.digestive_strength)
    matchup_reachability = gaussian(plant_species.unreachability, herbivore_species.size)

    return round(matchup_digestibility * matchup_reachability * AMOUNT_OF_POOLS)

def matchup_prey_to_carnivore(herbivore_species: HeterotrophSpecies, carnivore_species: HeterotrophSpecies):
    matchup_evasion = gaussian(herbivore_species.evasion, carnivore_species.anti_evasion)
    matchup_attack = gaussian(herbivore_species.defense, carnivore_species.attack)

    return round(matchup_evasion * matchup_attack * AMOUNT_OF_POOLS)

