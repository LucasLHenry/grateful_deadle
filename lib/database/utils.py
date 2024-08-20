from CONFIG import ROOT_DIR, DB_FILENAME
import json, io
from typing import TypeAlias
from datetime import date, datetime
import hashlib, textwrap
from typing import Iterable, Callable, TypeVar
import random
from threading import Thread

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

def get_venue_string(venue_hash: str, db: db_type = _DB) -> str:
    venue_name = truncate_str(db["venues"][venue_hash]["name"], 25)
    city_name = db["venues"][venue_hash]["city"]
    return f"{venue_name}, {city_name}"

def run_with_timeout(fn: Callable, time_out: float, restart: bool = False):
    retval = [None]
    first_time = True
    while first_time or (t.is_alive() and restart):
        t = Thread(target=return_val_wrapper(fn), args=[retval])
        t.start()
        t.join(timeout=time_out)
        first_time = False
    return retval[0]

def return_val_wrapper(fn: Callable):
    def inner(args: list):
        args[0] = fn()
    return inner

def gen_hash(s: str, len: int) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:len]

def parse_date_str(date_str: str) -> date:
    return datetime.strptime(date_str, "%d-%m-%Y")

def truncate_str(s: str, max_len: int):
    if len(s) > max_len:
        return s[:max_len - 1] + "..."
    return s


def wrap(s: str, len):
    wr = textwrap.TextWrapper(width=len)
    return '\n'.join(wr.wrap(s))

T=TypeVar('T')
def weighted_shuffle(items: Iterable[T], weight_func: Callable[[T], float]) -> list[T]:
    return sorted(items, key=lambda t: random.random() ** (1.0 / weight_func(t)), reverse=True)

_song_freq: dict[str, int] = {}
def calc_game_difficulty(game, raw_vals: bool = False, db: db_type = _DB) -> int:
    global _song_freq
    if not _song_freq:
        max_freq = 0
        for _, setlist in db["sets"].items():
            for song_hash in setlist["songs"]:
                _song_freq.setdefault(song_hash, 0.0)
                _song_freq[song_hash] += 1
                if _song_freq[song_hash] > max_freq: max_freq = _song_freq[song_hash]
        # normalize
        _song_freq = {hash: freq/max_freq for hash, freq in _song_freq.items()}
                
    total_possibilities: list[set[str]] = [game.possibilities_at(i, j) for i in range(3) for j in range(3)]
    
    # an easier game has more song possibilites for each answer, and uses more common songs
    # lowest num possilibites for a game is set in config, currently it is 1.
    # based on some tests, the average average is around 7, while the average median is around 5.
    # the average range is around 18. (difference between max and min)
    med = lambda x: sorted(x)[int(len(x)/2)]
    weight = lambda hash: _song_freq[hash] + 1
    foreach = lambda arr, fn: [fn(val) for val in arr]
    weighted_possibilites = [sum(foreach(songs, weight)) for songs in total_possibilities]
    
    # these cutoffs were calculated using the main() script in game_algorithm.py
    # they give an approximately uniform score distribution across games
    # (it's pretty much ultra-basic histogram equalization)
    score = med(weighted_possibilites)
    if raw_vals: return score
    
    if score < 4:
        return 5
    if score < 5:
        return 4
    if score < 6:
        return 3
    if score < 9:
        return 2
    return 1
    
    
def generate_constraint_type_weights(constraint_list):
    # constraint types that appear less often should have a higher weight
    c_amt_dict = {}
    for c in constraint_list:
        c_amt_dict.setdefault(c.constraint_type, 0)
        c_amt_dict[c.constraint_type] += 1
    max_amt = max([amt for _, amt in c_amt_dict.items()])
    return {k: max_amt / float(v) for k,v in c_amt_dict.items()}