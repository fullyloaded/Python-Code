import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
N = 100  # Spatial grid points
L = 100  # Spatial domain length
dx = L / N  # Spatial step
dt = 0.05  # Time step
T = 300  # Total time steps
m = 1.0  # Mass (inertia)
v = 1.0  # Vacuum expectation value
epsilon = 0.05  # External driving amplitude
omega = 0.1  # External driving frequency
lam_base = 0.1  # Baseline nonlinear coupling

# Dynamic coupling to model synaptic plasticity
def lam(t):
    return lam_base * (1 + 0.2 * np.sin(0.05 * t))

# Initialize field and momentum
phi = np.zeros(N)
pi = np.zeros(N)
phi[N//2 - 5:N//2 + 5] = 1.5  # Initial Gaussian perturbation

# History for visualization
phi_history = []
vev_history = []
energy_history = []
corr_history = []
entanglement_history = []

# Effective potential and its derivative
def V(phi, t):
    return (lam(t) / 4) * (phi**2 - v**2)**2 - epsilon * np.cos(omega * t) * phi**2

def dV_dphi(phi, t):
    return lam(t) * phi * (phi**2 - v**2) - 2 * epsilon * np.cos(omega * t) * phi

# Local energy density
def local_energy_density(phi, pi, dx, t):
    grad_phi = np.gradient(phi, dx)
    energy = 0.5 * pi**2 + 0.5 * grad_phi**2 + V(phi, t)
    return energy

# Spatial correlation with zero-std check
def spatial_correlation(phi):
    if np.std(phi[:-1]) == 0 or np.std(phi[1:]) == 0:
        return 0
    corr = np.corrcoef(phi[:-1], phi[1:])[0, 1]
    return corr if not np.isnan(corr) else 0

# Entanglement approximation with zero-std check
def compute_entanglement(phi, pi, dx, t):
    window_size = 10
    mutual = []
    for i in range(N - window_size):
        A = local_energy_density(phi[i:i+window_size], pi[i:i+window_size], dx, t)
        B = local_energy_density(phi[i+1:i+1+window_size], pi[i+1:i+1+window_size], dx, t)
        if np.std(A) == 0 or np.std(B) == 0:
            mutual.append(0)
            continue
        corr = np.corrcoef(A, B)[0, 1] if not np.isnan(np.corrcoef(A, B)[0, 1]) else 0
        mutual.append(corr)
    return np.mean(mutual) if mutual else 0

# Test Laplacian calculation
x = np.linspace(0, L, N)
phi_test = np.sin(2 * np.pi * x / L)
lap_phi_test = np.gradient(np.gradient(phi_test, dx), dx)
lap_phi_exact = -(2 * np.pi / L)**2 * np.sin(2 * np.pi * x / L)
if np.allclose(lap_phi_test, lap_phi_exact, atol=0.1):
    print("Laplacian calculation verified.")
else:
    print("Warning: Laplacian calculation may be inaccurate.")

# Simulation loop
for t in range(T):
    phi_history.append(phi.copy())
    vev_history.append(np.mean(phi))
    energy_history.append(local_energy_density(phi, pi, dx, t * dt))
    corr_history.append(spatial_correlation(phi))
    entanglement_history.append(compute_entanglement(phi, pi, dx, t * dt))
    
    # Compute Laplacian
    lap_phi = np.gradient(np.gradient(phi, dx), dx)
    
    # Update momentum
    pi += dt * (lap_phi - dV_dphi(phi, t * dt))
    
    # Update field
    phi += dt * pi

phi_history = np.array(phi_history)

# Setup figure for six subplots
fig, axs = plt.subplots(2, 3, figsize=(18, 10))
axs = axs.ravel()

# Subplot 1: Field Evolution (Animated)
def update_field(t):
    axs[0].cla()
    axs[0].plot(np.linspace(0, L, N), phi_history[t], 'b-', label='φ(x,t)')
    axs[0].set_title('Field Evolution')
    axs[0].set_xlabel('x')
    axs[0].set_ylabel('φ(x,t)')
    axs[0].set_ylim(-2, 2)
    axs[0].grid(True)
    axs[0].legend()

# Subplot 2: Vacuum Expectation Value
axs[1].plot(np.arange(T) * dt, vev_history, 'r-', label='<φ(t)>')
axs[1].set_title('Vacuum Expectation Value')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('<φ(t)>')
axs[1].grid(True)
axs[1].legend()

# Subplot 3: Energy Density (Animated)
def update_energy(t):
    axs[2].cla()
    axs[2].plot(np.linspace(0, L, N), energy_history[t], 'g-', label='Energy')
    axs[2].set_title('Energy Density')
    axs[2].set_xlabel('x')
    axs[2].set_ylabel('Energy')
    axs[2].set_ylim(0, np.max([np.max(e) for e in energy_history if np.max(e) > 0]) * 1.1)
    axs[2].grid(True)
    axs[2].legend()

# Subplot 4: Spatial Correlations
axs[3].plot(np.arange(T) * dt, corr_history, 'm-', label='Correlation')
axs[3].set_title('Spatial Correlations')
axs[3].set_xlabel('Time')
axs[3].set_ylabel('Correlation')
axs[3].grid(True)
axs[3].legend()

# Subplot 5: Phase Space (Center Point)
axs[4].plot(phi_history[:, N//2], [pi[N//2] for pi in phi_history], 'k-', label='Trajectory')
axs[4].set_title('Phase Space (Center)')
axs[4].set_xlabel('φ')
axs[4].set_ylabel('π')
axs[4].grid(True)
axs[4].legend()

# Subplot 6: Entanglement Approximation
axs[5].plot(np.arange(T) * dt, entanglement_history, 'c-', label='Mutual Corr.')
axs[5].set_title('Entanglement Approximation')
axs[5].set_xlabel('Time')
axs[5].set_ylabel('Mutual Correlation')
axs[5].grid(True)
axs[5].legend()

# Separate Phase Space Plot
fig_phase = plt.figure(figsize=(8, 6))
plt.plot(phi_history[:, N//2], [pi[N//2] for pi in phi_history], 'k-', label='Trajectory')
plt.title('Phase Space (Center Point)')
plt.xlabel('φ')
plt.ylabel('π')
plt.grid(True)
plt.legend()

# Animate subplots and assign to variables
anim_field = FuncAnimation(fig, update_field, frames=T, interval=50)
anim_energy = FuncAnimation(fig, update_energy, frames=T, interval=50)

plt.tight_layout()
plt.show()
