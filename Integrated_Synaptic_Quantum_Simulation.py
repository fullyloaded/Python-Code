import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
from PIL import Image
import os
import io

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector

# Initialize synaptic network
def init_synaptic_network(n_neurons):
    G = nx.erdos_renyi_graph(n_neurons, p=0.3)
    for (u, v) in G.edges():
        G[u][v]['weight'] = np.random.rand()
    return G

# Update synaptic connections
def update_synapses(G, prune_prob=0.1, form_prob=0.05):
    edges_to_remove = []
    for u, v in list(G.edges()):
        if np.random.rand() < prune_prob:
            edges_to_remove.append((u, v))
    G.remove_edges_from(edges_to_remove)
    nodes = list(G.nodes())
    for _ in range(len(nodes)):
        u, v = random.sample(nodes, 2)
        if not G.has_edge(u, v) and np.random.rand() < form_prob:
            G.add_edge(u, v, weight=np.random.rand())
    return G

# Reconfigure quantum gates
def quantum_gate_reconfig(n_qubits, current_gates):
    new_gates = []
    for gate in current_gates:
        if np.random.rand() < 0.2:
            continue
        new_gates.append(gate)
    for _ in range(np.random.randint(1, 3)):
        qubits = random.sample(range(n_qubits), 2)
        gate_type = random.choice(['CX', 'RY', 'H'])
        new_gates.append((gate_type, qubits))
    return new_gates

# Build Qiskit circuit
def build_quantum_circuit_from_gates(gate_list, num_qubits=5):
    qc = QuantumCircuit(num_qubits)
    for gate, qubits in gate_list:
        if any(q >= num_qubits for q in qubits):
            print(f"Warning: Invalid qubit index {qubits}, skipping gate")
            continue
        if gate == "H":
            for q in qubits:
                qc.h(q)
        elif gate == "Z":
            if len(qubits) == 1:
                qc.z(qubits[0])
            elif len(qubits) == 2:
                qc.cz(qubits[0], qubits[1])
        elif gate == "RY":
            for q in qubits:
                qc.ry(1.57, q)
        elif gate == "CX":
            qc.cx(qubits[0], qubits[1])
    qc.save_statevector()
    return qc

# Plot synaptic network individually
def plot_synaptic_graph(G, time_step):
    plt.figure()
    pos = nx.spring_layout(G, seed=42)
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, edge_color=weights, edge_cmap=plt.cm.Blues)
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    description = f'Neurons: {num_nodes}\nSynapses: {num_edges}\nTime Step: {time_step}'
    plt.title("Synaptic Network")
    plt.text(0.02, 0.95, description, transform=plt.gca().transAxes, fontsize=8,
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
    plt.savefig(f'synaptic_t{time_step}.png', bbox_inches='tight')
    plt.close()

# Plot quantum circuit individually
def plot_quantum_circuit(qc, time_step):
    plt.figure()
    qc.draw(output='mpl')
    num_qubits = qc.num_qubits
    num_gates = len(qc.data)
    description = f'Qubits: {num_qubits}\nGates: {num_gates}\nTime Step: {time_step}'
    plt.title("Quantum Circuit")
    plt.text(0.02, 0.95, description, transform=plt.gca().transAxes, fontsize=8,
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
    plt.savefig(f'circuit_t{time_step}.png', bbox_inches='tight')
    plt.close()

# Plot Bloch sphere individually
def plot_bloch_sphere(statevector, time_step):
    plt.figure()
    plot_bloch_multivector(statevector)
    num_qubits = statevector.num_qubits
    description = f'Qubits: {num_qubits}\nTime Step: {time_step}'
    plt.title("Bloch Sphere")
    plt.gca().text2D(0.02, 0.95, description, transform=plt.gca().transAxes, fontsize=8,
                     verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
    plt.savefig(f'bloch_t{time_step}.png', bbox_inches='tight')
    plt.close()

# Plot combined figure
def plot_combined(G, qc, statevector, title, time_step):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5), gridspec_kw={'width_ratios': [1, 1.5, 1]})
    
    # Synaptic network
    pos = nx.spring_layout(G, seed=42)
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, edge_color=weights, edge_cmap=plt.cm.Blues, ax=ax1)
    ax1.set_title("Synaptic Network")
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    description = f'Neurons: {num_nodes}\nSynapses: {num_edges}\nTime Step: {time_step}'
    ax1.text(0.02, 0.95, description, transform=ax1.transAxes, fontsize=8,
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

    # Quantum circuit
    qc.draw(output='mpl', ax=ax2)
    num_qubits = qc.num_qubits
    num_gates = len(qc.data)
    description = f'Qubits: {num_qubits}\nGates: {num_gates}\nTime Step: {time_step}'
    ax2.text(0.02, 0.95, description, transform=ax2.transAxes, fontsize=8,
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
    ax2.set_title("Quantum Circuit")

    # Apply tight layout before Bloch sphere to avoid layout issues
    plt.tight_layout()

    # Bloch sphere
    # Create a temporary figure for Bloch sphere
    temp_fig = plt.figure()
    plot_bloch_multivector(statevector)
    # Save to a bytes buffer
    buf = io.BytesIO()
    temp_fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    bloch_img = Image.open(buf)
    # Draw image onto ax3
    ax3.imshow(bloch_img)
    ax3.axis('off')  # Hide axes for image
    ax3.text(0.02, 0.95, description, transform=ax3.transAxes, fontsize=8,
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
    ax3.set_title("Bloch Sphere")
    plt.close(temp_fig)  # Close temporary figure
    buf.close()

    # Set suptitle with adjusted position to avoid overlapping qubit 2
    plt.suptitle(title, fontsize=12, y=1.05)
    plt.savefig(f'combined_t{time_step}.png', bbox_inches='tight')
    plt.close()

# Create GIF
def create_gif(time_steps):
    images = [Image.open(f'combined_t{t}.png') for t in range(time_steps)]
    images[0].save('combined_simulation.gif', save_all=True, append_images=images[1:], duration=1000, loop=0)
    
    # Clean up temporary files (keep individual PNGs)
    for t in range(time_steps):
        if os.path.exists(f'combined_t{t}.png'):
            os.remove(f'combined_t{t}.png')

# Main simulation function
def run_simulation(time_steps=3):
    G = init_synaptic_network(n_neurons=10)
    quantum_gates = [('H', [0]), ('CX', [0,1]), ('RY', [1,2])]

    simulator = AerSimulator()

    for t in range(time_steps):
        print(f"--- Time Step {t} ---")
        G = update_synapses(G)
        quantum_gates = quantum_gate_reconfig(n_qubits=5, current_gates=quantum_gates)
        print(f"Quantum Gate Structure: {quantum_gates}\n")
        qc = build_quantum_circuit_from_gates(quantum_gates, num_qubits=5)
        compiled = transpile(qc, simulator)
        result = simulator.run(compiled).result()
        statevector = result.get_statevector()
        # Generate individual PNGs
        plot_synaptic_graph(G, time_step=t)
        plot_quantum_circuit(qc, time_step=t)
        plot_bloch_sphere(statevector, time_step=t)
        # Generate combined PNG
        plot_combined(G, qc, statevector, f"Simulation Results (Time {t})", time_step=t)
    
    # Generate GIF
    create_gif(time_steps)

if __name__ == '__main__':
    run_simulation(time_steps=3)