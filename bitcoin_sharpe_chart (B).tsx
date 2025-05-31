import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

const BitcoinSharpeChart = () => {
  const [data, setData] = useState([]);
  const [timeFrame, setTimeFrame] = useState('1Y');

  // 模擬比特幣歷史數據和計算Sharpe比率
  const generateSharpeData = (months) => {
    const data = [];
    const startDate = new Date();
    startDate.setMonth(startDate.getMonth() - months);
    
    // 模擬比特幣價格波動和收益率數據
    let cumulativeReturn = 0;
    let volatilitySum = 0;
    const riskFreeRate = 0.02; // 2% 年化無風險利率
    
    for (let i = 0; i < months; i++) {
      const date = new Date(startDate);
      date.setMonth(date.getMonth() + i);
      
      // 模擬月收益率 (基於比特幣的高波動性特徵)
      const monthlyReturn = (Math.random() - 0.4) * 0.3 + 0.02; // 平均月收益2%，高波動
      cumulativeReturn += monthlyReturn;
      
      // 計算滾動波動率
      const volatility = Math.abs(monthlyReturn - 0.02) + Math.random() * 0.1;
      volatilitySum += volatility * volatility;
      
      // 計算Sharpe比率 (年化)
      const avgReturn = (cumulativeReturn / (i + 1)) * 12; // 年化收益
      const avgVolatility = Math.sqrt(volatilitySum / (i + 1)) * Math.sqrt(12); // 年化波動率
      const sharpeRatio = (avgReturn - riskFreeRate) / avgVolatility;
      
      data.push({
        date: date.toISOString().slice(0, 7),
        sharpe: Math.max(-3, Math.min(3, sharpeRatio)), // 限制在合理範圍內
        return: avgReturn * 100,
        volatility: avgVolatility * 100
      });
    }
    
    return data;
  };

  useEffect(() => {
    const months = timeFrame === '6M' ? 6 : timeFrame === '1Y' ? 12 : 24;
    setData(generateSharpeData(months));
  }, [timeFrame]);

  const formatTooltip = (value, name) => {
    if (name === 'sharpe') return [value?.toFixed(3), 'Sharpe 比率'];
    if (name === 'return') return [`${value?.toFixed(1)}%`, '年化收益率'];
    if (name === 'volatility') return [`${value?.toFixed(1)}%`, '年化波動率'];
    return [value, name];
  };

  const currentSharpe = data.length > 0 ? data[data.length - 1].sharpe : 0;
  const sharpeColor = currentSharpe > 1 ? '#10B981' : currentSharpe > 0 ? '#F59E0B' : '#EF4444';

  return (
    <div className="w-full max-w-6xl mx-auto p-6 bg-gray-900 text-white rounded-lg">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2 text-center">比特幣 Sharpe 比率分析</h2>
        <p className="text-gray-400 text-center mb-4">風險調整後收益表現指標</p>
        
        {/* 時間範圍選擇器 */}
        <div className="flex justify-center gap-2 mb-4">
          {['6M', '1Y', '2Y'].map((period) => (
            <button
              key={period}
              onClick={() => setTimeFrame(period)}
              className={`px-4 py-2 rounded ${
                timeFrame === period 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {period}
            </button>
          ))}
        </div>

        {/* 當前指標顯示 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-800 p-4 rounded-lg text-center">
            <div className="text-sm text-gray-400">當前 Sharpe 比率</div>
            <div className={`text-2xl font-bold`} style={{color: sharpeColor}}>
              {currentSharpe.toFixed(3)}
            </div>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg text-center">
            <div className="text-sm text-gray-400">年化收益率</div>
            <div className="text-2xl font-bold text-green-400">
              {data.length > 0 ? `${data[data.length - 1].return.toFixed(1)}%` : '0%'}
            </div>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg text-center">
            <div className="text-sm text-gray-400">年化波動率</div>
            <div className="text-2xl font-bold text-orange-400">
              {data.length > 0 ? `${data[data.length - 1].volatility.toFixed(1)}%` : '0%'}
            </div>
          </div>
        </div>
      </div>

      {/* Sharpe比率圖表 */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-4">Sharpe 比率趨勢</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="date" 
              stroke="#9CA3AF"
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              stroke="#9CA3AF"
              tick={{ fontSize: 12 }}
              domain={[-2, 2]}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1F2937', 
                border: '1px solid #374151',
                borderRadius: '8px'
              }}
              formatter={formatTooltip}
            />
            <ReferenceLine y={0} stroke="#6B7280" strokeDasharray="2 2" />
            <ReferenceLine y={1} stroke="#10B981" strokeDasharray="2 2" label="優秀" />
            <ReferenceLine y={-1} stroke="#EF4444" strokeDasharray="2 2" label="較差" />
            <Line 
              type="monotone" 
              dataKey="sharpe" 
              stroke="#3B82F6" 
              strokeWidth={3}
              dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, fill: '#60A5FA' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Sharpe比率解釋 */}
      <div className="bg-gray-800 p-4 rounded-lg">
        <h4 className="text-md font-semibold mb-3">Sharpe 比率解讀</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <div className="flex items-center mb-2">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span><strong>&gt; 1.0:</strong> 優秀表現</span>
            </div>
            <div className="flex items-center mb-2">
              <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
              <span><strong>0.5-1.0:</strong> 良好表現</span>
            </div>
          </div>
          <div>
            <div className="flex items-center mb-2">
              <div className="w-3 h-3 bg-orange-500 rounded-full mr-2"></div>
              <span><strong>0-0.5:</strong> 一般表現</span>
            </div>
            <div className="flex items-center mb-2">
              <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
              <span><strong>&lt; 0:</strong> 表現不佳</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BitcoinSharpeChart;