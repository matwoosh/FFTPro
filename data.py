import random

import matplotlib
import numpy as np


class FFTPlots:
    def __init__(self):
        font = {'family': 'sans-serif',
                'size': 12}
        matplotlib.rc('font', **font)

        Fs = 150.0  # sampling rate
        Ts = 1.0 / Fs # sampling interval
        self.t = np.arange(0, 1, Ts)  # time vector

        ff = 5  # frequency of the signal
        self.functions = [
            np.sin(2 * np.pi * ff * self.t),
            np.cos(2 * np.pi * ff * self.t),
            0.7*np.sin(2 * np.pi * ff * self.t) + 0.2*np.sin(2* 5 * np.pi * ff * self.t) + 0.4*np.sin(2*10 * np.pi * ff * self.t),
            0.7*np.cos(2 * np.pi * ff * self.t) + 0.2*np.cos(2* 5 * np.pi * ff * self.t) + 0.4*np.cos(2*10 * np.pi * ff * self.t),
        ]
        self.signal = self.functions[0]
        y = self.signal.copy()

        n = len(y)  # length of the signal
        k = np.arange(n)
        T = n / Fs
        frq = k / T # two sides frequency range
        frq = frq[list(range(n//2))]  # one side frequency range

        fft_res = np.fft.fft(y)  # fft computing
        Y = fft_res / n # normalization
        Y = Y[list(range(n//2))]

        self.y = y
        self.Y = Y
        self.freq = frq
        self.inverse_y = np.fft.ifft(fft_res)

    def set_signal_function(self, number):
        if number > len(self.functions) - 1:
            return
        self.signal = self.functions[number]

    def time_plot_data(self):
        return self.t, self.y

    def re_plot_data(self):
        return self.freq, self.Y.real

    def im_plot_data(self):
        return self.freq, self.Y.imag

    def inverse_time_plot_data(self):
        return self.t, self.inverse_y.real

    def recalculate(self, noise, noise_filter):
        random_noise = [random.uniform(0, noise) for i in range(0, self.signal.size)]
        y = self.signal.copy()
        y += np.array(random_noise)

        n = len(y)  # length of the signal
        fft_res = np.fft.fft(y)  # fft computing
        Y = fft_res / n  # normalization
        Y = Y[list(range(n//2))]

        self.y = y
        self.Y = Y
        if noise_filter:
            mean_value = np.mean(abs(fft_res))
            value = 1.1 * mean_value
            fft_res = [0 if (abs(res) < value) else res for res in fft_res]
        self.inverse_y = np.fft.ifft(fft_res)
