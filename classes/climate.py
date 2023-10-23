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
    hot_desert = 3
    oceanic = 4
    mediterannean = 5
    semi_arid = 6
    tundra = 7
    cold_continental = 8
    cold_desert = 9

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