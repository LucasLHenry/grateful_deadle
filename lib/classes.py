from datetime import date
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Callable, TypeVar
from lib.database.utils import gen_hash, parse_date_str, wrap
from lib.database.utils import (
    get_songname_from_hash, 
    get_hash_from_songname,
    db_type
)
from CONFIG import MINIMUM_SOLUTION_POSSIBILITES
import constraint as csp
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets, QtCore
import threading as tr
from time import perf_counter
import lib.stylesheets as ss
from functools import partial

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
    PLAYED_AT = auto()
    DEBUT = auto()
    TOUR = auto()
    PLAY_AMT_RANGE = auto()
    PLAY_AMT_TOUR = auto()
    SPECIAL_SHOW = auto()
    


class Constraint:
    def __init__(self, c_type: ConstraintType, value: str):
        self.constraint_type = c_type
        self.songs: set[str] = set()  # list of song hashes
        self.value: str = value  # changes in meaning depending on constraint type
        self.id = Constraint.gen_constraint_hash(c_type.value, value)
    
    def __str__(self) -> str:
        match self.constraint_type:
            case ConstraintType.DATE:
                # id is "date at venue"
                return f"Performed on {self.value}"
            case ConstraintType.DEBUT:
                # id is "date at venue"
                return f"Debuted on {self.value}"
            case ConstraintType.TOUR:
                # id is tour
                return f"Played during {self.value}"
            case ConstraintType.PLAYED_AT | ConstraintType.SPECIAL_SHOW:
                # id is venue
                return f"Played at {self.value}"
            case ConstraintType.PLAY_AMT_RANGE:
                # id is "number to number"
                return f"Played {self.value} times"
    
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
    
    def details(self) -> str:
        match self.constraint_type:
            case ConstraintType.DATE:
                out =  """
                This song must have been played by the Grateful Dead during their show on the given date.
                """
            case ConstraintType.DEBUT:
                out =  """
                This song must have been first played by the Grateful Dead during their show on the given date.
                """
            case ConstraintType.TOUR:
                out =  """
                This song must have been played by the Grateful Dead at some point during the given tour.
                """
            case ConstraintType.PLAYED_AT | ConstraintType.SPECIAL_SHOW:
                out =  """
                This song must have been played by the Grateful Dead at some point during their careers
                at the given venue.
                """
            case ConstraintType.PLAY_AMT_RANGE:
                out =  """
                Over the course of their career, the Grateful Dead must have played this song an amount
                of times in the given range.
                """
        return out.strip().replace('\n', '')


class ConstraintDisplay():
    def __init__(self, qt_object: QtWidgets.QPushButton):
        self._obj = qt_object
        self.constraint: Constraint | None = None
    
    def connect_clicked_callback(self, callback_fn: Callable):
        if self.constraint is None: raise ValueError("must set constraint first")
        self._obj.clicked.connect(partial(callback_fn, self.constraint.details()))
    
    def show_text(self):
        if self.constraint is None: raise ValueError("must set constraint first")
        self._obj.setText(wrap(str(self.constraint), 15))
    
    def style(self):
        self._obj.setStyleSheet(ss.display_ss)

