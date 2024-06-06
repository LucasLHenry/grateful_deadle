from lib.classes import Song, Setlist
from datetime import date

def get_all_dates(setlists: list[Setlist]) -> list[date]:
    return [setlist.date for setlist in setlists]