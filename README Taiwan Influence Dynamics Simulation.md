# Taiwan Influence Dynamics Simulation

This Python application simulates geopolitical influence dynamics around Taiwan, visualizing interactions between key actors (USA, China, Taiwan, Japan, EU) under normal and crisis scenarios. Built with Pygame for rendering and OpenCV for video recording, it replicates a React/D3.js-based visualization, showing influence flows, particle effects, and crisis-induced "vacuum bubbles" around Taiwan.

## Features
- **Interactive Visualization**: Displays nodes (countries) with influence connections (support, pressure, cooperation, competition).
- **Dynamic Animation**: Nodes repel each other, and particles move to represent influence flows.
- **Crisis Mode (φ₃ Crisis)**: Triggers visual effects like pulsing nodes and red vacuum bubbles around Taiwan to simulate instability (e.g., cross-strait tensions).
- **Video Recording**: Exports a 10-second MP4 video capturing the simulation, including all visual effects.
- **Simple UI**: Buttons to start/pause animation, toggle crisis mode, and record video.

## Requirements
- Python 3.6 or higher
- Libraries:
  - `pygame` (for rendering)
  - `opencv-python` (for video recording)
  - `numpy` (for frame processing)
- A system with a graphical display (e.g., Windows, macOS, Linux with X11)
- Approximately 10 MB of free disk space for video output

## Installation
1. **Install Python**: Ensure Python 3.6+ is installed. Download from [python.org](https://www.python.org/downloads/) if needed.
2. **Install Dependencies**: Run the following command to install required libraries:
   ```bash
   pip install pygame opencv-python numpy

	1.	Download the Code: Save the taiwan_influence_simulation.py file to your project directory.

Usage

	1.	Run the Simulation:
python taiwan_influence_simulation.py

This opens a 700x400 window titled “Taiwan Influence Dynamics Simulation.”
	2.	Interact with the Simulation:
	•	Start/Pause Animation: Click the green/red button to toggle animation (green = paused, red = playing).
	•	Trigger/Stop φ₃ Crisis: Click the blue/orange button to toggle crisis mode, adding vacuum bubbles and pulsing effects around Taiwan.
	•	Record Video (10s): Click the purple button to record a 10-second MP4 video (grayed out during recording). A progress bar shows recording progress.
	•	Stop Recording: If needed, click the button again to stop recording early.
	•	Close the window to exit the simulation.
	3.	Output:
	•	Videos are saved in the project directory with filenames like Taiwan-Influence-Dynamics-2025-05-29_08-32-00.mp4.
	•	Console messages indicate when recording starts and stops.

Visual Elements

	•	Nodes: Circles represent countries (USA: blue, China: orange, Taiwan: green, Japan: red, EU: purple) with sizes based on influence.
	•	Influence Lines: Connect nodes with colors indicating type (blue: support, orange: pressure, green: cooperation, red: competition).
	•	Particles: Small, fading circles move randomly to show dynamic influence flows.
	•	Crisis Effects: In φ₃ Crisis mode, Taiwan’s node pulses, and red vacuum bubbles appear, pulsing in size and opacity.
	•	Recording: Captures all visuals in a 10-second MP4 video at 30 FPS.

Example Workflow

	1.	Run the simulation: python taiwan_influence_simulation.py
	2.	Click “Trigger φ₃ Crisis” to activate crisis effects.
	3.	Click “Record Video (10s)” to capture the animation.
	4.	Wait 10 seconds for the video to save automatically.
	5.	Check the project directory for the MP4 file.

Troubleshooting

	•	No Window Appears:
	•	Ensure you’re running on a system with a graphical interface (not a headless server).
	•	On Linux, try: export SDL_VIDEODRIVER=x11.
	•	Module Not Found:
	•	Verify dependencies are installed: pip show pygame opencv-python numpy.
	•	Use pip3 if pip points to Python 2.
	•	Video Not Saving:
	•	Ensure OpenCV supports MP4 encoding. Install FFmpeg if needed: sudo apt-get install ffmpeg (Linux) or equivalent.
	•	Check for console errors related to mp4v codec.
	•	Font Issues:
	•	If Arial is unavailable, Pygame uses a default font. To change, edit pygame.font.SysFont("Arial", 12, bold=True) to another font (e.g., "freesansbold").
	•	Performance Lag:
	•	Reduce the number of particles in the code (change range(30) to a lower number, e.g., range(15)).
	•	Ensure your system has sufficient CPU/GPU resources.

Notes

	•	The force simulation is simplified compared to D3.js, using basic repulsion and boundary constraints.
	•	Videos are saved in MP4 format for broad compatibility. Use tools like FFmpeg (ffmpeg -i input.mp4 output.gif) to convert to GIF if needed.
	•	For best results, trigger the crisis mode before recording to capture dynamic effects.
	•	The simulation runs at ~30 FPS, but performance may vary based on system resources.

License

This project is provided as-is for educational and research purposes. No official license is specified.

Acknowledgments

	•	Adapted from a React/D3.js implementation to Python using Pygame and OpenCV.
	•	Inspired by geopolitical influence dynamics models, focusing on Taiwan’s strategic context.

For issues or feature requests, please open an issue or contact the maintainer.


### Explanation
- **Purpose**: The README provides a clear, concise guide for users to set up, run, and understand the simulation.
- **Structure**:
  - **Overview**: Describes the project and its features.
  - **Requirements/Installation**: Lists dependencies and setup steps.
  - **Usage**: Explains how to run and interact with the simulation.
  - **Visual Elements**: Details the visual components for user understanding.
  - **Troubleshooting**: Addresses common issues with solutions.
  - **Notes**: Highlights limitations and tips (e.g., simplified force simulation, video conversion).
- **Assumptions**: Assumes users have basic Python knowledge and a graphical environment.
- **File Placement**: Save this as `README.md` in the same directory as `taiwan_influence_simulation.py`.
If you need adjustments (e.g., adding a specific license, including screenshots, or tailoring for a specific audience), let me know!
