import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 100  # Number of spatial grid points
L = 10.0  # Spatial domain size
dx = L / N  # Spatial grid spacing
dt = 0.01  # Time step
T = 1000  # Number of time steps
m_phi, m_psi = 1.0, 1.0  # Field masses (inertia of social variables)
lam, eta = 0.1, 0.1  # Self-coupling constants (self-reinforcement)
g = 0.5  # Field coupling constant (interdependence)
window_size = 10  # Window size for entanglement approximation

# Social interpretation parameters
phi_label = "Opinion Strength"  # φ represents political opinion (-1: liberal, +1: conservative)
psi_label = "Economic Sentiment"  # ψ represents economic optimism/pessimism (-1: pessimistic, +1: optimistic)
grid_label = "Social Regions"  # Spatial grid represents geographic or network regions

# Local energy density function (for φ only, focusing on opinion dynamics)
def local_energy_density(phi, pi, dx, m_phi, lam):
    """
    Compute local energy density for φ field, representing social activity (e.g., opinion intensity).
    Inputs:
        phi: Field values (opinion strength)
        pi: Conjugate momentum (rate of change of opinion)
        dx: Spatial grid spacing
        m_phi: Mass parameter (inertia)
        lam: Self-coupling (self-reinforcement)
    Returns:
        energy: Energy density array
    """
    grad_phi = (np.roll(phi, -1) - np.roll(phi, 1)) / (2 * dx)  # Periodic central difference
    energy = 0.5 * pi**2 + 0.5 * grad_phi**2 + 0.5 * m_phi**2 * phi**2 + 0.25 * lam * phi**4
    return energy

# Initialize fields
x = np.linspace(0, L, N, endpoint=False)
phi, psi = np.zeros(N), np.zeros(N)
pi_phi, pi_psi = np.zeros(N), np.zeros(N)
phi = np.exp(-(x - L/2)**2 / 0.5)  # Initial opinion surge in central region
psi = 0.1 * np.sin(2 * np.pi * x / L)  # Oscillating economic sentiment

# Storage for analysis
phi_history = [phi.copy()]  # Store φ snapshots for visualization
psi_history = [psi.copy()]  # Store ψ snapshots
vev_phi = [np.mean(phi)]  # VEV of φ (average opinion)
vev_psi = [np.mean(psi)]  # VEV of ψ (average economic sentiment)
entanglement_time = []  # Average correlation (social connectivity)
energies = []  # Total energy (social activity)
phase_space = [(phi.copy(), pi_phi.copy())]  # Store (φ, π_φ ${({ \phi }}) for phase space

# Time evolution
for t in range(T):
    # Compute Laplacians (spatial diffusion of social variables)
    lap_phi = (np.roll(phi, -1) - 2 * phi + np.roll(phi, 1)) / dx**2
    lap_psi = (np.roll(psi, -1) - 2 * psi + np.roll(psi, 1)) / dx**2
    
    # Equations of motion (social dynamics with self-reinforcement and coupling)
    d2_phi = lap_phi - m_phi**2 * phi - lam * phi**3 + 2 * g * phi * psi
    d2_psi = lap_psi - m_psi**2 * psi - eta * psi**3 + g * phi**2
    
    # Leapfrog updates
    pi_phi += dt * d2_phi
    pi_psi += dt * d2_psi
    phi += dt * pi_phi
    psi += dt * pi_psi
    
    # Store data at selected times (every 200 steps)
    if t % 200 == 0:
        phi_history.append(phi.copy())
        psi_history.append(psi.copy())
        phase_space.append((phi.copy(), pi_phi.copy()))
    
    # Compute VEV (societal norms)
    vev_phi.append(np.mean(phi))
    vev_psi.append(np.mean(psi))
    
    # Compute total energy (social activity level)
    grad_phi = (np.roll(phi, -1) - np.roll(phi, 1)) / (2 * dx)
    grad_psi = (np.roll(psi, -1) - np.roll(psi, 1)) / (2 * dx)
    potential = (0.5 * m_phi**2 * phi**2 + 0.5 * m_psi**2 * psi**2 + 
                 0.25 * lam * phi**4 + 0.25 * eta * psi**4 - g * phi**2 * psi)
    energy = (0.5 * pi_phi**2 + 0.5 * pi_psi**2 + 0.5 * grad_phi**2 + 
              0.5 * grad_psi**2 + potential).sum() * dx
    energies.append(energy)
    
    # Entanglement approximation (social connectivity)
    entanglement_approx = []
    for i in range(len(phi) - window_size):
        A = local_energy_density(phi[i:i+window_size], pi_phi[i:i+window_size], dx, m_phi, lam)
        B = local_energy_density(phi[i+1:i+1+window_size], pi_phi[i+1:i+1+window_size], dx, m_phi, lam)
        if np.std(A) > 1e-10 and np.std(B) > 1e-10:
            mutual = np.corrcoef(A, B)[0, 1]
        else:
            mutual = 0.0
        entanglement_approx.append(mutual)
    entanglement_time.append(np.mean(entanglement_approx))

