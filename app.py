import sys

from PyQt4.QtGui import *
from PyQt4.uic.properties import QtCore
from matplotlib.figure import Figure
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from data import FFTPlots

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.type = 0
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class TimeCanvas(MyMplCanvas):
    def compute_initial_figure(self, fft_plot):
        t, y = fft_plot.time_plot_data()
        self.axes.plot(t, y)  # time domain
        self.axes.set_xlabel('Czas')
        self.axes.set_ylabel('Amplituda')
        self.draw()


class FreqCanvas(MyMplCanvas):

    def compute_initial_figure(self, fft_plot, plot_type):
        if plot_type == 2:      #ifft
            if plot_type != self.type:
                self.fig.delaxes(self.pl1)
                self.fig.delaxes(self.pl2)
                self.axes.get_xaxis().set_visible(True)
                self.axes.get_yaxis().set_visible(True)
                self.type = 2
            t, y = fft_plot.inverse_time_plot_data()
            self.axes.plot(t, y, 'r')
            self.axes.set_xlabel('Czas')
            self.axes.set_ylabel('Amplituda')

        else:

            self.pl1 = self.fig.add_subplot(211)
            self.pl2 = self.fig.add_subplot(212)
            self.pl1.hold(False)
            self.pl2.hold(False)

            freq, im = fft_plot.im_plot_data()
            freq2, re = fft_plot.re_plot_data()
            self.pl1.plot(freq2, re, 'b')
            self.pl2.plot(freq, im, 'r')
            self.pl1.set_xlabel(u'Częstotliwość (Hz)')
            self.pl1.set_ylabel('Amplituda')
            self.pl2.set_xlabel(u'Częstotliwość (Hz)')
            self.pl2.set_ylabel('Amplituda')
            self.pl1.set_title(u'Część rzeczywista')
            self.pl2.set_title(u'Część urojona')
            self.axes.get_xaxis().set_visible(False)
            self.axes.get_yaxis().set_visible(False)
        self.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("FFT")

        font = QFont('Sans-serif', 10, QFont.Light)
        self.setFont(font)

        self.fft_plots = FFTPlots()

        self.main_widget = QWidget(self)

        horizontal_layout = QHBoxLayout(self.main_widget)

        box_layout_plots = QVBoxLayout()

        self.time_domain = TimeCanvas(width=5, height=4, dpi=80)
        self.freq_domain = FreqCanvas(width=5, height=4, dpi=60)

        tabs = QTabWidget()
        tabs.addTab(self.time_domain, "1")
        tabs.addTab(self.freq_domain, "2")

        box_layout_plots.addWidget(tabs)

        box_layout_menu = QVBoxLayout()

        # functions
        box_layout_menu.addWidget(QLabel("Funkcje sygnałów"))
        self.function_button_group = QButtonGroup()
        self.function_buttons = [QRadioButton("&Funkcja " + str(i)) for i in range(1, 5)]
        for function_button in self.function_buttons:
            self.function_button_group.addButton(function_button)
            box_layout_menu.addWidget(function_button)
        self.function_buttons[0].click()  # set one trigger active

        # plot options
        box_layout_menu.addWidget(QLabel("Opcje wykresu"))
        self.plot_options_button_group = QButtonGroup()
        self.re_button = QRadioButton("FFT")
        self.ifft_button = QRadioButton("IFFT")
        self.plot_options_button_group.addButton(self.re_button)
        self.plot_options_button_group.addButton(self.ifft_button)
        box_layout_menu.addWidget(self.re_button)
        box_layout_menu.addWidget(self.ifft_button)
        self.re_button.click()  # set one trigger active

        # noise slider
        box_layout_menu.addWidget(QLabel("Noise"))
        self.noise_slider = QSlider()
        self.noise_slider.setMinimum(0)
        self.noise_slider.setMaximum(10)
        box_layout_menu.addWidget(self.noise_slider)

        # noise filter checkbox
        self.noise_filter = QCheckBox("Filter")
        box_layout_menu.addWidget(self.noise_filter)

        # draw button
        self.draw_button = QPushButton("Update")
        self.draw_button.clicked.connect(self.draw_plots)
        box_layout_menu.addWidget(self.draw_button)

        horizontal_layout.addLayout(box_layout_plots)
        horizontal_layout.addLayout(box_layout_menu)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.draw_plots()

    def closeEvent(self, ce):
        self.fileQuit()

    def draw_plots(self):
        function_index = self.function_button_group.checkedId() * (-1) - 2  # weird id...
        self.fft_plots.set_signal_function(function_index)
        self.fft_plots.recalculate(self.noise_slider.sliderPosition(), self.noise_filter.isChecked())
        self.time_domain.compute_initial_figure(self.fft_plots)
        plot_type = 0  # re_checked
        if self.ifft_button.isChecked():
            plot_type = 2
        self.freq_domain.compute_initial_figure(self.fft_plots, plot_type)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = ApplicationWindow()
    w.resize(1000, 600)
    w.setWindowTitle("FFTPro")
    w.show()
    app.exec_()

