from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from utils.sim import sim
from main import MainWindow
import time

#继承 QThread 类
class BigWorkThread(QThread):

    finishSignal = pyqtSignal(list)
    def __init__(self, t,parent=None):
        super(BigWorkThread, self).__init__(parent)
        self.t = t


    def run(self):
        if self.k == 0.0 or self.radian == 0.0:
            QMessageBox.information(self, "warning", "Please set the value of Radian or K")
        else:
            simTest = sim(k=self.k, radian=self.radian, wavelength=632.8)

            startPoint = int(self.workDistance * 10000)
            self.I0, self.I = simTest.simluation(startPoint)
            if self.workDistance > 10:
                self.workDistance = 0
            else:
                self.workDistance += 0.1
                time.sleep(1)
                self.auto.emit(1)

        self.finishSignal.emit(['tread Finish'])