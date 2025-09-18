import React from 'react';
import { Check, Clock, AlertCircle } from 'lucide-react';
import { AnalysisStep } from '../types';

interface AnalysisStepsProps {
  steps: AnalysisStep[];
}

const AnalysisSteps: React.FC<AnalysisStepsProps> = ({ steps }) => {
  const getStepIcon = (step: AnalysisStep) => {
    switch (step.status) {
      case 'completed':
        return <Check className="w-5 h-5 text-white" />;
      case 'running':
        return <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-white" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStepClasses = (step: AnalysisStep) => {
    switch (step.status) {
      case 'completed':
        return 'step-completed';
      case 'running':
        return 'step-active';
      case 'error':
        return 'bg-red-500 text-white';
      default:
        return 'step-pending';
    }
  };

  const getConnectorClasses = (index: number) => {
    if (index === steps.length - 1) return '';
    
    const currentStep = steps[index];
    
    if (currentStep.status === 'completed') {
      return 'bg-green-500';
    } else if (currentStep.status === 'running') {
      return 'bg-primary-600';
    } else {
      return 'bg-gray-300';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Progress</h3>
      
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <React.Fragment key={step.id}>
            <div className="flex flex-col items-center flex-1">
              {/* Step Circle */}
              <div className={`
                w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300
                ${getStepClasses(step)}
              `}>
                {getStepIcon(step)}
              </div>
              
              {/* Step Label */}
              <div className="mt-3 text-center">
                <p className="text-sm font-medium text-gray-900">{step.name}</p>
                {step.status === 'running' && (
                  <div className="mt-1">
                    <div className="w-16 bg-gray-200 rounded-full h-1">
                      <div 
                        className="bg-primary-600 h-1 rounded-full transition-all duration-300"
                        style={{ width: `${step.progress}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-500 mt-1">{step.progress}%</p>
                  </div>
                )}
                {step.status === 'error' && step.error && (
                  <p className="text-xs text-red-500 mt-1">{step.error}</p>
                )}
                {step.endTime && step.startTime && (
                  <p className="text-xs text-gray-500 mt-1">
                    {Math.round((step.endTime.getTime() - step.startTime.getTime()) / 1000)}s
                  </p>
                )}
              </div>
            </div>
            
            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div className="flex-1 px-4">
                <div className={`
                  h-1 rounded transition-all duration-300
                  ${getConnectorClasses(index)}
                `} />
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default AnalysisSteps;