# class Window(QtGui.QDialog):
#
#     def __init__(self, parent=None):
#         super(Window, self).__init__(parent)
#         self.argument = 1
#         self.deriv_type = DerivativeType.central
#         self.lbl1 = QtGui.QLabel("Function")
#         self.lbl2 = QtGui.QLabel("\nDifferentiation function type:")
#         self.lbl3 = QtGui.QLabel("\nFunction argument:")
#         self.lbl4 = QtGui.QLabel("\nFunction value:")
#         self.lbl5 = QtGui.QLabel("\nDerivative value:")
#         self.lbl6 = QtGui.QLabel("\nError:")
#         self.radio_widget = QtGui.QWidget(self)
#         self.error = QtGui.QLabel("-")
#         self.value = QtGui.QLabel("-")
#         self.derivative = QtGui.QLabel("-")
#         self.edit = QtGui.QLineEdit()
#         self.figure = plt.figure()  # a figure instance to plot on
#         self.canvas = FigureCanvas(self.figure)
#         self.combo = QtGui.QComboBox()
#         self.toolbar = NavigationToolbar(self.canvas, self)
#         self.init_ui()
#
#     def init_ui(self):
#         self.init_combo()
#         self.init_radio()
#         self.edit.textChanged[str].connect(self.change_argument)
#
#         layout = QtGui.QVBoxLayout(self)
#         # left = QtGui.QFrame()
#         # left.setFrameShape(QtGui.QFrame.StyledPanel)
#
#         splitter1 = QtGui.QSplitter(Qt.Vertical)
#         splitter1.addWidget(self.lbl1)
#         splitter1.addWidget(self.combo)
#         splitter1.addWidget(self.lbl2)
#         splitter1.addWidget(self.r0)
#         splitter1.addWidget(self.r1)
#         splitter1.addWidget(self.r2)
#         splitter1.addWidget(self.lbl3)
#         splitter1.addWidget(self.edit)
#         splitter1.addWidget(self.lbl4)
#         splitter1.addWidget(self.value)
#         splitter1.addWidget(self.lbl5)
#         splitter1.addWidget(self.derivative)
#         splitter1.addWidget(self.lbl6)
#         splitter1.addWidget(self.error)
#         # splitter1.addWidget(left)
#
#         splitter0 = QtGui.QSplitter(Qt.Horizontal)
#         splitter0.addWidget(splitter1)
#
#         splitter2 = QtGui.QSplitter(Qt.Vertical)
#         splitter2.addWidget(self.toolbar)
#         splitter2.addWidget(self.canvas)
#
#         splitter0.addWidget(splitter2)
#
#         layout.addWidget(splitter0)
#
#         self.setLayout(layout)
#         self.plot(0)
#
#     def plot(self, index):
#         data = functions[index]
#         p = Plot(data[1], data[2], self.deriv_type)
#         p.plot_function(self.canvas)
#         p.plot_derivative(self.canvas)
#
#     def init_combo(self):
#         for x in functions:
#             self.combo.addItem(x[0])
#         self.combo.currentIndexChanged.connect(self.plot)
#
#     def init_radio(self):
#         radio_group = QtGui.QButtonGroup(self.radio_widget)
#         self.r0 = QtGui.QRadioButton("central")
#         self.r1 = QtGui.QRadioButton("backward")
#         self.r2 = QtGui.QRadioButton("forward")
#
#         radio_group.addButton(self.r0)
#         radio_group.addButton(self.r1)
#         radio_group.addButton(self.r2)
#
#         self.r0.toggled.connect(self.choose_diff_type)
#         self.r1.toggled.connect(self.choose_diff_type)
#         self.r2.toggled.connect(self.choose_diff_type)
#
#     def change_argument(self, text):
#         try:
#             self.argument = float(text)
#             function_data = functions[self.combo.currentIndex()]
#             value = function_data[1](self.argument, 0)
#             derivative_result = deriv.central(function_data[1], self.argument, 1)
#             self.value.setText(str(value))
#             self.derivative.setText(str(derivative_result[0]))
#             self.error.setText(str(derivative_result[1]))
#         except:
#             print("Wrong input")
#
#     def choose_diff_type(self):
#         if self.r0.isChecked():
#             self.deriv_type = DerivativeType.central
#         elif self.r1.isChecked():
#             self.deriv_type = DerivativeType.backward
#         elif self.r2.isChecked():
#             self.deriv_type = DerivativeType.forward
#         else:
#             print("Fatal error occured!")
#         self.plot(self.combo.currentIndex())
#
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#
#     w = Window()
#     w.show()
#
#w.resize(1000, 600)
#     # Set window title
#     w.setWindowTitle("FFTPro")
#
#     sys.exit(app.exec_())