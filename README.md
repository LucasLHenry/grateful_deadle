# THE GREATFUL DEADLE

A simple trivia game for deadheads.

## Gameplay
It consists of a 3x3 grid of squares, as well as dates along the upper and left sides. The goal is to fill in each square with a song that was played by the grateful dead at their shows on both of those dates.

Clicking on a box opens up a window where you can input the name of a song, with autocomplete to help you out.

## Technical Info
This game was written in python, using qtpy to generate the ui. The UI was first laid out using qtDesigner, then the python equivalent files were generated using `regenerate_ui_files.sh`.

The program uses a json database to source all of its information, located in `lib/database/db.json`. This database was copied from MichaelAdamBerry's [darkstar-project](https://github.com/MichaelAdamBerry/darkstar-project). The `allsongs.json` file was generated from this file using `generate_song_list.py`.