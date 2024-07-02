from CONFIG import ROOT_DIR, DB_FILENAME
import json, io

def get_songname_from_hash(hash: str, db: dict) -> str:
    if not len(hash) == 8: raise ValueError("not a song hash")
    try:
        return db["songs"][hash]
    except KeyError:
        return "NOT A VALID HASH"

   
def get_hash_from_songname(songname: str, db: dict) -> str:
    for hash, _songname in db["songs"].items():
        if _songname.lower() == songname.lower(): return hash
    return "NOT A VALID SONG"

def get_db():
    with io.open(f"{ROOT_DIR}/lib/database/{DB_FILENAME.lower()}", mode='r', encoding='utf-8') as f:
        return json.load(f)