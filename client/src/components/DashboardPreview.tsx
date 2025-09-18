import React from 'react';
import Dashboard from './Dashboard';
import exampleResponse from '/Users/sesena/Documents/commencis/internal/gcloud/gcp-seo-tracker/client/example-response.json';

const DashboardPreview: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6 bg-white rounded-lg border border-gray-200 p-4">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Dashboard Preview</h1>
          <p className="text-gray-600">Testing dashboard with example response data</p>
        </div>
        
        <Dashboard 
          result={exampleResponse as any}
          url={exampleResponse.url}
        />
      </div>
    </div>
  );
};

export default DashboardPreview;
