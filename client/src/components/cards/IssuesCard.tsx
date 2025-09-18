import React from 'react';
import { AlertTriangle, AlertCircle, Info } from 'lucide-react';

interface Issue {
  priority: 'high' | 'medium' | 'low';
  description: string;
}

interface IssuesCardProps {
  title: string;
  issues: string[] | Issue[];
  type?: 'issues' | 'recommendations';
  className?: string;
}

const IssuesCard: React.FC<IssuesCardProps> = ({
  title,
  issues,
  type = 'issues',
  className = ''
}) => {
  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'medium':
        return <AlertCircle className="w-4 h-4 text-yellow-500" />;
      case 'low':
        return <Info className="w-4 h-4 text-blue-500" />;
      default:
        return <Info className="w-4 h-4 text-gray-500" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'border-l-red-500 bg-red-50';
      case 'medium':
        return 'border-l-yellow-500 bg-yellow-50';
      case 'low':
        return 'border-l-blue-500 bg-blue-50';
      default:
        return 'border-l-gray-500 bg-gray-50';
    }
  };

  const normalizedIssues = issues.map(issue => 
    typeof issue === 'string' 
      ? { description: issue, priority: 'medium' as const }
      : issue
  );

  const sortedIssues = [...normalizedIssues].sort((a, b) => {
    const priorityOrder = { high: 3, medium: 2, low: 1 };
    return priorityOrder[b.priority] - priorityOrder[a.priority];
  });

  const headerColor = type === 'issues' ? 'text-red-700' : 'text-green-700';
  const headerBg = type === 'issues' ? 'bg-red-50' : 'bg-green-50';

  return (
    <div className={`bg-white rounded-lg border border-gray-200 overflow-hidden ${className}`}>
      <div className={`px-6 py-4 ${headerBg} border-b border-gray-200`}>
        <h3 className={`text-lg font-semibold ${headerColor}`}>{title}</h3>
        <p className="text-sm text-gray-600 mt-1">
          {sortedIssues.length} {sortedIssues.length === 1 ? 'item' : 'items'} found
        </p>
      </div>
      
      <div className="p-6">
        {sortedIssues.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-gray-400 mb-2">
              {type === 'issues' ? '✅' : '💡'}
            </div>
            <p className="text-gray-500">
              {type === 'issues' ? 'No issues found!' : 'No recommendations available'}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {sortedIssues.map((item, index) => (
              <div
                key={index}
                className={`p-4 border-l-4 rounded-r-lg ${getPriorityColor(item.priority)}`}
              >
                <div className="flex items-start gap-3">
                  {getPriorityIcon(item.priority)}
                  <div className="flex-1">
                    <p className="text-sm text-gray-800">{item.description}</p>
                    <span className={`inline-block mt-2 px-2 py-1 text-xs rounded-full ${
                      item.priority === 'high' 
                        ? 'bg-red-100 text-red-800' 
                        : item.priority === 'medium'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {item.priority.toUpperCase()} PRIORITY
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default IssuesCard;