# Spatial correlation profile (range of social influence)
distances = np.arange(1, N - window_size + 1, 10)  # Ensure d + window_size <= N
correlations = []
for d in distances:
    A = local_energy_density(phi[0:window_size], pi_phi[0:window_size], dx, m_phi, lam)
    B = local_energy_density(phi[d:d+window_size], pi_phi[d:d+window_size], dx, m_phi, lam)
    if np.std(A) > 1e-10 and np.std(B) > 1e-10:
        correlations.append(np.corrcoef(A, B)[0, 1])
    else:
        correlations.append(0.0)

# Visualization with adjusted layout to prevent text overlap
plt.figure(figsize=(15, 12))

# Adjust subplot spacing
plt.subplots_adjust(hspace=0.4, wspace=0.3)  # Increase vertical and horizontal spacing

# Panel 1: Opinion dynamics (φ evolution, symmetry breaking)
plt.subplot(3, 2, 1)
for i, phi_snap in enumerate(phi_history):
    plt.plot(x, phi_snap, label=f't={i*200*dt:.1f}')
plt.xlabel(grid_label, fontsize=10)
plt.ylabel(phi_label, fontsize=10)
plt.title(f'{phi_label} Dynamics (Polarization)', fontsize=11, pad=10)
plt.legend(fontsize=8, loc='upper right', bbox_to_anchor=(1.15, 1.0))

# Panel 2: Economic sentiment dynamics (ψ evolution)
plt.subplot(3, 2, 2)
for i, psi_snap in enumerate(psi_history):
    plt.plot(x, psi_snap, label=f't={i*200*dt:.1f}')
plt.xlabel(grid_label, fontsize=10)
plt.ylabel(psi_label, fontsize=10)
plt.title(f'{psi_label} Dynamics', fontsize=11, pad=10)
plt.legend(fontsize=8, loc='upper right', bbox_to_anchor=(1.15, 1.0))

# Panel 3: Vacuum expectation values (societal norms)
plt.subplot(3, 2, 3)
plt.plot(np.arange(T+1) * dt, vev_phi, label=f'Average {phi_label}')
plt.plot(np.arange(T+1) * dt, vev_psi, label=f'Average {psi_label}')
plt.xlabel('Time', fontsize=10)
plt.ylabel('Average Value', fontsize=10)
plt.title('Societal Norms (VEV)', fontsize=11, pad=10)
plt.legend(fontsize=8, loc='upper right')

# Panel 4: Entanglement (social connectivity)
plt.subplot(3, 2, 4)
plt.plot(np.arange(T) * dt, entanglement_time)
plt.xlabel('Time', fontsize=10)
plt.ylabel('Average Correlation', fontsize=10)
plt.title('Social Connectivity (Entanglement)', fontsize=11, pad=10)

# Panel 5: Energy (social activity stability)
plt.subplot(3, 2, 5)
plt.plot(np.arange(T) * dt, energies)
plt.xlabel('Time', fontsize=10)
plt.ylabel('Total Social Activity', fontsize=10)
plt.title('Activity Stability', fontsize=11, pad=10)

# Panel 6: Spatial correlation profile (range of influence)
plt.subplot(3, 2, 6)
plt.plot(distances * dx, correlations)
plt.xlabel('Distance', fontsize=10)
plt.ylabel('Correlation', fontsize=10)
plt.title('Spatial Correlation Profile', fontsize=11, pad=10)

# Apply tight layout with extra padding
plt.tight_layout(pad=2.0)

# Show the plot
plt.show()

# Phase space plot (chaotic dynamics)
plt.figure(figsize=(8, 6))
for phi_snap, pi_snap in phase_space[::2]:  # Plot every other snapshot
    plt.scatter(phi_snap[::10], pi_snap[::10], s=5, alpha=0.5)
plt.xlabel(phi_label, fontsize=10)
plt.ylabel(f'Rate of Change of {phi_label}', fontsize=10)
plt.title('Phase Space (Chaotic Dynamics)', fontsize=11, pad=10)
plt.tight_layout(pad=2.0)
plt.show()
