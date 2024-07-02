from datetime import date
import hashlib, textwrap

def gen_hash(s: str, len: int) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:len]

def parse_date_str(date_str: str) -> date:
    day, month, year = tuple([int(el) for el in date_str.split('-')])
    if day not in range(1, 31+1): raise ValueError("date out of range")
    if month not in range(1, 12+1): raise ValueError("month out of range")
    if year not in range(1, 10000): raise ValueError("year out of range")
    return date(year, month, day)

def truncate_str(s: str, max_len: int):
    if len(s) > max_len:
        return s[:max_len - 1] + "..."
    return s


def wrap(s: str, len):
    wr = textwrap.TextWrapper(width=len)
    return '\n'.join(wr.wrap(s))