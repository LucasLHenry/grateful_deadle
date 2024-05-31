# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/input.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 128)
        Dialog.setStyleSheet("QPushButton {\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: rgb(234, 235, 164);\n"
"    font-size: 12;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border-radius: 5px;\n"
"    font-size: 12;\n"
"}")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.entry_le = QtWidgets.QLineEdit(Dialog)
        self.entry_le.setObjectName("entry_le")
        self.verticalLayout.addWidget(self.entry_le)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.submit_pb = QtWidgets.QPushButton(Dialog)
        self.submit_pb.setObjectName("submit_pb")
        self.horizontalLayout.addWidget(self.submit_pb)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancel_pb = QtWidgets.QPushButton(Dialog)
        self.cancel_pb.setObjectName("cancel_pb")
        self.horizontalLayout.addWidget(self.cancel_pb)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.submit_pb.setText(_translate("Dialog", "Submit"))
        self.cancel_pb.setText(_translate("Dialog", "Cancel"))
