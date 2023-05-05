import numpy as np

from typing import Tuple, List, Callable

class FourierPlotter:
    def __init__(self, start=0, stop=0, resolution=1000):
        self.resolution = resolution
        self.progess = 0
        self._space = np.linspace(start, stop, resolution)
        self._signal = np.zeros(resolution)
        self._frequencies = []
        self.amplitude = 0
        self.wrapped_signal = []
        self.wrapping_frequency = 0
        self.average_point_signal = []

    def __get_signal_from_frequency(self, frequency: float, amplitude: float, dc=1, func=np.cos):
        signal = dc + (amplitude * func(2 * np.pi * frequency * self._space))

        return signal

    def set_frequencies(self, frequencies: List[Tuple[float, float, float, Callable]]):
        self._signal = np.zeros(self.resolution)
        self._frequencies.clear()

        for frequency, amplitude, dc, func in frequencies:
            self._frequencies.append((frequency, amplitude, dc, func))
            self._signal += self.__get_signal_from_frequency(frequency, amplitude, dc, func)

    def set_progress(self, progress):
        self.progress = self._space[0] + ((progress / 1000) * (self._space[-1] - self._space[0]))

    def add_frequency(self, frequency: float, amplitude: float, dc=0, func=np.sin):
        self._frequencies.append((frequency, amplitude, dc, func))

        self._signal += __get_signal_from_frequency(frequency, amplitude, dc, func)

    def delete_frequency(self, frequency: float, amplitude: float, dc=0, func=np.sin):
        self._frequencies.remove((frequency, amplitude, dc, func))

        self._signal -= __get_signal_from_frequency(frequency, amplitude, dc, func)

    def calculate_amplitude(self):
        sum = 0

        for _, amplitude, dc, _ in self._frequencies:
            sum += amplitude + dc

        self.amplitude = sum

        return sum

    def signal(self) -> Tuple[np.array, np.array]:
        return (self._space, self._signal)

    def rotate_point(self, point: Tuple[float, float], wrapping_frequency: float):
        x, y = point

        return y * np.e ** (2 * (-1j) * np.pi * wrapping_frequency * x)


    def wrap_signal_around_point(self, wrapping_frequency: float):
        rotate = lambda x, y: y * np.e ** (2 * (-1j) * np.pi * wrapping_frequency * x)

        complex_values = np.array([rotate(x, y) for x, y in zip(self._space, self._signal)])

        real_values = np.array([c.real for c in complex_values])
        imaginary_values = np.array([c.imag for c in complex_values])

        self.wrapped_signal = [real_values, imaginary_values]
        self.wrapping_frequency = wrapping_frequency

        return (real_values, imaginary_values)

    def calculate_average_point(self) -> Tuple[float, float]:
        x, y = np.mean(self.wrapped_signal[0]), np.mean(self.wrapped_signal[1])
        
        if len(self.average_point_signal) <= (self.wrapping_frequency * 100):
            self.average_point_signal.append(complex(x, y))

        return x, y
