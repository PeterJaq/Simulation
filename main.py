import sys
import os
import time
from utils.sim import sim
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.ui import Ui_MainWindow
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time, threading
import tread





class MainWindow(QMainWindow, Ui_MainWindow):
    auto = pyqtSignal(int)
    auto1 = pyqtSignal(str)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer(self)

    # Parameter Init
        self.k = self.doubleSpinBox_2.value()
        self.radian = self.doubleSpinBox_3.value()
        self.wavelength = 632.8
        self.I0 = None
        self.I = None
        self.workDistance = 0

    # SIGNAL CONNECT

        self.doubleSpinBox_2.valueChanged.connect(lambda: self.set_Kvalue())
        self.doubleSpinBox_3.valueChanged.connect(lambda: self.set_Radian())
        self.pushButton_One.clicked.connect(lambda: self.start_simulation())
        self.pushButton_Auto.clicked.connect(lambda: self.auto_tread())
        #tread.BigWorkThread.finishSignal.connect(lambda: self.tread_setdata())

        self.bwThread = tread.BigWorkThread(self.workDistance, self.k, self.radian, self.wavelength)
        self.bwThread.updateSignal.connect(self.tread_setdata)
        self.bwThread.finishSignal.connect(self.tread_finish)

        self.timer.timeout.connect(lambda: self.show_figure())  # 计时结束调用operate()方法
        self.timer.start(200)

    def set_Kvalue(self):
        self.k = self.doubleSpinBox_2.value()

    def set_Radian(self):
        self.radian = self.doubleSpinBox_3.value()


    def auto_tread(self):
        self.pushButton_Auto.setEnabled(False)
        self.bwThread.start()

    def tread_setdata(self, data):
        self.I0 = data[0]
        self.I = data[1]
        self.workDistance = data[2]

    def tread_finish(self, finish):
        QMessageBox.information(self, "Finish", finish)
        self.pushButton_Auto.setEnabled(True)
        self.workDistance = 0

    def show_figure(self):

        self.fig = Figure(figsize=(900, 900), dpi=100, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        for i in range(self.gridLayout.count()): self.gridLayout.removeItem(self.gridLayout.itemAt(i))
        if self.I0 is not None and self.I is not None:
            self.ax.plot(self.I0, color='red')
            self.ax.plot(self.I, color='blue')

            self.gridLayout.addWidget(self.canvas)


def init_plot():
    fig = Figure(figsize=(900, 900), dpi=100, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    return canvas

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = MainWindow()
    form.gridLayout.addWidget(init_plot())
    form.show()
    sys.exit(app.exec_())

