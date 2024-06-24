from ui.main_window import Ui_MainWindow
from input_window_logic import InputWindow
from lib.classes import Setlist, Song, SubmitWindowInfo, SubmitType
from lib.database.db_parser import get_setlist_list, get_all_songs
from lib.game_algorithm import generate_game
from functools import partial
import stylesheets as ss

from PyQt5 import QtWidgets, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        # put UI elements into array for ease of access
        self.grid_buttons: list[list[QtWidgets.QPushButton]] = [
            [self.r1c1_pb, self.r1c2_pb, self.r1c3_pb],
            [self.r2c1_pb, self.r2c2_pb, self.r2c3_pb],
            [self.r3c1_pb, self.r3c2_pb, self.r3c3_pb]
        ]
        
        self.grid_displays: list[list[QtWidgets.QLineEdit]] = [
            [self.col_1_le, self.col_2_le, self.col_3_le],
            [self.row_1_le, self.row_2_le, self.row_3_le]
        ]
        
        # connect input window popup signals
        for row, grid_row in enumerate(self.grid_buttons):
            for col, button in enumerate(grid_row):
                button.clicked.connect(partial(self._show_input_window, row, col))
        
        # get data from db
        self._all_setlists: list[Setlist] = get_setlist_list()
        self._all_songs: list[Song] = get_all_songs()
        self._all_song_names: list[str] = [song.name for song in self._all_songs]
        
        # set up autocompleter
        self._completer = QtWidgets.QCompleter(self._all_song_names)
        self._completer.setCaseSensitivity(False)
        
        self._game = generate_game()
        print(self._game)
        self._display_constraints()
        
        self._set_stylesheets()
    
    # gets info from input window on what song was selected
    @QtCore.pyqtSlot(SubmitWindowInfo)
    def _handle_input_window(self, value: SubmitWindowInfo):
        self.setDisabled(False)  
        
        # ignore cancelled inputs
        if value.status == SubmitType.CANCEL:
            return
        
        x, y = value.pos
        if value.song_name == "":
            self.grid_buttons[x][y].setText("—")
            self.grid_buttons[x][y].setStyleSheet(ss.button_ss_default)
            return
        
        self.grid_buttons[x][y].setText(value.song_name)
        if value.song_name == self._game.songs[x][y]:
            self.grid_buttons[x][y].setStyleSheet(ss.button_ss_correct)
        else:
            self.grid_buttons[x][y].setStyleSheet(ss.button_ss_incorrect)
    
    def _show_input_window(self, row:int, col:int):
        self._iw = InputWindow()
        self._iw.set_pos(row, col) # window needs to know which cell it corresponds to
        self._iw.entry_le.setCompleter(self._completer) # autocomplete
        self._iw.callback.connect(self._handle_input_window)
        self._iw.show()
        
        # disable main window while the popup window is
        self.setDisabled(True)
    
    def _display_constraints(self):
        for display_list, constraint_list in zip(self.grid_displays, self._game.dates):
            for display, constraint in zip(display_list, constraint_list):
                display.setText(str(constraint))
                
    def _set_stylesheets(self):
        for button_list in self.grid_buttons:
            for button in button_list:
                button.setStyleSheet(ss.button_ss_default)



# runner and include guard
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
if __name__ == "__main__":
    main()