from ui.main_window import Ui_MainWindow
from input_window_logic import InputWindow
from error_window_logic import ErrorWindow
from functools import partial
from lib.classes import (
    SubmitWindowInfo, 
    SubmitType, 
    GridSquare,
    CORRECT
)
from game_algorithm import generate_game
import lib.stylesheets as ss
from lib.database.db_utils import get_hash_from_songname, get_db
from CONFIG import DEBUG, PB_WRAP_LEN

from PyQt5 import QtWidgets, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        # get data from db
        self._db = get_db()
        
        # generate GridSquare objects
        self.grid_buttons: list[list[GridSquare]] = []
        for i in range(3):
            buf = []
            for j in range(3):
                buf.append(GridSquare((i, j), getattr(self, f"r{i+1}c{j+1}_pb"), PB_WRAP_LEN, self._db))
            self.grid_buttons.append(buf)
        
        self.grid_displays: list[list[QtWidgets.QLabel]] = [
            [self.col_1_l, self.col_2_l, self.col_3_l],
            [self.row_1_l, self.row_2_l, self.row_3_l]
        ]
        
        self._used_song_hashes: set[str] = set()
        
        # connect input window popup signals
        for grid_row in self.grid_buttons:
            for button in grid_row:
                button.connect_click_callback(self._show_input_window)
        self.restart_pb.clicked.connect(self._restart_game)
        
        self._all_song_names: list[str] = [songname for _, songname in self._db["songs"].items()]
        
        # set up autocompleter
        self._completer = QtWidgets.QCompleter(self._all_song_names)
        self._completer.setCaseSensitivity(False)
        
        self.load_new_game()
        self._display_constraints()
        
        self._set_styles_to_default()
    
    # gets info from input window on what song was selected
    @QtCore.pyqtSlot(SubmitWindowInfo)
    def _handle_input_window(self, value: SubmitWindowInfo):
        self.setDisabled(False)  # re-enable main window
        # ignore cancelled inputs
        if value.status == SubmitType.CANCEL:
            return
        
        
        x, y = value.pos
        if value.song_name == "":
            self.grid_buttons[x][y].clear()
            self._update_game_status()
            self._check_complete()
            return
        
        try:
            song_hash = get_hash_from_songname(value.song_name)
        except ValueError:
            self._show_error_window("Invalid Song!")
            return
        
        if song_hash in self._used_song_hashes:
            self._show_error_window("Song already used...")
            return
            
        self.grid_buttons[x][y].update(song_hash)
        self._update_game_status()
        self._check_complete()
    
    def _show_input_window(self, row:int, col:int):
        self._iw = InputWindow()
        self._iw.set_pos(row, col) # window needs to know which cell it corresponds to
        self._iw.entry_le.setCompleter(self._completer) # autocomplete
        self._iw.callback.connect(self._handle_input_window)
        self._iw.show()
        # disable main window while the popup window is open
        self.setDisabled(True)
    
    def _display_constraints(self):
        for top_display, top_constraint in zip(self.grid_displays[0], self._game.top_constraints):
            top_display.setText(str(top_constraint))
            top_display.setWordWrap(True)
        for side_display, side_constraint in zip(self.grid_displays[1], self._game.side_constraints):
            side_display.setText(str(side_constraint))
            side_display.setWordWrap(True)
                
    def _set_styles_to_default(self):
        for button_list in self.grid_buttons:
            for button in button_list:
                button.clear()
        
        for display_list in self.grid_displays:
            for display in display_list:
                display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                display.setStyleSheet(ss.display_ss)
        
        self.restart_pb.setStyleSheet(ss.restart_button_ss)
    
    def _restart_game(self):
        self.setDisabled(True)
        self.setWindowTitle("Loading...")
        self.load_new_game()
        self._display_constraints()
        self._set_styles_to_default()
        self.setWindowTitle("The Grateful Grid")
        self.setDisabled(False)
        for button_list in self.grid_buttons:
            for button in button_list:
                button.set_enable(True)
    
    def _update_game_status(self):
        self._used_song_hashes = set()
        for button_list in self.grid_buttons:
            for button in button_list:
                if button.song_hash is not None:
                    self._used_song_hashes.add(button.song_hash)
                    
        for button_list in self.grid_buttons:
            for button in button_list:
                button.check_overconstrained(self._used_song_hashes)
    
    def _check_complete(self):
        for button_list in self.grid_buttons:
            for button in button_list:
                if button.status != CORRECT: return
        
        self.setWindowTitle("YOU WIN!")
        for button_list in self.grid_buttons:
            for button in button_list:
                button.set_enable(False)
    
    def load_new_game(self):
        self._game = generate_game()
        self._used_song_hashes = set()
        if DEBUG: self._game.print_all_info(self._db)
        for i in range(3):
            for j in range(3):
                self.grid_buttons[i][j].possibilities = self._game.possibilities_at(i, j)

    def _show_error_window(self, text: str):
        self._ew = ErrorWindow()
        self._ew.label.setText(text)
        self._ew.callback.connect(partial(self.setDisabled, False))
        self._ew.show()
        self.setDisabled(True)


# runner and include guard
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
if __name__ == "__main__":
    main()