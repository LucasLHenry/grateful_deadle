#!/bin/bash
cwd=$(pwd | sed 's \/c\/ C:\/ g; s \/ \\ g')
python -m PyInstaller --noconfirm --onedir --windowed --add-data "$cwd\lib\database\constraints.json;./lib/database/" --add-data "$cwd\lib\database\db.json;./lib/database/"  "$cwd\main.py"
rm -rf build/
mv dist/main/main.exe dist/main/grateful_grid.exe