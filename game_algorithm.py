from lib.classes import Constraint, Game
from typing import Optional
from constraints import load_constraints  
from lib.utils import weighted_shuffle, generate_constraint_type_weights

_ALL_CONSTRAINTS: list[Constraint]|None = None
_CONSTRAINT_WEIGHTS: dict[Constraint, int]|None = None

def generate_game():
    global _ALL_CONSTRAINTS, _CONSTRAINT_WEIGHTS
    # happens on startup
    if _ALL_CONSTRAINTS is None:
        _ALL_CONSTRAINTS = load_constraints()
        _CONSTRAINT_WEIGHTS = generate_constraint_type_weights(_ALL_CONSTRAINTS)
    
    # reshuffle every time
    shuffled_constraints = weighted_shuffle(_ALL_CONSTRAINTS, lambda c: _CONSTRAINT_WEIGHTS[c.constraint_type])
    
    game = Game()
    return recursive_search(game, 0, shuffled_constraints)
    
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