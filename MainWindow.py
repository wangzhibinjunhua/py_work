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
        self.setWindowTitle('蓝牙测试工具V1.0_20171109')
        self.init_config()

        self.btn_com.clicked.connect(self.btn_com_click)
        self.cb_rssi.stateChanged.connect(self.cb_rssi_state)
        self.cb_devname.stateChanged.connect(self.cb_devname_state)
        self.btn_conn_state.setStyleSheet('background-color:green')
        self.tv_last_snamac.setStyleSheet('color:green')
        self.btn_disconnect.clicked.connect(self.btn_disconnect_click)
        self.btn_next.clicked.connect(self.btn_next_click)
        self.tv_log.setFont(QtGui.QFont("Roman times",14))
        self.conn_info.setFont(QtGui.QFont("Roman times", 14))
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
        self.conn_info.setText('未连接')
        self.con_state=False
        self.sensor_re=False
        self.read_sensor_num=0
        self.write_snmac_flag = False
        self.sn_v=''
        self.mac_v=''
        self.acc_result=False
        self.gyr_result=False
        self.cps_result=False
        self.sn_result=False
        self.mac_result=False
        self.write_sn_state=False
        self.write_mac_state=False

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
        if self.write_snmac_flag == False:
            return
        snmac=self.et_snmac.toPlainText()
        if len(snmac) == 28:
            if snmac.startswith('QD'):
                self.tv_last_snamac.clear()
                self.tv_last_snamac.setText(snmac)
                self.et_snmac.clear()
                self.et_snmac.setFocus(True)
                self.write_snmac()
            else:
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
        self.sn_v=sn
        self.write_sn(sn)
        mac=snmac[26:28]+snmac[24:26]+snmac[22:24]+snmac[20:22]+snmac[18:20]+snmac[16:18]
        print('mac='+mac)
        self.mac_v=mac
        #Timer(3, self.write_mac, (mac,)).start()

    def write_sn(self,sn):
        self.write_sn_state=True
        print('write sn:'+sn)
        self.tv_log.insertPlainText('write sn:' + sn + '\n')
        self.tv_log.moveCursor(QTextCursor.End)
        value='0bffffffff'+bytes.decode((binascii.b2a_hex(sn.encode())))
        self.send_data(value)



    def write_mac(self,mac):
        self.write_mac_state=True
        print('write mac:'+mac)
        self.tv_log.insertPlainText('write mac:' + mac + '\n')
        self.tv_log.moveCursor(QTextCursor.End)
        value='0affffffff'+mac
        self.send_data(value)


    def read_sensor(self):
        _data='aa1700c1'
        self.send_data(_data)
        self.read_sensor_num+=1

    def stop_sensor(self):
        _data='ff07'
        self.send_data(_data)


    def on_receiveData(self):
        try:
            '''将串口接收到的QByteArray格式数据转为bytes,并用gkb或utf8解码'''
            receivedData = bytes(self.com.readAll())
            print(receivedData)
        except:
            QtWidgets.QMessageBox.critical(self, '严重错误', '串口接收数据错误')

        if len(receivedData) > 0:
            str_receivedData = receivedData.decode('utf-8','ignore')
            if 'OK+LOST' in str_receivedData:
                print('ble disconnected')
                self.con_state = False
                self.conn_info.setText('未连接')

            print('re_mode:'+self.rw_flag)

            if self.rw_flag == 'HEXMODE':
                #data = binascii.b2a_hex(receivedData).decode('ascii')
                data = binascii.b2a_hex(receivedData).decode('ascii')
                print('data='+data)
                print(type(data))
                #pattern = re.compile('.{2,2}')
                #hexStr = ' '.join(pattern.findall(data)) + ' '
                #print('2222 hexstr='+hexStr+'len='+len(hexStr))
                self.tv_log.insertPlainText('receive:' + data+'\n')
                self.tv_log.moveCursor(QTextCursor.End)
                self.parse_cmd(data)

            else:
                self.parse_cmd(str_receivedData)
                self.tv_log.insertPlainText('receive:'+str_receivedData+'\n')
                self.tv_log.moveCursor(QTextCursor.End)



    def parse_cmd(self,cmd):

        print('parse_cmd: mode='+self.rw_flag)
        if self.rw_flag == 'SCAN':
            if ',' in cmd:
                device_id=cmd[:1]
                s=cmd.split(',')
                device_rssi=s[1]
                device_name=s[2]
                #for test
                #self.ble_reconnect()
                #return
                ###
                if self.cb_rssi.isChecked():
                    if int(device_rssi)<int(self.et_rssi.toPlainText()):
                        print('rssi:'+device_rssi+'/'+self.et_rssi.toPlainText())
                        return
                if self.cb_devname.isChecked():
                    name=self.et_devname.toPlainText()
                    if  name in device_name== False:

                        print('name:'+device_name+'/'+self.et_devname.toPlainText())
                        return
                self.ble_connect(device_id)
        elif self.rw_flag == 'CONN':
            if 'OK+CONN' in cmd:
                self.conn_info.setText('已连接蓝牙设备')
                self.con_state=True

            elif 'Chars Found' in cmd:
                self.rw_flag='HEXMODE'
                self.read_sensor()

        elif self.rw_flag == 'HEXMODE':
            print('cmd:' + cmd)
            if cmd.startswith('aa9706') and len(cmd) == 6:
                #print('1111111111')
                self.tmp_sensor=cmd
                self.sensor_re=True
                return
            if self.sensor_re == True:
                if len(cmd)==40:
                    #print('3333333333')
                    self.sensor_re=False
                    result_sensor=self.tmp_sensor+cmd;
                    self.cal_sensor(result_sensor)
                    return
            if cmd.startswith('aa9706') and len(cmd)==46:
                #print('22222222')
                self.cal_sensor(cmd)
                return
            if cmd.startswith('ff07ff') and len(cmd)==6:
                self.tv_log.insertPlainText('stop sensor\n')
                self.tv_log.moveCursor(QTextCursor.End)
                self.write_snmac_flag=True
                self.et_snmac.clear()
                self.et_snmac.setFocus(True)
                return
            if cmd.startswith('0bff') and len(cmd)==36:
                re_sn=cmd[6:36]
                if re_sn == bytes.decode((binascii.b2a_hex(self.sn_v.encode()))):
                    self.set_sn_result(True)
                    self.sn_result=True
                else:
                    self.set_sn_result(False)
                    self.sn_result = False
                self.write_mac(self.mac_v)
                return
            if cmd.startswith('0aff') and len(cmd)==18:
                re_mac=cmd[6:18]
                if re_mac.lower()== self.mac_v.lower():
                    self.set_mac_result(True)
                    self.mac_result=True
                else:
                    self.set_mac_result(False)
                    self.mac_result=False

                if self.acc_result and self.gyr_result and self.cps_result and self.sn_result and self.mac_result:
                    self.set_result(True)
                else:
                    self.set_result(False)
                return

    def cal_sensor(self,cmd):
        for i in range(6, 30):
            #print('i=' + str(i) + 'v=' + cmd[i])
            if cmd[i] != '0':
                self.set_acc_result(True)
                self.acc_result = True
                break
        for i in range(30, 38):
            #print('i=' + str(i) + 'v=' + cmd[i])
            if cmd[i] != '0':
                self.set_gyr_result(True)
                self.gyr_result = True
                break
        for i in range(38, 46):
            #print('i=' + str(i) + 'v=' + cmd[i])
            if cmd[i] != '0':
                self.set_cps_result(True)
                self.cps_result = True
                break
        if self.read_sensor_num==1:
            self.tv_log.insertPlainText('第1次读取sensor:' + cmd+'\n')
            self.tv_log.insertPlainText('sleep 3s \n')
            self.tv_log.moveCursor(QTextCursor.End)
            print('第一次时间:')
            print(time.time())
            time.sleep(3)
            self.read_sensor()
        elif self.read_sensor_num==2:
            print('第二次时间:')
            print(time.time())
            self.tv_log.insertPlainText('第2次读取sensor:' + cmd+'\n')
            self.tv_log.moveCursor(QTextCursor.End)
            self.stop_sensor()

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
        self.et_snmac.setFocus()
        ##for test
        # self.read_sensor()
        # Timer(2, self.read_sensor, ()).start()
        # Timer(3, self.set_acc_result, (True,)).start()
        # Timer(3.5, self.set_gyr_result, (True,)).start()
        # Timer(4, self.set_cps_result, (True,)).start()
        return 0

    def send_data(self,data):
        if len(data) ==0:
            return

        if self.rw_flag == 'HEXMODE':
            print('send hex mode')
            print(data)
            s=data.replace(' ', '')
            try:
                hexData = binascii.a2b_hex(s)
            except:
                QtWidgets.QMessageBox.critical(self, '错误', '转换编码错误')
                return
            try:
                n = self.com.write(hexData)
                self.tv_log.insertPlainText('send:' + data + '\n')
                self.tv_log.moveCursor(QTextCursor.End)
            except:
                QtWidgets.QMessageBox.critical(self, '异常', '十六进制发送错误')
                return
        else:
            n = self.com.write(data.encode('utf-8', "ignore"))
            self.tv_log.insertPlainText('send:'+data+'\n')
            self.tv_log.moveCursor(QTextCursor.End)


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

        self.ble_disconnect()

    def btn_next_click(self):
        self.et_snmac.setFocus()
        self.reset_all_result()

        self.ble_scan()

    def cb_rssi_state(self,state):
        self.et_snmac.setFocus()
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
        self.et_snmac.setFocus()
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


    def ble_scan(self):
        self.rw_flag='SCAN'
        _cmd='AT+SCAN?'
        self.send_data(_cmd)
        self.conn_info.setText('BLE Scaning...')

    def ble_connect(self,id):
        self.rw_flag = 'CONN'
        _cmd='AT+CONN'+id
        self.send_data(_cmd)

    def ble_reconnect(self):
        self.rw_flag = 'CONN'
        _cmd='AT+CONNL'
        self.send_data(_cmd)

    def ble_disconnect(self):
        self.rw_flag= 'DISCON'
        _cmd='AT+DISCON'
        self.send_data(_cmd)

    def ble_set_tx_uuid(self):
        _cmd='AT+CHTX10'
        self.send_data(_cmd)

    def ble_set_rx_uuid(self):
        _cmd='AT+CHRX11'
        self.send_data(_cmd)

    def ble_set_scan_time(self,time=5):
        _cmd='AT+SDUR'+time
        self.send_data(_cmd)

    def ble_set_baud(self,baud=115200):
        if baud==115200:
            id=4
        elif baud==9600:
            id=0
        elif baud==19200:
            id=1
        elif baud==38400:
            id=2
        elif baud==57600:
            id=3
        else:
            id=4
        _cmd='AT+BAUD'+id
        self.send_data(_cmd)


    def ble_reset(self):
        _cmd='AT+RESET'
        self.send_data(_cmd)

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