from datetime import date, datetime
import hashlib, textwrap
from typing import Iterable, Callable, TypeVar
import random
from lib.database.db_utils import _DB, db_type
from CONFIG import DEBUG

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


_song_freq: dict[str, float] = {}
def calc_game_difficulty(game, db: db_type = _DB) -> int:
    global _song_freq
    if not _song_freq:
        for _, setlist in db["sets"].items():
            for song_hash in setlist["songs"]:
                _song_freq.setdefault(song_hash, 0.0)
                _song_freq[song_hash] += 1
        # normalize
        max_freq = max([freq for _, freq in _song_freq.items()])
        _song_freq = {hash: freq/max_freq for hash, freq in _song_freq.items()}
                
    total_possibilities: list[set[str]] = [game.possibilities_at(i, j) for i in range(3) for j in range(3)]

    avg = lambda x: sum(x) / len(x)
    med = lambda x: sorted(x)[int(len(x)/2)]
    # an easier game has more song possibilites for each answer, and uses more common songs
    num_possibilities = [len(songs) for songs in total_possibilities]
    avg_num_answers = avg(num_possibilities)
    med_num_answers = med(num_possibilities)
    min_num_answers = min(num_possibilities)
    max_num_answers = max(num_possibilities)
    if DEBUG: print(f"avg num answers is {avg_num_answers:.2f}, median is {med_num_answers}")
    
    weight = lambda hash: _song_freq[hash] + 1
    foreach = lambda arr, fn: [fn(val) for val in arr]
    weighted_possibilites = [sum(foreach(songs, weight)) for songs in total_possibilities]
    return med(weighted_possibilites)
    # lowest num possilibites for a game is set in config, currently it is 1.
    # based on some tests, the average average is around 7, while the average median is around 5.
    # the average range is around 18. (difference between max and min)
    
    # difficulty score will be out of 5, with 1 being easiest and 5 being hardest.
    