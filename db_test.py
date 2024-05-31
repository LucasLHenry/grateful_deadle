from lib.database.db_parser import get_setlist_list

db_filename = "DB.JSON"

def main():
    setlists = get_setlist_list(db_filename)
        
if __name__ == "__main__":
    main()