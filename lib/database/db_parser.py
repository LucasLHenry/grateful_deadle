from datetime import date
import io, json
from lib.classes import Song, Setlist
from typing import Iterator
from CONFIG import ROOT_DIR, DB_FILENAME, SONG_DB_FILENAME, RV_DB_FILENAME

def get_reverse_db():
    with open(f"{ROOT_DIR}/lib/database/{RV_DB_FILENAME.lower()}", 'r') as f:
        reverse_db: dict = json.load(f)
        
    for songname, datelist in reverse_db.items():
        reverse_db[songname] = set([parse_date_str(date_str) for date_str in datelist])
        
    return reverse_db

def parse_date_str(date_str: str) -> date:
    day, month, year = tuple([int(el) for el in date_str.split('-')])
    return date(year, month, day)

def yield_songs_from_setlist_dict(setlist_dict: dict) -> Iterator[Song]:
    for setlist in setlist_dict["sets"]["set"]:
        for song in setlist["song"]:
            yield Song(song["name"])

def get_setlist_list(db_filename: str = DB_FILENAME) -> list[Setlist]:
    with io.open(f"{ROOT_DIR}/lib/database/{db_filename.lower()}", mode='r', encoding='utf-8') as f:
        db = json.load(f)
    
    setlists = []
    for setlist_dict in db["setlists"]:
        venue = setlist_dict["venue"]["name"]
        new_date = parse_date_str(setlist_dict["eventDate"])
        new_setlist = Setlist(venue, new_date)
        
        for song in yield_songs_from_setlist_dict(setlist_dict):
            new_setlist.songs.add(song)
        
        setlists.append(new_setlist)
    
    return setlists

def get_all_songs(song_db_filename: str = SONG_DB_FILENAME) -> list[Song]:
    with io.open(f"{ROOT_DIR}/lib/database/{song_db_filename.lower()}", mode='r', encoding='utf-8') as f:
        song_db = json.load(f) 
    
    song_list = []
    for songname in song_db["songs"]:
        song_list.append(Song(songname["name"]))
    return song_list