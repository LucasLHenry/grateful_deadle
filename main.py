from ui.main_window import Ui_MainWindow
from input_window_logic import InputWindow

from PyQt5 import QtWidgets
import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.grid_buttons: list[list[QtWidgets.QPushButton]] = [
            [self.r1c1_pb, self.r1c2_pb, self.r1c3_pb],
            [self.r2c1_pb, self.r2c2_pb, self.r2c3_pb],
            [self.r3c1_pb, self.r3c2_pb, self.r3c3_pb]
        ]
        
        self.grid_displays: list[list[QtWidgets.QLineEdit]] = [
            [self.col_1_le, self.col_2_le, self.col_3_le],
            [self.row_1_le, self.row_2_le, self.row_3_le]
        ]
        
        for grid_row in self.grid_buttons:
            for button in grid_row:
                button.clicked.connect(self._show_input_window)
    
    def _show_input_window(self):
        self._iw = InputWindow()
        self._iw.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    
if __name__ == "__main__":
    main()