import lib.game_algorithm as g
from lib.database.db_parser import get_setlist_list, get_all_songs
from CONFIG import GAMES_DB_FILENAME, ROOT_DIR, DB_FILENAME, SONG_DB_FILENAME
import json

def main():
    all_setlists = get_setlist_list(DB_FILENAME)
    all_songs = get_all_songs(SONG_DB_FILENAME)
    games = g.generate_games(all_setlists, all_songs)
    json_output = json.dumps({"games": games}, indent=4)
    with open(f"{ROOT_DIR}/lib/database/{GAMES_DB_FILENAME.lower()}", 'w') as f:
        f.write(json_output)
    
if __name__ == "__main__":
    main()