# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/error.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(198, 141)
        Dialog.setStyleSheet("QPushButton {\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    background-color: rgb(234, 235, 164);\n"
"    font: 12pt;\n"
"}\n"
"\n"
"QLabel {\n"
"    border-radius: 5px;\n"
"    font: 10pt;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "*error_text_here*"))
        self.pushButton.setText(_translate("Dialog", "Ok"))
