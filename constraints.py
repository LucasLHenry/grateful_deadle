from lib.classes import Constraint, ConstraintType
from lib.database.utils import (
    db_type, 
    generate_play_amounts,
    parse_date_str,
    truncate_str, 
    get_venue_string
)
import io, json, re
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
        db: db_type = json.load(f)
        
    parsed_dict = dict()
    add_constraints_to_out_dict_and_print(filter_constraints(generate_date_constraints(db)),           parsed_dict)
    add_constraints_to_out_dict_and_print(filter_constraints(generate_debut_constraints(db)),          parsed_dict)
    add_constraints_to_out_dict_and_print(filter_constraints(generate_play_amt_constraints(db)),       parsed_dict)
    add_constraints_to_out_dict_and_print(filter_constraints(generate_played_at_constraints(db)),      parsed_dict)
    add_constraints_to_out_dict_and_print(filter_constraints(generate_tour_constraints(db)),           parsed_dict)
    add_constraints_to_out_dict_and_print(filter_constraints(generate_play_amt_range_constraints(db)), parsed_dict)
    
    with io.open(f"{ROOT_DIR}/lib/database/{CONSTRAINTS_FILENAME.lower()}", mode='w', encoding='utf-8') as f:
        json.dump(parsed_dict, f, ensure_ascii=False, indent=4)

def add_constraints_to_out_dict_and_print(constraint_list: list[Constraint], out_dict: dict) -> None:
    for c in constraint_list:
        out_dict[c.id] = c.to_dict()
    print(f"{len(constraint_list)} constraints of type {str(constraint_list[0].constraint_type)[15:]}")

def filter_constraints(constraint_list: list[Constraint]) -> list[Constraint]:
    # only want constraints with at least 3 songs, otherwise they aren't useful
    return [c for c in constraint_list if len(c.songs) >= 3]

def load_constraints() -> list[Constraint]:
    with io.open(f"{ROOT_DIR}/lib/database/{CONSTRAINTS_FILENAME.lower()}", mode='r', encoding='utf-8') as f:
        cdb = json.load(f)
    
    all_constraints = []
    for _, val in cdb.items():
        all_constraints.append(Constraint.from_dict(val))
    
    return all_constraints




############## CONSTRAINT GENERATION ALGORITHMS START HERE ###################

def generate_date_constraints(db: db_type) -> list[Constraint]:
    # this constraint is: the song must have been played on this date.
    # really easy to generate because the db is already in that format
    c_type = ConstraintType.DATE
    
    constraint_list = []
    for date_str, setlist in db["sets"].items():
        venue_str = get_venue_string(setlist["venue_id"])
        date_str_pretty = parse_date_str(date_str).strftime("%b %d, %Y")
        c = Constraint(c_type, f"{date_str_pretty} at {venue_str}")
        for song in setlist["songs"]:
            c.songs.add(song)
        constraint_list.append(c)
    return constraint_list

def generate_debut_constraints(db: db_type) -> list[Constraint]:
    c_type = ConstraintType.DEBUT
    
    sorted_dates: list[date] = sorted([parse_date_str(date_str) for date_str in db["sets"].keys()])
    # setlists from oldest to newest
    sorted_setlists = [db["sets"][date_obj.strftime("%d-%m-%Y")] for date_obj in sorted_dates]
    
    constraint_list = []
    seen_song_hashes = set()
    for setlist in sorted_setlists:
        venue_str = get_venue_string(setlist["venue_id"])
        date_str_pretty = parse_date_str(setlist["date"]).strftime("%b %d, %Y")
        c = Constraint(c_type, f"{date_str_pretty} at {venue_str}")
        for song_hash in setlist["songs"]:
            if song_hash not in seen_song_hashes:
                c.songs.add(song_hash)
                seen_song_hashes.add(song_hash)
        if not len(c.songs) == 0:
            constraint_list.append(c)
    
    return constraint_list

def generate_play_amt_constraints(db: db_type) -> list[Constraint]:
    c_type = ConstraintType.PLAY_AMT
    
    # all possible constraints of this type. there will be significantly less than this,
    # will be filtered out
    constraint_list: list[Constraint] = [Constraint(c_type, str(i + 1)) for i in range(len(db["sets"]))]
    
    # play amount dict
    play_amts: dict[str, int] = generate_play_amounts()
    
    for song_hash, play_amt in play_amts.items():
        constraint_list[play_amt].songs.add(song_hash)
    
    return constraint_list

def generate_played_at_constraints(db: db_type) -> list[Constraint]:
    c_type = ConstraintType.PLAYED_AT
    
    constraint_dict: dict[str, Constraint] = {}
    for _, setlist in db["sets"].items():
        venue_hash = setlist["venue_id"]
        constraint_dict.setdefault(venue_hash, Constraint(c_type, get_venue_string(venue_hash)))
        for song_hash in setlist["songs"]:
            constraint_dict[setlist["venue_id"]].songs.add(song_hash)
        
    return [c for _, c in constraint_dict.items()]

def generate_tour_constraints(db: db_type) -> list[Constraint]:
    c_type = ConstraintType.TOUR
    
    tourless_set_count = 0
    constraint_dict: dict[str, Constraint] = {}
    for _, setlist in db["sets"].items():
        tour_name = setlist["tour"]
        if tour_name == "No Tour Assigned": tourless_set_count += 1
        constraint_dict.setdefault(tour_name, Constraint(c_type, f"{tour_name}"))
        for song_hash in setlist["songs"]:
            constraint_dict[tour_name].songs.add(song_hash)
    print(f"{tourless_set_count} sets played without a tour assigned")
    return [c for _, c in constraint_dict.items() if c.value not in ("No Tour Assigned")]


def generate_play_amt_range_constraints(db: db_type) -> list[Constraint]:
    c_type = ConstraintType.PLAY_AMT_RANGE
    
    play_amt_arr = [0, 10, 20, 50, 100, 200, 300, 400, 1000, 999999]
    def play_amt_range_str(idx: int) -> str:
        lower_bound = play_amt_arr[idx - 1]
        upper_bound = play_amt_arr[idx]
        if idx - 1 == 0:
            return f"less than {upper_bound}"
        if idx == len(play_amt_arr) - 1:
            return f"more than {lower_bound}"
        return f"between {lower_bound} and {upper_bound}"
        
    constraint_list = [Constraint(c_type, play_amt_range_str(i)) for i in range(1, len(play_amt_arr))]
    play_amts: dict[str, int] = generate_play_amounts()
    
    for song_hash, amt in play_amts.items():
        truncated_arr = [amt_ for amt_ in play_amt_arr if amt_ < amt]
        constraint_list[len(truncated_arr) - 1].songs.add(song_hash)
    return constraint_list

def generate_play_amt_during_tour_constraints(db: db_type) -> list[Constraint]:
    c_type = ConstraintType.PLAY_AMT_TOUR
    
    

if __name__ == "__main__":
    main()