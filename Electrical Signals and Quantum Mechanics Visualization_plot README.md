Electrical Signals and Quantum Mechanics Visualization
Overview
This project provides a Python-based visualization tool to demonstrate electrical signals and their quantum mechanics analogies. It generates two charts:

Voltage and Current Waveforms: Visualizes the voltage ( V(t) = \cos(\omega t) ) and current ( I(t) = C \omega \sin(\omega t) ) of a capacitor, illustrating the 90° phase difference where current leads voltage, with an analogy to water level and flow.
Fourier Transform of a Square Wave: Displays a square wave in the time domain and its frequency domain representation using the Fourier Transform, decomposing the signal into single-frequency components.

The visualizations use analogies (e.g., water level for voltage, water flow for current) to make electrical and quantum concepts more intuitive.
Features

Waveform Visualization: Plots capacitor voltage and current over time, highlighting the phase difference.
Fourier Transform Analysis: Shows a square wave and its frequency spectrum, illustrating signal decomposition.
Intuitive Analogies: Uses water level and flow metaphors to explain electrical signals.
Customizable Parameters: Allows modification of frequency (( \omega )), capacitance (( C )), and time range.
Clear Annotations: Includes labels, gridlines, and text annotations for key points (e.g., wave upslope).

Prerequisites
To run the script, you need the following Python packages:

numpy
matplotlib
scipy

Install them using pip:
pip install numpy matplotlib scipy

Installation

Clone the repository (or download the script):git clone https://github.com/your-username/electrical-signals-quantum-visualization.git
cd electrical-signals-quantum-visualization


Ensure the required dependencies are installed (see Prerequisites).
Place the script Electrical Signals and Quantum Mechanics Visualization 1.py in your working directory.

Usage

Navigate to the directory containing the script.
Run the script using Python:python "Electrical Signals and Quantum Mechanics Visualization 1.py"


The script will generate:
A plot showing voltage and current waveforms with a 90° phase difference and water analogy annotations.
A two-panel plot showing a square wave in the time domain and its Fourier Transform in the frequency domain.



Parameters
Key parameters in the script can be modified:

Chart 1 (Voltage and Current):
omega: Frequency of the signal (default: 1).
C: Capacitance (default: 1).
t: Time array (default: 0 to ( 4\pi ), 1000 points).


Chart 2 (Fourier Transform):
t: Time array for the square wave (default: 0 to 4, 1000 points).
Square wave frequency is set via 2 * np.pi * t (modifiable in the signal.square function).



Output
The script produces:

Chart 1: A single plot showing:
Blue solid line: Voltage ( V(t) ) (water level).
Red dashed line: Current ( I(t) ) (water flow).
Gray dotted line and text annotation at ( t = \pi/4 ), indicating maximum flow when the water level rises.


Chart 2: A two-panel figure:
Left: Time-domain square wave.
Right: Frequency-domain spectrum (amplitude vs. frequency).


Both plots include titles, labels, legends, and grids for clarity.

Notes

The script uses the Microsoft YaHei font for rendering, ensuring compatibility with systems supporting this font. If unavailable, Matplotlib will fall back to a default font.
The Fourier Transform plot shows only positive frequencies for simplicity.
Ensure Matplotlib is configured to display plots correctly (e.g., check your backend if plots do not appear).

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Create a pull request.

Please open an issue to discuss proposed changes or report bugs.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments
Inspired by electrical engineering principles and quantum mechanics analogies, with visualizations designed to bridge technical concepts and intuitive understanding.

