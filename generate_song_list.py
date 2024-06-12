from lib.database.db_parser import get_setlist_list
from lib.classes import Setlist
from CONFIG import DB_FILENAME, SONG_DB_FILENAME, ROOT_DIR
import json

def main():
    all_setlists: list[Setlist] = get_setlist_list(DB_FILENAME)
    all_song_names: set[str] = set()
    for setlist in all_setlists:
        for song in setlist.songs:
            all_song_names.add(song.name)
    all_songs_dict: list[dict[str, str]] = [{"name": songname} for songname in all_song_names if songname != ""]
    json_output_dict: dict = {"songs": all_songs_dict}
    json_output = json.dumps(json_output_dict, indent=4)
    with open(f"{ROOT_DIR}/lib/database/{SONG_DB_FILENAME.lower()}", 'w') as f:
        f.write(json_output)

if __name__ == "__main__":
    main()