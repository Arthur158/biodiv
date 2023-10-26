from enum import Enum

class Humidity(Enum):
    high = 1
    medium = 2
    low = 3

class Temperature(Enum):
    high = 1
    temperate = 2
    low = 3

class Climate(Enum):
    tropical_rainforest = "tropical_rainforest" 
    tropical_savanna = "tropical_savanna"
    hot_desert = "hot_desert"
    oceanic = "oceanic"
    mediterannean = "mediterannean"
    semi_arid = "semi_arid"
    tundra = "tundra"
    cold_continental = "cold_continental"
    cold_desert = "cold_desert"

def infer_climate(humidity: Humidity, temperature: Temperature) -> Climate:
    climate_mapping = {
        (Temperature.high, Humidity.high): Climate.tropical_rainforest,
        (Temperature.high, Humidity.medium): Climate.tropical_savanna,
        (Temperature.high, Humidity.low): Climate.hot_desert,
        (Temperature.temperate, Humidity.high): Climate.oceanic,
        (Temperature.temperate, Humidity.medium): Climate.mediterannean,
        (Temperature.temperate, Humidity.low): Climate.semi_arid,
        (Temperature.low, Humidity.high): Climate.tundra,
        (Temperature.low, Humidity.medium): Climate.cold_continental,
        (Temperature.low, Humidity.low): Climate.cold_desert
    }
    return climate_mapping.get((temperature, humidity), None)