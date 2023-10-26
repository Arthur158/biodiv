#constants

from classes.climate import Climate
from classes.status import Status


STRINGS_TO_CLIMATES = {
    "tropical_rainforest": Climate.tropical_rainforest,
    "tropical_savanna": Climate.tropical_savanna ,
    "hot_desert": Climate.hot_desert ,
    "oceanic": Climate.oceanic ,
    "mediterannean": Climate.mediterannean ,
    "cold_continental": Climate.cold_continental,
    "cold_desert": Climate.cold_desert,
    "semi_arid": Climate.semi_arid,
    "tundra": Climate.tundra,
}
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
STATUS_TO_STRING = {
    Status.closed: "closed",
    Status.paused: "paused",
    Status.playing: "playing"
}