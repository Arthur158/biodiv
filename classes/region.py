from typing import Dict
from classes.climate import Climate
from classes.population import Population
from constants import CLIMATE_TO_RESOURCES, DATABASE_NAME
from database_handler import DatabaseHandler

class Region:
    def __init__(self, name: str, climate: Climate, db_name = DATABASE_NAME) -> None:

        self.climate: Climate = climate
        self.name = name
        self.sunlight_available = CLIMATE_TO_RESOURCES[Climate(self.climate)]
        self.populations: Dict[str, Population] = dict()
        
        self.db_handler = DatabaseHandler(db_name)

    def add_population(self, population: Population):
        self.populations[population.species.name] = population

    def remove_population(self, species_name):
        del self.populations[species_name]

    def empty_out(self):
        self.populations = dict()
