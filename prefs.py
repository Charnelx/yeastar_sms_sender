# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefs.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PrefWindow(object):
    def setupUi(self, PrefWindow):
        PrefWindow.setObjectName(_fromUtf8("PrefWindow"))
        PrefWindow.resize(450, 150)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PrefWindow.sizePolicy().hasHeightForWidth())
        PrefWindow.setSizePolicy(sizePolicy)
        PrefWindow.setMaximumSize(QtCore.QSize(450, 150))
        self.centralwidget = QtGui.QWidget(PrefWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_6.addWidget(self.label_3)
        self.txt_addr = QtGui.QTextEdit(self.centralwidget)
        self.txt_addr.setMaximumSize(QtCore.QSize(16777215, 25))
        self.txt_addr.setObjectName(_fromUtf8("txt_addr"))
        self.horizontalLayout_6.addWidget(self.txt_addr)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 240, -1)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.cmb_slot = QtGui.QComboBox(self.centralwidget)
        self.cmb_slot.setMinimumSize(QtCore.QSize(40, 0))
        self.cmb_slot.setMaximumSize(QtCore.QSize(40, 16777215))
        self.cmb_slot.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.cmb_slot.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cmb_slot.setObjectName(_fromUtf8("cmb_slot"))
        self.horizontalLayout_2.addWidget(self.cmb_slot)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.chk_num_auto = QtGui.QCheckBox(self.centralwidget)
        self.chk_num_auto.setText(_fromUtf8(""))
        self.chk_num_auto.setObjectName(_fromUtf8("chk_num_auto"))
        self.horizontalLayout_5.addWidget(self.chk_num_auto)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btn_save = QtGui.QPushButton(self.centralwidget)
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_def = QtGui.QPushButton(self.centralwidget)
        self.btn_def.setObjectName(_fromUtf8("btn_def"))
        self.horizontalLayout.addWidget(self.btn_def)
        self.btn_cancel = QtGui.QPushButton(self.centralwidget)
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        PrefWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PrefWindow)
        self.cmb_slot.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(PrefWindow)

    def retranslateUi(self, PrefWindow):
        PrefWindow.setWindowTitle(_translate("PrefWindow", "Настройки", None))
        self.label_3.setText(_translate("PrefWindow", "Адрес шлюза", None))
        self.label.setText(_translate("PrefWindow", "Слот для отправки СМС", None))
        self.label_2.setText(_translate("PrefWindow", "Автоматическая очистка номеров", None))
        self.btn_save.setText(_translate("PrefWindow", "Сохранить", None))
        self.btn_def.setText(_translate("PrefWindow", "По умолчанию", None))
        self.btn_cancel.setText(_translate("PrefWindow", "Отмена", None))

