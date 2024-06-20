from lib.classes import Setlist, Game
from typing import Optional
from lib.database.db_parser import get_setlist_list
from datetime import date

def setlist_list_to_fwd_db(setlists: list[Setlist]) -> dict[date, set[str]]:
    out_dict: dict[date, set[str]] = dict()
    for setlist in setlists:
        out_dict[setlist.date] = set(setlist.songnames)
    return out_dict        

def generate_games():
    setlists: list[Setlist] = get_setlist_list()
    db: dict[date, set[str]] = setlist_list_to_fwd_db(setlists)
    all_dates: list[date] = db.keys()
    game = Game()
    return recursive_search(game, 0, all_dates, db)
    

def recursive_search(
        game: Game, 
        depth: int, 
        all_dates: list[date], 
        db: dict[date, set[str]]
    ) -> Optional[Game]:
    
    # these two variables are constants that dictate the order in which variable assignments are done
    variable_indices_in_assignment_order = [(0,0), (1,0), (0,0), (0,1), (1,1), (1,1), (0,1), (1,0), (0,2), (1,2), (2,2), (0,2), (2,0), (1,2), (2,1)]
    variable_is_date_in_assignment_order = [1,     1,     0,     1,     1,     0,     0,     0,     1,     1,     0,     0,     0,     0,     0    ]
    
    if depth >= 15: return game
    
    x, y = variable_indices_in_assignment_order[depth]  # indices of variable to assign
    if variable_is_date_in_assignment_order[depth] == 1:  # it's a date
        for date in all_dates:  # because of the search order, dates are never constrained
            if date not in (game.dates[0] + game.dates[1]):  # must be a new date
                game.dates[x][y] = date  # assign
                soln = recursive_search(game, depth+1, all_dates, db)  # test assignment
                if soln is not None: 
                    return soln  # good soln
                else: 
                    game.dates[x][y] = None  # bad soln, undo assignment
        return None  # no solutions, backtrack
    else:  # it's a song
        # because of order, songs always have both relevant dates already assigned
        # use set intersection to make search space smaller
        for song in (db[game.dates[0][y]] & db[game.dates[1][x]]):
            if song not in (game.songs[0] + game.songs[1] + game.songs[2]):  # must be unique
                game.songs[x][y] = song  # assign
                soln = recursive_search(game, depth+1, all_dates, db)  # test assignment
                if soln is not None: 
                    return soln  # good soln, return
                else: 
                    game.songs[x][y] = None  # bad soln, undo assignment
        return None  # no solutions, backtrack