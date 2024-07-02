#!/bin/bash

python -m PyInstaller --noconfirm --onedir --windowed --add-data "C:\Users\lucas\Documents\Projects\Code\Contract Work\Grateful Deadle for Brian\work\lib\database\constraints.json;./lib/database/" --add-data "C:\Users\lucas\Documents\Projects\Code\Contract Work\Grateful Deadle for Brian\work\lib\database\db.json;./lib/database/"  "C:\Users\lucas\Documents\Projects\Code\Contract Work\Grateful Deadle for Brian\work\main.py"
rm -rf build/