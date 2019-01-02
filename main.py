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

    # SIGNAL CONNECT

        self.doubleSpinBox_2.valueChanged.connect(lambda: self.set_Kvalue())
        self.doubleSpinBox_3.valueChanged.connect(lambda: self.set_Radian())
        self.pushButton_One.clicked.connect(lambda: self.start_simulation())
        self.pushButton_Auto.clicked.connect(lambda: self.auto_tread())
        #self.auto.connect(lambda: self.show_figure())
        #self.auto1.connect(lambda: self.auto_tread())

    # Parameter Init

        self.k = self.doubleSpinBox_2.value()
        self.radian = self.doubleSpinBox_3.value()
        self.wavelength = 632.8
        self.I0 = None
        self.I = None
        self.workDistance = 0

    def set_Kvalue(self):
        self.k = self.doubleSpinBox_2.value()

    def set_Radian(self):
        self.radian = self.doubleSpinBox_3.value()

    def start_simulation(self):

        if self.k == 0.0 or self.radian == 0.0:
            QMessageBox.information(self, "warning", "Please set the value of Radian or K")
        else:
            simTest = sim(k=self.k, radian=self.radian, wavelength=632.8)
            i = int(self.doubleSpinBox.value())
            print(i)
            I0, I = simTest.simluation(i * 10000)

            self.ax.plot(I0, color='red')
            for i in range(self.gridLayout.count()): self.gridLayout.itemAt(i).widget().close()
            self.ax.plot(I, color='blue')
            for i in range(self.gridLayout.count()): self.gridLayout.itemAt(i).widget().close()
            #self.gridLayout.removeWidget(self.gridLayout.item)
            self.gridLayout.addWidget(FigureCanvas(self.fig))

    def auto_tread(self):
        self.bwThread = tread.BigWorkThread(int(1))
        self.bwThread.finishSignal.connect(self.show_figure())
        self.bwThread.start()

    def start_simulation_Auto(self):

        if self.k == 0.0 or self.radian == 0.0:
            QMessageBox.information(self, "warning", "Please set the value of Radian or K")
        else:
            simTest = sim(k=self.k, radian=self.radian, wavelength=632.8)

            startPoint = self.workDistance * 10000
            self.I0, self.I = simTest.simluation(startPoint)
            if self.workDistance > 10:
                self.workDistance = 0
            else:
                self.workDistance += 1
                time.sleep(1)
                self.auto.emit(1)

    def show_figure(self):
        print('run this')
        self.fig = Figure(figsize=(600, 600), dpi=100, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        #for j in range(self.gridLayout.count()): self.gridLayout.itemAt(j).widget().close()
        for i in range(self.gridLayout.count()): self.gridLayout.removeItem(self.gridLayout.itemAt(i))
        self.ax.plot(self.I0, color='red')
        self.ax.plot(self.I, color='blue')

        self.gridLayout.addWidget(self.canvas)
        #if self.workDistance <= 10:
        #self.auto1.connect(self.auto_tread())


def init_plot():
    fig = Figure(figsize=(600, 600), dpi=100, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    # generate the canvas to display the plot
    return canvas

if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = MainWindow()
    form.gridLayout.addWidget(init_plot())
    form.show()
    sys.exit(app.exec_())

