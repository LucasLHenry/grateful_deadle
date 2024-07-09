from datetime import date, datetime
import hashlib, textwrap
from typing import Iterable, Callable, TypeVar
import random
from lib.database.db_utils import db_type, _DB
from CONFIG import DEBUG
from threading import Thread

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
def calc_game_difficulty(game: 'Game', db: db_type = _DB) -> int:
    if not _song_freq:
        for _, setlist in db["sets"].items():
            for song_hash in setlist["songs"]:
                _song_freq.setdefault(song_hash, 0)
                _song_freq[song_hash] += 1
                
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
    # lowest num possilibites for a game is set in config, currently it is 1.
    # based on some tests, the average average is around 7, while the average median is around 5.
    # the average range is around 18. (difference between max and min)
    return (avg_num_answers, med_num_answers, max_num_answers - min_num_answers)
    