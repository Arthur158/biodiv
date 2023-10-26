from classes.diet import Trophic_type
from classes.population import Population
from classes.region import Region
from classes.species import Species
from classes.status import Status
from constants import DATABASE_NAME
from database_handler import DatabaseHandler


class Planet:
    def __init__(self, database_name = DATABASE_NAME) -> None:
        self.status = Status.closed
        self.regions = None
        self.species = None
        self.db_handler = DatabaseHandler(database_name)
        

    def start_simulation(self):
        self.status = Status.paused

        species = self.db_handler.execute_sql_query("SELECT name,trophic_type,heterotroph_level FROM species")
        self.species = {specie[0]: Species(specie[0], Trophic_type(specie[1]), specie[2]) for specie in species}

        regions = self.db_handler.execute_sql_query("SELECT name, climate FROM regions")
        self.regions = [Region(region[0], region[1]) for region in regions]

        for region in self.regions:
            populations = self.db_handler.execute_sql_query(f"SELECT species, population_size from populations where populations.region = ?", (region.name,))
            region.add_populations([Population(self.species[population[0]], population[1]) for population in populations])

    def stop_simulation(self):
        self.status = Status.closed

        self.db_handler.remove_all()

        for specie in self.species.values():
            self.db_handler.insert_species(specie.name, specie.trophic_type.value, specie.heterotroph_level)

        for region in self.regions:
            self.db_handler.insert_region(region.name, region.climate)
            for population in region.populations:
                self.db_handler.insert_population(population.species.name, population.population_size, region.name)

        


    def execute_generation(self):
        pass