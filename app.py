import sys
from pygsl import deriv

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot, Qt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

from data import functions, DerivativeType
from plot import Plot


class Window(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.argument = 1
        self.deriv_type = DerivativeType.central
        self.lbl1 = QtGui.QLabel("Function")
        self.lbl2 = QtGui.QLabel("\nDifferentiation function type:")
        self.lbl3 = QtGui.QLabel("\nFunction argument:")
        self.lbl4 = QtGui.QLabel("\nFunction value:")
        self.lbl5 = QtGui.QLabel("\nDerivative value:")
        self.lbl6 = QtGui.QLabel("\nError:")
        self.radio_widget = QtGui.QWidget(self)
        self.error = QtGui.QLabel("-")
        self.value = QtGui.QLabel("-")
        self.derivative = QtGui.QLabel("-")
        self.edit = QtGui.QLineEdit()
        self.figure = plt.figure()  # a figure instance to plot on
        self.canvas = FigureCanvas(self.figure)
        self.combo = QtGui.QComboBox()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.init_ui()

    def init_ui(self):
        self.init_combo()
        self.init_radio()
        self.edit.textChanged[str].connect(self.change_argument)

        layout = QtGui.QVBoxLayout(self)
        # left = QtGui.QFrame()
        # left.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(Qt.Vertical)
        splitter1.addWidget(self.lbl1)
        splitter1.addWidget(self.combo)
        splitter1.addWidget(self.lbl2)
        splitter1.addWidget(self.r0)
        splitter1.addWidget(self.r1)
        splitter1.addWidget(self.r2)
        splitter1.addWidget(self.lbl3)
        splitter1.addWidget(self.edit)
        splitter1.addWidget(self.lbl4)
        splitter1.addWidget(self.value)
        splitter1.addWidget(self.lbl5)
        splitter1.addWidget(self.derivative)
        splitter1.addWidget(self.lbl6)
        splitter1.addWidget(self.error)
        # splitter1.addWidget(left)

        splitter0 = QtGui.QSplitter(Qt.Horizontal)
        splitter0.addWidget(splitter1)

        splitter2 = QtGui.QSplitter(Qt.Vertical)
        splitter2.addWidget(self.toolbar)
        splitter2.addWidget(self.canvas)

        splitter0.addWidget(splitter2)

        layout.addWidget(splitter0)

        self.setLayout(layout)
        self.plot(0)

    def plot(self, index):
        data = functions[index]
        p = Plot(data[1], data[2], self.deriv_type)
        p.plot_function(self.canvas)
        p.plot_derivative(self.canvas)

    def init_combo(self):
        for x in functions:
            self.combo.addItem(x[0])
        self.combo.currentIndexChanged.connect(self.plot)

    def init_radio(self):
        radio_group = QtGui.QButtonGroup(self.radio_widget)
        self.r0 = QtGui.QRadioButton("central")
        self.r1 = QtGui.QRadioButton("backward")
        self.r2 = QtGui.QRadioButton("forward")

        radio_group.addButton(self.r0)
        radio_group.addButton(self.r1)
        radio_group.addButton(self.r2)

        self.r0.toggled.connect(self.choose_diff_type)
        self.r1.toggled.connect(self.choose_diff_type)
        self.r2.toggled.connect(self.choose_diff_type)

    def change_argument(self, text):
        try:
            self.argument = float(text)
            function_data = functions[self.combo.currentIndex()]
            value = function_data[1](self.argument, 0)
            derivative_result = deriv.central(function_data[1], self.argument, 1)
            self.value.setText(str(value))
            self.derivative.setText(str(derivative_result[0]))
            self.error.setText(str(derivative_result[1]))
        except:
            print("Wrong input")

    def choose_diff_type(self):
        if self.r0.isChecked():
            self.deriv_type = DerivativeType.central
        elif self.r1.isChecked():
            self.deriv_type = DerivativeType.backward
        elif self.r2.isChecked():
            self.deriv_type = DerivativeType.forward
        else:
            print("Fatal error occured!")
        self.plot(self.combo.currentIndex())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    w = Window()
    w.show()
    w.resize(1000, 600)

    # Set window title
    w.setWindowTitle("NumDiff")

    sys.exit(app.exec_())

###########################################333

# # Create an PyQT4 application object.
# from plot import Plot
#
# a = QApplication(sys.argv)
#
# # The QWidget widget is the base class of all user interface objects in PyQt4.
# w = QMainWindow()
#
#
#
# # Add a button
# btn = QPushButton('Test button', w)
# btn.setToolTip('Click to quit!')
# btn.resize(btn.sizeHint())
# btn.move(10, 40)
#
# # Create the actions
# @pyqtSlot()
# def on_click():
#     print('clicked')
#
# @pyqtSlot()
# def on_press():
#     print('pressed')
#
# @pyqtSlot()
# def on_release():
#     x1 = np.arange(0, 10, 0.1)
#     y1 = np.sin(x1)
#     p1 = Plot(y1, x1)
#     p1.plot_function()
#     print('released')
#
# # connect the signals to the slots
# btn.clicked.connect(on_click)
# btn.pressed.connect(on_press)
# btn.released.connect(on_release)
#
#
# # Create main menu
# mainMenu = w.menuBar()
# mainMenu.setNativeMenuBar(False)
# fileMenu = mainMenu.addMenu('File')
# helpMenu = mainMenu.addMenu('Help')
#
# # Add exit button
# exitButton = QAction(QIcon('exit24.png'), 'Exit', w)
# exitButton.setShortcut('Ctrl+Q')
# exitButton.setStatusTip('Exit application')
# exitButton.triggered.connect(w.close)
# fileMenu.addAction(exitButton)
#
# helpButton = QAction(QIcon('exit24.png'), 'Help', w)
# helpButton.setShortcut('Ctrl+H')
# helpButton.setStatusTip('Show help')
# helpButton.triggered.connect(w.close)
# fileMenu.addAction(exitButton)