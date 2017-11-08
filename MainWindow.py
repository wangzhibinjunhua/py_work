# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>
import sys
import configparser
import binascii
import re
import sys
import time

from PyQt5.QtGui import QTextCursor
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtCore,QtGui,QtWidgets
from gevent.corecext import SIGNAL

from ui_mainwindow import Ui_MainWindow
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow,QtWidgets.QDialog):
    config = configparser.ConfigParser()
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('蓝牙测试工具')
        self.init_config()

        self.btn_com.clicked.connect(self.btn_com_click)
        self.cb_rssi.stateChanged.connect(self.cb_rssi_state)
        self.cb_devname.stateChanged.connect(self.cb_devname_state)
        self.btn_conn_state.setStyleSheet('background-color:green')
        self.tv_last_snamac.setStyleSheet('color:green')
        self.btn_disconnect.clicked.connect(self.btn_disconnect_click)
        self.btn_next.clicked.connect(self.btn_next_click)
        self.tv_log.setFont(QtGui.QFont("Roman times",20))
        self.et_snmac.setFocus()
        self.et_snmac.setFont(QtGui.QFont("Roman times", 20))
        self.et_snmac.textChanged.connect(self.snmac_change)
        self.tv_last_snamac.setFont(QtGui.QFont("Roman times",20))
        self.set_result(False)
        self.init_com()


    def init_com(self):
        self.com=QSerialPort()
        self.com.readyRead.connect(self.on_receiveData)


    def set_result(self,result):
        if result == True:
            self.btn_result.setText('PASS')
            self.btn_result.setStyleSheet('background-color:green')
        else:
            self.btn_result.setText('FAIL')
            self.btn_result.setStyleSheet('background-color:red')

    def snmac_change(self):
        #print('sn mac change')
        snmac=self.et_snmac.toPlainText()
        if len(snmac) == 28:
            self.tv_last_snamac.setText(snmac)
            self.et_snmac.clear()
            self.et_snmac.setFocus(True)
            self.write_snmac()
        elif len(snmac) >28:
            self.et_snmac.clear()
            self.et_snmac.setFocus(True)
            QtWidgets.QMessageBox.critical(self, '严重错误', 'sn/mac 格式不正确')

    def write_snmac(self):
        print('write sn mac')
        snmac=self.tv_last_snamac.toPlainText()
        if len(snmac) != 28:
            QtWidgets.QMessageBox.critical(self, '严重错误', 'sn/mac 格式不正确')
            self.set_result(False)
            return
        self.set_result(True)
        print('write sn')
        sn=snmac[:15]
        print('sn='+sn)
        time.sleep(3)
        print('write mac')
        mac=snmac[26:28]+snmac[24:26]+snmac[22:24]+snmac[20:22]+snmac[18:20]+snmac[16:18]

        print('mac='+mac)


    def write_sn(self,sn):
        value='0aff'+sn
        self.send_data(value)

    def write_mac(self,mac):
        pass

    def read_sensor(self):
        pass

    def on_receiveData(self):
        try:
            '''将串口接收到的QByteArray格式数据转为bytes,并用gkb或utf8解码'''
            receivedData = bytes(self.com.readAll())
        except:
            QtWidgets.QMessageBox.critical(self, '严重错误', '串口接收数据错误')
        if len(receivedData) > 0:
            self.tv_log.insertPlainText(receivedData.decode('ascii'))
            self.tv_log.moveCursor(QTextCursor.End)
            self.parse_cmd(receivedData)

    def parse_cmd(self,cmd):
        if cmd.startswith('AT'):
            print(cmd)
        elif cmd.startswith('0aff01'):
            print(cmd)

    def openSerial(self,com_id):

        self.com.setPortName('COM'+com_id)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QtWidgets.QMessageBox.critical(self, '严重错误', '串口打开失败')
                return -1
        except:
            QtWidgets.QMessageBox.critical(self, '严重错误', '串口打开失败')
            return -1
        self.com.setBaudRate(115200)

        return 0

    def send_data(self,data):
        if len(data) ==0:
            return
        n = self.com.write(data.encode('utf-8', "ignore"))

    def init_config(self):
        self.config.read('v.cfg')

        com = self.config.get('info', 'com')
        self.et_com.setText(com)
        self.et_com.setFont(QtGui.QFont("Roman times", 20))
        rssi = self.config.get('info', 'rssi')
        self.et_rssi.setText(rssi)
        self.et_rssi.setFont(QtGui.QFont("Roman times", 20))
        devname = self.config.get('info', 'devname')
        self.et_devname.setText(devname)
        self.et_devname.setFont(QtGui.QFont("Roman times", 20))

    def btn_disconnect_click(self):

        ##for test
        self.send_data('ff01')

    def btn_next_click(self):
        self.et_snmac.setFocus()

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
        if self.openSerial(com)!= -1:
            self.et_com.setEnabled(False)
            self.btn_com.setEnabled(False)
            print(com)
            self.config.set('info','com',com)
            self.config.write(open('v.cfg','w'))



if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainWindow=MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())