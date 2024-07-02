# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(582, 526)
        MainWindow.setStyleSheet("QPushButton {\n"
"    border-radius: 10px;\n"
"    background-color: rgb(234, 235, 164)\n"
"}\n"
"\n"
"QTextEdit {\n"
"    border-radius: 10px;\n"
"    font: 10pt \"Segoe UI Variable Display\";\n"
"    \n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display Light")
        font.setPointSize(24)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_2.addWidget(self.title_label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.r2c1_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r2c1_pb.sizePolicy().hasHeightForWidth())
        self.r2c1_pb.setSizePolicy(sizePolicy)
        self.r2c1_pb.setMinimumSize(QtCore.QSize(120, 120))
        self.r2c1_pb.setObjectName("r2c1_pb")
        self.gridLayout.addWidget(self.r2c1_pb, 2, 1, 1, 1)
        self.r2c3_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r2c3_pb.sizePolicy().hasHeightForWidth())
        self.r2c3_pb.setSizePolicy(sizePolicy)
        self.r2c3_pb.setMinimumSize(QtCore.QSize(60, 60))
        self.r2c3_pb.setObjectName("r2c3_pb")
        self.gridLayout.addWidget(self.r2c3_pb, 2, 3, 1, 1)
        self.r1c3_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r1c3_pb.sizePolicy().hasHeightForWidth())
        self.r1c3_pb.setSizePolicy(sizePolicy)
        self.r1c3_pb.setMinimumSize(QtCore.QSize(120, 120))
        self.r1c3_pb.setObjectName("r1c3_pb")
        self.gridLayout.addWidget(self.r1c3_pb, 1, 3, 1, 1)
        self.r3c2_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r3c2_pb.sizePolicy().hasHeightForWidth())
        self.r3c2_pb.setSizePolicy(sizePolicy)
        self.r3c2_pb.setMinimumSize(QtCore.QSize(120, 120))
        self.r3c2_pb.setObjectName("r3c2_pb")
        self.gridLayout.addWidget(self.r3c2_pb, 3, 2, 1, 1)
        self.r3c3_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r3c3_pb.sizePolicy().hasHeightForWidth())
        self.r3c3_pb.setSizePolicy(sizePolicy)
        self.r3c3_pb.setMinimumSize(QtCore.QSize(120, 120))
        self.r3c3_pb.setObjectName("r3c3_pb")
        self.gridLayout.addWidget(self.r3c3_pb, 3, 3, 1, 1)
        self.r2c2_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r2c2_pb.sizePolicy().hasHeightForWidth())
        self.r2c2_pb.setSizePolicy(sizePolicy)
        self.r2c2_pb.setMinimumSize(QtCore.QSize(60, 60))
        self.r2c2_pb.setObjectName("r2c2_pb")
        self.gridLayout.addWidget(self.r2c2_pb, 2, 2, 1, 1)
        self.r1c1_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r1c1_pb.sizePolicy().hasHeightForWidth())
        self.r1c1_pb.setSizePolicy(sizePolicy)
        self.r1c1_pb.setMinimumSize(QtCore.QSize(120, 120))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Display Light")
        self.r1c1_pb.setFont(font)
        self.r1c1_pb.setStyleSheet("font: \"Segoe UI Variable Display Light\"")
        self.r1c1_pb.setObjectName("r1c1_pb")
        self.gridLayout.addWidget(self.r1c1_pb, 1, 1, 1, 1)
        self.r3c1_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r3c1_pb.sizePolicy().hasHeightForWidth())
        self.r3c1_pb.setSizePolicy(sizePolicy)
        self.r3c1_pb.setMinimumSize(QtCore.QSize(120, 120))
        self.r3c1_pb.setObjectName("r3c1_pb")
        self.gridLayout.addWidget(self.r3c1_pb, 3, 1, 1, 1)
        self.r1c2_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r1c2_pb.sizePolicy().hasHeightForWidth())
        self.r1c2_pb.setSizePolicy(sizePolicy)
        self.r1c2_pb.setMinimumSize(QtCore.QSize(120, 120))
        self.r1c2_pb.setObjectName("r1c2_pb")
        self.gridLayout.addWidget(self.r1c2_pb, 1, 2, 1, 1)
        self.col_1_te = QtWidgets.QTextEdit(self.centralwidget)
        self.col_1_te.setObjectName("col_1_te")
        self.gridLayout.addWidget(self.col_1_te, 0, 1, 1, 1)
        self.col_2_te = QtWidgets.QTextEdit(self.centralwidget)
        self.col_2_te.setObjectName("col_2_te")
        self.gridLayout.addWidget(self.col_2_te, 0, 2, 1, 1)
        self.col_3_te = QtWidgets.QTextEdit(self.centralwidget)
        self.col_3_te.setObjectName("col_3_te")
        self.gridLayout.addWidget(self.col_3_te, 0, 3, 1, 1)
        self.row_1_te = QtWidgets.QTextEdit(self.centralwidget)
        self.row_1_te.setObjectName("row_1_te")
        self.gridLayout.addWidget(self.row_1_te, 1, 0, 1, 1)
        self.row_2_te = QtWidgets.QTextEdit(self.centralwidget)
        self.row_2_te.setReadOnly(False)
        self.row_2_te.setObjectName("row_2_te")
        self.gridLayout.addWidget(self.row_2_te, 2, 0, 1, 1)
        self.row_3_te = QtWidgets.QTextEdit(self.centralwidget)
        self.row_3_te.setObjectName("row_3_te")
        self.gridLayout.addWidget(self.row_3_te, 3, 0, 1, 1)
        self.restart_pb = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restart_pb.sizePolicy().hasHeightForWidth())
        self.restart_pb.setSizePolicy(sizePolicy)
        self.restart_pb.setObjectName("restart_pb")
        self.gridLayout.addWidget(self.restart_pb, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 582, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The Grateful Grid"))
        self.title_label.setText(_translate("MainWindow", "The Grateful Grid"))
        self.r2c1_pb.setText(_translate("MainWindow", "—"))
        self.r2c3_pb.setText(_translate("MainWindow", "—"))
        self.r1c3_pb.setText(_translate("MainWindow", "—"))
        self.r3c2_pb.setText(_translate("MainWindow", "—"))
        self.r3c3_pb.setText(_translate("MainWindow", "—"))
        self.r2c2_pb.setText(_translate("MainWindow", "—"))
        self.r1c1_pb.setText(_translate("MainWindow", "—"))
        self.r3c1_pb.setText(_translate("MainWindow", "—"))
        self.r1c2_pb.setText(_translate("MainWindow", "—"))
        self.restart_pb.setText(_translate("MainWindow", "Restart"))
