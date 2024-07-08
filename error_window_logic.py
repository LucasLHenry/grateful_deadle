from ui.error_window import Ui_Dialog

from PyQt5 import QtWidgets, QtCore

class ErrorWindow(QtWidgets.QDialog, Ui_Dialog):
    callback = QtCore.pyqtSignal()
    
    def __init__(self, *args, obj=None, **kwargs):
        super(ErrorWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.closeEvent)
        
    def closeEvent(self, event):
        self.callback.emit()
        self.close()