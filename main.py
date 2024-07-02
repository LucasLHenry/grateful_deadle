from ui.main_window import Ui_MainWindow
from input_window_logic import InputWindow
from lib.classes import SubmitWindowInfo, SubmitType
from game_algorithm import generate_game
from functools import partial
import stylesheets as ss
from utils import wrap
from lib.database.db_utils import get_hash_from_songname, get_db

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
        
        self.grid_displays: list[list[QtWidgets.QTextEdit]] = [
            [self.col_1_te, self.col_2_te, self.col_3_te],
            [self.row_1_te, self.row_2_te, self.row_3_te]
        ]
        
        # connect input window popup signals
        for row, grid_row in enumerate(self.grid_buttons):
            for col, button in enumerate(grid_row):
                button.clicked.connect(partial(self._show_input_window, row, col))
        
        # get data from db
        self._db = get_db()
        self._all_song_names: list[str] = [songname for _, songname in self._db["songs"].items()]
        
        # set up autocompleter
        self._completer = QtWidgets.QCompleter(self._all_song_names)
        self._completer.setCaseSensitivity(False)
        
        self._game = generate_game()
        print(self._game)
        self._game.print_all_info(self._db)
        self._display_constraints()
        
        self._set_styles()
    
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
        
        self.grid_buttons[x][y].setText(wrap(value.song_name, 15))
        song_hash = get_hash_from_songname(value.song_name, self._db)
        if song_hash in self._game.possibilities_at(x, y):
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
        for top_display, top_constraint in zip(self.grid_displays[0], self._game.top_constraints):
            top_display.setText(str(top_constraint))
        for side_display, side_constraint in zip(self.grid_displays[1], self._game.side_constraints):
            side_display.setText(str(side_constraint))
                
    def _set_styles(self):
        for button_list in self.grid_buttons:
            for button in button_list:
                button.setStyleSheet(ss.button_ss_default)
        
        for display_list in self.grid_displays:
            for display in display_list:
                display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)



# runner and include guard
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
if __name__ == "__main__":
    main()