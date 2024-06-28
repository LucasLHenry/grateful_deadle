from CONFIG import RAW_DB_FILENAME, DB_FILENAME, ROOT_DIR
import json, io
from datetime import date
import hashlib as h

def gen_hash(s: str, len: int) -> str:
    return h.sha256(s.encode('utf-8')).hexdigest()[:len]

def parse_date_str(date_str: str) -> date:
    day, month, year = tuple([int(el) for el in date_str.split('-')])
    return date(year, month, day)

def main():
    with io.open(f"{ROOT_DIR}/lib/database/{RAW_DB_FILENAME.lower()}", mode='r', encoding='utf-8') as f:
        raw_db = json.load(f)
    
    # the raw database is structured as follows:
    # {
    #     "setlists": [
    #         {
    #             ...
    #             "eventDate": "dd-mm-yyyy",
    #             "venue": {
    #                 "id": "xxxxxxxx",
    #                 "name": "",
    #                 "city": {
    #                     "id": "ddddddd",
    #                     "name": "",
    #                 }
    #             },
    #             "tour": {
    #                 "name": "",
    #             }
    #             "sets": {
    #                 "set": [
    #                     {
    #                         "name": "Set x / Encore",
    #                         "song": [
    #                             {
    #                                 "name": ""
    #                             }...
    #                         ]
    #                     }...
    #                 ]
    #             }
    #         }...
    #     ]
    # }
    # the relevant information from this is the date of the setlist, the song names,
    # the location, and the venue name.
    # this information must be in the final database, as well as unique ids.
    # these should be hex hashes, and to distinguish type (song vs venue) will have 
    # different lengths.
    # additionally, the song "Jam" should not be included, and any show after 1995
    # (the death of Jerry Garcia) should not be included.
    
    # output database structure:
    # {
    #     "sets": {
    #         "dd-mm-yyyy": {
    #             "venue_id": "xxxxxxx",
    #             "tour": "",
    #             "songs": [
    #                 "xxxxxxxx",  -> disambiguation for song name
    #                  ...
    #             ]
    #         }...
    #     }
    #     "songs": {  -> lookup table for songnames
    #         "xxxxxxxx": "name"
    #         ...
    #     }
    #     "venues": {  -> lookup table for venue info
    #         "xxxxxxx": {
    #             "name": "",
    #             "city": "",
    #          }
    #         ...
    #     }
    # }
    all_songs: set[str] = set()
    all_venues: set[tuple[str, str]] = set()
    parsed_dict: dict = {"sets": {}, "songs": {}, "venues": {}}
    
    num_sets = 0
    for setlist in raw_db["setlists"]:
        date_str: str = setlist["eventDate"]
        show_date: date = parse_date_str(date_str)
        if show_date.year > 1995: continue
        set_dict = dict()
        
        venue: str = setlist["venue"]["name"]
        city: str = setlist["venue"]["city"]["name"]
        all_venues.add((venue, city))
        set_dict["venue_id"] = gen_hash(venue, 6)
        
        tour_name: str = setlist["tour"]["name"]
        set_dict["tour"] = tour_name
        
        set_dict["songs"] = []
        if len(setlist["sets"]["set"]) == 0: continue
        
        for _set in setlist["sets"]["set"]:
            for song in _set["song"]:
                song_name: str = song["name"]
                if song_name in ["Jam", ""]: continue
                
                all_songs.add(song_name)
                set_dict["songs"].append(gen_hash(song_name, 8))
        
        parsed_dict["sets"][date_str] = set_dict
        num_sets += 1
    
    num_songs = 0
    for song in list(all_songs):
        parsed_dict["songs"][gen_hash(song, 8)] = song
        num_songs += 1
    
    num_venues = 0
    for venue, city in list(all_venues):
        parsed_dict["venues"][gen_hash(venue, 6)] = {
            "name": venue,
            "city": city
        }
        num_venues += 1

    with io.open(f"{ROOT_DIR}/lib/database/{DB_FILENAME.lower()}", mode='w', encoding='utf-8') as f:
        json.dump(parsed_dict, f, ensure_ascii=False, indent=4)
        
    print(f"file written, {num_sets} different shows played")
    print(f"{num_venues} places played at, with {num_songs} unique songs")
    
if __name__ == "__main__":
    main()