from lib.classes import Constraint, ConstraintType
import io, json
from CONFIG import ROOT_DIR, DB_FILENAME, CONSTRAINTS_FILENAME

def main():  # generates constraints list
    # we will add new constraint types to this as they are implemented
    # constraints have the format:
    # {
    #     "type": d  -> digit for ConstraintType (enums encode to integers)
    #     "value": ""   -> changes form depending on type (for date constraint its the date)
    #     "id": "xxxxxxxxxx" -> 10 digit hash
    #     "songs": [ -> song hashes that satisfy the constraint
    #         "xxxxxxxx",
    #         ...
    #     ]
    # }
    
    # this will be the value, where the key is a 10 digit hash constructed from the value and type
    with io.open(f"{ROOT_DIR}/lib/database/{DB_FILENAME.lower()}", mode='r', encoding='utf-8') as f:
        db = json.load(f)

    date_constraints = generate_date_constraints(db)
    
    parsed_dict = dict()
    for c in date_constraints:
        parsed_dict[c.id] = c.to_dict()
    
    with io.open(f"{ROOT_DIR}/lib/database/{CONSTRAINTS_FILENAME.lower()}", mode='w', encoding='utf-8') as f:
        json.dump(parsed_dict, f, ensure_ascii=False, indent=4)

def generate_date_constraints(db: dict) -> list[Constraint]:
    # this constraint is: the song must have been played on this date.
    # really easy to generate because the db is already in that format
    c_type = ConstraintType.DATE
    
    constraint_list = []
    for date_str, val in db["sets"].items():
        c = Constraint(c_type, date_str)
        for song in val["songs"]:
            c.songs.add(song)
        constraint_list.append(c)
    return constraint_list

def load_constraints() -> list[Constraint]:
    with io.open(f"{ROOT_DIR}/lib/database/{CONSTRAINTS_FILENAME.lower()}", mode='r', encoding='utf-8') as f:
        cdb = json.load(f)
    
    all_constraints = []
    for _, val in cdb.items():
        all_constraints.append(Constraint.from_dict(val))
    
    return all_constraints

if __name__ == "__main__":
    main()