from PyQt4.QtGui import QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


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
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Amplitude')
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
            self.axes.set_xlabel('Time')
            self.axes.set_ylabel('Amplitude')

        else:

            self.pl1 = self.fig.add_subplot(211)
            self.pl2 = self.fig.add_subplot(212)
            self.pl1.hold(False)
            self.pl2.hold(False)

            freq, im = fft_plot.im_plot_data()
            freq2, re = fft_plot.re_plot_data()
            self.pl1.plot(freq2, re, 'b')
            self.pl2.plot(freq, im, 'r')
            self.pl1.set_xlabel('Frequency (Hz)')
            self.pl1.set_ylabel('Amplitude')
            self.pl2.set_xlabel('Frequency (Hz)')
            self.pl2.set_ylabel('Amplitude')
            self.pl1.set_title('Real part')
            self.pl2.set_title('Imaginary part')
            self.axes.get_xaxis().set_visible(False)
            self.axes.get_yaxis().set_visible(False)
        self.draw()