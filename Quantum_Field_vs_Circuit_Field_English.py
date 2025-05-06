import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.font_manager as fm
from scipy.fft import fft, fftfreq
import logging
import os
import shutil

# Suppress font-related warnings
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

# Try importing imageio, with fallback
try:
    import imageio
except ModuleNotFoundError:
    print("Error: 'imageio' module not found. Please install it with 'pip install imageio'.")
    print("Animation (euler_animation.gif) will be skipped.")
    imageio = None

# Clear Matplotlib font cache
def clear_matplotlib_cache():
    cache_dir = os.path.expanduser('~/.cache/matplotlib')
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print("Cleared Matplotlib font cache.")
    else:
        print("Matplotlib font cache not found.")

# Set font for English text with subscript support
def set_english_font():
    font_candidates = ['Liberation Serif', 'DejaVu Sans', 'Times New Roman', 'serif']
    available_fonts = [f.name for f in fm.FontManager().ttflist]
    selected_font = None
    for font in font_candidates:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['font.family'] = 'serif'
            selected_font = font
            break
    if selected_font:
        print(f"Using font: {selected_font}")
    else:
        print(f"Warning: No preferred font found in {font_candidates}. Using default font.")
    plt.rcParams['axes.unicode_minus'] = False  # Handle minus signs correctly

# Test subscript rendering
def test_subscript_rendering():
    try:
        plt.figure(figsize=(2, 2))
        plt.text(0.5, 0.5, 'Eₙ', fontsize=12, ha='center')
        plt.axis('off')
        plt.savefig('test_subscript.png')
        plt.close()
        print("Generated test_subscript.png to verify subscript rendering.")
    except Exception as e:
        print(f"Subscript rendering test failed: {e}")

# Clear cache and set font
clear_matplotlib_cache()
set_english_font()
test_subscript_rendering()

# Constants
hbar = 1.0545718e-34  # Planck's constant (J·s)

