#constants

from classes.climate import Climate

AMOUNT_OF_POOLS = 4
MATCHUP_SEVERITY = 2
DATABASE_NAME = "planet.db"
SPECIES_IMAGE_FOLDER = "static/images/species"
CLIMATE_TO_RESOURCES = {
    Climate.tropical_rainforest: (300000,300000),
    Climate.tropical_savanna: (300000,200000),
    Climate.hot_desert: (300000,100000),
    Climate.oceanic: (200000,300000),
    Climate.mediterannean: (200000,200000),
    Climate.cold_continental: (200000,100000),
    Climate.cold_desert: (100000,300000),
    Climate.semi_arid: (100000,200000),
    Climate.tundra: (100000,100000),
}
