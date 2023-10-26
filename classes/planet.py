from classes.region import Region
from classes.status import Status
from constants import DATABASE_NAME


class Planet:
    def __init__(self, database_name = DATABASE_NAME) -> None:
        self.status = Status.closed

    def start_simulation(self):
        self.status = Status.paused
        pass

    def stop_simulation(self):
        self.status = Status.closed

    def execute_generation(self):
        pass