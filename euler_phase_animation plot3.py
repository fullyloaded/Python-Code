import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for animation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Set font to support rendering (Microsoft YaHei for compatibility, though text is in English)
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# Set parameters
theta_v = 0  # Voltage phase (0°)
theta_i = np.pi / 2  # Current phase (+90°)
omega = 1  # Angular frequency of quantum wave function (rad/s)
initial_phase = np.pi / 4  # Initial phase of quantum vector (45°)
t = np.linspace(0, 2 * np.pi, 100)  # Time range, one full rotation
frames = 100  # Number of animation frames

# Create unit circle
circle_t = np.linspace(0, 2 * np.pi, 100)
x_circle = np.cos(circle_t)
y_circle = np.sin(circle_t)

# Create main plot with wider figure
fig = plt.figure(figsize=(10, 8))  # Increased width from 8 to 10
ax = plt.gca()

# Draw unit circle (static)
ax.plot(x_circle, y_circle, 'k-', linewidth=1, label='Unit Circle')

# Draw voltage vector (static, blue)
ax.quiver(0, 0, np.cos(theta_v), np.sin(theta_v), color='blue', angles='xy', scale_units='xy', scale=1, label='Voltage V(ω)')

# Draw current vector (static, red)
ax.quiver(0, 0, np.cos(theta_i), np.sin(theta_i), color='red', angles='xy', scale_units='xy', scale=1, label='Current I(ω)')

# Initialize quantum wave function vector (dynamic, dark cyan, shorter)
quantum_vector = ax.quiver(0, 0, 0, 0, color='darkcyan', angles='xy', scale_units='xy', scale=1.5, label='Quantum Wave e^(j(kx-ωt))')

# Set axes
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, linestyle='--', alpha=0.7)

# Set title and labels
ax.set_title('Euler’s Formula and Phase: Classical Circuits and Quantum Waves', fontsize=12)
ax.set_xlabel('Real Part (Re)', fontsize=10)
ax.set_ylabel('Imaginary Part (Im)', fontsize=10)

# Add annotations (static, adjusted x-position to fit wider figure)
ax.text(0.65, 0.7, r'Euler’s Formula: $e^{j \theta} = \cos(\theta) + j \sin(\theta)$', fontsize=10)
ax.text(0.65, 0.6, r'Current Leads Voltage by 90°: $I(\omega) = j \omega C V(\omega)$', fontsize=10)
ax.text(0.65, 0.5, r'Quantum Phase: $e^{j (kx - \omega t)}$ Rotates with Time', fontsize=10)

# Add reservoir illustration (inset plot)
ax_inset = fig.add_axes([0.15, 0.15, 0.2, 0.2])  # Position and size [left, bottom, width, height]
t_wave = np.linspace(0, 2 * np.pi, 100)
water_level = np.sin(t_wave)  # Water level (voltage) sine wave
ax_inset.plot(t_wave, water_level, 'b-', label='Water Level (Voltage)')
ax_inset.arrow(1.57, 0, 0.5, 0, head_width=0.1, head_length=0.2, fc='red', ec='red', label='Water Flow (Current)')  # Flow arrow, leads by π/2
ax_inset.text(0, 1.2, 'Flow Leads by π/2', fontsize=8, ha='left')
ax_inset.set_xticks([])
ax_inset.set_yticks([])
ax_inset.set_xlim(0, 2 * np.pi)
ax_inset.set_ylim(-1.5, 1.5)
ax_inset.set_frame_on(False)  # Remove inset border
ax_inset.legend(fontsize=6, loc='lower center')

# Set legend
ax.legend(fontsize=8, loc='lower right')

# Set axes aspect ratio and limits
ax.set_aspect('equal')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Update function (for animation)
def update(frame):
    # Calculate current quantum phase (-ωt + initial_phase)
    t_current = frame * 2 * np.pi / frames
    theta_q = -omega * t_current + initial_phase  # Start from 45°
    # Update quantum vector
    quantum_vector.set_UVC(np.cos(theta_q), np.sin(theta_q))
    return [quantum_vector]

# Create animation
ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)

# Save as GIF
ani.save('euler_phase_animation.gif', writer=PillowWriter(fps=20))

# Close plot (avoid displaying static figure)
plt.close()
