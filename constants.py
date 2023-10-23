#constants

from classes.climate import Climate


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
DATABASE_NAME = "planet.db";