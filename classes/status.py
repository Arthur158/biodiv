from enum import Enum, auto

class Status(Enum):
    closed = auto()
    paused = auto()
    playing = auto()