import React, { useState, useCallback, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import AnalysisSteps from './components/AnalysisSteps';
import ChatInterface from './components/ChatInterface';
import NewAnalysisModal from './components/NewAnalysisModal';
import Dashboard from './components/Dashboard';
import DashboardPreview from './components/DashboardPreview';
import { Analysis, AnalysisContent, ChatMessage } from './types';
import { createInitialSteps } from './utils/analysisSteps';
const API_BASE_URL = 'http://localhost:8501';

export const createSession = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/apps/app/users/user/sessions`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'tr,tr-TR',
        'Connection': 'keep-alive'
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Failed to create session:', response.status, errorText);
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // The POST request should return the new session object directly.
    const newSession = await response.json();
    if (!newSession || !newSession.id) {
      console.error('Invalid session object received:', newSession);
      throw new Error('Invalid session object received from API');
    }

    return newSession;
  } catch (error) {
    console.error('Error in createSession:', error);
    throw error;
  }
};

export interface ChatService {
  sendMessage: (
    message: string,
    sessionId: string,
    onMessage: (response: any) => void,
    onComplete: () => void,
    onError: (error: string) => void,
    onAgentChange: (agentName: string) => void
  ) => void;
}

export const createChatService = (): ChatService => {
  const sendMessage = async (
    message: string,
    sessionId: string,
    onMessage: (response: any) => void,
    onComplete: () => void,
    onError: (error: string) => void,
  ) => {
    try {
      const requestBody = {
        appName: "app",
        userId: "user",
        sessionId: sessionId,
        newMessage: {
          role: "user",
          parts: [{ text: message }]
        },
        streaming: true
      };

      const response = await fetch(`${API_BASE_URL}/run_sse`, {
        method: 'POST',
        headers: {
          'Accept': 'text/event-stream',
          'Accept-Language': 'tr,tr-TR;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
          'Connection': 'keep-alive',
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Handle Server-Sent Events streaming response
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('Failed to get response reader');
      }

      const decoder = new TextDecoder();
      let buffer = '';
      let finalResponse = '';

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6); // Remove 'data: ' prefix
              if (data === '[DONE]') {
                // End of stream
                if (finalResponse) {
                  onMessage(finalResponse);
                }
                onComplete();
                return;
              }
              try {
                const parsedData = JSON.parse(data);
                if (parsedData.content) {
                  // Stream chunk - accumulate the response
                  finalResponse += parsedData.content;
                } else if (parsedData.message) {
                  // Complete message
                  finalResponse = parsedData.message;
                }
              } catch (parseError) {
                // If JSON parsing fails, treat as plain text
                finalResponse += data;
              }
            }
          }
        }

        // If we reach here without [DONE], send accumulated response
        if (finalResponse) {
          onMessage(finalResponse);
        }
        onComplete();
      } finally {
        reader.releaseLock();
      }
    } catch (error) {
      console.error('API call failed:', error);
      onError(error instanceof Error ? error.message : 'Bir hata oluştu');
    }
  };

  return { sendMessage };
};

const App: React.FC = () => {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [selectedAnalysis, setSelectedAnalysis] = useState<Analysis | null>(null);
  const [isNewAnalysisModalOpen, setIsNewAnalysisModalOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isStartingAnalysis, setIsStartingAnalysis] = useState(false);
  const [isAnalysisRunning, setIsAnalysisRunning] = useState(false);
  const [isPreviewMode, setIsPreviewMode] = useState(false);


  // Generate unique session ID for this user session
  const [sessionId, setSessionId] = useState<string | null>(null);
  const fetchSession = async () => {
    const session = await createSession();
    setSessionId(session.id);
  };
  useEffect(() => {
    fetchSession();
  }, []);

  const chatService = createChatService();

  function handleMessage(message: string) {
    setIsAnalysisRunning(false);
    console.log('Received WebSocket message:', message);

    const newMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      type: 'assistant',
      content: message,
      timestamp: new Date(),
      analysis_id: selectedAnalysis?.id
    };
    setChatMessages(prev => [...prev, newMessage]);
  } 


  const handleAnalysisComplete = (response: AnalysisContent) => {
    setIsAnalysisRunning(false);
    console.log('Analysis complete:', response);

    // const analysis = JSON.parse(response);
    setSelectedAnalysis(prev => ({ ...prev, status: 'completed', result:response } as Analysis));
    setIsStartingAnalysis(false);
  }


  const handleStartAnalysis = useCallback(async (url: string) => {
    if (!sessionId) {
      await fetchSession();
      if (!sessionId) {
        console.error('Failed to establish session');
        return;
      }
    }

    setIsStartingAnalysis(true);
    
    const newAnalysis: Analysis = {
      id: `analysis-${Date.now()}`,
      url,
      title: new URL(url).hostname,
      status: 'running',
      createdAt: new Date(),
      steps: createInitialSteps(),
      result: undefined
    };

    setAnalyses(prev => [newAnalysis, ...prev]);
    setSelectedAnalysis(newAnalysis);
    setIsNewAnalysisModalOpen(false);
    setChatMessages([]);

    // Send analysis request
    const analysisPrompt = `Please analyze the website: ${url}. Extract HTML content, perform SEO analysis, and generate image optimization suggestions.`;
    
    chatService.sendMessage(analysisPrompt, sessionId, handleAnalysisComplete, () => {}, () => {}, () => {});
  }, [sessionId, fetchSession]);

  const handleSendChatMessage = useCallback((message: string) => {
    // if (!isConnected || !selectedAnalysis) return;
    if (!selectedAnalysis) return;

    const newMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      type: 'user',
      content: message,
      timestamp: new Date(),
      analysis_id: selectedAnalysis.id
    };

    setChatMessages(prev => [...prev, newMessage]);
    // sendTextMessage(message);
    chatService.sendMessage(message, sessionId!, handleMessage, () => {}, () => {}, () => {});
    setIsAnalysisRunning(true);
  }, [selectedAnalysis]);

  if (isPreviewMode) {
    return (
      <div className="min-h-screen bg-gray-100">
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <h1 className="text-xl font-semibold">Dashboard Preview Mode</h1>
            <button
              onClick={() => setIsPreviewMode(false)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Exit Preview
            </button>
          </div>
        </div>
        <DashboardPreview />
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      
      {/* Preview Mode Toggle Button */}
      {/* <div className="bg-white border-b border-gray-200 px-6 py-2">
        <button
          onClick={() => setIsPreviewMode(true)}
          className="text-sm px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
        >
          🎨 Preview Dashboard
        </button>
      </div> */}
      
      <div className="flex h-[calc(100vh-120px)]">
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
              
              {/* Results Dashboard */}
              {selectedAnalysis.status === 'completed' && selectedAnalysis.result && (
                <Dashboard 
                  result={selectedAnalysis!.result!} 
                  url={selectedAnalysis.url}
                />
              )}
              <div>
                {JSON.stringify(selectedAnalysis)}
              </div>
              {/* Chat Interface */}
              <ChatInterface
                messages={chatMessages}
                onSendMessage={handleSendChatMessage}
                isConnected={sessionId !== null}
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
