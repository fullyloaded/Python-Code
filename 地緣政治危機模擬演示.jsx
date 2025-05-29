import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Play, Pause, RotateCcw, BarChart3, Info } from 'lucide-react';

const GeopoliticalFieldSimulation = () => {
  const svgRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [scenario, setScenario] = useState('normal');
  const [showMetrics, setShowMetrics] = useState(false);
  const [metrics, setMetrics] = useState({
    stability: { us: 0.9, china: 0.9, taiwan: 0.7, others: 0.6 },
    tension: 0.1,
    cooperation: 0.8,
    particleCount: 150
  });

  const scenarios = {
    normal: 'Normal State',
    tradeWar: 'Trade War',
    militaryConflict: 'Military Conflict',
    economicRecession: 'Economic Recession',
    techDecoupling: 'Tech Decoupling',
    pandemic: 'Global Pandemic'
  };

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = 900;
    const height = 700;

    svg.attr('width', width).attr('height', height);
    svg.selectAll('*').remove();

    // Enhanced gradients and effects
    const defs = svg.append('defs');
    
    // Field gradients
    const gradients = [
      { id: 'usGradient', color: '#3b82f6', secondary: '#1e40af', name: 'United States' },
      { id: 'cnGradient', color: '#f59e0b', secondary: '#d97706', name: 'China' },
      { id: 'twGradient', color: '#10b981', secondary: '#059669', name: 'Taiwan' },
      { id: 'otherGradient', color: '#8b5cf6', secondary: '#7c3aed', name: 'International Actors' }
    ];

    gradients.forEach(g => {
      const gradient = defs.append('radialGradient')
        .attr('id', g.id)
        .attr('cx', '50%').attr('cy', '50%').attr('r', '60%');
      gradient.append('stop').attr('offset', '0%').attr('stop-color', g.color).attr('stop-opacity', 0.9);
      gradient.append('stop').attr('offset', '70%').attr('stop-color', g.secondary).attr('stop-opacity', 0.4);
      gradient.append('stop').attr('offset', '100%').attr('stop-color', g.color).attr('stop-opacity', 0.1);
    });

    // Instability gradient
    const instabilityGradient = defs.append('radialGradient')
      .attr('id', 'instabilityGradient')
      .attr('cx', '50%').attr('cy', '50%').attr('r', '50%');
    instabilityGradient.append('stop').attr('offset', '0%').attr('stop-color', '#ef4444').attr('stop-opacity', 0.8);
    instabilityGradient.append('stop').attr('offset', '50%').attr('stop-color', '#f87171').attr('stop-opacity', 0.4);
    instabilityGradient.append('stop').attr('offset', '100%').attr('stop-color', '#fca5a5').attr('stop-opacity', 0.1);

    // Cooperation gradient
    const cooperationGradient = defs.append('radialGradient')
      .attr('id', 'cooperationGradient')
      .attr('cx', '50%').attr('cy', '50%').attr('r', '50%');
    cooperationGradient.append('stop').attr('offset', '0%').attr('stop-color', '#22c55e').attr('stop-opacity', 0.6);
    cooperationGradient.append('stop').attr('offset', '100%').attr('stop-color', '#16a34a').attr('stop-opacity', 0.2);

    // Background field
    svg.append('rect')
      .attr('width', width)
      .attr('height', height)
      .attr('fill', 'url(#backgroundGradient)');

    const backgroundGradient = defs.append('radialGradient')
      .attr('id', 'backgroundGradient')
      .attr('cx', '50%').attr('cy', '50%').attr('r', '80%');
    backgroundGradient.append('stop').attr('offset', '0%').attr('stop-color', '#f8fafc').attr('stop-opacity', 1);
    backgroundGradient.append('stop').attr('offset', '100%').attr('stop-color', '#e2e8f0').attr('stop-opacity', 1);

    // Field definitions with enhanced positioning
    const fields = [
      { id: 'us', x: 180, y: 180, baseRadius: 70, color: '#3b82f6', gradient: 'usGradient', name: 'φ₁ (US)', stability: 0.9 },
      { id: 'cn', x: 720, y: 180, baseRadius: 70, color: '#f59e0b', gradient: 'cnGradient', name: 'φ₂ (China)', stability: 0.9 },
      { id: 'tw', x: 450, y: 120, baseRadius: 85, color: '#10b981', gradient: 'twGradient', name: 'φ₃ (Taiwan)', stability: 0.7 },
      { id: 'other', x: 450, y: 450, baseRadius: 60, color: '#8b5cf6', gradient: 'otherGradient', name: 'φ₄ (Others)', stability: 0.6 }
    ];

    // Field visualization
    const fieldGroup = svg.append('g').attr('class', 'fields');
    
    const fieldCircles = fieldGroup.selectAll('.field')
      .data(fields)
      .enter()
      .append('g')
      .attr('class', 'field');

    // Outer glow effect
    fieldCircles.append('circle')
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('r', d => d.baseRadius + 15)
      .attr('fill', d => d.color)
      .attr('opacity', 0.1)
      .attr('filter', 'blur(8px)');

    // Main field circles
    fieldCircles.append('circle')
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('r', d => d.baseRadius)
      .attr('fill', d => `url(#${d.gradient})`)
      .attr('stroke', d => d.color)
      .attr('stroke-width', 2)
      .attr('filter', 'drop-shadow(0 0 10px rgba(255,255,255,0.1))');

    // Field labels
    fieldCircles.append('text')
      .attr('x', d => d.x)
      .attr('y', d => d.y - d.baseRadius - 20)
      .attr('text-anchor', 'middle')
      .attr('font-size', '14px')
      .attr('font-weight', 'bold')
      .attr('fill', d => d.color)
      .attr('filter', 'drop-shadow(0 0 3px rgba(255,255,255,0.8))')
      .text(d => d.name);

    // Initialize enhanced particles
    let particles = [];
    const createParticles = (count = 150) => {
      particles = [];
      for (let i = 0; i < count; i++) {
        particles.push({
          id: i,
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 3,
          vy: (Math.random() - 0.5) * 3,
          radius: Math.random() * 2 + 1,
          field: Math.floor(Math.random() * 4),
          life: Math.random() * 150,
          energy: Math.random() * 100,
          type: Math.random() > 0.8 ? 'special' : 'normal'
        });
      }
    };
    createParticles();

    const particleGroup = svg.append('g').attr('class', 'particles');
    let vacuumBubbles = [];
    let cooperationFields = [];
    const vacuumGroup = svg.append('g').attr('class', 'vacuum-bubbles');
    const cooperationGroup = svg.append('g').attr('class', 'cooperation-fields');

    const createVacuumBubble = (x, y, intensity = 1) => {
      vacuumBubbles.push({
        x, y,
        radius: 8,
        maxRadius: 120 * intensity,
        intensity,
        life: 0,
        maxLife: 80 + Math.random() * 40
      });
    };

    const createCooperationField = (x, y) => {
      cooperationFields.push({
        x, y,
        radius: 5,
        maxRadius: 80,
        life: 0,
        maxLife: 60
      });
    };

    // Enhanced scenario configurations
    const scenarioConfigs = {
      normal: { 
        stabilities: [0.9, 0.9, 0.7, 0.6], 
        bubbleFrequency: 0, 
        bubbleIntensity: 0, 
        twRepulsion: 0, 
        competitionFactor: 0.015, 
        usOtherCooperation: 0.012, 
        cnOtherCompetition: 0.010,
        cooperationFrequency: 0.02,
        particleCount: 150
      },
      tradeWar: { 
        stabilities: [1.0, 1.0, 0.5, 0.7], 
        bubbleFrequency: 0.05, 
        bubbleIntensity: 1.8, 
        twRepulsion: 0.6, 
        competitionFactor: 0.025, 
        usOtherCooperation: 0.018, 
        cnOtherCompetition: 0.020,
        cooperationFrequency: 0.01,
        particleCount: 180
      },
      militaryConflict: { 
        stabilities: [1.2, 1.1, 0.3, 0.8], 
        bubbleFrequency: 0.08, 
        bubbleIntensity: 2.2, 
        twRepulsion: 0.8, 
        competitionFactor: 0.035, 
        usOtherCooperation: 0.025, 
        cnOtherCompetition: 0.030,
        cooperationFrequency: 0.005,
        particleCount: 200
      },
      economicRecession: { 
        stabilities: [0.6, 0.6, 0.4, 0.4], 
        bubbleFrequency: 0.03, 
        bubbleIntensity: 1.2, 
        twRepulsion: 0.4, 
        competitionFactor: 0.008, 
        usOtherCooperation: 0.008, 
        cnOtherCompetition: 0.008,
        cooperationFrequency: 0.015,
        particleCount: 120
      },
      techDecoupling: { 
        stabilities: [1.3, 0.8, 0.5, 0.9], 
        bubbleFrequency: 0.06, 
        bubbleIntensity: 1.9, 
        twRepulsion: 0.7, 
        competitionFactor: 0.028, 
        usOtherCooperation: 0.022, 
        cnOtherCompetition: 0.018,
        cooperationFrequency: 0.008,
        particleCount: 170
      },
      pandemic: { 
        stabilities: [0.7, 0.8, 0.6, 0.5], 
        bubbleFrequency: 0.04, 
        bubbleIntensity: 1.0, 
        twRepulsion: 0.2, 
        competitionFactor: 0.005, 
        usOtherCooperation: 0.020, 
        cnOtherCompetition: 0.015,
        cooperationFrequency: 0.025,
        particleCount: 100
      }
    };

    let animationId;
    let frameCount = 0;
    
    const tick = () => {
      if (!isPlaying) return;
      frameCount++;

      const config = scenarioConfigs[scenario];
      fields.forEach((f, i) => f.stability = config.stabilities[i]);

      // Adjust particle count if needed
      if (particles.length !== config.particleCount) {
        createParticles(config.particleCount);
      }

      let totalTension = 0;
      let totalCooperation = 0;

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        
        // Boundary conditions with damping
        if (p.x < 10) { p.x = 10; p.vx *= -0.8; }
        if (p.x > width - 10) { p.x = width - 10; p.vx *= -0.8; }
        if (p.y < 10) { p.y = 10; p.vy *= -0.8; }
        if (p.y > height - 10) { p.y = height - 10; p.vy *= -0.8; }

        // Field interactions
        fields.forEach((field, index) => {
          const dx = field.x - p.x;
          const dy = field.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          
          if (dist < field.baseRadius * 2.5) {
            const force = (field.stability * 0.025) / (dist + 1);
            p.vx += dx * force;
            p.vy += dy * force;
            p.energy += force * 10;
          }

          // US-China competition
          if (index === 0 || index === 1) {
            const otherField = fields[index === 0 ? 1 : 0];
            const odx = otherField.x - p.x;
            const ody = otherField.y - p.y;
            const odist = Math.sqrt(odx * odx + ody * ody);
            const competitionForce = config.competitionFactor / (odist + 1);
            p.vx -= odx * competitionForce;
            p.vy -= ody * competitionForce;
            totalTension += competitionForce;
          }

          // US-Others cooperation
          if (index === 0) {
            const other = fields[3];
            const odx = other.x - p.x;
            const ody = other.y - p.y;
            const odist = Math.sqrt(odx * odx + ody * ody);
            const coop = config.usOtherCooperation / (odist + 1);
            p.vx += odx * coop;
            p.vy += ody * coop;
            totalCooperation += coop;
            
            if (Math.random() < config.cooperationFrequency) {
              createCooperationField(p.x, p.y);
            }
          }

          // China-Others competition
          if (index === 1) {
            const other = fields[3];
            const odx = other.x - p.x;
            const ody = other.y - p.y;
            const odist = Math.sqrt(odx * odx + ody * ody);
            const comp = config.cnOtherCompetition / (odist + 1);
            p.vx -= odx * comp;
            p.vy -= ody * comp;
            totalTension += comp;
          }

          // Taiwan instability effects
          if (scenario !== 'normal' && index === 2 && dist < field.baseRadius * 3) {
            const repulsion = config.twRepulsion / (dist + 1);
            p.vx -= dx * repulsion;
            p.vy -= dy * repulsion;
            
            if (Math.random() < config.bubbleFrequency) {
              createVacuumBubble(p.x, p.y, config.bubbleIntensity);
            }
          }
        });

        // Energy dissipation
        p.vx *= 0.995;
        p.vy *= 0.995;
        p.energy *= 0.98;

        p.life++;
        if (p.life > 250) {
          p.life = 0;
          p.x = Math.random() * width;
          p.y = Math.random() * height;
          p.field = Math.floor(Math.random() * 4);
          p.energy = Math.random() * 100;
        }
      });

      // Update vacuum bubbles
      vacuumBubbles.forEach(bubble => {
        bubble.life++;
        bubble.radius = (bubble.life / bubble.maxLife) * bubble.maxRadius;
      });
      vacuumBubbles = vacuumBubbles.filter(b => b.life < b.maxLife);

      // Update cooperation fields
      cooperationFields.forEach(field => {
        field.life++;
        field.radius = Math.sin((field.life / field.maxLife) * Math.PI) * field.maxRadius;
      });
      cooperationFields = cooperationFields.filter(f => f.life < f.maxLife);

      // Update metrics
      if (frameCount % 30 === 0) {
        setMetrics({
          stability: {
            us: config.stabilities[0],
            china: config.stabilities[1],
            taiwan: config.stabilities[2],
            others: config.stabilities[3]
          },
          tension: Math.min(totalTension / particles.length * 1000, 1),
          cooperation: Math.min(totalCooperation / particles.length * 1000, 1),
          particleCount: particles.length
        });
      }

      // Render particles with enhanced effects
      const ps = particleGroup.selectAll('.particle')
        .data(particles, d => d.id);
      
      ps.enter()
        .append('circle')
        .attr('class', 'particle')
        .merge(ps)
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .attr('r', d => d.radius + (d.energy > 50 ? 1 : 0))
        .attr('fill', d => {
          if (d.type === 'special') return '#fbbf24';
          if (d.energy > 80) return '#f87171';
          if (d.energy > 50) return '#60a5fa';
          return '#6b7280';
        })
        .attr('opacity', d => Math.max(0.4, Math.min(1, d.energy / 100)));
      
      ps.exit().remove();

      // Render vacuum bubbles
      const vs = vacuumGroup.selectAll('.bubble')
        .data(vacuumBubbles);
      vs.enter()
        .append('circle')
        .attr('class', 'bubble')
        .attr('fill', 'url(#instabilityGradient)')
        .merge(vs)
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .attr('r', d => d.radius)
        .attr('opacity', d => 1 - (d.life / d.maxLife));
      vs.exit().remove();

      // Render cooperation fields
      const cs = cooperationGroup.selectAll('.cooperation')
        .data(cooperationFields);
      cs.enter()
        .append('circle')
        .attr('class', 'cooperation')
        .attr('fill', 'url(#cooperationGradient)')
        .merge(cs)
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .attr('r', d => d.radius)
        .attr('opacity', d => Math.sin((d.life / d.maxLife) * Math.PI) * 0.6);
      cs.exit().remove();

      animationId = requestAnimationFrame(tick);
    };

    tick();

    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    };
  }, [isPlaying, scenario]);

  const handleReset = () => {
    setScenario('normal');
    setIsPlaying(true);
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6 bg-white text-gray-800 rounded-xl shadow-2xl border border-gray-200">
      <div className="mb-6">
        <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Geopolitical Quantum Field Theory Simulation
        </h1>
        <p className="text-gray-600 text-sm">
          Advanced visualization of field interactions and particle dynamics under various geopolitical scenarios
        </p>
      </div>

      <div className="mb-4 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex gap-2">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-200 shadow-lg hover:shadow-blue-500/25"
          >
            {isPlaying ? <Pause size={16} /> : <Play size={16} />}
            {isPlaying ? 'Pause' : 'Play'}
          </button>
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-all duration-200 shadow-lg"
          >
            <RotateCcw size={16} />
            Reset
          </button>
          <button
            onClick={() => setShowMetrics(!showMetrics)}
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-all duration-200 shadow-lg"
          >
            <BarChart3 size={16} />
            Metrics
          </button>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-600">Scenario:</label>
          <select
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            className="px-3 py-2 bg-white text-gray-800 rounded-lg border border-gray-300 focus:border-blue-500 focus:outline-none transition-colors"
          >
            {Object.entries(scenarios).map(([key, label]) => (
              <option key={key} value={key}>{label}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-4">
        <div className="lg:col-span-3">
          <div className="relative bg-white rounded-lg overflow-hidden shadow-lg border-2 border-gray-200">
            <svg ref={svgRef} className="w-full h-auto"></svg>
          </div>
        </div>
        
        {showMetrics && (
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-300 shadow-sm">
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2 text-gray-800">
              <BarChart3 size={18} />
              Live Metrics
            </h3>
            <div className="space-y-3 text-sm">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-700">Global Tension</span>
                  <span className="text-gray-800">{(metrics.tension * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-red-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${metrics.tension * 100}%` }}
                  ></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-700">Cooperation Index</span>
                  <span className="text-gray-800">{(metrics.cooperation * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${metrics.cooperation * 100}%` }}
                  ></div>
                </div>
              </div>
              <div className="pt-2 border-t border-gray-300">
                <div className="text-xs text-gray-500 mb-2">Field Stability</div>
                <div className="space-y-1 text-gray-700">
                  <div className="flex justify-between">
                    <span className="text-blue-600">US</span>
                    <span>{metrics.stability.us.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-orange-600">China</span>
                    <span>{metrics.stability.china.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-600">Taiwan</span>
                    <span>{metrics.stability.taiwan.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-purple-600">Others</span>
                    <span>{metrics.stability.others.toFixed(2)}</span>
                  </div>
                </div>
              </div>
              <div className="pt-2 border-t border-gray-300">
                <div className="flex justify-between text-xs text-gray-600">
                  <span>Active Particles</span>
                  <span>{metrics.particleCount}</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-4 h-4 rounded-full bg-blue-500 shadow-lg shadow-blue-500/50"></div>
            <span className="font-semibold text-blue-700">φ₁ (United States)</span>
          </div>
          <p className="text-gray-600 text-xs leading-relaxed">
            High stability field with cooperative tendencies towards international actors. Exhibits strong field coherence and particle attraction.
          </p>
        </div>
        
        <div className="bg-orange-50 p-4 rounded-lg border border-orange-200 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-4 h-4 rounded-full bg-orange-500 shadow-lg shadow-orange-500/50"></div>
            <span className="font-semibold text-orange-700">φ₂ (China)</span>
          </div>
          <p className="text-gray-600 text-xs leading-relaxed">
            Robust stability with competitive dynamics. Shows strong field strength and selective particle interactions based on strategic interests.
          </p>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg border border-green-200 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-4 h-4 rounded-full bg-green-500 shadow-lg shadow-green-500/50"></div>
            <span className="font-semibold text-green-700">φ₃ (Taiwan)</span>
          </div>
          <p className="text-gray-600 text-xs leading-relaxed">
            Medium stability with high susceptibility to external field fluctuations. Generates instability bubbles under stress conditions.
          </p>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-4 h-4 rounded-full bg-purple-500 shadow-lg shadow-purple-500/50"></div>
            <span className="font-semibold text-purple-700">φ₄ (International)</span>
          </div>
          <p className="text-gray-600 text-xs leading-relaxed">
            Variable stability influenced by major power dynamics. Responds to both cooperative and competitive field interactions.
          </p>
        </div>
      </div>

      <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-300 shadow-sm">
        <div className="flex items-start gap-2">
          <Info size={16} className="text-blue-600 mt-0.5 flex-shrink-0" />
          <div className="text-xs text-gray-600 leading-relaxed">
            <strong className="text-gray-800">Simulation Theory:</strong> This model applies quantum field theory concepts to geopolitical dynamics. 
            Particles represent policy decisions, trade flows, and diplomatic interactions. Field strength correlates with national power and stability. 
            Vacuum bubbles indicate regional instability, while cooperation fields show positive-sum interactions. 
            Different scenarios modify field parameters to simulate real-world conditions and their effects on international relations.
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeopoliticalFieldSimulation;
