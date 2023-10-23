from classes.region import Region


class Planet:
    def __init__(self) -> None:
       self.regions = [] 

    def add_region(self, region: Region):
        self.regions.append(region)