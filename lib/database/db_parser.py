from datetime import date
import io, json
from lib.classes import Song, Setlist
from typing import Iterator
from CONFIG import ROOT_DIR

def parse_date_str(date_str: str) -> date:
    day, month, year = tuple([int(el) for el in date_str.split('-')])
    return date(year, month, day)

def yield_songs_from_setlist_dict(setlist_dict: dict) -> Iterator[Song]:
    for setlist in setlist_dict["sets"]["set"]:
        for song in setlist["song"]:
            yield Song(song["name"])

def get_setlist_list(db_filename: str) -> list[Setlist]:
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

def get_all_songs(song_db_filename: str) -> list[Song]:
    with io.open(f"{ROOT_DIR}/lib/database/{song_db_filename.lower()}", mode='r', encoding='utf-8') as f:
        song_db = json.load(f) 
    
    song_list = []
    for songname in song_db["songs"]:
        song_list.append(Song(songname["name"]))
    return song_list