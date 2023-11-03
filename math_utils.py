import numpy as np
import math

from constants import MATCHUP_SEVERITY

def gaussian(x, mu):
    sigma = mu / MATCHUP_SEVERITY
    z = (x - mu) / (sigma * np.sqrt(2))
    return 0.5 * (1 + math.erf(z))


def calculate_stats_autotroph(toxicity, height, depth_of_roots, size_of_leaves):

    toxicity = 1.0 * toxicity
    unreachability = 1.0 * height
    light_absorption = 0.4 * height + 0.6 * size_of_leaves
    water_absorption = 1.0 * depth_of_roots

    calories_cost = 0.2 * toxicity + 0.3 * height + 0.2 * depth_of_roots + 0.3 * size_of_leaves
    provided_food = 0.4 * height + 0.3 * depth_of_roots + 0.3 * size_of_leaves

    return round(toxicity), round(unreachability), round(light_absorption), round(water_absorption), round(calories_cost), round(provided_food)

def calculate_stats_heterotroph(armor, speed, strength, digestive_strength, size):
        evasion = 1.0 * speed
        anti_evasion =  1.0 * speed

        attack = 0.2 * armor + 0.8 * strength
        defense = 0.8 * armor + 0.2 * strength

        calories_cost = 0.3 * speed + 0.2 * armor + 0.2 * strength + 0.1 * digestive_strength + 0.2 * size

        provided_food = 0.2 * speed + 0.3 * strength + 0.5 * size

        reach = 0.3 * speed + 0.4 * strength + 0.3 * size

        return round(evasion), round(anti_evasion), round(attack), round(defense), round(calories_cost), round(provided_food), round(reach)

