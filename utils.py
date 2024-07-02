from datetime import date, datetime
import hashlib, textwrap

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