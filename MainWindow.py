# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>
import sys
import configparser
from PyQt5 import QtCore,QtGui,QtWidgets
from ui_mainwindow import Ui_MainWindow
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    config = configparser.ConfigParser()
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.init_config()

        self.btn_com.clicked.connect(self.btn_com_click)
        self.cb_rssi.stateChanged.connect(self.cb_rssi_state)
        self.cb_devname.stateChanged.connect(self.cb_devname_state)
        self.btn_conn_state.setStyleSheet('background-color:green')


    def init_config(self):
        self.config.read('v.cfg')
        com = self.config.get('info', 'com')
        self.et_com.setText(com)
        rssi = self.config.get('info', 'rssi')
        self.et_rssi.setText(rssi)
        devname = self.config.get('info', 'devname')
        self.et_devname.setText(devname)

    def cb_rssi_state(self,state):
        if state == QtCore.Qt.Checked:
            print('rssi true')
            self.et_rssi.setEnabled(False)
            rssi=self.et_rssi.toPlainText()
            self.config.set('info', 'rssi', rssi)
            self.config.write(open('v.cfg', 'w'))
        else:
            print('rssi false')
            self.et_rssi.setEnabled(True)

    def cb_devname_state(self,state):
        if state == QtCore.Qt.Checked:
            print('devname true')
            self.et_devname.setEnabled(False)
            devname=self.et_devname.toPlainText()
            self.config.set('info', 'devname', devname)
            self.config.write(open('v.cfg', 'w'))
        else:
            print('devname false')
            self.et_devname.setEnabled(True)

    def btn_com_click(self):
        print('btn com click')
        com=self.et_com.toPlainText()
        self.et_com.setEnabled(False)
        print(com)
        self.config.set('info','com',com)
        self.config.write(open('v.cfg','w'))


if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainWindow=MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())