import numpy as np
import math

from classes.autotroph_species import AutotrophSpecies
from classes.heterotroph_species import HeterotrophSpecies
from constants import MATCHUP_SEVERITY

def gaussian(x, mu):
    sigma = mu / MATCHUP_SEVERITY
    z = (x - mu) / (sigma * np.sqrt(2))
    return 0.5 * (1 + math.erf(z))

def matchup_plant_to_herbivore(plant_species: AutotrophSpecies, herbivore_species: HeterotrophSpecies):

    matchup_digestibility = gaussian(plant_species.toxicity, herbivore_species.digestive_strength)
    matchup_reachability = gaussian(plant_species.unreachability, herbivore_species.height)

def matchup_prey_to_carnivore(plant_species: AutotrophSpecies, herbivore_species: HeterotrophSpecies):
    pass

def calculate_stats_autotroph(toxicity, height, depth_of_roots, size_of_leaves):

    toxicity = 1.0 * toxicity
    unreachability = 1.0 * height
    light_absorption = 0.4 * height + 0.6 * size_of_leaves
    water_absorption = 1.0 * depth_of_roots

    calories_cost = 1.0 * toxicity + 1.5 * height + 1.0 * depth_of_roots + 0.6 * size_of_leaves
    provided_food = 1.5 * height + 0.8 * depth_of_roots + 1.0 * size_of_leaves

    return toxicity, unreachability, light_absorption, water_absorption, calories_cost, provided_food

def calculate_stats_heterotroph(armor, speed, strength, digestive_strength, height):
        evasion = 1.0 * speed
        anti_evasion =  1.0 * speed

        attack = 0.2 * armor + 0.8 * strength
        defense = 0.8 * armor + 0.2 * strength

        calories_cost = 1.5 * speed + 1.0 * armor + 1.0 * strength + 1.0 * digestive_strength + 1.0 * height

        provided_food = 1.5 * speed + 2.0 * strength + 2.5 * height

        reach = 0.5 * speed + 0.8 * strength + 0.3 * height

        return evasion, anti_evasion, attack, defense, calories_cost, provided_food, reach


