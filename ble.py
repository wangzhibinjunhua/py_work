# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>

import serial.tools.list_ports
import sys
from PyQt5.QtWidgets import QApplication , QMainWindow
from bleui import  *

app = QApplication(sys.argv)
mainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mainWindow)
mainWindow.show()
sys.exit(app.exec_())