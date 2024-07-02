from lib.classes import Constraint, ConstraintType
from utils import parse_date_str
import io, json
from CONFIG import ROOT_DIR, DB_FILENAME, CONSTRAINTS_FILENAME
from datetime import date

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
        
    parsed_dict = dict()
    add_constraints_to_out_dict_and_print(filter_constraints(generate_date_constraints(db)),  parsed_dict)
    add_constraints_to_out_dict_and_print(filter_constraints(generate_debut_constraints(db)), parsed_dict)
    
    with io.open(f"{ROOT_DIR}/lib/database/{CONSTRAINTS_FILENAME.lower()}", mode='w', encoding='utf-8') as f:
        json.dump(parsed_dict, f, ensure_ascii=False, indent=4)

def add_constraints_to_out_dict_and_print(constraint_list: list[Constraint], out_dict: dict) -> None:
    for c in constraint_list:
        out_dict[c.id] = c.to_dict()
    print(f"{len(constraint_list)} constraints of type {str(constraint_list[0].constraint_type)[15:]}")

def filter_constraints(constraint_list: list[Constraint]) -> list[Constraint]:
    # only want constraints with at least 3 songs, otherwise they aren't useful
    return [c for c in constraint_list if len(c.songs) >= 3]

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

def generate_debut_constraints(db: dict) -> list[Constraint]:
    c_type = ConstraintType.DEBUT
    
    sorted_dates: list[date] = sorted([parse_date_str(date_str) for date_str in db["sets"].keys()])
    # setlists from oldest to newest
    sorted_setlists = [db["sets"][date_obj.strftime("%d-%m-%Y")] for date_obj in sorted_dates]
    
    constraint_list = []
    seen_song_hashes = set()
    for setlist in sorted_setlists:
        c = Constraint(c_type, setlist["date"])
        for song_hash in setlist["songs"]:
            if song_hash not in seen_song_hashes:
                c.songs.add(song_hash)
                seen_song_hashes.add(song_hash)
        if not len(c.songs) == 0:
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