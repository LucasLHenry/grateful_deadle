from CONFIG import ROOT_DIR, DB_FILENAME
import json, io
from typing import TypeAlias

db_type: TypeAlias = dict[str, dict[str, dict[str, str | list[str]] | str]]

def get_db():
    with io.open(f"{ROOT_DIR}/lib/database/{DB_FILENAME.lower()}", mode='r', encoding='utf-8') as f:
        return json.load(f)
    
_DB = get_db()

def get_songname_from_hash(hash: str, db: db_type = _DB) -> str:
    if not len(hash) == 8: raise ValueError("not a song hash")
    try:
        return db["songs"][hash]
    except KeyError:
        return "NOT A VALID HASH"

   
def get_hash_from_songname(songname: str, db: db_type = _DB) -> str:
    for hash, _songname in db["songs"].items():
        if _songname.lower() == songname.lower(): return hash
    raise ValueError("songname not in list")

def generate_play_amounts(db: db_type = _DB) -> dict[str, int]:
    play_amts: dict[str, int] = {}
    for _, setlist in db["sets"].items():
        for song_hash in setlist["songs"]:
            play_amts.setdefault(song_hash, 0)
            play_amts[song_hash] += 1
    return play_amts