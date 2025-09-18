import React from 'react';
import { Plus, Clock, CheckCircle, AlertCircle, ExternalLink, Search } from 'lucide-react';
import { Analysis } from '../types';

interface SidebarProps {
  analyses: Analysis[];
  selectedAnalysis: Analysis | null;
  onSelectAnalysis: (analysis: Analysis) => void;
  onNewAnalysis: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  analyses,
  selectedAnalysis,
  onSelectAnalysis,
  onNewAnalysis
}) => {
  const getStatusIcon = (status: Analysis['status']) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-4 h-4 text-gray-400" />;
      case 'running':
        return <div className="w-4 h-4 border-2 border-primary-600 border-t-transparent rounded-full animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return <Clock className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: Analysis['status']) => {
    switch (status) {
      case 'pending':
        return 'text-gray-600';
      case 'running':
        return 'text-primary-600';
      case 'completed':
        return 'text-green-600';
      case 'error':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const truncateUrl = (url: string, maxLength: number = 30) => {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
  };

  return (
    <div className="w-80 bg-gray-50 border-r border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={onNewAnalysis}
          className="w-full btn-primary flex items-center justify-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>New Analysis</span>
        </button>
      </div>

      {/* History */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4">
          <h2 className="text-sm font-semibold text-gray-700 mb-3">History</h2>
          
          {analyses.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-gray-400 mb-2">
                <Search className="w-8 h-8 mx-auto" />
              </div>
              <p className="text-sm text-gray-500">No analyses yet</p>
              <p className="text-xs text-gray-400 mt-1">
                Click "New Analysis" to get started
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {analyses.map((analysis) => (
                <div
                  key={analysis.id}
                  onClick={() => onSelectAnalysis(analysis)}
                  className={`p-3 rounded-lg cursor-pointer transition-colors duration-200 ${
                    selectedAnalysis?.id === analysis.id
                      ? 'bg-primary-50 border border-primary-200'
                      : 'bg-white hover:bg-gray-50 border border-gray-200'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2 flex-1 min-w-0">
                      {getStatusIcon(analysis.status)}
                      <div className="flex-1 min-w-0">
                        <h3 className="text-sm font-medium text-gray-900 truncate">
                          {analysis.title || 'Untitled Analysis'}
                        </h3>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-1 mb-2">
                    <ExternalLink className="w-3 h-3 text-gray-400 flex-shrink-0" />
                    <span className="text-xs text-gray-500 truncate" title={analysis.url}>
                      {truncateUrl(analysis.url)}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className={`text-xs font-medium ${getStatusColor(analysis.status)}`}>
                      {analysis.status.charAt(0).toUpperCase() + analysis.status.slice(1)}
                    </span>
                    <span className="text-xs text-gray-400">
                      {analysis.createdAt.toLocaleDateString('tr-TR', {
                        day: '2-digit',
                        month: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
