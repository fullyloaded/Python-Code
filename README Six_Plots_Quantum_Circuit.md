Visualization Details and Python Script


Figure 1: Capacitor V(t) V(t) V(t), I(t) I(t) I(t) Time Domain vs. Frequency Domain Waveforms

• Description: Show the time-domain waveforms of voltage 𝑉(𝑡) = cos(𝜔𝑡) and current 𝐼(𝑡) = 𝐶𝜔 sin(𝜔𝑡), highlighting the 90° phase lead of current over voltage. Include frequency-domain amplitude spectra via Fourier transform, showing single-frequency peaks.

• Parameters:

• 𝜔 = 1 rad/s

• 𝐶 = 1 F

• Time range: 𝑡 ∈ [0, 4𝜋]

• Visuals:

• Time Domain: Plot 𝑉(𝑡) (blue solid line) and 𝐼(𝑡) (red dashed line), showing current leading voltage by 90°.

• Frequency Domain: Plot amplitude spectra of 𝑉(𝑡) and 𝐼(𝑡), with peaks at 𝜔 = 1 rad/s.

• Inset: Reservoir analogy showing water level (voltage) and flow (current) with phase difference.

• Output: voltage_current.png




Figure 2: Fourier Decomposition of Square Wave and Frequency Components

• Description: Display a square wave 𝑠(𝑡) in the time domain and its Fourier transform, emphasizing odd harmonics and linking to quantum energy levels.

• Parameters:

• Period 𝑇 = 4 s

• Frequencies: 𝑓 = 𝑛⁄𝑇, 𝑛 = 1, 3, 5, …

• Visuals:

• Time Domain: Plot square wave 𝑠(𝑡).

• Frequency Domain: Amplitude spectrum showing peaks at odd harmonics.

• Annotation: Note “Related to quantum energy levels (see Figure 6)” to connect to quantized modes.

• Output: square_wave_fft.png




Figure 3: Euler’s Formula and Phase Rotation Animation

• Description: Visualize Euler’s formula 𝑒^{𝑗𝜃} = cos(𝜃) + 𝑗 sin(𝜃) with rotating vectors in the complex plane.

• Vectors:

• Voltage (blue): cos(𝜔𝑡) + 𝑗 sin(𝜔𝑡), length 1

• Current (red dashed): sin(𝜔𝑡) + 𝑗 cos(𝜔𝑡), leading by 90°, length 1

• Quantum (cyan): Initial phase 45°, length 0.5

• Visuals:

• Animate vectors rotating on the unit circle at 20 fps, looping infinitely

• Inset: Reservoir analogy showing water level vs. flow phase difference

• Output: euler_animation.gif




Figure 4: LC Resonance vs. Field Mode Energy Distribution

• Description: Compare LC circuit resonance with quantum field mode energy levels.

• Parameters:

 • 𝐿 = 1 𝐻, 𝐶 = 1 𝐹, resonance frequency 𝑓₀ = 1∕(2π√(𝐿𝐶)) ≈ 0.159 𝐻𝐳

 • Quantum modes: 𝐸ₙ = 𝑛 ħ 𝜔, 𝑛 = 0, 1, 2, …

 • ħ = 1.0545718 × 10⁻³⁴ 𝐽⋅𝑠

• Visuals:

 • Top: LC frequency response (current amplitude vs. frequency)

 • Bottom: Discrete quantum energy levels 𝐸ₙ

• Output: lc_resonance.png




Figure 5: Quantum Field vs. Circuit Field Comparison (Table)

• Description: Tabular comparison of circuit and quantum field concepts.








• Output: quantum_circuit_table.png



Figure 6: Superconducting Qubit and Energy Level Diagram

• Description: Show energy levels of a superconducting qubit, analogous to a quantum harmonic oscillator, with a simplified circuit diagram.

• Parameters:

　・𝜔 = 2π × 5 GHz

　・ħ = 1.0545718 × 10⁻³⁴ J·s

　・Energy levels: 𝐸ₙ = ħ𝜔 (𝑛 + 1∕2), 𝑛 = 0, 1, 2, …

• Visuals:

　・Energy level diagram with ∣0⟩, ∣1⟩, and transition frequency 𝜔₀₁

　・Inset: Simplified LC + Josephson junction circuit

• Output: superconducting_qubit.png

