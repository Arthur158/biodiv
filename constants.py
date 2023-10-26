#constants

from classes.climate import Climate
from classes.status import Status

DATABASE_NAME = "planet.db"
SPECIES_IMAGE_FOLDER = "static/images/species"
CLIMATE_TO_RESOURCES = {
    Climate.tropical_rainforest: (300,300),
    Climate.tropical_savanna: (300,200),
    Climate.hot_desert: (300,100),
    Climate.oceanic: (200,300),
    Climate.mediterannean: (200,200),
    Climate.cold_continental: (200,100),
    Climate.cold_desert: (100,300),
    Climate.semi_arid: (100,200),
    Climate.tundra: (100,100),
}
