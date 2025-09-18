import { AnalysisStep } from '../types';

export const createInitialSteps = (): AnalysisStep[] => [
  {
    id: 'web-crawler',
    name: 'Web Crawler',
    status: 'pending',
    progress: 0
  },
  {
    id: 'content-analyzer', 
    name: 'Content Analyzer',
    status: 'pending',
    progress: 0
  },
  {
    id: 'competitor-analysis',
    name: 'Competitor Analysis', 
    status: 'pending',
    progress: 0
  }
];

export const getStepDisplayName = (stepId: string): string => {
  const stepNames = {
    'web-crawler': 'Web Crawler',
    'content-analyzer': 'Content Analyzer', 
    'competitor-analysis': 'Competitor Analysis',
    'html-content-extractor': 'HTML Content Extractor',
    'image-generator': 'Image Generator',
    'seo-analyzer': 'SEO Analyzer'
  };
  
  return stepNames[stepId as keyof typeof stepNames] || stepId;
};

export const mapFunctionCallToStep = (functionName: string): string => {
  const functionToStepMap = {
    'extract_html_content': 'web-crawler',
    'extract_specific_tags': 'web-crawler', 
    'analyze_webpage_seo': 'content-analyzer',
    'extract_page_keywords': 'content-analyzer',
    'generate_image_with_alt_text': 'competitor-analysis',
    'generate_alt_text_for_web_images': 'competitor-analysis'
  };
  
  return functionToStepMap[functionName as keyof typeof functionToStepMap] || 'web-crawler';
};

export const updateStepProgress = (
  steps: AnalysisStep[],
  stepId: string,
  status: AnalysisStep['status'],
  progress: number = 0
): AnalysisStep[] => {
  return steps.map(step => {
    if (step.id === stepId) {
      const updatedStep = {
        ...step,
        status,
        progress: Math.min(100, Math.max(0, progress))
      };
      
      if (status === 'running' && !step.startTime) {
        updatedStep.startTime = new Date();
      }
      
      if (status === 'completed' || status === 'error') {
        updatedStep.endTime = new Date();
        if (status === 'completed') {
          updatedStep.progress = 100;
        }
      }
      
      return updatedStep;
    }
    return step;
  });
};
