from lib.classes import Setlist, Song, Game
from typing import Iterator, Optional
import constraint as csp
from lib.database.db_utils import get_all_dates
from datetime import date

def generate_games(setlists: list[Setlist], all_songs: list[Song]) -> list[dict]: #Iterator[Game]:
    # this problem will be formatted as a CSP (constraint satisfaction problem).

    problem = csp.Problem()
    for i in range(3):
        problem.addVariable(f"row{i}", get_all_dates(setlists))
        problem.addVariable(f"col{i}", get_all_dates(setlists))
        for j in range(3):
            problem.addVariable(f"cell{i}{j}", [song.name for song in all_songs])
    
    problem.addConstraint(csp.AllDifferentConstraint())
    
    def get_setlist_with_date(d: date) -> Setlist:
        return [s for s in setlists if s.date == d][0]
    
    for i in range(3):
        for j in range(3):
            problem.addConstraint(lambda date, songname: songname in get_setlist_with_date(date).songnames, (f"col{i}", f"cell{j}{i}"))
            problem.addConstraint(lambda date, songname: songname in get_setlist_with_date(date).songnames, (f"row{i}", f"cell{i}{j}"))
    
    return problem.getSolution()
    # for solution in problem.getSolutions():
        # result = Game()
        # for var, val in solution.items():
        #     if len(var) == 4:  # setlist value
        #         if var[0] == "r":
        #             result.dates[0][int(var[-1])] = val.date
        #         else:
        #             result.dates[1][int(var[-1])] = val.date
        #     else:
        #         result.songs[int(var[-1])][int(var[-2])] = val
        # yield result