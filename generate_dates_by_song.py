import json
from lib.classes import Setlist, Song
from lib.database.db_parser import get_setlist_list, get_all_songs
from CONFIG import RV_DB_FILENAME, ROOT_DIR

def main():
    # database is a bunch of setlists, with dates and the songs played there.
    # this fucntion creates another json file to reorganize it as having a list
    # of songs, where each song has a list of dates (the shows where it was played)
    setlists = get_setlist_list()
    songs = get_all_songs()
    out_dict = dict()
    for song in songs:
        out_dict[song.name] = []
    for setlist in setlists:
        for songname in setlist.songnames:
            out_dict[songname].append(setlist.date.strftime("%d-%m-%Y"))

    with open(f"{ROOT_DIR}/lib/database/{RV_DB_FILENAME.lower()}", 'w') as f:
        f.write(json.dumps(out_dict, indent=4))
    
    
if __name__ == "__main__":
    main()