import matplotlib.pyplot as plt
from pygsl import deriv

from data import DerivativeType


class Plot:
    def __init__(self, function, arguments, deriv_type):
        self.arguments = arguments
        self.function = function
        self.deriv_type = deriv_type

    def plot_function(self, canvas):
        plt.clf()
        canvas.draw()
        x = self.arguments
        y = []
        for number in x:
            y.append(self.function(number, 0))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot(x, y)
        canvas.draw()

    def plot_derivative(self, canvas):
        x = self.arguments
        y = []
        if self.deriv_type == DerivativeType.central:
            for number in x:
                y.append(deriv.central(self.function, number, 1)[0])
        elif self.deriv_type == DerivativeType.backward:
            for number in x:
                y.append(deriv.backward(self.function, number, 1)[0])
        elif self.deriv_type == DerivativeType.forward:
            for number in x:
                y.append(deriv.forward(self.function, number, 1)[0])
        else:
            print("Fatal error occured!")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.plot(x, y)
        canvas.draw()



