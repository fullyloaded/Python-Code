import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for headless environments
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy import signal
from matplotlib.patches import FancyArrowPatch
from PIL import Image
import os
import glob
import warnings

# Set font for Chinese and mathematical symbols
try:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'DejaVu Sans']
    plt.rcParams['mathtext.fontset'] = 'stix'  # Use STIX for rendering math symbols
    plt.rcParams['axes.unicode_minus'] = False  # Ensure negative signs display correctly
except Exception as e:
    print(f"Warning: Unable to load font, Chinese or mathematical symbols may not display correctly. Error: {e}")
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['mathtext.fontset'] = 'dejavusans'

# General parameters
time = np.linspace(0, 4 * np.pi, 1000)  # Time array for Figures 1 and 3
square_wave_time = np.linspace(0, 4, 1000)  # Time array for Figure 2
ω = 1  # Angular frequency (rad/s, U+03C9)
capacitance = 1  # Capacitance (F)
inductance = 1  # Inductance (H)
ℏ = 1.0545718e-34  # Reduced Planck constant (J·s, U+210F)

# Figure 1: Capacitor V(t), I(t) in time domain vs frequency domain
def plot_voltage_current():
    voltage = np.cos(ω * time)
    current = capacitance * ω * np.sin(ω * time)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    # Time domain
    ax1.plot(time, voltage, 'b-', label=r'Voltage $V(t) = \cos(\omega t)$')
    ax1.plot(time, current, 'r--', label=r'Current $I(t) = C \omega \sin(\omega t)$')
    ax1.axvline(np.pi/4, color='k', linestyle=':', label=r'$t = \pi/4$')
    ax1.annotate('Current maximum, voltage rising', xy=(np.pi/4, 1), xytext=(np.pi/2, 1.3),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Capacitor Time Domain Waveform', pad=20)  # Increased padding for title
    ax1.grid(True)
    ax1.legend()
    
    # Inset: Reservoir analogy
    inset_ax = ax1.inset_axes([0.6, 0.1, 0.3, 0.3])
    inset_time = np.linspace(0, 2 * np.pi, 100)
    inset_ax.plot(inset_time, np.cos(inset_time), 'b-', label='Water level')
    inset_ax.arrow(np.pi/4, 0, 0, 1, head_width=0.1, head_length=0.2, fc='r', ec='r', label='Flow')
    inset_ax.set_title('Reservoir Analogy', fontsize=8)
    inset_ax.set_xticks([]); inset_ax.set_yticks([])
    inset_ax.text(0.1, 1.0, r'Flow leads by $\pi/2$', fontsize=8)
    
    # Frequency domain
    voltage_fft = np.abs(np.fft.fft(voltage))[0:len(voltage)//2]
    current_fft = np.abs(np.fft.fft(current))[0:len(current)//2]
    frequency = np.fft.fftfreq(len(time), time[1] - time[0])[0:len(time)//2]
    ax2.plot(frequency, voltage_fft, 'b-', label='Voltage Spectrum')
    ax2.plot(frequency, current_fft, 'r--', label='Current Spectrum')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Frequency Domain Spectrum')
    ax2.set_xlim(0, 0.5)
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('voltage_current.png', dpi=300)
    plt.close()

# Figure 2: Fourier decomposition of water level wave and frequency components
def plot_square_wave_fft():
    square_wave = signal.square(2 * np.pi * square_wave_time)
    fft = np.fft.fft(square_wave)
    frequency = np.fft.fftfreq(len(square_wave_time), square_wave_time[1] - square_wave_time[0])
    positive_freq = frequency > 0
    frequency = frequency[positive_freq]
    fft_magnitude = np.abs(fft)[positive_freq]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    ax1.plot(square_wave_time, square_wave, 'b-', label='Square Wave (Water Level)')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Time Domain Square Wave')
    ax1.grid(True)
    ax1.legend()
    
    ax2.stem(frequency, fft_magnitude, 'b', label='Frequency Components')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Frequency Domain Spectrum (Odd Harmonics)')
    ax2.grid(True)
    ax2.legend()
    ax2.text(0.5, max(fft_magnitude) * 0.9, 'Related to quantum energy levels (Figure 6)', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('square_wave_fft.png', dpi=300)
    plt.close()

# Figure 3: Euler's formula and phase rotation animation
def plot_unit_circle_animation():
    fig, ax = plt.subplots(figsize=(8, 8))
    θ = np.linspace(0, 2 * np.pi, 100)
    ax.plot(np.cos(θ), np.sin(θ), 'k-', label='Unit Circle')
    ax.axhline(0, color='k', alpha=0.3); ax.axvline(0, color='k', alpha=0.3)
    
    # Initial vectors
    initial_time = np.pi / 4
    voltage_vector, = ax.plot([0, np.cos(ω * initial_time)], [0, np.sin(ω * initial_time)], 'b-', lw=2, label=r'Voltage $\cos(\omega t)$')
    current_vector, = ax.plot([0, np.sin(ω * initial_time)], [0, np.cos(ω * initial_time)], 'r--', lw=2, label=r'Current $\sin(\omega t)$')
    quantum_vector, = ax.plot([0, 0.5 * np.cos(ω * initial_time + np.pi/4)], [0, 0.5 * np.sin(ω * initial_time + np.pi/4)],
                             'c-', lw=2, label=r'Quantum ($45^\circ$ initial)')
    
    # Inset: Reservoir analogy
    inset_ax = ax.inset_axes([0.1, 0.1, 0.3, 0.3])
    inset_time = np.linspace(0, 2 * np.pi, 100)
    inset_ax.plot(inset_time, np.cos(inset_time), 'b-', label='Water level')
    inset_ax.arrow(np.pi/4, 0, 0, 1, head_width=0.1, head_length=0.2, fc='r', ec='r', label='Flow')
    inset_ax.set_title('Reservoir Analogy', fontsize=8)
    inset_ax.set_xticks([]); inset_ax.set_yticks([])
    inset_ax.text(0.1, 1.0, r'Flow leads by $\pi/2$', fontsize=8)
    
    ax.set_xlabel('Real Part')
    ax.set_ylabel('Imaginary Part')
    ax.set_title(r'Euler\'s Formula: $e^{j\theta} = \cos(\theta) + j \sin(\theta)$')
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.grid(True)
    ax.legend()
    ax.text(0.1, 1.3, 'Current leads voltage by 90°.\nQuantum phase starts at 45° and evolves.', fontsize=10)
    
    def update(frame):
        time_value = frame
        voltage_vector.set_data([0, np.cos(ω * time_value)], [0, np.sin(ω * time_value)])
        current_vector.set_data([0, np.sin(ω * time_value)], [0, np.cos(ω * time_value)])
        quantum_vector.set_data([0, 0.5 * np.cos(ω * time_value + np.pi/4)],
                               [0, 0.5 * np.sin(ω * time_value + np.pi/4)])
        return voltage_vector, current_vector, quantum_vector
    
    final_gif = 'euler_animation.gif'
    temp_frame_dir = 'temp_frames'
    os.makedirs(temp_frame_dir, exist_ok=True)
    
    try:
        frame_list = np.arange(0, 2 * np.pi, 0.1)
        print(f"Generating {len(frame_list)} frames for animation")
        for i, frame in enumerate(frame_list):
            update(frame)
            fig.canvas.draw()
            plt.savefig(os.path.join(temp_frame_dir, f'frame_{i:04d}.png'), dpi=300)
        
        frame_files = sorted(glob.glob(os.path.join(temp_frame_dir, 'frame_*.png')))
        print(f"Combining {len(frame_files)} frames into GIF")
        image_list = [Image.open(frame_path) for frame_path in frame_files]
        image_list[0].save(
            final_gif,
            save_all=True,
            append_images=image_list[1:],
            duration=50,  # 50 ms per frame (20 fps)
            loop=0  # Infinite loop
        )
        
        for frame_path in frame_files:
            os.remove(frame_path)
        os.rmdir(temp_frame_dir)
        
    except Exception as e:
        print(f"Error occurred during animation generation: {e}")
    finally:
        plt.close()

# Figure 4: LC resonance vs field mode energy distribution
def plot_lc_resonance():
    frequency = np.linspace(0.01, 0.5, 1000)  # Frequency (Hz)
    resonance_frequency = 1 / (2 * np.pi * np.sqrt(inductance * capacitance))  # f_0 = 1/(2π√LC)
    impedance = np.abs(1j * 2 * np.pi * frequency * inductance + 1 / (1j * 2 * np.pi * frequency * capacitance))
    current_magnitude = 1 / impedance  # Assuming input voltage = 1V
    
    # Quantum field modes
    modes = np.arange(0, 5)  # Modes n = 0, 1, 2, ...
    mode_energy = ℏ * 2 * np.pi * resonance_frequency * (modes + 0.5)  # E_n = ℏω (n + 1/2)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    # LC resonance
    ax1.plot(frequency, current_magnitude, 'b-', label=r'Current Magnitude $I = 1/|Z|$')
    ax1.axvline(resonance_frequency, color='k', linestyle=':', label=r'$f_0 = \frac{1}{2\pi \sqrt{LC}}$')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Current Magnitude (A)')
    ax1.set_title('LC Resonance')
    ax1.grid(True)
    ax1.legend()
    
    # Field modes
    ax2.stem(modes, mode_energy, 'b', label=r'Energy $E_n = \hbar \omega (n + \frac{1}{2})$')
    ax2.set_xlabel('Mode $n$')
    ax2.set_ylabel('Energy (J)')
    ax2.set_title('Quantum Field Mode Energy Distribution')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('lc_resonance.png', dpi=300)
    plt.close()

# Figure 5: Quantum field vs circuit field comparison (table format)
def plot_quantum_circuit_comparison():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Table data
    columns = ['Physical Quantity', 'Circuit Field Description', 'Quantum Field Description']
    data = [
        ['Voltage', r'$V(t) = V_0 \cos(\omega t)$', r'$\psi \sim e^{-j E t / \hbar}$ (phase evolution)'],
        ['Current', r'$I(t) = C \frac{dV}{dt}$', r'Photon flux $\propto \hat{a}^\dagger \hat{a}$'],
        ['Energy', r'$E = \frac{1}{2} C V^2 + \frac{1}{2} L I^2$', r'$E_n = \hbar \omega (n + \frac{1}{2})$'],
        ['Resonance Frequency', r'$f_0 = \frac{1}{2\pi \sqrt{LC}}$', r'Mode frequency $\omega$']
    ]
    
    table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    ax.set_title('Quantum Field vs Circuit Field Comparison Table')
    plt.tight_layout()
    plt.savefig('quantum_circuit_table.png', dpi=300)
    plt.close()

# Figure 6: Superconducting qubit and energy level structure diagram
def plot_superconducting_qubit():
    qubit_frequency = 2 * np.pi * 5e9  # 5 GHz
    modes = np.arange(0, 4)  # Energy levels n = 0, 1, 2, 3
    energy_levels = ℏ * qubit_frequency * (modes + 0.5)  # E_n = ℏω (n + 1/2)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    for n, E in enumerate(energy_levels):
        ax.axhline(E, color='b', linestyle='-', xmin=0.2, xmax=0.8)
        ax.text(0.85, E, r'$|%d\rangle$' % n, fontsize=12, verticalalignment='center')
    ax.arrow(0.5, energy_levels[0], 0, energy_levels[1] - energy_levels[0], head_width=0.02, head_length=0.1e-24, fc='r', ec='r')
    ax.text(0.55, (energy_levels[0] + energy_levels[1]) / 2, r'$\omega_{01}$', fontsize=10, color='r')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5e-24, energy_levels[-1] * 1.2)
    ax.set_xlabel('Schematic Axis')
    ax.set_ylabel('Energy (J)')
    ax.set_title('Superconducting Qubit Energy Level Structure')
    ax.grid(True, axis='y')
    
    # Inset: Simplified superconducting circuit
    inset_ax = ax.inset_axes([0.1, 0.6, 0.3, 0.3])
    inset_ax.plot([0, 1], [0, 0], 'k-', lw=2)  # Circuit line
    inset_ax.text(0.5, 0.1, 'Josephson Junction', fontsize=8)
    inset_ax.set_xlim(-0.2, 1.2)
    inset_ax.set_ylim(-0.2, 0.3)
    inset_ax.set_xticks([]); inset_ax.set_yticks([])
    inset_ax.set_title('Superconducting Circuit', fontsize=8)
    
    ax.text(0.1, energy_levels[-1] * 1.3, 'Discrete energy levels for quantum computing', fontsize=10)  # Adjusted y-coordinate
    
    plt.tight_layout()
    plt.savefig('superconducting_qubit.png', dpi=300)
    plt.close()

# Main function: Generate all figures
def main():
    plot_voltage_current()  # Figure 1
    plot_square_wave_fft()  # Figure 2
    plot_unit_circle_animation()  # Figure 3
    plot_lc_resonance()  # Figure 4
    plot_quantum_circuit_comparison()  # Figure 5
    plot_superconducting_qubit()  # Figure 6
    print("All figures generated successfully: voltage_current.png, square_wave_fft.png, euler_animation.gif, lc_resonance.png, quantum_circuit_table.png, superconducting_qubit.png")

if __name__ == "__main__":
    main()
