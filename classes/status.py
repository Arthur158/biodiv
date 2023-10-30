from enum import Enum, auto

class Status(Enum):
    closed = "closed"
    paused = "paused"
    playing = "playing"