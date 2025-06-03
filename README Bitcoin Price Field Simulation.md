# Bitcoin Price Field Simulation

This project simulates Bitcoin price dynamics using the **Klein-Gordon equation**, a partial differential equation that models wave propagation with a mass term. Integrated with sample Bitcoin price data from May 1, 2025, to June 3, 2025, the simulation visualizes price evolution as a field over time and market sentiment, comparing theoretical predictions with real-world data.

## Features
- **Klein-Gordon Model**: Simulates Bitcoin price as a field \( P(t, x) \) using the equation:
  \[
  \frac{\partial^2 P}{\partial t^2} - c^2 \frac{\partial^2 P}{\partial x^2} + m^2 P = J(t, x)
  \]
  where \( t \) is time, \( x \) is market sentiment (0 to 1), and \( J(t, x) \) is a source term driven by real price changes or sinusoidal oscillation.
- **Visualizations**:
  - **3D Surface Plot**: Displays price field evolution over time and market sentiment.
  - **Heatmap**: Highlights high-price regions (> $110,000) with a marker for the peak price ($112,500 on May 22, 2025).
  - **Comparison Plot**: Compares simulated prices (red line) with real Bitcoin prices (yellow line).
  - **Real Data Plot**: Shows sample Bitcoin price data from May-June 2025.
- **Interactive Controls**:
  - Adjust parameters like wave speed (\( c \)), mass (\( m \)), source strength (\( A \)), and initial price (\( P_0 \)).
  - Auto-fit parameters to match real data volatility and trends.
  - Load sample data or paste custom CSV data (Date, Price format).
- **Responsive Design**: Built with HTML, JavaScript, and Plotly.js, optimized for desktop and mobile browsers.
- **Optimized Layout**: Heatmap adjusted for clear label spacing, with increased margins and title standoffs.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/bitcoin-price-simulation.git
   cd bitcoin-price-simulation
   ```
2. **Serve the Application**:
   - Use a local web server to avoid CORS issues with local files.
   - Install Python (if not already installed) and run:
     ```bash
     python -m http.server 8000
     ```
   - Alternatively, use Node.js with `http-server`:
     ```bash
     npm install -g http-server
     http-server
     ```
3. **Access the Application**:
   - Open your browser and navigate to `http://localhost:8000/bitcoin_price_simulation.html`.

## Usage
1. **Load Data**:
   - Click **"Load Sample Data"** to populate the textarea with sample Bitcoin prices (May 1, 2025, to June 3, 2025).
   - Optionally, paste custom CSV data in the format:
     ```
     Date,Price
     2025-05-01,95000
     2025-05-02,97200
     ...
     ```
   - Click **"Fetch Live Data"** for a simulated API call (currently enhances sample data with random noise).
2. **Adjust Parameters**:
   - Use sliders to modify:
     - **Wave Speed (c)**: Controls wave propagation speed (default: 0.3).
     - **Mass Parameter (m)**: Influences damping (default: 0.3).
     - **Source Strength (A)**: Amplifies source term (default: 2500).
     - **Oscillation Frequency**: Sets source oscillation rate (default: 0.8).
     - **Initial Price**: Starting price level (default: $105,000).
     - **Resolution**: Grid points for simulation (default: 100).
   - Click **"Auto-Fit to Real Data"** to optimize parameters based on data volatility.
   - Click **"Reset Parameters"** to revert to defaults.
3. **Run Simulation**:
   - Click **"Run Simulation"** to generate 3D surface, heatmap, and real data plots.
   - The heatmap marks the high-price region ($112,500 on May 22, 2025) with white contours.
4. **Compare with Real Data**:
   - Click **"Compare with Real Data"** to plot simulated prices (red line) against real prices (yellow line).
   - The red line should oscillate, reflecting source term dynamics and real price trends.

## Project Structure
```
bitcoin-price-simulation/
├── bitcoin_price_simulation.html  # Main application file (HTML, CSS, JS)
└── README.md                      # Project documentation
```
- **bitcoin_price_simulation.html**:
  - **HTML**: Defines the UI with data input, controls, and plot containers.
  - **CSS**: Styles the interface with a modern gradient background and responsive layout.
  - **JavaScript**:
    - **Initialization**: Sets up sliders and loads sample data.
    - **Data Handling**: Parses CSV, loads sample data, and simulates API calls.
    - **Simulation**: Implements Klein-Gordon equation with finite differences.
    - **Plotting**: Uses Plotly.js for 3D surface, heatmap, comparison, and real data plots.
    - **Stats**: Displays max, min, average price, volatility, and RMSE.

## Key Modifications
- **Source Term**: Combines sinusoidal oscillation with normalized real price changes to ensure oscillatory behavior in the comparison plot’s red line.
- **Parameters**: Adjusted defaults (\( c = 0.3 \), \( m = 0.3 \), \( A = 2500 \), \( P_0 = 105,000 \)) to promote price oscillations.
- **Heatmap Layout**: Increased left margin (`margin.l: 100`), y-axis title standoff (`title_standoff: 30`), and colorbar position (`colorbar.x: 1.2`) for clear label spacing.
- **Numerical Stability**: Increased time steps (`Nt = realBitcoinData.length * 20`) to reduce \( \Delta t \), improving simulation accuracy.

## Known Issues
- **Simulated API**: The "Fetch Live Data" button adds random noise to sample data instead of calling a real API.
- **Numerical Stability**: High wave speed (\( c > 0.5 \)) or low resolution (\( Nx < 50 \)) may cause instability.
- **Comparison Plot**: Simulated prices may not perfectly match real data due to simplified source term modeling.

## Future Improvements
- **Real API Integration**: Connect to CoinGecko or Binance API for live Bitcoin price data.
- **Nonlinear Terms**: Add terms like \( \lambda P^3 \) to model market bubbles or crashes.
- **Dynamic Source Term**: Use Fourier analysis to extract frequency components from real data for a multi-frequency source.
- **Enhanced Auto-Fit**: Implement optimization algorithms (e.g., gradient descent) to minimize RMSE between simulated and real prices.
- **Interactive Annotations**: Allow users to click on the heatmap to add custom price markers.

## Dependencies
- **Plotly.js** (v2.18.0): Loaded via CDN for data visualization.
- No additional libraries required; runs in modern browsers (Chrome, Firefox, Edge).

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

