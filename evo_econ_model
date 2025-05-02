import numpy as np
import matplotlib
import shutil
import os
# Dynamically select a suitable backend
backends = ['Qt5Agg', 'TkAgg', 'Agg']
for backend in backends:
    try:
        matplotlib.use(backend)
        print(f"Using backend: {backend}")
        break
    except:
        continue
else:
    raise ImportError("No suitable matplotlib backend found")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from IPython.display import HTML

# Check for ffmpeg availability
ffmpeg_available = shutil.which('ffmpeg') is not None
if not ffmpeg_available:
    print("Warning: ffmpeg not found. Install ffmpeg and add to PATH to save MP4. See https://ffmpeg.org/download.html")
    print("Falling back to GIF using Pillow.")

# Configure matplotlib fonts and layout
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # Fix negative sign display
plt.rcParams['font.size'] = 10  # Global font size

# Configure Jupyter environment
try:
    from IPython import get_ipython
    if 'IPKernelApp' in get_ipython().config:
        get_ipython().run_line_magic('matplotlib', 'inline')
except:
    pass

class EvoEconFieldModel:
    """Quantum Field Theory Model for Evolutionary Economics"""
    
    def __init__(self, params=None):
        """Initialize model parameters"""
        self.params = {
            'Nx': 100,           # Number of spatial grid points
            'Nt': 500,           # Number of time steps
            'dx': 0.5,           # Spatial step size
            'dt': 0.01,          # Time step size (reduced for stability)
            'm2': -1.0,          # Potential term parameter
            'lambda': 0.1,       # Self-interaction strength (reduced for stability)
            'g': 0.5,            # Agent-field interaction strength
            'D_phi': 1.0,        # Knowledge diffusion coefficient
            'D_rho': 0.1,        # Agent diffusion coefficient
            'beta': 0.1,         # Agent response to technological field
            'xi': 0.05,          # Random environmental noise strength
            'init_center': 0.5,  # Initial innovation center position
            'init_width': 0.1,   # Initial innovation width
        }
        
        if params:
            for key, value in params.items():
                if key in self.params:
                    self.params[key] = value
        
        self.initialize_fields()
        self.history = {'phi': [], 'rho': []}
        self.fig = None  # Store figure for animation
        self.anim = None  # Store animation object
    
    def initialize_fields(self):
        """Initialize field variables"""
        p = self.params
        self.x = np.linspace(0, p['Nx']*p['dx'], p['Nx'])
        
        center = int(p['init_center'] * p['Nx'])
        width = int(p['init_width'] * p['Nx'])
        self.phi = np.zeros(p['Nx'])
        self.phi_old = np.zeros(p['Nx'])
        for i in range(p['Nx']):
            self.phi[i] = np.exp(-(i - center)**2 / (2 * width**2))
        self.phi_old = self.phi.copy()
        self.phi_new = np.zeros(p['Nx'])
        
        self.rho = np.ones(p['Nx']) * 0.1
        for i in range(p['Nx']):
            self.rho[i] += 0.05 * np.exp(-(i - center)**2 / (2 * width**2))
        self.rho_new = np.zeros(p['Nx'])
        
        np.random.seed(42)
        self.phi += np.random.normal(0, 0.01, p['Nx'])
        self.rho += np.random.normal(0, 0.01, p['Nx'])
    
    def potential_derivative(self, phi):
        """Compute potential function derivative dV/dphi"""
        p = self.params
        return p['m2'] * phi + p['lambda'] * phi**3
    
    def update_fields(self):
        """Update fields for one time step"""
        p = self.params
        
        for i in range(1, p['Nx'] - 1):
            laplacian = (self.phi[i+1] - 2*self.phi[i] + self.phi[i-1]) / (p['dx']**2)
            V_prime = self.potential_derivative(self.phi[i])
            source = p['g'] * self.rho[i]
            noise = p['xi'] * np.random.normal(0, 1)
            self.phi_new[i] = (2 * self.phi[i] - self.phi_old[i] + 
                              (p['dt']**2) * (p['D_phi'] * laplacian - V_prime + source + noise))
        
        self.phi_new = np.clip(self.phi_new, -10, 10)
        
        for i in range(1, p['Nx'] - 1):
            diffusion = p['D_rho'] * (self.rho[i+1] - 2*self.rho[i] + self.rho[i-1]) / (p['dx']**2)
            reaction = p['beta'] * self.rho[i] * (self.phi[i]**2 - 0.5)
            self.rho_new[i] = self.rho[i] + p['dt'] * (diffusion + reaction)
            self.rho_new[i] = max(0, self.rho_new[i])
        
        self.phi_new[0] = self.phi_new[-1] = 0
        self.rho_new[0] = self.rho_new[-1] = 0.1
        
        self.phi_old = self.phi.copy()
        self.phi = self.phi_new.copy()
        self.rho = self.rho_new.copy()
    
    def run_simulation(self):
        """Run the full simulation"""
        p = self.params
        self.history = {'phi': [], 'rho': []}
        self.history['phi'].append(self.phi.copy())
        self.history['rho'].append(self.rho.copy())
        
        for t in range(p['Nt']):
            if t % 100 == 0:
                print(f"Simulation Progress: {t/p['Nt']*100:.1f}%")
            self.update_fields()
            if t % 10 == 0:
                self.history['phi'].append(self.phi.copy())
                self.history['rho'].append(self.rho.copy())
        
        print("Simulation Completed")
        return self.history
    
    def plot_results(self):
        """Plot simulation results"""
        p = self.params
        phi_history = np.array(self.history['phi'])
        rho_history = np.array(self.history['rho'])
        
        if phi_history.size == 0 or rho_history.size == 0:
            raise ValueError("History data is empty, cannot plot")
        if np.any(np.isnan(phi_history)) or np.any(np.isnan(rho_history)):
            raise ValueError("History data contains NaN, cannot plot")
        
        fig = plt.figure(figsize=(15, 10))
        
        # Subplot 1: Technological Field Heatmap
        ax1 = fig.add_subplot(2, 2, 1)
        im1 = ax1.imshow(
            phi_history, 
            aspect='auto', 
            origin='lower',
            extent=[0, p['Nx']*p['dx'], 0, p['Nt']*p['dt']],
            cmap='viridis'
        )
        cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.8)
        cbar1.set_label('Technological Field Intensity', fontsize=9)
        cbar1.ax.tick_params(labelsize=8)
        ax1.set_xlabel('Spatial Position', fontsize=9)
        ax1.set_ylabel('Time', fontsize=9)
        ax1.set_title('Technological Field Evolution', fontsize=10)
        
        # Subplot 2: Agent Density Heatmap
        ax2 = fig.add_subplot(2, 2, 2)
        im2 = ax2.imshow(
            rho_history, 
            aspect='auto', 
            origin='lower',
            extent=[0, p['Nx']*p['dx'], 0, p['Nt']*p['dt']],
            cmap='plasma'
        )
        cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.8)
        cbar2.set_label('Agent Density', fontsize=9)
        cbar2.ax.tick_params(labelsize=8)
        ax2.set_xlabel('Spatial Position', fontsize=9)
        ax2.set_ylabel('Time', fontsize=9)
        ax2.set_title('Agent Distribution Evolution', fontsize=10)
        
        # Subplot 3: Initial and Final Field Comparison
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(self.x, phi_history[-1], 'b-', label='Final Technological Field')
        ax3.plot(self.x, rho_history[-1], 'r-', label='Final Agent Distribution')
        ax3.plot(self.x, phi_history[0], 'b--', alpha=0.5, label='Initial Technological Field')
        ax3.plot(self.x, rho_history[0], 'r--', alpha=0.5, label='Initial Agent Distribution')
        ax3.set_xlabel('Spatial Position', fontsize=9)
        ax3.set_ylabel('Field Intensity/Density', fontsize=9)
        ax3.set_title('Initial vs Final Field Comparison', fontsize=10)
        ax3.legend(fontsize=8, bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.grid(True)
        
        # Subplot 4: Peak Tracking
        ax4 = fig.add_subplot(2, 2, 4)
        phi_max = np.max(phi_history, axis=1)
        rho_max = np.max(rho_history, axis=1)
        time_points = np.linspace(0, p['Nt']*p['dt'], len(phi_max))
        ax4.plot(time_points, phi_max, 'b-', label='Technological Field Maximum')
        ax4.plot(time_points, rho_max, 'r-', label='Agent Density Maximum')
        ax4.set_xlabel('Time', fontsize=9)
        ax4.set_ylabel('Maximum Value', fontsize=9)
        ax4.set_title('Evolution of Field Maxima', fontsize=10)
        ax4.legend(fontsize=8)
        ax4.grid(True)
        
        plt.subplots_adjust(wspace=0.3, hspace=0.4)  # Adjust subplot spacing
        plt.tight_layout()
        plt.savefig('evo_econ_results.png')
        plt.show()
        return fig
    
    def create_animation(self):
        """Create animation of field evolution"""
        p = self.params
        phi_history = np.array(self.history['phi'])
        rho_history = np.array(self.history['rho'])
        
        if phi_history.size == 0 or rho_history.size == 0:
            raise ValueError("History data is empty, cannot create animation")
        
        self.fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        line1, = ax1.plot(self.x, phi_history[0], 'b-', lw=2)
        line2, = ax2.plot(self.x, rho_history[0], 'r-', lw=2)
        
        ax1.set_ylim(np.min(phi_history) - 0.1, np.max(phi_history) + 0.1)
        ax1.set_xlabel('Spatial Position', fontsize=9)
        ax1.set_ylabel('Technological Field (φ)', fontsize=9)
        ax1.set_title('Technological Field Evolution', fontsize=10)
        ax1.grid(True)
        
        ax2.set_ylim(np.min(rho_history) - 0.1, np.max(rho_history) + 0.1)
        ax2.set_xlabel('Spatial Position', fontsize=9)
        ax2.set_ylabel('Agent Density (ρ)', fontsize=9)
        ax2.set_title('Agent Distribution Evolution', fontsize=10)
        ax2.grid(True)
        
        time_text = self.fig.suptitle('t = 0.0', y=0.98, fontsize=10)
        
        def animate(i):
            if ax1 is None or ax2 is None:
                raise ValueError("Axis objects are None, cannot update animation")
            line1.set_ydata(phi_history[i])
            line2.set_ydata(rho_history[i])
            time_text.set_text(f't = {i * p["dt"] * 10:.2f}')
            return line1, line2, time_text
        
        self.anim = FuncAnimation(
            self.fig,
            animate,
            frames=len(phi_history),
            interval=100,
            blit=True
        )
        
        plt.subplots_adjust(wspace=0.3)
        plt.tight_layout()
        
        # Save animation
        try:
            if ffmpeg_available:
                save_path = os.path.join(os.getcwd(), 'evo_econ_animation.mp4')
                writer = FFMpegWriter(fps=10, bitrate=1800)
                self.anim.save(save_path, writer=writer)
                print(f"Animation saved as {save_path}")
            else:
                save_path = os.path.join(os.getcwd(), 'evo_econ_animation.gif')
                writer = PillowWriter(fps=10)
                self.anim.save(save_path, writer=writer)
                print(f"Animation saved as {save_path}")
        except Exception as e:
            print(f"Failed to save animation: {e}")
        
        plt.show(block=False)  # Keep window open non-blocking
        return HTML(self.anim.to_jshtml()) if 'IPython' in globals() else self.anim

if __name__ == "__main__":
    model = EvoEconFieldModel()
    model.run_simulation()
    model.plot_results()
    plt.show()
    anim = model.create_animation()
