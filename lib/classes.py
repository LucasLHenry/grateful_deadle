from datetime import date
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

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
        self._songnames: list[str] = []
        
    @property
    def songnames(self):
        if len(self.songs) != len(self._songnames):
            self._songnames = [song.name for song in self.songs]
        return self._songnames
            


# these two classes (SubmitType and SubmitWindowInfo) are passed
# between the main window and the input window to provide info
# on what song was selected

class SubmitType(Enum):
    SUMBIT = auto()
    CANCEL = auto()

@dataclass
class SubmitWindowInfo:
    song_name: str
    pos: tuple[int, int]
    status: SubmitType
    
@dataclass
class Game:
    songs: list[list[Optional[Song]]]  # 3x3 (the grid (list of rows))
    dates: list[list[Optional[date]]]  # 2x3 (the edges (left then top))