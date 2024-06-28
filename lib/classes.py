from datetime import date
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union
from utils import truncate_str, gen_hash


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

class ConstraintType(Enum):
    DATE = auto()
    DEBUT = auto()
    TOUR = auto()
    PLAY_AMT = auto()
    PLAYED_AT = auto()

class Constraint:
    def __init__(self, c_type: ConstraintType, value: Union[date]):
        self.constraint_type = c_type
        self.songs: set[str] = set()  # list of song hashes
        self.value: Union[date] = value  # changes in meaning depending on constraint type
        self.id = Constraint.gen_constraint_hash(c_type.value, value)
    
    @property
    def text(self) -> str:
        match self.constraint_type:
            case ConstraintType.DATE:
                # id is the tour date
                return f"Played on {self.value.strftime("%b %d, %Y")}"
            case ConstraintType.DEBUT:
                raise ValueError("debut not implemented")
            case ConstraintType.TOUR:
                raise ValueError("tour not implemented")
            case ConstraintType.PLAY_AMT:
                raise ValueError("play_amt not implemented")
            case ConstraintType.PLAYED_AT:
                raise ValueError("played_at not implemented")
    
    def gen_constraint_hash(c_type: int, value: str):
        return gen_hash(str(c_type) + value, 10)
    
    def to_dict(self) -> dict:
        constraint_dict = {"type": self.constraint_type.value, "value": self.value}
        hash = Constraint.gen_constraint_hash(self.constraint_type.value, self.value)
        constraint_dict["songs"] = []
        constraint_dict["id"] = hash
        for song_hash in list(self.songs):
            constraint_dict["songs"].append(song_hash)
        return constraint_dict

    def from_dict(d: dict):
        c_type = ConstraintType(d["type"])
        out = Constraint(c_type, d["value"])
        for song in d["songs"]:
            out.songs.add(song)
        return out
    
    
class TightGame:
    def __init__(self):
        self.songs = [[None]*3, [None]*3, [None]*3]
        self.dates = [[None]*3, [None]*3]
    
    def __repr__(self):
        return (
            f"{'': <15}{str(self.dates[0][0]): ^25}{str(self.dates[0][1]): ^25}{str(self.dates[0][2]): >25} \n"
            f"{str(self.dates[1][0]): <15}{truncate_str(self.songs[0][0], 20): ^25}{truncate_str(self.songs[0][1], 20): ^25}{truncate_str(self.songs[0][2], 20): >25} \n"
            f"{str(self.dates[1][1]): <15}{truncate_str(self.songs[1][0], 20): ^25}{truncate_str(self.songs[1][1], 20): ^25}{truncate_str(self.songs[1][2], 20): >25} \n"
            f"{str(self.dates[1][2]): <15}{truncate_str(self.songs[2][0], 20): ^25}{truncate_str(self.songs[2][1], 20): ^25}{truncate_str(self.songs[2][2], 20): >25} \n"
        )

class Game:
    def __init__(self):
        # self.constraint_ids: list[list[Optional[str]]] = [[None]*3, [None]*3]
        self.constraints: list[list[Optional[Constraint]]] = [[None]*3, [None]*3]
    
    @property
    def ids(self) -> list[str]:
        return [c.id for c in (self.constraints[0] + self.constraints[1])]
    # def load(self, constraint_db):
    #     # populates constraints from ids
    #     for i, row_or_col in enumerate(self.constraint_ids):
    #         for j, id in enumerate(row_or_col):
    #             self.constraints[i][j] = Constraint.from_dict(constraint_db[id])