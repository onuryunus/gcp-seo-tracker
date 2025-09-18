import React, { useState, useEffect, useCallback, useMemo } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import AnalysisSteps from './components/AnalysisSteps';
import ChatInterface from './components/ChatInterface';
import NewAnalysisModal from './components/NewAnalysisModal';
import AnalysisResults from './components/AnalysisResults';
import { useWebSocket } from './hooks/useWebSocket';
import { Analysis, ChatMessage, WebSocketMessage, MessagePart } from './types';
import { createInitialSteps, mapFunctionCallToStep, updateStepProgress } from './utils/analysisSteps';

// Generate a unique session ID
const generateSessionId = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

const App: React.FC = () => {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [selectedAnalysis, setSelectedAnalysis] = useState<Analysis | null>(null);
  const [isNewAnalysisModalOpen, setIsNewAnalysisModalOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isStartingAnalysis, setIsStartingAnalysis] = useState(false);

  // Generate unique session ID for this user session
  const sessionId = useMemo(() => generateSessionId(), []);

  // WebSocket connection
  const { isConnected, connect, disconnect, sendTextMessage, isConnecting } = useWebSocket({
    url: `ws://localhost:8000/ws/${sessionId}`,
    onMessage: handleWebSocketMessage,
    onOpen: () => {
      console.log('WebSocket connected with session ID:', sessionId);
    },
    onClose: () => {
      console.log('WebSocket disconnected');
    },
    onError: (error) => {
      console.error('WebSocket error:', error);
    }
  });

  function handleWebSocketMessage(message: WebSocketMessage) {
    console.log('Received WebSocket message:', message);

    // Handle function calls (analysis steps)
    if (message.parts) {
      message.parts.forEach((part: MessagePart) => {
        if (part.type === 'function_call' && selectedAnalysis) {
          const stepId = mapFunctionCallToStep(part.data.name);
          updateAnalysisStep(selectedAnalysis.id, stepId, 'running', 50);
        } else if (part.type === 'function_response' && selectedAnalysis) {
          const stepId = mapFunctionCallToStep(part.data.name);
          updateAnalysisStep(selectedAnalysis.id, stepId, 'completed', 100);
          
          // Store results
          updateAnalysisResults(selectedAnalysis.id, part.data.name, part.data.response);
        }
      });
    }

    // Handle text responses
    if (message.output_transcription && message.output_transcription.is_final) {
      const newMessage: ChatMessage = {
        id: `msg-${Date.now()}`,
        type: 'assistant',
        content: message.output_transcription.text,
        timestamp: new Date(),
        analysis_id: selectedAnalysis?.id
      };
      setChatMessages(prev => [...prev, newMessage]);
    }

    // Handle analysis completion
    if (message.turn_complete && selectedAnalysis) {
      setAnalyses(prev => prev.map(analysis => 
        analysis.id === selectedAnalysis.id 
          ? { ...analysis, status: 'completed' as const }
          : analysis
      ));
      setIsStartingAnalysis(false);
    }
  }

  const updateAnalysisStep = (analysisId: string, stepId: string, status: 'pending' | 'running' | 'completed' | 'error', progress: number) => {
    setAnalyses(prev => prev.map(analysis => {
      if (analysis.id === analysisId) {
        const updatedSteps = updateStepProgress(analysis.steps, stepId, status, progress);
        return { ...analysis, steps: updatedSteps };
      }
      return analysis;
    }));

    if (selectedAnalysis?.id === analysisId) {
      setSelectedAnalysis(prev => {
        if (!prev) return null;
        const updatedSteps = updateStepProgress(prev.steps, stepId, status, progress);
        return { ...prev, steps: updatedSteps };
      });
    }
  };

  const updateAnalysisResults = (analysisId: string, functionName: string, result: any) => {
    setAnalyses(prev => prev.map(analysis => {
      if (analysis.id === analysisId) {
        const updatedResults = { ...analysis.results };
        
        if (functionName.includes('html_content')) {
          updatedResults.htmlContent = result;
        } else if (functionName.includes('seo')) {
          updatedResults.seoAnalysis = result;
        } else if (functionName.includes('image')) {
          updatedResults.imageGeneration = result;
        }
        
        return { ...analysis, results: updatedResults };
      }
      return analysis;
    }));

    if (selectedAnalysis?.id === analysisId) {
      setSelectedAnalysis(prev => {
        if (!prev) return null;
        const updatedResults = { ...prev.results };
        
        if (functionName.includes('html_content')) {
          updatedResults.htmlContent = result;
        } else if (functionName.includes('seo')) {
          updatedResults.seoAnalysis = result;
        } else if (functionName.includes('image')) {
          updatedResults.imageGeneration = result;
        }
        
        return { ...prev, results: updatedResults };
      });
    }
  };

  const handleStartAnalysis = useCallback(async (url: string) => {
    setIsStartingAnalysis(true);
    
    const newAnalysis: Analysis = {
      id: `analysis-${Date.now()}`,
      url,
      title: new URL(url).hostname,
      status: 'running',
      createdAt: new Date(),
      steps: createInitialSteps(),
      results: {}
    };

    setAnalyses(prev => [newAnalysis, ...prev]);
    setSelectedAnalysis(newAnalysis);
    setIsNewAnalysisModalOpen(false);
    setChatMessages([]);

    // Connect to WebSocket if not connected
    if (!isConnected) {
      connect();
    }

    // Send analysis request
    const analysisPrompt = `Please analyze the website: ${url}. Extract HTML content, perform SEO analysis, and generate image optimization suggestions.`;
    
    setTimeout(() => {
      sendTextMessage(analysisPrompt);
    }, 1000);
  }, [isConnected, connect, sendTextMessage]);

  const handleSendChatMessage = useCallback((message: string) => {
    if (!isConnected || !selectedAnalysis) return;

    const newMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      type: 'user',
      content: message,
      timestamp: new Date(),
      analysis_id: selectedAnalysis.id
    };

    setChatMessages(prev => [...prev, newMessage]);
    sendTextMessage(message);
  }, [isConnected, selectedAnalysis, sendTextMessage]);

  const isAnalysisRunning = selectedAnalysis?.status === 'running' || isStartingAnalysis;

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      
      <div className="flex h-[calc(100vh-80px)]">
        <Sidebar
          analyses={analyses}
          selectedAnalysis={selectedAnalysis}
          onSelectAnalysis={setSelectedAnalysis}
          onNewAnalysis={() => setIsNewAnalysisModalOpen(true)}
        />
        
        <main className="flex-1 p-6 overflow-y-auto">
          {selectedAnalysis ? (
            <div className="space-y-6">
              {/* Analysis Steps */}
              <AnalysisSteps steps={selectedAnalysis.steps} />
              
              {/* Results */}
              {selectedAnalysis.status === 'completed' && selectedAnalysis.results && (
                <AnalysisResults 
                  results={selectedAnalysis.results} 
                  url={selectedAnalysis.url}
                />
              )}
              
              {/* Chat Interface */}
              <ChatInterface
                messages={chatMessages}
                onSendMessage={handleSendChatMessage}
                isConnected={isConnected}
                isAnalysisRunning={isAnalysisRunning}
              />
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="bg-gray-200 rounded-full p-8 mb-4 inline-block">
                  <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Welcome to PubTender
                </h3>
                <p className="text-gray-600 mb-6">
                  Start by creating a new analysis to analyze any website for SEO optimization.
                </p>
                <button
                  onClick={() => setIsNewAnalysisModalOpen(true)}
                  className="btn-primary"
                >
                  Create New Analysis
                </button>
              </div>
            </div>
          )}
        </main>
      </div>

      <NewAnalysisModal
        isOpen={isNewAnalysisModalOpen}
        onClose={() => setIsNewAnalysisModalOpen(false)}
        onStartAnalysis={handleStartAnalysis}
        isLoading={isStartingAnalysis}
      />
    </div>
  );
};

export default App;
