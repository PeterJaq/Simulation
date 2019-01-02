import numpy as np
import math
import matplotlib.pyplot as plt

class sim():

    def __init__(self, k, radian, wavelength):
        self.k = k
        self.radian = radian
        self.wavelength = wavelength
        self.degree = self.radian / 1000 * (180 / math.pi)
        self.thickPosition = self.cal_distance(100000)
        self.dict_I0 = [i for i in range(0, 20000)]
        self.cal_input(dict_I0=self.dict_I0)

    def cal_input(self, dict_I0):
        sig = math.sqrt(2000)
        u = 10000

        for i in dict_I0:
            dict_I0[i] = np.exp(-(i - u) ** 2 / (1000 * sig ** 2)) / (math.sqrt(2 * math.pi) * sig) * 65526

        return dict_I0

    def cal_distance(self, width):
        distance = [0 for i in range(0, 20000)]
        for i in range(width):
            #print(math.tan(self.degree) * i, self.degree)
            distance.append(math.tan(self.degree) * i)
        return distance

    def cal_indensity(self, I_0, width):
        I = []
        for i in range(len(I_0)):
            I.append(I_0[i] * math.exp(-1*self.k*width[i]))
            """
                        if I_0[i] >= 1:
                print(I_0[i], width[i])
                #print(I_0[i] * )
            if I_0[i] * math.exp(-1*self.k*width[i]) >= 1:
                print(I_0[i] * math.exp(-1*self.k*width[i]))
            """

        return I

    def simluation(self, start_point):
        return self.dict_I0, self.cal_indensity(self.dict_I0, self.thickPosition[start_point:start_point+len(self.dict_I0)])

if __name__ == '__main__':
    simTest = sim(k=3.577, radian=0.00001, wavelength=632.8)
    I0, I = simTest.simluation(20000)
    plt.plot(I, color='blue')
    plt.plot(I0, color='red')
    plt.show()