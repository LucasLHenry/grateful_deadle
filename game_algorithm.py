from lib.classes import Constraint, Game
from typing import Optional
from constraints import load_constraints  
from lib.database.db_utils import get_db
from utils import weighted_shuffle

from random import shuffle

def main():
    game = generate_game()
    game.print_all_info(get_db())

def generate_game():
    all_constraints = load_constraints()
    all_constraints = weighted_shuffle(all_constraints, lambda c: c.constraint_type.value ** 3)
    
    game = Game()
    return recursive_search(game, 0, all_constraints)
    
def recursive_search(
        game: Game, 
        depth: int, 
        all_constraints: list[Constraint]
    ) -> Optional[Game]:
    
    if not game.is_valid():  # this is where the constraints are checked
        return None
    
    if depth == 6:  # max depth (all assignments)
        return game
    
    # this variable is a constant that dictates the order in which variable assignments are done
    variable_indices_in_assignment_order = [(0,0), (1,0), (0,1), (1,1), (0,2), (1,2)]
    
    # ts = 0 -> top row, ts = 1 -> side column
    ts, pos = variable_indices_in_assignment_order[depth]  # indices of variable to assign
    for c in all_constraints:  # because of the search order, dates are never constrained
        if c.id in game.ids: continue # must be a new constraint
        
        if ts == 0: game.top_constraints[pos] = c  # assign
        else: game.side_constraints[pos] = c
        
        soln = recursive_search(game, depth+1, all_constraints)  # test assignment
        
        if soln is not None: return soln  # good soln, pass back up chain
        else: # bad soln, undo assignment
            if ts == 0: game.top_constraints[pos] = None  # assign
            else: game.side_constraints[pos] = None
    return None  # no solutions, backtrack



if __name__ == "__main__":
    main()