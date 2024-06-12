from lib.classes import Setlist, Song, Game
from typing import Iterator, Optional
import constraint as csp
from lib.database.db_utils import get_all_dates
from lib.database.db_parser import get_reverse_db, get_all_songs, get_setlist_list
from ortools.sat.python import cp_model
from datetime import date

def generate_games() -> list[dict]:
    # this problem will be formatted as a CSP (constraint satisfaction problem).
    setlists = get_setlist_list()
    all_songs = get_all_songs()
    all_dates = get_all_dates(setlists)
    reverse_db = get_reverse_db()
    
    problem = csp.Problem()
    for i in range(3):
        problem.addVariable(f"row{i}", all_dates)
        problem.addVariable(f"col{i}", all_dates)
        for j in range(3):
            problem.addVariable(f"cell{i}{j}", [song.name for song in all_songs])
    
    problem.addConstraint(csp.AllDifferentConstraint())
    
    for i in range(3):
        for j in range(3):
            problem.addConstraint(lambda date, songname: date in reverse_db[songname], (f"col{i}", f"cell{j}{i}"))
            problem.addConstraint(lambda date, songname: date in reverse_db[songname], (f"row{i}", f"cell{i}{j}"))
    
    return problem.getSolution()

def generate_games_ortool() -> list[dict]:
    setlists: list[Setlist] = get_setlist_list()
    all_dates: list[date] = get_all_dates(setlists)
    all_songs: list[str] = [song.name for song in get_all_songs()]
    reverse_db: dict[str, list[date]] = get_reverse_db()
    
    date_domain = cp_model.Domain.from_values(all_dates)
    song_domain = cp_model.Domain.from_values(all_songs)
    
    model = cp_model.CpModel()
    
    date_vars = [[], []]
    song_vars = [[], [], []]
    for i in range(3):
        date_vars[0].append(model.new_int_var_from_domain(date_domain, f"row{i}"))
        date_vars[1].append(model.new_int_var_from_domain(date_domain, f"col{i}"))
        for j in range(3):
            song_vars[i].append(model.new_int_var_from_domain(song_domain, f"cell{i}{j}"))
        
    date_vars_flat = date_vars[0].extend(date_vars[1])
    song_vars_flat = song_vars[0].extend(song_vars[1].extend(song_vars[2]))
    
    model.add_all_different(date_vars_flat)
    model.add_all_different(song_vars_flat)
    
    solver = cp_model.CpSolver()
    solver.solve(model)
    print(solver.solution_info())

import random as r

def generate_games_raw():
    setlists: list[Setlist] = get_setlist_list()
    all_dates: list[date] = get_all_dates(setlists)
    all_songs: list[str] = [song.name for song in get_all_songs()]
    reverse_db: dict[str, list[date]] = get_reverse_db()
    
    game = Game().init()
    