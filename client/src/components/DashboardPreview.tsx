import React from 'react';
import Dashboard from './Dashboard';
import exampleResponse from '../../example-response.json';

interface DashboardPreviewProps {
  onExit?: () => void;
}

const DashboardPreview: React.FC<DashboardPreviewProps> = ({ onExit }) => {
  return (
    <div className="bg-gray-50 rounded-lg border-2 border-dashed border-blue-300 p-6">
      <div className="mb-6 bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2">
              🎨 Dashboard Preview
            </h1>
            <p className="text-gray-600">Testing dashboard with example response data</p>
          </div>
          {onExit && (
            <button
              onClick={onExit}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              Exit Preview
            </button>
          )}
        </div>
      </div>
      
      <Dashboard 
        result={exampleResponse as any}
        url={exampleResponse.url}
      />
    </div>
  );
};

export default DashboardPreview;
