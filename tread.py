from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from utils.sim import sim
from main import MainWindow
import time
import csv

#继承 QThread 类
class BigWorkThread(QThread):

    finishSignal = pyqtSignal(str)
    updateSignal = pyqtSignal(list)

    def __init__(self, workDistance, k, radian, wavelength,parent=None):
        super(BigWorkThread, self).__init__(parent)
        self.workDistance = workDistance
        self.k = k
        self.wavelength = wavelength
        self.radian = radian
        self.path = './data/'
        self.writeData = []


    def run(self):

        if self.k == 0.0 or self.radian == 0.0:
            QMessageBox.information(self, "warning", "Please set the value of Radian or K")
        else:
            while self.workDistance <= 10:
                simTest = sim(k=self.k, radian=self.radian, wavelength=632.8)

                startPoint = int(self.workDistance * 10000)
                self.I0, self.I = simTest.simluation(startPoint)
                self.writeData.append(self.I)

                if self.workDistance > 10:
                    self.workDistance = 0
                else:
                    self.workDistance += 0.1
                    time.sleep(0.1)
                    self.updateSignal.emit([self.I0, self.I, self.workDistance])

            self.finishSignal.emit("Finish")
            self.save_data()
            self.workDistance = 0

    def save_data(self):

        f = open('./data/data_%f.csv' % 0.01, 'w')
            #with open('./data/data_%f.csv' % self.radian) as f:
        writer = csv.writer(f)
        for data in self.writeData:
            writer.writerow(data)
        f.close()

        f = open('./data/I0_data_%f.csv' % 0.01, 'w', newline='')
            # with open('./data/data_%f.csv' % self.radian) as f:
        writer = csv.writer(f)
        writer.writerow(self.I0)
        f.close()




