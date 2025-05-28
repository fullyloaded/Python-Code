import React, { useState, useRef, useEffect } from 'react';
import * as d3 from 'd3';

const TaiwanInfluenceSimulation = () => {
  const svgRef = useRef();
  const canvasRef = useRef();
  const [isPlaying, setIsPlaying] = useState(false);
  const [crisis, setCrisis] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingProgress, setRecordingProgress] = useState(0);
  const mediaRecorderRef = useRef();
  const recordedChunksRef = useRef([]);

  // Node data for countries/actors
  const nodes = [
    { id: '美國', x: 120, y: 200, color: '#3B82F6', size: 35, influence: 0.8 },
    { id: '中國', x: 580, y: 200, color: '#F97316', size: 35, influence: 0.9 },
    { id: '台灣', x: 350, y: 250, color: '#10B981', size: 30, influence: 0.6 },
    { id: '日本', x: 200, y: 120, color: '#DC2626', size: 25, influence: 0.4 },
    { id: '歐盟', x: 500, y: 120, color: '#7C3AED', size: 25, influence: 0.3 }
  ];

  // Influence flow connections
  const links = [
    { source: '美國', target: '台灣', type: 'support', strength: 0.8 },
    { source: '中國', target: '台灣', type: 'pressure', strength: 0.9 },
    { source: '美國', target: '日本', type: 'cooperation', strength: 0.6 },
    { source: '美國', target: '歐盟', type: 'cooperation', strength: 0.5 },
    { source: '中國', target: '日本', type: 'competition', strength: 0.4 },
    { source: '中國', target: '歐盟', type: 'competition', strength: 0.3 },
    { source: '日本', target: '台灣', type: 'cooperation', strength: 0.5 },
    { source: '歐盟', target: '台灣', type: 'cooperation', strength: 0.4 }
  ];

  const [vacuumBubbles, setVacuumBubbles] = useState([]);
  const animationRef = useRef();

  const toggleAnimation = () => {
    setIsPlaying(!isPlaying);
  };

  const triggerCrisis = () => {
    setCrisis(!crisis);
    if (!crisis) {
      // Generate vacuum bubbles around Taiwan
      const newBubbles = Array.from({ length: 5 }, (_, i) => ({
        id: i,
        x: 350 + (Math.random() - 0.5) * 120,
        y: 250 + (Math.random() - 0.5) * 120,
        radius: Math.random() * 20 + 15,
        opacity: 0.7
      }));
      setVacuumBubbles(newBubbles);
    } else {
      setVacuumBubbles([]);
    }
  };

  const startRecording = async () => {
    if (!canvasRef.current || !svgRef.current) return;

    const canvas = canvasRef.current;
    const svg = svgRef.current;
    
    // Set fixed canvas dimensions
    canvas.width = 700;
    canvas.height = 400;
    canvas.style.width = '700px';
    canvas.style.height = '400px';

    try {
      // Try different mimeTypes for better compatibility
      let mimeType = 'video/webm;codecs=vp9';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = 'video/webm;codecs=vp8';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
          mimeType = 'video/webm';
          if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/mp4';
          }
        }
      }

      const stream = canvas.captureStream(30);
      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: mimeType,
        videoBitsPerSecond: 2500000 // 2.5 Mbps for better quality
      });

      recordedChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(recordedChunksRef.current, { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        // Create download link with better filename
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        const fileExtension = mimeType.includes('mp4') ? 'mp4' : 'webm';
        const filename = `Taiwan-Influence-Dynamics-${timestamp}.${fileExtension}`;
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        
        // Add to document, click, and remove
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        // Clean up
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        
        alert(`影片已成功下載！\n檔案名稱: ${filename}\n請檢查您的下載資料夾或桌面。`);
      };

      mediaRecorderRef.current.onerror = (event) => {
        console.error('MediaRecorder error:', event);
        alert('錄影時發生錯誤，請重試。');
        setIsRecording(false);
      };

      setIsRecording(true);
      setRecordingProgress(0);
      mediaRecorderRef.current.start(100); // Collect data every 100ms

      // Record for 10 seconds with better progress tracking
      let progress = 0;
      const recordingInterval = setInterval(() => {
        progress += 10;
        setRecordingProgress(progress);
        
        if (progress >= 100) {
          clearInterval(recordingInterval);
          setTimeout(() => {
            stopRecording();
          }, 500); // Small delay to ensure last frame is captured
        }
      }, 1000);

    } catch (error) {
      console.error('Error starting recording:', error);
      alert('錄影功能不支援此瀏覽器。建議使用 Chrome、Firefox 或 Edge 瀏覽器。');
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
    setRecordingProgress(0);
  };

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const canvas = canvasRef.current;
    const ctx = canvas ? canvas.getContext('2d') : null;
    
    svg.selectAll("*").remove();
    
    const width = 700;
    const height = 400;
    
    svg.attr("width", width).attr("height", height);
    
    if (canvas) {
      canvas.width = width;
      canvas.height = height;
    }

    const simulation = d3.forceSimulation(nodes)
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(d => d.size + 10))
      .force("x", d3.forceX().x(d => Math.max(d.size + 20, Math.min(width - d.size - 20, d.x))))
      .force("y", d3.forceY().y(d => Math.max(d.size + 20, Math.min(height - d.size - 20, d.y))));

    // Create influence flow particles
    const particles = [];
    for (let i = 0; i < 30; i++) {
      particles.push({
        x: Math.random() * (width - 40) + 20,
        y: Math.random() * (height - 40) + 20,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        life: Math.random()
      });
    }

    const animate = () => {
      if (!isPlaying && !isRecording) return;

      svg.selectAll("*").remove();
      
      if (ctx && isRecording) {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, width, height);
      }

      // Draw influence flow lines
      const linkGroup = svg.append("g").attr("class", "links");
      
      links.forEach(link => {
        const sourceNode = nodes.find(n => n.id === link.source);
        const targetNode = nodes.find(n => n.id === link.target);
        
        if (sourceNode && targetNode) {
          let strokeColor = '#666';
          let strokeWidth = link.strength * 3;
          
          if (link.type === 'support') strokeColor = '#3B82F6';
          else if (link.type === 'pressure') strokeColor = '#F97316';
          else if (link.type === 'cooperation') strokeColor = '#10B981';
          else if (link.type === 'competition') strokeColor = '#DC2626';

          // Add pulsing effect during crisis
          if (crisis && (link.source === '台灣' || link.target === '台灣')) {
            strokeWidth *= (1 + 0.3 * Math.sin(Date.now() * 0.01));
          }

          linkGroup.append("line")
            .attr("x1", sourceNode.x)
            .attr("y1", sourceNode.y)
            .attr("x2", targetNode.x)
            .attr("y2", targetNode.y)
            .attr("stroke", strokeColor)
            .attr("stroke-width", strokeWidth)
            .attr("opacity", 0.6);

          if (ctx && isRecording) {
            ctx.strokeStyle = strokeColor;
            ctx.lineWidth = strokeWidth;
            ctx.globalAlpha = 0.6;
            ctx.beginPath();
            ctx.moveTo(sourceNode.x, sourceNode.y);
            ctx.lineTo(targetNode.x, targetNode.y);
            ctx.stroke();
          }
        }
      });

      // Draw flowing particles
      particles.forEach(particle => {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.life += 0.01;

        // Keep particles within bounds
        if (particle.x < 10 || particle.x > width - 10) {
          particle.vx *= -1;
          particle.x = Math.max(10, Math.min(width - 10, particle.x));
        }
        if (particle.y < 10 || particle.y > height - 10) {
          particle.vy *= -1;
          particle.y = Math.max(10, Math.min(height - 10, particle.y));
        }
        
        if (particle.life > 1) particle.life = 0;

        const opacity = Math.sin(particle.life * Math.PI);
        
        svg.append("circle")
          .attr("cx", particle.x)
          .attr("cy", particle.y)
          .attr("r", 2)
          .attr("fill", "#4338CA")
          .attr("opacity", opacity * 0.5);

        if (ctx && isRecording) {
          ctx.globalAlpha = opacity * 0.5;
          ctx.fillStyle = "#4338CA";
          ctx.beginPath();
          ctx.arc(particle.x, particle.y, 2, 0, 2 * Math.PI);
          ctx.fill();
        }
      });

      // Draw vacuum bubbles during crisis
      if (crisis) {
        vacuumBubbles.forEach(bubble => {
          // Ensure bubbles stay within bounds
          const constrainedX = Math.max(bubble.radius, Math.min(width - bubble.radius, bubble.x));
          const constrainedY = Math.max(bubble.radius, Math.min(height - bubble.radius, bubble.y));
          
          const pulseRadius = bubble.radius * (1 + 0.2 * Math.sin(Date.now() * 0.005 + bubble.id));
          
          svg.append("circle")
            .attr("cx", constrainedX)
            .attr("cy", constrainedY)
            .attr("r", pulseRadius)
            .attr("fill", "none")
            .attr("stroke", "#DC2626")
            .attr("stroke-width", 2)
            .attr("opacity", bubble.opacity * Math.sin(Date.now() * 0.003 + bubble.id));

          if (ctx && isRecording) {
            ctx.globalAlpha = bubble.opacity * Math.sin(Date.now() * 0.003 + bubble.id);
            ctx.strokeStyle = "#DC2626";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(constrainedX, constrainedY, pulseRadius, 0, 2 * Math.PI);
            ctx.stroke();
          }
        });
      }

      // Draw country nodes
      const nodeGroup = svg.append("g").attr("class", "nodes");
      
      nodes.forEach(node => {
        let nodeSize = node.size;
        let nodeColor = node.color;

        // Taiwan pulsing effect during crisis
        if (crisis && node.id === '台灣') {
          nodeSize *= (1 + 0.4 * Math.sin(Date.now() * 0.008));
          nodeColor = d3.interpolate(node.color, "#DC2626")(0.3);
        }

        nodeGroup.append("circle")
          .attr("cx", node.x)
          .attr("cy", node.y)
          .attr("r", nodeSize)
          .attr("fill", nodeColor)
          .attr("stroke", "#fff")
          .attr("stroke-width", 3);

        nodeGroup.append("text")
          .attr("x", node.x)
          .attr("y", node.y + 5)
          .attr("text-anchor", "middle")
          .attr("fill", "white")
          .attr("font-size", "12px")
          .attr("font-weight", "bold")
          .text(node.id);

        if (ctx && isRecording) {
          ctx.globalAlpha = 1;
          ctx.fillStyle = nodeColor;
          ctx.beginPath();
          ctx.arc(node.x, node.y, nodeSize, 0, 2 * Math.PI);
          ctx.fill();
          
          ctx.strokeStyle = "#fff";
          ctx.lineWidth = 3;
          ctx.stroke();
          
          ctx.fillStyle = "white";
          ctx.font = "bold 12px Arial";
          ctx.textAlign = "center";
          ctx.fillText(node.id, node.x, node.y + 5);
        }
      });

      if (isPlaying || isRecording) {
        animationRef.current = requestAnimationFrame(animate);
      }
    };

    if (isPlaying || isRecording) {
      animate();
    } else {
      // Static render
      animate();
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isPlaying, crisis, vacuumBubbles, isRecording]);

  return (
    <div className="w-full max-w-6xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-3">Taiwan Influence Dynamics Simulation</h2>
        <p className="text-gray-600 text-sm mb-4">
          Simulates influence flows in Taiwan under U.S.-China competition, with interactions involving other international actors (e.g., Japan, EU) and crisis scenarios like cross-strait tensions.
        </p>
      </div>

      <div className="mb-4 flex gap-4 flex-wrap">
        <button onClick={toggleAnimation} className={`px-6 py-2 rounded font-semibold transition-colors ${isPlaying ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-green-500 hover:bg-green-600 text-white'}`}>
          {isPlaying ? 'Pause Animation' : 'Start Animation'}
        </button>
        <button onClick={triggerCrisis} className={`px-6 py-2 rounded font-semibold transition-colors ${crisis ? 'bg-orange-500 hover:bg-orange-600 text-white' : 'bg-blue-500 hover:bg-blue-600 text-white'}`}>
          {crisis ? 'Stop φ₃ Crisis' : 'Trigger φ₃ Crisis'}
        </button>
        <button onClick={startRecording} disabled={isRecording} className={`px-6 py-2 rounded font-semibold transition-colors ${isRecording ? 'bg-gray-400 cursor-not-allowed text-white' : 'bg-purple-500 hover:bg-purple-600 text-white'}`}>
          {isRecording ? `Recording... ${recordingProgress}%` : '📹 Export Video (10s)'}
        </button>
        {isRecording && (
          <button onClick={stopRecording} className="px-6 py-2 rounded font-semibold bg-red-600 hover:bg-red-700 text-white">
            Stop Recording
          </button>
        )}
      </div>

      {isRecording && (
        <div className="mb-4">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-purple-600 h-2 rounded-full transition-all duration-100" style={{ width: `${recordingProgress}%` }}></div>
          </div>
          <p className="text-sm text-gray-600 mt-1">Recording progress: {recordingProgress}% (will auto-stop and download)</p>
        </div>
      )}

      <div className="border rounded-lg overflow-hidden relative" style={{ height: '400px' }}>
        <svg ref={svgRef} className="w-full h-full" viewBox="0 0 700 400" preserveAspectRatio="xMidYMid meet"></svg>
        <canvas ref={canvasRef} className="absolute top-0 left-0 pointer-events-none" style={{ display: isRecording ? 'block' : 'none', opacity: 0.1 }} />
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div className="bg-blue-50 p-4 rounded border-l-4 border-blue-500">
          <h3 className="font-semibold text-blue-800 mb-2">φ₁ - 美國</h3>
          <p className="text-blue-700">Provides military support (e.g., arms sales), economic ties, and diplomatic backing to Taiwan; cooperates with Japan, EU.</p>
        </div>
        <div className="bg-orange-50 p-4 rounded border-l-4 border-orange-500">
          <h3 className="font-semibold text-orange-800 mb-2">φ₂ - 中國</h3>
          <p className="text-orange-700">Exerts economic pressure and diplomatic influence on Taiwan; competes with U.S. and other actors.</p>
        </div>
        <div className="bg-green-50 p-4 rounded border-l-4 border-green-500">
          <h3 className="font-semibold text-green-800 mb-2">φ₃ - 台灣</h3>
          <p className="text-green-700">Focal point of U.S.-China rivalry, with high-tech economy and strategic importance; unstable during crises.</p>
        </div>
        <div className="bg-red-50 p-4 rounded border-l-4 border-red-500">
          <h3 className="font-semibold text-red-800 mb-2">φ₄ - 其他國際行為者</h3>
          <p className="text-red-700">Includes Japan (tech cooperation), EU (trade ties); cooperates with U.S., competes with China.</p>
        </div>
      </div>

      <div className="mt-4 bg-gray-50 p-4 rounded">
        <h3 className="font-semibold text-gray-800 mb-2">Animation Effects Explanation:</h3>
        <ul className="text-sm text-gray-700 space-y-1">
          <li>• <strong>Normal State:</strong> Influence flows dynamically, with Taiwan balancing U.S. support, Chinese pressure, and cooperation with Japan, EU.</li>
          <li>• <strong>φ₃ Crisis State:</strong> Taiwan faces instability (e.g., cross-strait tensions), causing influence outflows and vacuum bubbles.</li>
          <li>• <strong>Vacuum Bubble Effect:</strong> Red circles indicate areas where Taiwan's influence (e.g., economic or diplomatic) suddenly vanishes.</li>
          <li>• <strong>Competitive Interactions:</strong> U.S. and China compete intensely for Taiwan's influence; U.S. cooperates with Japan, EU.</li>
          <li>• <strong>Video Export:</strong> Record 10 seconds of animation to visualize Taiwan's influence dynamics.</li>
        </ul>
      </div>

      <div className="mt-4 bg-blue-50 p-4 rounded border-l-4 border-blue-500">
        <h3 className="font-semibold text-blue-800 mb-2">📹 Video Export Feature Guide:</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Click "Export Video" to record a 10-second animation of Taiwan's influence dynamics.</li>
          <li>• Supports modern browsers like Chrome, Firefox.</li>
          <li>• Auto-generates WebM format video for download.</li>
          <li>• Trigger φ₃ crisis before recording to capture full crisis effects.</li>
          <li>• Use online tools to convert WebM to GIF or MP4 if needed.</li>
        </ul>
      </div>
    </div>
  );
};

export default TaiwanInfluenceSimulation;
