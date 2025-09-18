import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface Keyword {
  word: string;
  count: number;
  percentage: number;
}

interface KeywordChartProps {
  keywords: Keyword[];
  maxItems?: number;
  height?: number;
  className?: string;
}

const KeywordChart: React.FC<KeywordChartProps> = ({
  keywords,
  maxItems = 10,
  height = 300,
  className = ''
}) => {
  const sortedKeywords = [...keywords]
    .sort((a, b) => b.count - a.count)
    .slice(0, maxItems);

  const getBarColor = (percentage: number) => {
    if (percentage >= 3) return '#EF4444'; // Red for high density
    if (percentage >= 2) return '#F59E0B'; // Yellow for medium density
    if (percentage >= 1) return '#10B981'; // Green for optimal density
    return '#6B7280'; // Gray for low density
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium">{`Keyword: ${label}`}</p>
          <p className="text-sm text-gray-600">{`Count: ${data.count}`}</p>
          <p className="text-sm text-gray-600">{`Density: ${data.percentage.toFixed(2)}%`}</p>
        </div>
      );
    }
    return null;
  };

  if (!sortedKeywords.length) {
    return (
      <div className={`flex items-center justify-center h-${height/4} ${className}`}>
        <p className="text-gray-500">No keyword data available</p>
      </div>
    );
  }

  return (
    <div className={className} style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={sortedKeywords}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="word" 
            angle={-45}
            textAnchor="end"
            height={80}
            fontSize={12}
          />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {sortedKeywords.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getBarColor(entry.percentage)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default KeywordChart;
