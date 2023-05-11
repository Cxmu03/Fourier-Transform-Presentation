import numpy as np
import matplotlib.pyplot as plt

#fs is sampling frequency
fs = 100.0
ts = 0
te = 10
time = np.linspace(0,10,int((te - ts) * fs),endpoint=False)

#wave is the sum of sine wave(1Hz) and cosine wave(10 Hz)
wave = np.sin(1.25 * 2 * np.pi*time)
#wave = np.exp(2j * np.pi * time )

# Compute the Discrete Fourier Transform sample frequencies.

fft_wave = np.fft.fftshift(np.fft.fft(wave))

fft_fre = np.fft.fftfreq(n=wave.size, d=1/fs)

inv_fft = np.fft.ifft(np.fft.fftshift(fft_wave))

print(fft_fre)

plt.subplot(311)
plt.plot(np.linspace(0, 10, int((te - ts) * fs), endpoint=False), wave)
plt.title("Originales Signal")

plt.subplot(312)
plt.plot(np.linspace(-50, 50, 100 * 10, endpoint=False), np.abs(fft_wave), label="Real part")
plt.legend(loc=1)
plt.title("DFT")

plt.subplot(313)
plt.plot(np.linspace(0, 10, int((te - ts) * fs), endpoint=False), wave, color="red")
plt.plot(np.linspace(0, 10, int((te - ts) * fs), endpoint=False), np.real(inv_fft), linestyle="dashed", color="yellow")
plt.title("Rekonstruiertes Signal")

plt.show()
