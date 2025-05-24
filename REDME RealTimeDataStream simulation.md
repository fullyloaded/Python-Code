# Real-Time Data Simulation and Influence Dynamics Visualization

This repository contains two Python scripts for visualizing dynamic data simulations:
1. **`influence_animation.py`**: Generates an animated bar chart showing the evolving influence of the US, China, and First Island Chain countries (Taiwan, Japan, Philippines, South Korea) from 2025 to 2027.
2. **`realtime_simulation.py`**: Simulates a real-time data stream with a simple AI model, displaying Data, Prediction, and Field State as dynamic line plots.

Both scripts use Matplotlib for visualization and produce MP4 animations, based on data simulations as of May 24, 2025, 15:33 CST.

## Features

### Influence Animation (`influence_animation.py`)
- **Purpose**: Visualizes the influence strength (0-10) of six countries (USA, China, Taiwan, Japan, Philippines, South Korea) over 2025–2027.
- **Data**: Quarterly interpolated data (12 time points, from 2025.01 to 2027.10), derived from hypothetical field equations (□ φ_I + m_I² φ_I = k_AI φ_A - k_CI φ_C).
- **Output**: A 6-second MP4 (`influence_evolution.mp4`) with animated bar charts, showing influence changes per quarter.
- **Visualization**:
  - Bars are spaced for clarity (width=0.12, gap=0.02).
  - Colors: USA (blue), China (red), Taiwan (green), Japan (yellow), Philippines (purple), South Korea (orange).
  - Time labels in `YYYY.MM` format (e.g., `2025.01`).
  - White background, DejaVu Sans font to avoid glyph errors.

### Real-Time Data Simulation (`realtime_simulation.py`)
- **Purpose**: Simulates a real-time data stream with a simple AI model predicting values and a predictive field updating its state.
- **Data**: Simulated sinusoidal data with random noise, processed over 100 steps.
- **Output**: A 6-second MP4 (`realtime_simulation.mp4`) with animated line plots, plus a live plot display during execution.
- **Visualization**:
  - Three lines: Data (blue), Prediction (red), Field State (green).
  - Dynamic X-axis window slides after 50 steps for recent data focus.
  - White background, grid, and legend for clarity.

## Prerequisites

- **Python**:**: Python 3.x
- **Required Libraries**:
  - `numpy`: For numerical computations (`pip install numpy`)
  - `matplotlib`: For plotting and animation (`pip install matplotlib`)
- **FFmpeg**: For MP4 output.
  - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH.
  - **Mac**: `brew install ffmpeg`
  - **Linux**: `sudo apt-get install ffmpeg`
- **Optional**: Pillow for GIF output (`pip install Pillow`) if FFmpeg is unavailable.

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
