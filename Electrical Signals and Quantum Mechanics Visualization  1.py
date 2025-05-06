import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Set font for rendering (Microsoft YaHei for compatibility, though text is in English)
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

# Chart 1: Voltage and Current Waveforms
t = np.linspace(0, 4*np.pi, 1000)
omega = 1  # Frequency
C = 1      # Capacitance
V_t = np.cos(omega * t)          # Voltage V(t) = cos(ωt)
I_t = C * omega * np.sin(omega * t)  # Current I(t) = Cω sin(ωt)

plt.figure(figsize=(10, 5))
plt.plot(t, V_t, 'b-', label='Voltage V(t) (Water Level)')
plt.plot(t, I_t, 'r--', label='Current I(t) (Water Flow)')
plt.title('Capacitor Voltage and Current: Current Leads by 90°')
plt.xlabel('Time t (seconds)')
plt.ylabel('Amplitude')
plt.axvline(np.pi/4, linestyle=':', color='gray', label='Wave Upslope')
plt.text(np.pi/4, 1, 'Water level rising, flow at maximum', rotation=90)
plt.legend()
plt.grid(True)
plt.show()

# Chart 2: Fourier Transform (Simplified to Square Wave Spectrum)
t = np.linspace(0, 4, 1000)
V_t = signal.square(2 * np.pi * t)  # Square wave
freq = np.fft.fftfreq(len(t), t[1] - t[0])
V_omega = np.abs(np.fft.fft(V_t))[:len(t)//2]  # Take positive frequencies
freq = freq[:len(t)//2]

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t, V_t, 'b-')
plt.title('Time Domain: Complex Water Level Fluctuation (Square Wave)')
plt.xlabel('Time t')
plt.ylabel('Voltage V(t)')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.stem(freq, V_omega, 'b', basefmt=' ')
plt.title('Frequency Domain: Decomposed into Single-Frequency Waves')
plt.xlabel('Frequency ω')
plt.ylabel('Amplitude |V(ω)|')
plt.grid(True)
plt.tight_layout()
plt.show()
