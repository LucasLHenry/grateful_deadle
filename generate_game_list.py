import lib.game_algorithm as g
from lib.database.db_parser import get_setlist_list, get_all_songs
from CONFIG import GAMES_DB_FILENAME, ROOT_DIR
import json
import profile

def main():
    games = g.generate_game()
    print("\n")
    print(games)
    with open(f"{ROOT_DIR}/lib/database/{GAMES_DB_FILENAME.lower()}", 'w') as f:
        g.generate_games(f)
    
if __name__ == "__main__":
    main()