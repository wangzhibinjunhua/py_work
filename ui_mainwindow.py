# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1114, 860)
        MainWindow.setStyleSheet("")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.btn_com = QtWidgets.QPushButton(self.centralWidget)
        self.btn_com.setGeometry(QtCore.QRect(130, 40, 61, 31))
        self.btn_com.setObjectName("btn_com")
        self.et_com = QtWidgets.QTextEdit(self.centralWidget)
        self.et_com.setGeometry(QtCore.QRect(20, 40, 91, 31))
        self.et_com.setObjectName("et_com")
        self.et_rssi = QtWidgets.QTextEdit(self.centralWidget)
        self.et_rssi.setGeometry(QtCore.QRect(200, 10, 91, 31))
        self.et_rssi.setObjectName("et_rssi")
        self.cb_rssi = QtWidgets.QCheckBox(self.centralWidget)
        self.cb_rssi.setGeometry(QtCore.QRect(300, 10, 61, 31))
        self.cb_rssi.setObjectName("cb_rssi")
        self.et_devname = QtWidgets.QTextEdit(self.centralWidget)
        self.et_devname.setGeometry(QtCore.QRect(430, 10, 181, 31))
        self.et_devname.setObjectName("et_devname")
        self.cb_devname = QtWidgets.QCheckBox(self.centralWidget)
        self.cb_devname.setGeometry(QtCore.QRect(630, 20, 91, 21))
        self.cb_devname.setObjectName("cb_devname")
        self.btn_conn_state = QtWidgets.QPushButton(self.centralWidget)
        self.btn_conn_state.setGeometry(QtCore.QRect(890, 20, 81, 51))
        self.btn_conn_state.setObjectName("btn_conn_state")
        self.btn_disconnect = QtWidgets.QPushButton(self.centralWidget)
        self.btn_disconnect.setGeometry(QtCore.QRect(240, 60, 81, 31))
        self.btn_disconnect.setObjectName("btn_disconnect")
        self.btn_next = QtWidgets.QPushButton(self.centralWidget)
        self.btn_next.setGeometry(QtCore.QRect(370, 50, 111, 41))
        self.btn_next.setObjectName("btn_next")
        self.tv_log = QtWidgets.QTextBrowser(self.centralWidget)
        self.tv_log.setGeometry(QtCore.QRect(20, 100, 641, 291))
        self.tv_log.setObjectName("tv_log")
        self.btn_acc = QtWidgets.QPushButton(self.centralWidget)
        self.btn_acc.setGeometry(QtCore.QRect(20, 560, 101, 41))
        self.btn_acc.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btn_acc.setObjectName("btn_acc")
        self.btn_gyr = QtWidgets.QPushButton(self.centralWidget)
        self.btn_gyr.setGeometry(QtCore.QRect(150, 560, 101, 41))
        self.btn_gyr.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btn_gyr.setObjectName("btn_gyr")
        self.btn_cps = QtWidgets.QPushButton(self.centralWidget)
        self.btn_cps.setGeometry(QtCore.QRect(280, 560, 121, 41))
        self.btn_cps.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btn_cps.setObjectName("btn_cps")
        self.btn_sn = QtWidgets.QPushButton(self.centralWidget)
        self.btn_sn.setGeometry(QtCore.QRect(430, 560, 111, 41))
        self.btn_sn.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btn_sn.setObjectName("btn_sn")
        self.btn_mac = QtWidgets.QPushButton(self.centralWidget)
        self.btn_mac.setGeometry(QtCore.QRect(570, 560, 121, 41))
        self.btn_mac.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btn_mac.setObjectName("btn_mac")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 10, 101, 21))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(30, 440, 101, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(30, 530, 81, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(160, 530, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(300, 530, 61, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(460, 530, 61, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(600, 530, 54, 12))
        self.label_6.setObjectName("label_6")
        self.tv_last_snamac = QtWidgets.QTextBrowser(self.centralWidget)
        self.tv_last_snamac.setGeometry(QtCore.QRect(90, 400, 571, 41))
        self.tv_last_snamac.setObjectName("tv_last_snamac")
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(40, 410, 31, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralWidget)
        self.label_8.setGeometry(QtCore.QRect(30, 480, 41, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralWidget)
        self.label_9.setGeometry(QtCore.QRect(900, 160, 71, 51))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.btn_result = QtWidgets.QPushButton(self.centralWidget)
        self.btn_result.setGeometry(QtCore.QRect(780, 230, 281, 251))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.btn_result.setFont(font)
        self.btn_result.setObjectName("btn_result")
        self.conn_info = QtWidgets.QTextBrowser(self.centralWidget)
        self.conn_info.setGeometry(QtCore.QRect(810, 90, 221, 41))
        self.conn_info.setObjectName("conn_info")
        self.ln_total_num = QtWidgets.QLCDNumber(self.centralWidget)
        self.ln_total_num.setGeometry(QtCore.QRect(800, 500, 161, 41))
        self.ln_total_num.setObjectName("ln_total_num")
        self.btn_reset_total_num = QtWidgets.QPushButton(self.centralWidget)
        self.btn_reset_total_num.setGeometry(QtCore.QRect(980, 500, 75, 31))
        self.btn_reset_total_num.setObjectName("btn_reset_total_num")
        self.tv_systime = QtWidgets.QTextBrowser(self.centralWidget)
        self.tv_systime.setGeometry(QtCore.QRect(800, 550, 251, 51))
        self.tv_systime.setObjectName("tv_systime")
        self.et_snmac = QtWidgets.QLineEdit(self.centralWidget)
        self.et_snmac.setGeometry(QtCore.QRect(90, 460, 571, 51))
        self.et_snmac.setObjectName("et_snmac")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1114, 23))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_com.setText(_translate("MainWindow", "打开"))
        self.cb_rssi.setText(_translate("MainWindow", "Rssi"))
        self.cb_devname.setText(_translate("MainWindow", "过滤设备名"))
        self.btn_conn_state.setText(_translate("MainWindow", "连接状态"))
        self.btn_disconnect.setText(_translate("MainWindow", "断开连接"))
        self.btn_next.setText(_translate("MainWindow", "继续"))
        self.btn_acc.setText(_translate("MainWindow", "fail"))
        self.btn_gyr.setText(_translate("MainWindow", "fail"))
        self.btn_cps.setText(_translate("MainWindow", "fail"))
        self.btn_sn.setText(_translate("MainWindow", "fail"))
        self.btn_mac.setText(_translate("MainWindow", "fail"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">串口号</p></body></html>"))
        self.label.setText(_translate("MainWindow", "SN/MAC"))
        self.label_2.setText(_translate("MainWindow", "加速度传感器"))
        self.label_3.setText(_translate("MainWindow", "陀螺仪"))
        self.label_4.setText(_translate("MainWindow", "地磁"))
        self.label_5.setText(_translate("MainWindow", "SN"))
        self.label_6.setText(_translate("MainWindow", "MAC"))
        self.label_7.setText(_translate("MainWindow", "写入:"))
        self.label_8.setText(_translate("MainWindow", "扫码枪:"))
        self.label_9.setText(_translate("MainWindow", "结果"))
        self.btn_result.setText(_translate("MainWindow", "PASS"))
        self.btn_reset_total_num.setText(_translate("MainWindow", "重置"))

