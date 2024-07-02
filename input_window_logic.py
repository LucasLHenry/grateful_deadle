from ui.input_window import Ui_Dialog
from lib.classes import SubmitWindowInfo, SubmitType

from PyQt5 import QtWidgets, QtCore
from typing import Optional

class InputWindow(QtWidgets.QDialog, Ui_Dialog):
    callback = QtCore.pyqtSignal(SubmitWindowInfo)
    
    def __init__(self, *args, obj=None, **kwargs):
        super(InputWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.submit_pb.clicked.connect(self._submit_clicked)
        self.cancel_pb.clicked.connect(self._cancel_clicked)
    
    def set_pos(self, row: int, col: int):
        self._pos = (row, col)
    
    def _submit_clicked(self):
        output = SubmitWindowInfo(self.entry_le.text(), self._pos, SubmitType.SUMBIT)
        self.callback.emit(output)
        self.close()
    
    def _cancel_clicked(self):
        output = SubmitWindowInfo(self.entry_le.text(), self._pos, SubmitType.CANCEL)
        self.callback.emit(output)
        self.close()
        
    def closeEvent(self, event):
        self._cancel_clicked()  # to make sure we send the callback