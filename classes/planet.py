import math
from typing import Dict, List
from classes.autotroph_species import AutotrophSpecies
from classes.climate import Climate
from classes.heterotroph_species import HeterotrophSpecies
from classes.population import Population
from classes.region import Region
from classes.species import Species
from classes.status import Status
from constants import CLIMATE_TO_RESOURCES, DATABASE_NAME
from database_handler import DatabaseHandler


class Planet:
    def __init__(self, database_name=DATABASE_NAME) -> None:
        """Initialize the Planet class with default values."""
        self.status = Status.closed
        self.regions: Dict[str, Region] = {}
        self.species: Dict[str, Species] = {}
        self.db_handler = DatabaseHandler(database_name)
        self.db_handler.create_table()
        self.year = 0
        

    def get_from_database(self):
        """Load regions and species from the database."""
        self.status = Status.paused
        self.regions, self.species = {}, {}
        
        # Fetch species and regions from the database
        species_data = self.db_handler.execute_sql_query("SELECT name, trophic_type, heterotroph_level FROM species")

        for specie_data in species_data:
            if(specie_data[1] == "autotrophic"):
                self.species[specie_data[0]] = AutotrophSpecies(specie_data[0])
            elif(specie_data[1] == "heterotrophic"):
                self.species[specie_data[0]] = HeterotrophSpecies(specie_data[0], specie_data[2])

        autotroph_species_data = self.db_handler.execute_sql_query("SELECT name, toxicity, height, depth_of_roots, size_of_leaves FROM autotroph_species")

        for autotroph_specie_data in autotroph_species_data:
            self.species.get(autotroph_specie_data[0]).update_stats(autotroph_specie_data[1], autotroph_specie_data[2], autotroph_specie_data[3], autotroph_specie_data[4])

        heterotroph_species_data = self.db_handler.execute_sql_query("SELECT name, armor, speed, strength, digestive_strength, height FROM heterotroph_species")

        for heterotroph_specie_data in heterotroph_species_data:
            self.species.get(heterotroph_specie_data[0]).update_stats(heterotroph_specie_data[1], heterotroph_specie_data[2], heterotroph_specie_data[3], heterotroph_specie_data[4], heterotroph_specie_data[5])


        region_data = self.db_handler.execute_sql_query("SELECT name, climate FROM regions")
        self.regions = {region[0]: Region(region[0], Climate(region[1])) for region in region_data}
        
        # Populate regions with their populations
        for region in self.regions.values():
            populations_data = self.db_handler.execute_sql_query("SELECT species, population_size FROM populations WHERE region=?", (region.name,))
            for population_data in populations_data:
                species = self.species[population_data[0]]
                population_size = population_data[1]
                region.add_population(Population(species, population_size))


    def save_simulation(self):
        """Save the current state of the simulation to the database."""
        # Clear existing data
        self.db_handler.remove_all()

        # Save species to the database
        for species in self.species.values():
            if isinstance(species, AutotrophSpecies):
                self.db_handler.insert_autotroph_species(species.name, species.toxicity, species.height, species.depth_of_roots, species.size_of_leaves)
            if isinstance(species, HeterotrophSpecies):
                self.db_handler.insert_heterotroph_species(species.name, "heterotrophic", species.heterotroph_level, species.armor, species.speed, species.strength, species.digestive_strength, species.height)

        # Save regions and their populations to the database
        for region in self.regions.values():
            self.db_handler.insert_region(region.name, region.climate.value)
            for population in region.populations.values():
                self.db_handler.insert_population(population.species.name, population.population_size, region.name)

        
    def empty_out(self):
        """Remove all species and empty out all regions."""
        self.species = {}
        for region in self.regions.values():
            region.empty_out()
        self.regions = {}

    def execute_generation(self):
        """Simulate one generation for all regions."""
        for region in self.regions.values():
            autotrophic_populations, heterotrophic_populations, herbivorous_populations, carnivorous_populations = self._categorize_populations(region)
            self._distribute_food_to_autotrophs(region, autotrophic_populations)
            self._distribute_food_to_herbivores(autotrophic_populations, herbivorous_populations)
            self._distribute_food_to_carnivores(heterotrophic_populations, carnivorous_populations)
            self._calculate_growth_factors(region)
            self._update_populations(region)
        self.year += 1

    def _categorize_populations(self, region):
        """Categorize populations based on their trophic type."""
        autotrophic_populations = [population for population in region.populations.values() if isinstance(population.species, AutotrophSpecies)]
        heterotrophic_populations = [population for population in region.populations.values() if isinstance(population.species, HeterotrophSpecies)]
        
        # Herbivorous populations have heterotroph_level greater than 0 but less than 100
        herbivorous_populations = [population for population in heterotrophic_populations if 0 < population.species.heterotroph_level]
        
        # Carnivorous populations have heterotroph_level less than 100
        carnivorous_populations = [population for population in heterotrophic_populations if population.species.heterotroph_level < 100]
        
        return autotrophic_populations, heterotrophic_populations, herbivorous_populations, carnivorous_populations


    def _distribute_food_to_autotrophs(self, region, autotrophic_populations):
        """Distribute food among autotrophic populations based on their gathering power."""
        resources = CLIMATE_TO_RESOURCES[Climate(region.climate)]
        
        #first, share resources from light.
        pool = resources[0]

        # Calculate the total gathering power of all autotrophic populations
        total_gathering_power = sum([population.population_size * population.species.effectiveness[0] for population in autotrophic_populations])
        
        # Distribute resources based on each population's proportion of the total gathering power
        for population in autotrophic_populations:
            population_gathering_power = population.population_size * population.species.effectiveness[0]
            population.food_collected += pool * (population_gathering_power / total_gathering_power)

        pool = resources[1]

    def _distribute_food_to_herbivores(self, autotrophic_populations, herbivorous_populations):
        """Distribute food among herbivorous populations."""
        for auto_population in autotrophic_populations:
            # Calculate the total food pool available for herbivores
            total_food_pool = auto_population.species.food_content * auto_population.population_size
            
            # Calculate the total gathering power of all herbivorous populations
            total_gathering_power = sum([population.population_size * population.species.effectiveness[1] for population in herbivorous_populations])
            
            # Distribute food among herbivorous populations based on their gathering power
            for population in herbivorous_populations:
                population_gathering_power = population.population_size * population.species.effectiveness[1]
                food_taken = total_food_pool * (population_gathering_power / total_gathering_power)
                population.grass_collected += food_taken
                population.grass_debts[auto_population] = population_gathering_power / total_gathering_power


    def _distribute_food_to_carnivores(self, heterotrophic_populations, carnivorous_populations):
        """Distribute food among carnivorous populations."""
        for prey_population in heterotrophic_populations:
            # Calculate the total food pool available for carnivores
            total_food_pool = prey_population.species.food_content * prey_population.population_size
            
            # Calculate the total gathering power of all carnivorous populations
            total_gathering_power = sum([predator.population_size * predator.species.effectiveness[2] for predator in carnivorous_populations if predator != prey_population])
            
            # Distribute food among carnivorous populations based on their gathering power
            for predator in carnivorous_populations:
                if predator != prey_population:
                    predator_gathering_power = predator.population_size * predator.species.effectiveness[2]
                    food_taken = total_food_pool * (predator_gathering_power / total_gathering_power if total_gathering_power > 0 else 0)
                    predator.meat_collected += food_taken
                    if food_taken:
                        predator.meat_debts[prey_population] = predator_gathering_power / total_gathering_power



    def _calculate_growth_factors(self, region):
        #see how much of their food pool each population eats.    
            for population in region.populations.values():

                ratio: float = 0

                if isinstance(population.species, HeterotrophSpecies):

                    ratio_grass, ratio_meat = 0.0, 0.0

                    if(population.species.heterotroph_level > 0):

                        ratio_grass =  (population.grass_collected * 100) / (population.population_size * population.species.cost * 5 * population.species.heterotroph_level)
                        #iterate through its grass debts
                        if ratio_grass != 0:
                            for predated_population, pool_share in population.grass_debts.items():
                                predated_population.losse_to_predation += pool_share * (1 / ratio_grass)

                    if(population.species.heterotroph_level < 100):

                        ratio_meat = (population.meat_collected * 100) / (population.population_size * population.species.cost * 5 * (100 - population.species.heterotroph_level))
                        if ratio_meat != 0:   
                            for predated_population, pool_share in population.meat_debts.items():
                                predated_population.losse_to_predation += pool_share * (1 / ratio_meat)

                    ratio =  (min(1, ratio_meat) * (100 - population.species.heterotroph_level) + min(1 ,ratio_grass) * population.species.heterotroph_level) / 100

                elif isinstance(population.species, AutotrophSpecies):
                    ratio = min(population.food_collected / (population.population_size * population.species.cost), 1.0)

                population.growth_factor *= ratio * 1.2

                        #see how much each population has been predated
            for population in region.populations.values():
                population.growth_factor *= (1 - 0.12 * population.losse_to_predation)

    def _update_populations(self, region):
        """Update the population size for all populations in a region."""
        for population in list(region.populations.values()):
            population.grow()
            if population.population_size <= 0:
                # Remove extinct populations
                region.remove_population(population.species.name)
            else:
                self._reset_population_attributes(population)

    def _reset_population_attributes(self, population):
        """Reset population attributes after each generation."""
        population.growth_factor = 1
        population.food_collected, population.grass_collected, population.meat_collected, population.losse_to_predation = 0, 0, 0, 0
        population.meat_debts, population.grass_debts = {}, {}

    def add_species(self, species: Species):
        self.species[species.name] = species
        self.db_handler.insert_species(species.name, species.trophic_type.value, species.heterotroph_level)

    def add_region(self, region: Region):
        self.regions[region.name] = region
        self.db_handler.insert_region(region.name, region.climate.value)
