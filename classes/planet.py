import math
from typing import Dict, List
from classes.climate import Climate
from classes.diet import Trophic_type
from classes.population import Population
from classes.region import Region
from classes.species import Species
from classes.status import Status
from constants import CLIMATE_TO_RESOURCES, DATABASE_NAME
from database_handler import DatabaseHandler


class Planet:
    def __init__(self, database_name = DATABASE_NAME) -> None:
        self.status = Status.closed
        self.regions: Dict[str, Region] = dict()
        self.species: Dict[str, Region] = dict()
        self.db_handler = DatabaseHandler(database_name)
        self.year = 0
        

    def get_from_database(self):
        self.status = Status.paused

        self.regions = dict()
        self.species = dict()

        species = self.db_handler.execute_sql_query("SELECT name,trophic_type,heterotroph_level FROM species")
        self.species = {specie[0]: Species(specie[0], Trophic_type(specie[1]), specie[2]) for specie in species}

        regions = self.db_handler.execute_sql_query("SELECT name, climate FROM regions")
        self.regions = {region[0]: Region(region[0], Climate(region[1])) for region in regions}

        for region in self.regions.values():
            populations = self.db_handler.execute_sql_query(f"SELECT species, population_size from populations where populations.region = ?", (region.name,))
            for population in populations:
                region.add_population(Population(self.species[population[0]], population[1]))


    def save_simulation(self):

        self.db_handler.remove_all()

        for specie in self.species.values():

            self.db_handler.insert_species(specie.name, specie.trophic_type.value, specie.heterotroph_level)

        for region in self.regions.values():
            
            self.db_handler.insert_region(region.name, region.climate.value)

            for population in region.populations.values():
                print(str(population))
                self.db_handler.insert_population(population.species.name, population.population_size, region.name)

        
    def empty_out(self):
        species = dict()

        for region in self.regions.values():
            region.empty_out()

        self.regions = dict()


    def execute_generation(self):

        for region in self.regions.values():

            print(f"initial pops: {[str(pop) for pop in region.populations.values()]}")
            autotrophic_populations: List[Population] = []
            heterotrophic_populations: List[Population] = []
            herbivorous_populations: List[Population] = []
            carnivorous_populations: List[Population] = [population for population in heterotrophic_populations if population.species.heterotroph_level < 100]

            for population in region.populations.values():
                if population.species.trophic_type == Trophic_type.autotrophic:
                    autotrophic_populations.append(population)
                elif population.species.trophic_type == Trophic_type.heterotrophic:
                    heterotrophic_populations.append(population)

            for population in heterotrophic_populations:
                if population.species.heterotroph_level < 100:
                    carnivorous_populations.append(population)
                elif population.species.heterotroph_level > 0:
                    herbivorous_populations.append(population)
                    
             
            #distribute food to autotrophic populations
            resources = CLIMATE_TO_RESOURCES[Climate(region.climate)]      #gets the resources available in the region
            pool = resources[0] + resources[1]                    #adds them up for now, should change in the future

            gathering_powers = [population.population_size * population.species.effectiveness[0] for population in autotrophic_populations]
            total_gathering_power = sum(gathering_powers)

            # Figuring out which population get which part of the pool
            for index, population in enumerate(autotrophic_populations):
                population.food_collected += pool * (gathering_powers[index] / total_gathering_power)
                print(f"{population.species.name} autotroph: population.food_collected: {population.food_collected} += pool: {pool} * (gathering_powers[index]: {gathering_powers[index]} / total_gathering_power: {total_gathering_power})")
                print("----")



            #distribute food to herbivores
            

            # print(f"herbivo: {herbivorous_populations}")


            for autotrophic_population in autotrophic_populations:

                pool = autotrophic_population.species.food_content * autotrophic_population.population_size

                gathering_powers = [population.population_size * population.species.effectiveness[1] for population in herbivorous_populations]
                # gathering power for each of the heterotrophic populations. Later on, it will be specific to the autotrophic population we are looking at,
                # hence it is in the for loop.
                total_gathering_power = sum(gathering_powers)

                # Figuring out which population get which part of the pool
                for index, population in enumerate(herbivorous_populations):

                    food_taken = pool * (gathering_powers[index] / total_gathering_power)
                    print(f"food taken for {population.species.name}: {pool} * ({gathering_powers[index]} / {total_gathering_power})")
                    population.grass_collected += food_taken
                    population.grass_debts[autotrophic_population] = gathering_powers[index] / total_gathering_power
                    print(f"grass debt from {population.species.name} to {autotrophic_population.species.name} is {population.grass_debts[autotrophic_population]}")
                    print("---")


            # breakpoint()

            #distribute food to carnivores
            for predated_population in heterotrophic_populations:

                pool = predated_population.species.food_content * predated_population.population_size


                gathering_powers = [population.population_size * population.species.effectiveness[2] if population is not predated_population else 0.0 for population in carnivorous_populations]
                # gathering power for each of the heterotrophic populations. Later on, it will be specific to the autotrophic population we are looking at,
                # hence it is in the for loop.
                total_gathering_power = sum(gathering_powers)

                # Figuring out which population get which part of the pool
                for population in carnivorous_populations:
                    if population is not predated_population:
                        food_taken = pool * (gathering_powers[index] / total_gathering_power if total_gathering_power > 0 else 0)
                        print(f"food hunted by {population.species.name} : {food_taken} = pool: {pool} * gatherpower {gathering_powers[index]} / {total_gathering_power}")
                        population.meat_collected += food_taken
                        if(food_taken != 0):
                            population.meat_debts[predated_population] = gathering_powers[index] / total_gathering_power
                            print(f"meat debt from {population.species.name} to {predated_population.species.name} is {population.meat_debts[predated_population]}")
                        print("---")

            #see how much of their food pool each population eats.    
            for population in region.populations.values():

                ratio: float = 0

                if(population.species.trophic_type == Trophic_type.heterotrophic and population.species.heterotroph_level is not None):

                    ratio_grass, ratio_meat = 0.0, 0.0

                    if(population.species.heterotroph_level > 0):

                        ratio_grass =  (population.grass_collected * 100) / (population.population_size * population.species.cost * 5 * population.species.heterotroph_level)
                        print(f"ratio grass for {population.species.name} : grass_collected: {population.grass_collected} / pop size: {population.population_size} * pop species cost: {population.species.cost} * population species hetero level: {population.species.heterotroph_level}")
                        #iterate through its grass debts
                        if ratio_grass != 0:
                            for predated_population, pool_share in population.grass_debts.items():
                                predated_population.losse_to_predation += pool_share * (1 / ratio_grass)
                    if(population.species.heterotroph_level < 100):

                        ratio_meat = (population.meat_collected * 100) / (population.population_size * population.species.cost * 5 * (100 - population.species.heterotroph_level))
                        print(f"ratio of meat for {population.species.name}: meat collected: {population.meat_collected} * 100 / pop size {population.population_size} * species.cost: {population.species.cost} * hetero: {100 - population.species.heterotroph_level}")
                        if ratio_meat != 0:   
                            for predated_population, pool_share in population.meat_debts.items():
                                predated_population.losse_to_predation += pool_share * (1 / ratio_meat)

                    ratio =  (min(1, ratio_meat) * (100 - population.species.heterotroph_level) + min(1 ,ratio_grass) * population.species.heterotroph_level) / 100

                else:
                    ratio = min(population.food_collected / (population.population_size * population.species.cost), 1.0)
                    print(f"ratio  of sun for {population.species.name}: {ratio}")

                print(f"ratio of food for {population.species.name} was {ratio}")
                population.growth_factor *= ratio * 1.2
                print(f"growth factor: {population.growth_factor}")
                print("-----")

            #see how much each population has been predated
            for population in region.populations.values():
                population.growth_factor *= (1 - 0.12 * population.losse_to_predation)
                print(f"pop {population.species.name} lost {population.losse_to_predation} to predation")
                print(f"-------")

            #here introduce other factors

            for population in list(region.populations.values()):
                
                # print(f"pop size before: {population.population_size}")

                population.grow()

                # print(f"pop size after: {population.population_size}")


                if population.population_size <= 0:
                   # EXTINCTION
                   region.remove_population(population.species.name)

                else:
                    population.growth_factor = 1
                    population.food_collected, population.grass_collected, population.losse_to_predation = 0, 0, 0

                    population.meat_debts = dict()
                    population.grass_debts = dict()
                    print(f"list {[str(pop) for pop in region.populations.values()]}")

            # print(f"keys to remove: {keys_to_remove}")
            # print(f"before removal: {region.populations}")
            # for key in keys_to_remove:
            # print(f"after removal: {region.populations}")
        # for region in self.regions.values():
        #     print(f"list after {[str(pop) for pop in region.populations.values()]}")

        self.year += 1

    def add_species(self, species: Species):
        self.species[species.name] = species
        self.db_handler.insert_species(species.name, species.trophic_type.value, species.heterotroph_level)

    def add_region(self, region: Region):
        self.regions[region.name] = region
        self.db_handler.insert_region(region.name, region.climate.value)
