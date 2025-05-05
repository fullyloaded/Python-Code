import numpy as np
import matplotlib.pyplot as plt

# Set font for rendering (Microsoft YaHei for compatibility, though text is in English)
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # Ensure proper rendering of minus signs

# Planck’s constant (hbar, unit: J·s)
hbar = 1.0545718e-34  # Reduced Planck’s constant

# Frequency range (rad/s, simulating low to high frequencies)
omega = np.linspace(0, 1e15, 1000)  # Frequency range, 0 to 10^15 rad/s
energy = hbar * omega  # Energy E = hbar * omega

# Select specific frequency points (simulating photon frequencies)
omega_points = np.array([1e13, 5e13, 1e14, 5e14])  # Example frequencies
energy_points = hbar * omega_points

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(omega, energy, 'b-', label=r'$E = \hbar \omega$')  # Energy-frequency relationship
plt.scatter(omega_points, energy_points, color='red', s=100, label='Quantum Energy Levels')  # Specific frequency points

# Annotations
plt.title('Planck’s Constant: The Metronome of the Quantum World', fontsize=14)
plt.xlabel('Frequency ω (rad/s)', fontsize=12)
plt.ylabel('Energy E (J)', fontsize=12)
plt.grid(True)

# Add text annotations, positioned to avoid overlap
plt.text(1.5e14, 2.5e-20, r'Planck’s constant $\hbar$ converts frequency to energy', fontsize=9)
plt.text(2.5e14, 1.8e-20, 'Classical Circuit: ω determines wave speed\nQuantum World: E = ħω determines energy levels', fontsize=9)
plt.text(6e14, 0.6e-20, 'Quantum Reservoir:\nDiscrete energy levels\n(Quantized water levels)', fontsize=9, bbox=dict(facecolor='lightgray', alpha=0.5))

# Legend
plt.legend(fontsize=10)

# Save plot
plt.savefig('planck_constant_plot.png', dpi=300, bbox_inches='tight')

# Close plot to free memory
plt.close()
