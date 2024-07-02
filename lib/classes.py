from datetime import date
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union
from utils import truncate_str, gen_hash, parse_date_str


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
    def __init__(self, c_type: ConstraintType, value: str):
        self.constraint_type = c_type
        self.songs: set[str] = set()  # list of song hashes
        self.value: str = value  # changes in meaning depending on constraint type
        self.id = Constraint.gen_constraint_hash(c_type.value, value)
    
    def __str__(self) -> str:
        match self.constraint_type:
            case ConstraintType.DATE:
                # id is the tour date
                return f"Played on {parse_date_str(self.value).strftime("%b %d, %Y")}"
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
    
    def __str__(self):
        return (
            f"{'': <15}{str(self.dates[0][0]): ^25}{str(self.dates[0][1]): ^25}{str(self.dates[0][2]): >25} \n"
            f"{str(self.dates[1][0]): <15}{truncate_str(self.songs[0][0], 20): ^25}{truncate_str(self.songs[0][1], 20): ^25}{truncate_str(self.songs[0][2], 20): >25} \n"
            f"{str(self.dates[1][1]): <15}{truncate_str(self.songs[1][0], 20): ^25}{truncate_str(self.songs[1][1], 20): ^25}{truncate_str(self.songs[1][2], 20): >25} \n"
            f"{str(self.dates[1][2]): <15}{truncate_str(self.songs[2][0], 20): ^25}{truncate_str(self.songs[2][1], 20): ^25}{truncate_str(self.songs[2][2], 20): >25} \n"
        )

class Game:
    def __init__(self):
        self.top_constraints: list[Optional[Constraint]] = [None] * 3
        self.side_constraints: list[Optional[Constraint]] = [None] * 3
        self.constraints: list[list[Optional[Constraint]]] = [[None]*3, [None]*3]
    
    @property
    def ids(self) -> list[str]:
        # return [c.id for c in (self.constraints[0] + self.constraints[1]) if c is not None]
        return [c.id for c in (self.top_constraints + self.side_constraints) if c is not None]
    
    def possibilities_at(self, x: int, y: int) -> set[str]:
        c1 = self.top_constraints[x].songs if self.top_constraints[x] is not None else set()
        c2 = self.side_constraints[y].songs if self.side_constraints[y] is not None else set()
        if len(c1) == 0 and len(c2) == 0:
            return set(str(range(999)))
        elif len(c1) == 0: return c2
        elif len(c2) == 0: return c1
        return c1 & c2
    
    def is_valid(self) -> bool:
        for i in range(3):
            for j in range(3):
                if len(self.possibilities_at(i, j)) == 0: return False
        return True
                
    def __str__(self) -> str:
        return (
            f"{'': <15}{str(self.top_constraints[0]): ^25}{str(self.top_constraints[1]): ^25}{str(self.top_constraints[2]): >25} \n"
            f"{str(self.side_constraints[0]): <15}{len(self.possibilities_at(0, 0)): ^25}{len(self.possibilities_at(1, 0)): ^25}{len(self.possibilities_at(2, 0)): >25} \n"
            f"{str(self.side_constraints[1]): <15}{len(self.possibilities_at(0, 1)): ^25}{len(self.possibilities_at(1, 1)): ^25}{len(self.possibilities_at(2, 1)): >25} \n"
            f"{str(self.side_constraints[2]): <15}{len(self.possibilities_at(0, 2)): ^25}{len(self.possibilities_at(1, 2)): ^25}{len(self.possibilities_at(2, 2)): >25} \n"
        )
    # def load(self, constraint_db):
    #     # populates constraints from ids
    #     for i, row_or_col in enumerate(self.constraint_ids):
    #         for j, id in enumerate(row_or_col):
    #             self.constraints[i][j] = Constraint.from_dict(constraint_db[id])