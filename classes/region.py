from typing import List
from classes.climate import Temperature, Humidity, Climate, infer_climate
from classes.population import Population
from constants import CLIMATE_TO_RESOURCES
from errors import InputError

class Region:
    def __init__(self, name: str, climate: Climate) -> None:
#        if temperature is None and humidity is None and climate is None:
#            raise InputError("The region was given neither a climate nor a humidity and a temperature")
#        elif climate is not None and (humidity is not None or temperature is not None):
#            raise InputError("The region was given both a climate and a humidity or a temperature")
#        elif humidity is None and temperature is not None:
#            raise InputError("The region was given a temperature but no humidity")
#        elif humidity is not None and temperature is None:
#            raise InputError("The region was given a humidity but no temperature")
#        elif climate is not None:
#            self.climate = climate
#        else:
#            self.climate = infer_climate(temperature, humidity) 
        self.climate: Climate = climate
        self.name = name
        self.sunlight_available = CLIMATE_TO_RESOURCES[Climate(self.climate)]
        self.populations: List[Population] = []

    def add_population(self, population: Population):
        self.populations.append(population)

    def add_populations(self, populations: List[Population]):
        self.populations.extend(populations)
       