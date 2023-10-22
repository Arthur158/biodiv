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
    tropical_rainforest = 1
    tropical_savanna = 2
    oceanic = 3
    mediterannean = 4
    semi_arid = 5
    tundra = 6
    cold_continental = 7
    cold_desert = 8

def infer_climate(humidity: Humidity, temperature: Temperature) -> Climate:
    climate_mapping = {
        (Temperature.high, Humidity.high): Climate.tropical_rainforest,
        (Temperature.high, Humidity.medium): Climate.tropical_savanna,
        (Temperature.temperate, Humidity.high): Climate.oceanic,
        (Temperature.temperate, Humidity.medium): Climate.mediterannean,
        (Temperature.low, Humidity.high): Climate.tundra,
        (Temperature.low, Humidity.medium): Climate.cold_continental
    }
    return climate_mapping.get((temperature, humidity), None)
