
# -*- coding: utf-8 -*-
# @Time    : 2016-12-07 16:00
# @Author  : wzb<wangzhibin_x@foxmail.com>


import  sys
from PyQt5.QtWidgets import QWidget,QCheckBox,QApplication
from PyQt5.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cb=QCheckBox('show title',self)
        cb.move(50,50)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)

        self.setGeometry(300,300,500,450)
        self.setWindowTitle('qcheckbox')
        self.show()

    def changeTitle(self,state):
        if state == Qt.Checked:
            self.setWindowTitle('true')
        else :
            self.setWindowTitle('false')


if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())