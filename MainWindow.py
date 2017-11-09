# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>
import sched
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
from threading import Timer

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
        self.init_com()
        self.reset_all_result()
        self.con_state_timer=QtCore.QTimer()
        self.con_state_timer.timeout.connect(self.update_con_state)
        self.con_state_counter=0
        self.con_state=False
        self.con_state_timer.start(200)


    def init_com(self):
        self.com=QSerialPort()
        self.com.readyRead.connect(self.on_receiveData)

    def update_con_state(self):
        if  self.con_state_counter <=2:
            self.con_state_counter+=1
            if self.con_state == False:
                self.btn_conn_state.setStyleSheet('background-color:red')
            else:
                self.btn_conn_state.setStyleSheet('background-color:green')
        else:
            self.con_state_counter = 0
            self.btn_conn_state.setStyleSheet('background-color:white ')

    def set_result(self,result):
        print('set_result:',result)
        if result == True:
            self.btn_result.setText('PASS')
            self.btn_result.setStyleSheet('background-color:green')
        else:
            self.btn_result.setText('FAIL')
            self.btn_result.setStyleSheet('background-color:red')

    def reset_all_result(self):
        self.set_result(False)
        self.set_acc_result(False)
        self.set_gyr_result(False)
        self.set_cps_result(False)
        self.set_sn_result(False)
        self.set_mac_result(False)

    def set_acc_result(self,r):
        if r == True:
            self.btn_acc.setText('PASS')
            self.btn_acc.setStyleSheet('background-color:green')
        else:
            self.btn_acc.setText('FAIL')
            self.btn_acc.setStyleSheet('background-color:red')

    def set_gyr_result(self,r):
        if r == True:
            self.btn_gyr.setText('PASS')
            self.btn_gyr.setStyleSheet('background-color:green')
        else:
            self.btn_gyr.setText('FAIL')
            self.btn_gyr.setStyleSheet('background-color:red')

    def set_cps_result(self,r):
        if r == True:
            self.btn_cps.setText('PASS')
            self.btn_cps.setStyleSheet('background-color:green')
        else:
            self.btn_cps.setText('FAIL')
            self.btn_cps.setStyleSheet('background-color:red')

    def set_sn_result(self,r):
        if r == True:
            self.btn_sn.setText('PASS')
            self.btn_sn.setStyleSheet('background-color:green')
        else:
            self.btn_sn.setText('FAIL')
            self.btn_sn.setStyleSheet('background-color:red')

    def set_mac_result(self,r):
        if r == True:
            self.btn_mac.setText('PASS')
            self.btn_mac.setStyleSheet('background-color:green')
        else:
            self.btn_mac.setText('FAIL')
            self.btn_mac.setStyleSheet('background-color:red')

    def snmac_change(self):
        #print('sn mac change')
        snmac=self.et_snmac.toPlainText()
        if len(snmac) == 28:
            self.tv_last_snamac.clear()
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

        sn=snmac[:15]
        print('sn='+sn)
        self.write_sn(sn)
        mac=snmac[26:28]+snmac[24:26]+snmac[22:24]+snmac[20:22]+snmac[18:20]+snmac[16:18]
        print('mac='+mac)
        Timer(3, self.write_mac, (mac,)).start()

    def write_sn(self,sn):
        print('write sn:'+sn)
        value='0bffffffff'+sn
        self.send_data(value)

        #test
        self.set_sn_result(True)


    def write_mac(self,mac):
        print('write mac:'+mac)
        value='0affffffff'+mac
        self.send_data(value)

        #test
        self.set_mac_result(True)
        self.set_result(True)

    def read_sensor(self):
        pass

    def on_receiveData(self):
        try:
            '''将串口接收到的QByteArray格式数据转为bytes,并用gkb或utf8解码'''
            receivedData = bytes(self.com.readAll())
            if len(receivedData) > 0:
                str_receivedData=receivedData.decode('ascii')
                self.tv_log.insertPlainText(str_receivedData)
                self.tv_log.moveCursor(QTextCursor.End)
                self.parse_cmd(str_receivedData)
        except:
            QtWidgets.QMessageBox.critical(self, '严重错误', '串口接收数据错误')


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
        self.con_state=True

        ##for test
        Timer(3, self.set_acc_result, (True,)).start()
        Timer(3.5, self.set_gyr_result, (True,)).start()
        Timer(4, self.set_cps_result, (True,)).start()
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
        self.et_devname.setFont(QtGui.QFont("Roman times", 12))

    def btn_disconnect_click(self):

        ##for test
        self.send_data('ff01')

    def btn_next_click(self):
        self.et_snmac.setFocus()
        self.reset_all_result()
        ##for test
        Timer(3, self.set_acc_result, (True,)).start()
        Timer(3.5, self.set_gyr_result, (True,)).start()
        Timer(4, self.set_cps_result, (True,)).start()

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

    def closeSerial(self):
        self.com.close()

    def __del__(self):
        print('del')
        self.closeSerial()
        if self.con_state_timer.isActive():
            self.con_state_timer.stop()

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainWindow=MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())