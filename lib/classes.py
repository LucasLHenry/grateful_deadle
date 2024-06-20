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
    
class Game:
    def __init__(self):
        self.songs = [[None]*3, [None]*3, [None]*3]
        self.dates = [[None]*3, [None]*3]
    
    def __repr__(self):
        def truncate_str(s: str, max_len: int):
            if len(s) > max_len:
                return s[:max_len - 1] + "..."
            return s
        
        return (
            f"{'': <15}{str(self.dates[0][0]): ^25}{str(self.dates[0][1]): ^25}{str(self.dates[0][2]): >25} \n"
            f"{str(self.dates[1][0]): <15}{truncate_str(self.songs[0][0], 20): ^25}{truncate_str(self.songs[0][1], 20): ^25}{truncate_str(self.songs[0][2], 20): >25} \n"
            f"{str(self.dates[1][1]): <15}{truncate_str(self.songs[1][0], 20): ^25}{truncate_str(self.songs[1][1], 20): ^25}{truncate_str(self.songs[1][2], 20): >25} \n"
            f"{str(self.dates[1][2]): <15}{truncate_str(self.songs[2][0], 20): ^25}{truncate_str(self.songs[2][1], 20): ^25}{truncate_str(self.songs[2][2], 20): >25} \n"
        )