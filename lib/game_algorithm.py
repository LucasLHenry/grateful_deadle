from lib.classes import Setlist, Song, Game
from typing import Iterator, Optional
import constraint as csp
from lib.database.db_utils import get_all_dates
from lib.database.db_parser import get_reverse_db, get_all_songs, get_setlist_list
from ortools.sat.python import cp_model
from datetime import date

# def generate_games() -> list[dict]:
#     # this problem will be formatted as a CSP (constraint satisfaction problem).
#     setlists = get_setlist_list()
#     all_songs = get_all_songs()
#     all_dates = get_all_dates(setlists)
#     reverse_db = get_reverse_db()
    
#     problem = csp.Problem()
#     for i in range(3):
#         problem.addVariable(f"row{i}", all_dates)
#         problem.addVariable(f"col{i}", all_dates)
#         for j in range(3):
#             problem.addVariable(f"cell{i}{j}", [song.name for song in all_songs])
    
#     problem.addConstraint(csp.AllDifferentConstraint())
    
#     for i in range(3):
#         for j in range(3):
#             problem.addConstraint(lambda date, songname: date in reverse_db[songname], (f"col{i}", f"cell{j}{i}"))
#             problem.addConstraint(lambda date, songname: date in reverse_db[songname], (f"row{i}", f"cell{i}{j}"))
    
#     return problem.getSolution()

# def generate_games_ortool() -> list[dict]:
#     setlists: list[Setlist] = get_setlist_list()
#     all_dates: list[date] = get_all_dates(setlists)
#     all_songs: list[str] = [song.name for song in get_all_songs()]
#     reverse_db: dict[str, list[date]] = get_reverse_db()
    
#     date_domain = cp_model.Domain.from_values(all_dates)
#     song_domain = cp_model.Domain.from_values(all_songs)
    
#     model = cp_model.CpModel()
    
#     date_vars = [[], []]
#     song_vars = [[], [], []]
#     for i in range(3):
#         date_vars[0].append(model.new_int_var_from_domain(date_domain, f"row{i}"))
#         date_vars[1].append(model.new_int_var_from_domain(date_domain, f"col{i}"))
#         for j in range(3):
#             song_vars[i].append(model.new_int_var_from_domain(song_domain, f"cell{i}{j}"))
        
#     date_vars_flat = date_vars[0].extend(date_vars[1])
#     song_vars_flat = song_vars[0].extend(song_vars[1].extend(song_vars[2]))
    
#     model.add_all_different(date_vars_flat)
#     model.add_all_different(song_vars_flat)
    
#     solver = cp_model.CpSolver()
#     solver.solve(model)
#     print(solver.solution_info())

# import random as r
def setlist_list_to_fwd_db(setlists: list[Setlist]) -> dict[date, set[str]]:
    out_dict: dict[date, set[str]] = dict()
    for setlist in setlists:
        out_dict[setlist.date] = set(setlist.songnames)
    return out_dict        

def generate_games_raw():
    setlists: list[Setlist] = get_setlist_list()
    all_dates: list[date] = get_all_dates(setlists)
    all_songs: list[str] = [song.name for song in get_all_songs()]
    reverse_db: dict[str, set[date]] = get_reverse_db()
    forward_db: dict[date, set[str]] = setlist_list_to_fwd_db(setlists)
    game = Game()
    return recursive_search(game, 0, all_dates, forward_db)
    

def recursive_search(
        game: Game, 
        depth: int, 
        all_dates: list[date], 
        db: dict[date, set[str]]
    ) -> Optional[Game]:
    variable_indices_in_assignment_order = [(0,0), (1,0), (0,0), (0,1), (1,1), (1,1), (0,1), (1,0), (0,2), (1,2), (2,2), (0,2), (2,0), (1,2), (2,1)]
    variable_is_date_in_assignment_order = [1,     1,     0,     1,     1,     0,     0,     0,     1,     1,     0,     0,     0,     0,     0    ]
    
    if depth >= 15: return game
    
    x, y = variable_indices_in_assignment_order[depth]
    if variable_is_date_in_assignment_order[depth] == 1:  # it's a date
        for date in all_dates:  # because of the search order, dates are never constrained
            if date not in (game.dates[0] + game.dates[1]):  # must be a new date
                game.dates[x][y] = date  # assign
                soln = recursive_search(game, depth+1, all_dates, db)  # test assignment
                if soln is not None: return soln  # good soln
                else: game.dates[x][y] = None  # bad soln, undo assignment
        return None  # no solutions, backtrack
    else:  # it's a song
        # because of order, songs always have both relevant dates already assigned
        # use set intersection to make search space smaller
        for song in (db[game.dates[0][y]] & db[game.dates[1][x]]):
            if song not in (game.songs[0] + game.songs[1] + game.songs[2]):  # must be unique
                game.songs[x][y] = song  # assign
                soln = recursive_search(game, depth+1, all_dates, db)  # test assignment
                if soln is not None: return soln  # good soln, return
                else: game.songs[x][y] = None  # bad soln, undo assignment
        return None  # no solutions, backtrack