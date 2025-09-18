export interface Analysis {
  id: string;
  url: string;
  title: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  createdAt: Date;
  steps: AnalysisStep[];
  results?: AnalysisResults;
}

export interface AnalysisStep {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  progress: number;
  startTime?: Date;
  endTime?: Date;
  result?: any;
  error?: string;
}

export interface AnalysisResults {
  htmlContent?: HtmlContentResult;
  seoAnalysis?: SeoAnalysisResult;
  imageGeneration?: ImageGenerationResult;
}

export interface HtmlContentResult {
  status: string;
  url: string;
  extraction_timestamp: string;
  headings: Record<string, any[]>;
  paragraphs: any[];
  divisions: any[];
  summary: any;
  detailed_report: string;
  total_elements: number;
}

export interface SeoAnalysisResult {
  status: string;
  url: string;
  seo_score: number;
  total_checks: number;
  passed_checks: number;
  issues: string[];
  recommendations: string[];
  keywords: string[];
  detailed_report: string;
  page_info: any;
}

export interface ImageGenerationResult {
  status: string;
  url: string;
  total_images: number;
  processed_images: number;
  alt_text_suggestions: any[];
  page_context: string;
}

export interface WebSocketMessage {
  author: string;
  is_partial: boolean;
  turn_complete: boolean;
  interrupted: boolean;
  parts: MessagePart[];
  input_transcription?: {
    text: string;
    is_final: boolean;
  };
  output_transcription?: {
    text: string;
    is_final: boolean;
  };
}

export interface MessagePart {
  type: 'text' | 'audio/pcm' | 'function_call' | 'function_response';
  data: any;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  analysis_id?: string;
}