# Figure 1: Voltage and Current Waveforms (Time and Frequency Domain)
def plot_voltage_current():
    omega = 1  # rad/s
    C = 1      # F
    t = np.linspace(0, 4*np.pi, 1000)
    V_t = np.cos(omega * t)
    I_t = C * omega * np.sin(omega * t)  # I(t) = C * dV/dt

    # Time domain
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(t, V_t, 'b-', label='Voltage V(t) = cos(ωt)')
    ax1.plot(t, I_t, 'r--', label='Current I(t) = Cω sin(ωt)')
    ax1.set_xlabel('Time t (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Time Domain: Voltage and Current (Current Leads by 90°)')
    ax1.legend()
    ax1.grid(True)

    # Frequency domain
    N = len(t)
    T = t[1] - t[0]
    V_f = fft(V_t) / N
    I_f = fft(I_t) / N
    freq = fftfreq(N, T)[:N//2]
    ax2.plot(freq, 2 * np.abs(V_f[:N//2]), 'b-', label='V(t) Spectrum')
    ax2.plot(freq, 2 * np.abs(I_f[:N//2]), 'r--', label='I(t) Spectrum')
    ax2.set_xlabel('Frequency (rad/s)')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Frequency Domain: Fourier Transform Magnitude Spectrum')
    ax2.set_xlim(0, 2)
    ax2.legend()
    ax2.grid(True)

    # Inset: Circuit analogy
    ax1.text(0.05, 0.95, 'Circuit Analogy: Voltage as potential, Current as flow', 
             transform=ax1.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig('voltage_current.png')
    plt.close()

# Figure 2: Square Wave Fourier Decomposition
def plot_square_wave_fft():
    T = 4  # Period (s)
    t = np.linspace(0, T, 1000, endpoint=False)
    s_t = np.sign(np.sin(2 * np.pi * t / T))  # Square wave

    # Time domain
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(t, s_t, 'b-')
    ax1.set_xlabel('Time t (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Time Domain: Square Wave s(t)')
    ax1.grid(True)

    # Frequency domain
    N = len(t)
    dt = t[1] - t[0]
    s_f = fft(s_t) / N
    freq = fftfreq(N, dt)[:N//2]
    ax2.stem(freq, 2 * np.abs(s_f[:N//2]), 'b', markerfmt='bo', basefmt='r-')
    ax2.set_xlabel('Frequency f (Hz)')
    ax2.set_ylabel('Amplitude')
    ax2.set_title('Frequency Domain: Fourier Transform (Odd Harmonics)')
    ax2.set_xlim(0, 2)
    ax2.grid(True)
    ax2.text(0.05, 0.95, 'Related to Quantum Energy Levels (Figure 6)', 
             transform=ax2.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig('square_wave_fft.png')
    plt.close()

# Figure 3: Euler’s Formula Animation
def plot_euler_animation():
    if imageio is None:
        print("Skipping euler_animation.gif due to missing imageio.")
        return

    omega = 1
    t = np.linspace(0, 2*np.pi, 100)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel('Real Part')
    ax.set_ylabel('Imaginary Part')
    ax.set_title('Euler’s Formula: Vector Rotation')
    ax.grid(True)
    ax.set_aspect('equal')

    # Unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--')

    # Vectors
    voltage, = ax.plot([], [], 'b-', label='Voltage Vector')
    current, = ax.plot([], [], 'r--', label='Current Vector')
    quantum, = ax.plot([], [], 'c-', label='Quantum Vector (45° Phase)')
    ax.legend()

    # Inset text
    ax.text(-1.4, 1.2, 'Circuit Analogy: Phase difference between voltage and current', 
            fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    def update(frame):
        t = frame * 0.1
        # Voltage: e^(jωt)
        v_x = np.cos(omega * t)
        v_y = np.sin(omega * t)
        voltage.set_data([0, v_x], [0, v_y])
        # Current: e^(j(ωt + π/2))
        i_x = np.sin(omega * t)
        i_y = np.cos(omega * t)
        current.set_data([0, i_x], [0, i_y])
        # Quantum: 0.5 * e^(j(ωt + π/4))
        q_x = 0.5 * np.cos(omega * t + np.pi/4)
        q_y = 0.5 * np.sin(omega * t + np.pi/4)
        quantum.set_data([0, q_x], [0, q_y])
        return voltage, current, quantum

    try:
        anim = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)  # 20 fps
        anim.save('euler_animation.gif', writer='imagemagick')
        print("Generated euler_animation.gif")
    except Exception as e:
        print(f"Failed to generate euler_animation.gif: {e}")
        print("Ensure ImageMagick is installed and added to PATH.")
        print("Alternatively, install imageio-ffmpeg and modify the script to save as MP4.")
    plt.close()

# Figure 4: LC Resonance vs. Quantum Field Modes
def plot_lc_resonance():
    L = 1  # H
    C = 1  # F
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))  # ≈ 0.159 Hz
    f = np.linspace(1e-3, 0.5, 1000)  # Start from 1e-3 to avoid division by zero
    Z_L = 2j * np.pi * f * L
    Z_C = 1 / (2j * np.pi * f * C)
    Z_total = Z_L + Z_C
    I = 1 / np.abs(Z_total)  # Current amplitude for V=1

    # Quantum modes
    n = np.arange(0, 5)
    E_n = n * hbar * 2 * np.pi * f0  # Simplified E_n = n ħ ω

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(f, I, 'b-')
    ax1.set_xlabel('Frequency f (Hz)')
    ax1.set_ylabel('Current Amplitude')
    ax1.set_title(f'LC Resonance (f₀ ≈ {f0:.3f} Hz)')
    ax1.grid(True)

    ax2.stem(n, E_n, 'b', markerfmt='bo', basefmt='r-')
    ax2.set_xlabel('Mode n')
    ax2.set_ylabel('Energy Eₙ (J)')
    ax2.set_title('Quantum Field Mode Energy (Eₙ = n ħ ω)')
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('lc_resonance.png')
    plt.close()

# Figure 5: Quantum Field vs. Circuit Field Table
def plot_quantum_circuit_table():
    data = [
        ['Quantity', 'Circuit Field', 'Quantum Field'],
        ['Voltage', 'V(t) = V₀·cos(ωt)', 'ψ ∼ e⁽⁻ʲᴱᵗ⁾'],
        ['Current', 'I(t) = C·(dV/dt)', 'Photon Flux ∝ â†â'],
        ['Energy', 'E = (1/2)CV² + (1/2)LI²', 'Eₙ = ℏω(n + 1/2)'],
        ['Resonant Frequency', 'f₀ = 1 / (2π√(LC))', 'Mode Frequency ω']
    ]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    table = ax.table(cellText=data, cellLoc='center', loc='center', colWidths=[0.2, 0.4, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.title('Quantum Field vs. Circuit Field Comparison Table')
    plt.savefig('quantum_circuit_table.png')
    plt.close()

# Figure 6: Superconducting Qubit Energy Levels
def plot_superconducting_qubit():
    omega = 2 * np.pi * 5e9  # 5 GHz
    n = np.arange(0, 4)
    E_n = hbar * omega * (n + 0.5)  # E_n = ħ ω (n + 1/2)

    fig, ax = plt.subplots(figsize=(6, 4))
    for i, e in enumerate(E_n):
        ax.axhline(e, xmin=0.2, xmax=0.8, color='b')
        ax.text(0.85, e, f'| {i}⟩', verticalalignment='center')
    ax.set_xlabel('State')
    ax.set_ylabel('Energy Eₙ (J)')
    ax.set_title('Superconducting Qubit Energy Levels')
    ax.text(0.05, 0.05, 'Illustration: LC + Josephson Junction Circuit', 
            transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    ax.grid(True)
    plt.savefig('superconducting_qubit.png')
    plt.close()

# Generate all plots
try:
    plot_voltage_current()
    print("Generated voltage_current.png")
    plot_square_wave_fft()
    print("Generated square_wave_fft.png")
    plot_euler_animation()  # May skip if imageio is missing
    plot_lc_resonance()
    print("Generated lc_resonance.png")
    plot_quantum_circuit_table()
    print("Generated quantum_circuit_table.png")
    plot_superconducting_qubit()
    print("Generated superconducting_qubit.png")
except Exception as e:
    print(f"An error occurred: {e}")

print("Script execution completed.")
