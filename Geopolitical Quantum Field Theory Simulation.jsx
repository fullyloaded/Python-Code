import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Play, Pause, RotateCcw } from 'lucide-react';

const GeopoliticalFieldSimulation = () => {
  const svgRef = useRef(null);
  const canvasRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [scenario, setScenario] = useState('normal');

  const scenarios = {
    normal: 'Normal State',
    tradeWar: 'Trade War',
    militaryConflict: 'Military Conflict',
    economicRecession: 'Economic Recession',
    techDecoupling: 'Tech Decoupling'
  };

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 600;

    // 設置 Canvas（錄影用途）
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.width = width;
      canvas.height = height;
      canvas.style.display = 'none';
    }
    svg.attr('width', width).attr('height', height);
    svg.selectAll('*').remove();

    // 定義漸層
    const defs = svg.append('defs');
    const gradients = [
      { id: 'usGradient', color: '#1f77b4', name: 'United States' },
      { id: 'cnGradient', color: '#ff7f0e', name: 'China' },
      { id: 'twGradient', color: '#2ca02c', name: 'Taiwan' },
      { id: 'otherGradient', color: '#d62728', name: 'Other International Actors' }
    ];
    gradients.forEach(g => {
      const gradient = defs.append('radialGradient')
        .attr('id', g.id)
        .attr('cx', '50%').attr('cy', '50%').attr('r', '50%');
      gradient.append('stop').attr('offset', '0%').attr('stop-color', g.color).attr('stop-opacity', 0.8);
      gradient.append('stop').attr('offset', '100%').attr('stop-color', g.color).attr('stop-opacity', 0.2);
    });

    const instabilityGradient = defs.append('radialGradient')
      .attr('id', 'instabilityGradient')
      .attr('cx', '50%').attr('cy', '50%').attr('r', '50%');
    instabilityGradient.append('stop').attr('offset', '0%').attr('stop-color', '#ff0000').attr('stop-opacity', 0.9);
    instabilityGradient.append('stop').attr('offset', '100%').attr('stop-color', '#ff6666').attr('stop-opacity', 0.3);

    // 領域定義
    const fields = [
      { id: 'us', x: 200, y: 150, baseRadius: 60, color: '#1f77b4', gradient: 'usGradient', name: 'φ₁ (US)', stability: 0.9 },
      { id: 'cn', x: 600, y: 150, baseRadius: 60, color: '#ff7f0e', gradient: 'cnGradient', name: 'φ₂ (China)', stability: 0.9 },
      { id: 'tw', x: 400, y: 100, baseRadius: 80, color: '#2ca02c', gradient: 'twGradient', name: 'φ₃ (Taiwan)', stability: 0.7 },
      { id: 'other', x: 400, y: 350, baseRadius: 50, color: '#d62728', gradient: 'otherGradient', name: 'φ₄ (Others)', stability: 0.6 }
    ];

    // 領域圖形
    const fieldCircles = svg.selectAll('.field')
      .data(fields)
      .enter()
      .append('g')
      .attr('class', 'field');

    fieldCircles.append('circle')
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('r', d => d.baseRadius)
      .attr('fill', d => `url(#${d.gradient})`)
      .attr('stroke', d => d.color)
      .attr('stroke-width', 2);

    fieldCircles.append('text')
      .attr('x', d => d.x)
      .attr('y', d => d.y - d.baseRadius - 10)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('font-weight', 'bold')
      .attr('fill', d => d.color)
      .text(d => d.name);

    // 初始化粒子
    let particles = [];
    const createParticles = () => {
      particles = [];
      for (let i = 0; i < 100; i++) {
        particles.push({
          id: i,
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          radius: Math.random() * 3 + 1,
          field: Math.floor(Math.random() * 4),
          life: Math.random() * 100
        });
      }
    };
    createParticles();

    const particleGroup = svg.append('g').attr('class', 'particles');
    let vacuumBubbles = [];
    const vacuumGroup = svg.append('g').attr('class', 'vacuum-bubbles');

    const createVacuumBubble = (x, y, intensity = 1) => {
      vacuumBubbles.push({
        x, y,
        radius: 5,
        maxRadius: 100 * intensity,
        intensity,
        life: 0,
        maxLife: 100
      });
    };

    // 情境設定
    const scenarioConfigs = {
      normal: { stabilities: [0.9, 0.9, 0.7, 0.6], bubbleFrequency: 0, bubbleIntensity: 0, twRepulsion: 0, competitionFactor: 0.015, usOtherCooperation: 0.01, cnOtherCompetition: 0.01 },
      tradeWar: { stabilities: [1.0, 1.0, 0.5, 0.7], bubbleFrequency: 0.04, bubbleIntensity: 1.5, twRepulsion: 0.5, competitionFactor: 0.02, usOtherCooperation: 0.015, cnOtherCompetition: 0.015 },
      militaryConflict: { stabilities: [1.1, 1.0, 0.3, 0.7], bubbleFrequency: 0.06, bubbleIntensity: 1.8, twRepulsion: 0.6, competitionFactor: 0.025, usOtherCooperation: 0.02, cnOtherCompetition: 0.02 },
      economicRecession: { stabilities: [0.7, 0.7, 0.4, 0.5], bubbleFrequency: 0.02, bubbleIntensity: 1.0, twRepulsion: 0.3, competitionFactor: 0.01, usOtherCooperation: 0.005, cnOtherCompetition: 0.005 },
      techDecoupling: { stabilities: [1.2, 0.7, 0.5, 0.8], bubbleFrequency: 0.04, bubbleIntensity: 1.5, twRepulsion: 0.5, competitionFactor: 0.02, usOtherCooperation: 0.02, cnOtherCompetition: 0.015 }
    };

    let animationId;
    const tick = () => {
      if (!isPlaying) return;

      const config = scenarioConfigs[scenario];
      fields.forEach((f, i) => f.stability = config.stabilities[i]);

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        fields.forEach((field, index) => {
          const dx = field.x - p.x;
          const dy = field.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < field.baseRadius * 2) {
            const force = (field.stability * 0.02) / (dist + 1);
            p.vx += dx * force;
            p.vy += dy * force;
          }

          if (index === 0 || index === 1) {
            const otherField = fields[index === 0 ? 1 : 0];
            const odx = otherField.x - p.x;
            const ody = otherField.y - p.y;
            const odist = Math.sqrt(odx * odx + ody * ody);
            const competitionForce = config.competitionFactor / (odist + 1);
            p.vx -= odx * competitionForce;
            p.vy -= ody * competitionForce;
          }

          if (index === 0) {
            const other = fields[3];
            const odx = other.x - p.x;
            const ody = other.y - p.y;
            const odist = Math.sqrt(odx * odx + ody * ody);
            const coop = config.usOtherCooperation / (odist + 1);
            p.vx += odx * coop;
            p.vy += ody * coop;
          }

          if (index === 1) {
            const other = fields[3];
            const odx = other.x - p.x;
            const ody = other.y - p.y;
            const odist = Math.sqrt(odx * odx + ody * ody);
            const comp = config.cnOtherCompetition / (odist + 1);
            p.vx -= odx * comp;
            p.vy -= ody * comp;
          }

          if (scenario !== 'normal' && index === 2 && dist < field.baseRadius * 3) {
            const repulsion = config.twRepulsion / (dist + 1);
            p.vx -= dx * repulsion;
            p.vy -= dy * repulsion;
            if (Math.random() < config.bubbleFrequency) {
              createVacuumBubble(p.x, p.y, config.bubbleIntensity);
            }
          }
        });

        p.life++;
        if (p.life > 200) {
          p.life = 0;
          p.x = Math.random() * width;
          p.y = Math.random() * height;
          p.field = Math.floor(Math.random() * 4);
        }
      });

      vacuumBubbles.forEach(bubble => {
        bubble.life++;
        bubble.radius = (bubble.life / bubble.maxLife) * bubble.maxRadius;
      });
      vacuumBubbles = vacuumBubbles.filter(b => b.life < b.maxLife);

      // 畫出粒子
      const ps = particleGroup.selectAll('.particle')
        .data(particles, d => d.id);
      ps.enter()
        .append('circle')
        .attr('class', 'particle')
        .attr('r', d => d.radius)
        .attr('fill', '#ccc')
        .merge(ps)
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
      ps.exit().remove();

      // 畫出真空泡泡
      const vs = vacuumGroup.selectAll('.bubble')
        .data(vacuumBubbles);
      vs.enter()
        .append('circle')
        .attr('class', 'bubble')
        .attr('fill', 'url(#instabilityGradient)')
        .merge(vs)
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .attr('r', d => d.radius);
      vs.exit().remove();

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
    <div className="w-full max-w-6xl mx-auto p-6 bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white rounded-xl shadow-2xl">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          Geopolitical Quantum Field Theory Simulation
        </h1>
        <p className="text-gray-300 text-sm">
          Observe field interactions and particle dynamics under different geopolitical scenarios
        </p>
      </div>

      <div className="mb-4 flex flex-wrap gap-4 items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          >
            {isPlaying ? <Pause size={16} /> : <Play size={16} />}
            {isPlaying ? 'Pause' : 'Play'}
          </button>
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <RotateCcw size={16} />
            Reset
          </button>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-300">Scenario:</label>
          <select
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            className="px-3 py-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
          >
            {Object.entries(scenarios).map(([key, label]) => (
              <option key={key} value={key}>{label}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="relative bg-black rounded-lg overflow-hidden shadow-inner">
        <svg ref={svgRef} className="w-full h-auto border border-gray-700"></svg>
        <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
        <div className="bg-blue-900/30 p-3 rounded-lg border border-blue-500/30">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="font-semibold">φ₁ (US)</span>
          </div>
          <p className="text-gray-300 text-xs">High stability, cooperates with other international actors</p>
        </div>
        
        <div className="bg-orange-900/30 p-3 rounded-lg border border-orange-500/30">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span className="font-semibold">φ₂ (China)</span>
          </div>
          <p className="text-gray-300 text-xs">High stability, competes with other international actors</p>
        </div>
        
        <div className="bg-green-900/30 p-3 rounded-lg border border-green-500/30">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="font-semibold">φ₃ (Taiwan)</span>
          </div>
          <p className="text-gray-300 text-xs">Medium stability, influenced by external factors</p>
        </div>
        
        <div className="bg-red-900/30 p-3 rounded-lg border border-red-500/30">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="font-semibold">φ₄ (Others)</span>
          </div>
          <p className="text-gray-300 text-xs">Lower stability, affected by major power policies</p>
        </div>
      </div>
    </div>
  );
};

export default GeopoliticalFieldSimulation;
