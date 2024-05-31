from ui.input_window import Ui_Dialog

from PyQt5 import QtWidgets
import sys

class InputWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(InputWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)