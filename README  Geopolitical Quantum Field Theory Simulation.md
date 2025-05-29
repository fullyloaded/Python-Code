# Geopolitical Quantum Field Theory Simulation

A sophisticated React-based interactive visualization that applies quantum field theory principles to geopolitical dynamics, demonstrating how different international actors interact under various global scenarios.

## 🌟 Overview

This simulation models international relations through the lens of quantum field theory, where:
- **Quantum Fields** represent geopolitical actors (US, China, Taiwan, Other International Actors)
- **Particles** represent political influence, economic ties, or information flow
- **Field Interactions** simulate cooperation, competition, and conflict dynamics
- **Vacuum Bubbles** represent instability and crisis points

## 🚀 Features

### Interactive Controls
- **Play/Pause**: Control simulation execution
- **Reset**: Return to normal state scenario
- **Scenario Selection**: Switch between different geopolitical contexts

### Simulation Scenarios
1. **Normal State**: Baseline international relations with standard cooperation/competition
2. **Trade War**: Economic tensions with increased competition factors
3. **Military Conflict**: High tension scenario with maximum field repulsion
4. **Economic Recession**: Global economic downturn affecting all actors
5. **Tech Decoupling**: Technology separation creating new interaction patterns

### Visual Elements
- **Gradient Fields**: Radial gradients representing influence zones
- **Dynamic Particles**: 100+ particles following physics-based movement
- **Vacuum Bubbles**: Red instability zones that expand and dissipate
- **Real-time Animation**: Smooth 60fps rendering with requestAnimationFrame

## 🔬 Physics Model

### Field Definitions
- **φ₁ (United States)**: High stability field with cooperative tendencies toward other international actors
- **φ₂ (China)**: High stability field with competitive dynamics
- **φ₃ (Taiwan)**: Medium stability field, highly influenced by external pressures
- **φ₄ (Other International Actors)**: Lower stability field affected by major power policies

### Force Calculations
```javascript
// Attraction force within field radius
const force = (field.stability * 0.02) / (distance + 1);

// Competition between US and China
const competitionForce = config.competitionFactor / (distance + 1);

// US-Others cooperation
const cooperationForce = config.usOtherCooperation / (distance + 1);

// Taiwan repulsion during crisis scenarios
const repulsionForce = config.twRepulsion / (distance + 1);
```

### Scenario Parameters
Each scenario modifies key parameters:
- **Field Stability**: Individual stability coefficients for each actor
- **Bubble Frequency**: Rate of instability zone creation
- **Bubble Intensity**: Size and impact of vacuum bubbles
- **Interaction Factors**: Competition, cooperation, and repulsion strengths

## 🛠️ Technical Implementation

### Built With
- **React 18+**: Component-based architecture with hooks
- **D3.js**: Data visualization and SVG manipulation
- **Tailwind CSS**: Utility-first styling framework
- **Lucide React**: Modern icon components

### Key Components
- **useEffect Hook**: Manages D3 lifecycle and animation loop
- **SVG Rendering**: Scalable vector graphics for smooth visualization
- **Canvas Support**: Hidden canvas element for potential recording features
- **State Management**: React useState for simulation controls

### Performance Optimizations
- **Efficient Particle Updates**: Optimized physics calculations
- **Smart DOM Updates**: D3's data binding for minimal re-renders
- **Animation Frame**: Browser-optimized animation timing
- **Memory Management**: Proper cleanup of animation frames

## 📦 Installation & Setup

### Prerequisites
- Node.js 16+ and npm/yarn
- Modern web browser with ES6+ support

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd geopolitical-simulation

# Install dependencies
npm install
# or
yarn install

# Start development server
npm start
# or
yarn start
```

### Dependencies
```json
{
  "react": "^18.0.0",
  "d3": "^7.0.0",
  "lucide-react": "^0.263.1",
  "tailwindcss": "^3.0.0"
}
```

## 🎮 Usage Guide

### Basic Controls
1. **Start/Stop**: Use the Play/Pause button to control animation
2. **Reset**: Return to normal state at any time
3. **Scenario Selection**: Choose from dropdown to see different dynamics

### Observation Points
- Watch particle clustering around stable fields (US, China)
- Notice Taiwan's volatility during crisis scenarios
- Observe vacuum bubble formation during instability
- Monitor cooperation vs. competition dynamics

### Educational Applications
- **International Relations**: Visualize power dynamics and influence
- **Complexity Theory**: Understand emergent behaviors in complex systems
- **Physics Education**: Demonstrate field theory concepts
- **Policy Analysis**: Model scenario outcomes and system stability

## 🔍 Scenario Analysis

### Normal State
- Balanced field interactions
- Moderate particle movement
- Stable system equilibrium
- No vacuum bubble formation

### Trade War
- Increased US-China repulsion
- Taiwan field destabilization
- Enhanced competition factors
- Moderate instability bubbles

### Military Conflict
- Maximum field tensions
- High Taiwan repulsion
- Frequent vacuum bubbles
- System-wide instability

### Economic Recession
- Reduced overall stability
- Weakened cooperation
- Global field contraction
- Scattered instability

### Tech Decoupling
- US field enhancement
- China field weakening
- Modified interaction patterns
- Strategic realignment visualization

## 🎨 Visual Design

### Color Scheme
- **US Field**: Blue (#1f77b4) - Trust and stability
- **China Field**: Orange (#ff7f0e) - Energy and ambition  
- **Taiwan Field**: Green (#2ca02c) - Growth and vulnerability
- **Others Field**: Red (#d62728) - Complexity and risk
- **Instability**: Red gradient - Danger and crisis

### Animation Features
- Smooth particle trajectories
- Dynamic field pulsing
- Expanding instability zones
- Responsive hover effects
- Modern glassmorphism UI

## 🔬 Research Applications

This simulation can be used for:
- **Academic Research**: Model testing in international relations
- **Policy Simulation**: Scenario planning and outcome prediction
- **Educational Tool**: Teaching complex systems and field theory
- **Data Visualization**: Representing multi-dimensional geopolitical data

## 🤝 Contributing

### Development Guidelines
1. Follow React best practices
2. Maintain D3.js integration patterns
3. Ensure responsive design compatibility
4. Add comprehensive JSDoc comments
5. Include unit tests for new features

### Feature Requests
- Additional geopolitical scenarios
- More sophisticated physics models
- Data export capabilities
- Historical scenario replay
- Multi-language support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Quantum field theory concepts adapted from theoretical physics
- Geopolitical modeling inspired by international relations theory
- D3.js community for visualization techniques
- React community for component patterns

## 📊 Technical Specifications

### Performance Metrics
- **Frame Rate**: 60 FPS target
- **Particle Count**: 100 active particles
- **Field Calculations**: ~400 force computations per frame
- **Memory Usage**: <50MB typical
- **Browser Support**: Chrome 80+, Firefox 75+, Safari 13+

### Browser Compatibility
- Modern browsers with ES6+ support
- SVG 2.0 and Canvas API support
- requestAnimationFrame support
- CSS Grid and Flexbox support

---

**Note**: This simulation is for educational and research purposes. Real geopolitical dynamics involve numerous factors not captured in this simplified model.
