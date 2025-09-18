import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

interface DonutChartProps {
  score: number;
  maxScore?: number;
  size?: number;
  colors?: {
    filled: string;
    empty: string;
  };
  showLabel?: boolean;
  className?: string;
}

const DonutChart: React.FC<DonutChartProps> = ({
  score,
  maxScore = 100,
  size = 200,
  colors = {
    filled: '#10B981',
    empty: '#E5E7EB'
  },
  showLabel = true,
  className = ''
}) => {
  const percentage = Math.min((score / maxScore) * 100, 100);
  
  const data = [
    { name: 'Score', value: percentage, color: colors.filled },
    { name: 'Remaining', value: 100 - percentage, color: colors.empty }
  ];

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#10B981'; // Green
    if (score >= 60) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  const renderCustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      if (data.name === 'Score') {
        return (
          <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
            <p className="font-medium">{`Score: ${score}/${maxScore}`}</p>
            <p className="text-sm text-gray-600">{`${percentage.toFixed(1)}%`}</p>
          </div>
        );
      }
    }
    return null;
  };

  return (
    <div className={`relative ${className}`}>
      <ResponsiveContainer width={size} height={size}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={size * 0.25}
            outerRadius={size * 0.4}
            startAngle={90}
            endAngle={-270}
            dataKey="value"
            stroke="none"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip content={renderCustomTooltip} />
        </PieChart>
      </ResponsiveContainer>
      
      {showLabel && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div 
              className="text-3xl font-bold"
              style={{ color: getScoreColor(score) }}
            >
              {score}
            </div>
            <div className="text-sm text-gray-600">/{maxScore}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DonutChart;
