import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  color?: 'green' | 'yellow' | 'red' | 'blue' | 'purple' | 'gray';
  className?: string;
  children?: React.ReactNode;
}

const MetricsCard: React.FC<MetricsCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  color = 'blue',
  className = '',
  children
}) => {
  const colorClasses = {
    green: 'border-green-200 bg-green-50',
    yellow: 'border-yellow-200 bg-yellow-50',
    red: 'border-red-200 bg-red-50',
    blue: 'border-blue-200 bg-blue-50',
    purple: 'border-purple-200 bg-purple-50',
    gray: 'border-gray-200 bg-gray-50'
  };

  const iconColorClasses = {
    green: 'text-green-600',
    yellow: 'text-yellow-600',
    red: 'text-red-600',
    blue: 'text-blue-600',
    purple: 'text-purple-600',
    gray: 'text-gray-600'
  };

  return (
    <div className={`bg-white rounded-lg border-2 ${colorClasses[color]} p-6 ${className}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-sm font-medium text-gray-600 mb-2">{title}</h3>
          <div className="text-2xl font-bold text-gray-900 mb-1">{value}</div>
          {subtitle && (
            <p className="text-sm text-gray-500">{subtitle}</p>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-full ${colorClasses[color]}`}>
            <Icon className={`w-6 h-6 ${iconColorClasses[color]}`} />
          </div>
        )}
      </div>
      {children && (
        <div className="mt-4">
          {children}
        </div>
      )}
    </div>
  );
};

export default MetricsCard;
