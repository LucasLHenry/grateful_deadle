from datetime import date
from dataclasses import dataclass
from enum import Enum, auto

class Song:
    def __init__(self, name: str):
        self.name = name
    
    def to_dict(self) -> dict:
        out_dict = {}
        out_dict["name"] = self.name
        return out_dict


class Setlist:
    def __init__(self, venue: str, date: date):
        self.venue = venue
        self.date = date
        self.songs: set[Song] = set()

class SubmitType(Enum):
    SUMBIT = auto()
    CANCEL = auto()

@dataclass
class SubmitWindowInfo:
    song_name: str
    pos: tuple[int, int]
    status: SubmitType