class Game:
    def __init__(self):
        self.top_constraints: list[Optional[Constraint]] = [None] * 3
        self.side_constraints: list[Optional[Constraint]] = [None] * 3
        self._possibilites: Optional[list[set[str]]] = None
    
    @property
    def ids(self) -> list[str]:
        return [c.id for c in (self.top_constraints + self.side_constraints) if c is not None]
    
    def possibilities_at(self, x: int, y: int) -> set[str]:
        c1 = self.top_constraints[x].songs if self.top_constraints[x] is not None else set()
        c2 = self.side_constraints[y].songs if self.side_constraints[y] is not None else set()
        if len(c1) == 0 and len(c2) == 0:
            return set(str(list(range(10))))  # flag value, definitely computationally inefficient though
        elif len(c1) == 0: return c2
        elif len(c2) == 0: return c1
        return c1 & c2
    
    def is_valid(self) -> bool:
        # each song square must have at least min_soln_possibilites solutions
        for i in range(3):
            for j in range(3):
                if len(self.possibilities_at(i, j)) < MINIMUM_SOLUTION_POSSIBILITES:
                    return False
        
        # also, there must be a solution where all the songs are different
        problem = csp.Problem()
        for i in range(3):
            for j in range(3):
                problem.addVariable(f"{i}{j}", list(self.possibilities_at(i, j)))
        problem.addConstraint(csp.AllDifferentConstraint())
        if problem.getSolution() is None:
            return False
        
        # each constraint combo must actually constrain that tile (less possibilities than either of them)
        for i in range(3):
            for j in range(3):
                if self.top_constraints[i] is None: continue
                if self.side_constraints[j] is None: continue
                tile_possibilities = len(self.possibilities_at(i, j))
                if tile_possibilities == len(self.top_constraints[i].songs):
                    return False
                if tile_possibilities == len(self.side_constraints[j].songs):
                    return False
        
        return True
                
    def __str__(self) -> str:
        return (
            f"{'': <15}{str(self.top_constraints[0]): ^25}{str(self.top_constraints[1]): ^25}{str(self.top_constraints[2]): >25} \n"
            f"{str(self.side_constraints[0]): <15}{len(self.possibilities_at(0, 0)): ^25}{len(self.possibilities_at(1, 0)): ^25}{len(self.possibilities_at(2, 0)): >25} \n"
            f"{str(self.side_constraints[1]): <15}{len(self.possibilities_at(0, 1)): ^25}{len(self.possibilities_at(1, 1)): ^25}{len(self.possibilities_at(2, 1)): >25} \n"
            f"{str(self.side_constraints[2]): <15}{len(self.possibilities_at(0, 2)): ^25}{len(self.possibilities_at(1, 2)): ^25}{len(self.possibilities_at(2, 2)): >25} \n"
        )
    
    def print_all_info(self, db):
        print("constraints and possibilites:")
        print(str(self))
        for i in range(3):
            for j in range(3):
                print(f"songs at {i+1}, {j+1}:")
                for song_hash in self.possibilities_at(i, j):
                    print(f"\t{get_songname_from_hash(song_hash, db)}")
 

class SquareStatus(Enum):
    CORRECT = auto()
    INCORRECT = auto()
    UNFILLED = auto()
    OVERCONSTRAINED = auto()
    
CORRECT = SquareStatus.CORRECT
INCORRECT = SquareStatus.INCORRECT
UNFILLED = SquareStatus.UNFILLED
OVERCONSTRAINED = SquareStatus.OVERCONSTRAINED
                   
class GridSquare:
    def __init__(self, 
                 pos: tuple[int, int], 
                 qt_object: QtWidgets.QPushButton, 
                 wrap_chars: int,
                 db: db_type
                ):
        self._obj = qt_object
        self.x, self.y = pos
        self.wrap_len = wrap_chars
        self.status = SquareStatus.UNFILLED
        self.text = "—"
        self.song_hash: str|None = None
        self.possibilities: set[str] = set()
        self._db = db
    
    def connect_click_callback(self, callback_fn: Callable):
        self._obj.clicked.connect(partial(callback_fn, self.x, self.y))
        
    def set_enable(self, enabled: bool):
        self._obj.setEnabled(enabled)
        
    def update(self, song_hash: str):
        self.song_hash = song_hash
        self.status = CORRECT if song_hash in self.possibilities else INCORRECT
        self.show()
    
    def clear(self):
        self.status = UNFILLED
        self.song_hash = None
        self.show()
    
    def show(self):
        sheet = ss.button_ss_default
        match self.status:
            case SquareStatus.CORRECT:
                sheet = ss.button_ss_correct
            case SquareStatus.INCORRECT:
                sheet = ss.button_ss_incorrect
            case SquareStatus.OVERCONSTRAINED:
                sheet = ss.button_ss_overconstrained
        self._obj.setStyleSheet(sheet)
        
        if self.status in (CORRECT, INCORRECT):
            self.text = get_songname_from_hash(self.song_hash)
        else:
            self.text = "—"
        self._obj.setText(wrap(self.text, self.wrap_len))
        
        self.set_enable(self.status != OVERCONSTRAINED)
            
    
    def check_overconstrained(self, used_hashes: set[str]):
        if len(self.possibilities - used_hashes) == 0:
            if self.status == UNFILLED:
                self.status = OVERCONSTRAINED
        else:
            if self.status == OVERCONSTRAINED:
                self.status = UNFILLED
        self.show()
        
        
        

# T = TypeVar('T')
# class restartingThread():
#     finished = pyqtSignal(T)
#     def __init__(self, func: Callable[[], T], timeout_ms: int):
#         self._f = func
#         self._timeout = timeout_ms
#         self.thread = tr.Thread(target=self._f, args=(), daemon=True)
    
#     def start(self):
#         self._time_ms = -perf_counter() / 1000