from datetime import date

class Song:
    def __init__(self, name: str):
        self.name = name


class Setlist:
    def __init__(self, venue: str, date: date):
        self.venue = venue
        self.date = date
        self.songs: set[Song] = set()