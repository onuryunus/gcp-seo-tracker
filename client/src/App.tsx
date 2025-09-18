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
        streaming: false
      };

      // const response = await fetch(`${API_BASE_URL}/run`, {
      //   method: 'POST',
      //   headers: {
      //     'Accept': 'text/application/json',
      //     'Accept-Language': 'tr,tr-TR;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
      //     'Connection': 'keep-alive',
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(requestBody)
      // });

      // if (!response.ok) {
      //   throw new Error(`HTTP error! status: ${response.status}`);
      // }

      // // Response is a list of messages, last message's content.parts.text is the response we are looking for
      // const messages = await response.json();
      // const lastMessage = messages[messages.length - 1];
      // const responseText = lastMessage.content.parts[0].text;
      
      const response: AnalysisContent = {"status": "success", "url": "https://commencis.com", "seo_score": 89, "total_checks": 9, "passed_checks": 4, "issues": ["Meta description too long (164 characters)", "Multiple H1 tags (3 count)", "Paragraphs too short (average 13.7 words)", "commencis keyword too dense (3.7%)", "digital keyword too dense (3.38%)", "experience keyword too dense (3.22%)", "Internal links count low (1 count)"], "recommendations": ["Meta description should be at most 160 characters", "Page should have only one H1 tag", "Paragraphs should contain at least 20 words", "Keep keyword density between 1-3%", "Add at least 3 internal links"], "keywords": [{"word": "commencis", "count": 23, "percentage": 3.7}, {"word": "digital", "count": 21, "percentage": 3.38}, {"word": "experience", "count": 20, "percentage": 3.22}, {"word": "transformation", "count": 11, "percentage": 1.77}, {"word": "cloud", "count": 9, "percentage": 1.45}, {"word": "partnered", "count": 8, "percentage": 1.29}, {"word": "intelligent", "count": 6, "percentage": 0.96}, {"word": "app", "count": 6, "percentage": 0.96}, {"word": "software", "count": 6, "percentage": 0.96}, {"word": "performance", "count": 6, "percentage": 0.96}, {"word": "infrastructure", "count": 5, "percentage": 0.8}, {"word": "banking", "count": 5, "percentage": 0.8}, {"word": "enhancing", "count": 5, "percentage": 0.8}, {"word": "strategy", "count": 4, "percentage": 0.64}, {"word": "designsoftware", "count": 4, "percentage": 0.64}, {"word": "engineeringproduct", "count": 4, "percentage": 0.64}, {"word": "managementai", "count": 4, "percentage": 0.64}, {"word": "datacloud", "count": 4, "percentage": 0.64}, {"word": "financeinsurancetravel", "count": 4, "percentage": 0.64}, {"word": "airlinesretail", "count": 4, "percentage": 0.64}], "detailed_report": "SEO Technical Audit Report\n========================================\nURL: https://commencis.com\nSEO Score: 44/100\nStatus: Poor\n\n🔑 KEYWORDS ANALYSIS (MANDATORY):\n1. commencis: 23 occurrences (3.7% density) - Primary\n2. digital: 21 occurrences (3.38% density) - Secondary\n3. experience: 20 occurrences (3.22% density) - Secondary\n4. transformation: 11 occurrences (1.77% density) - Secondary\n5. cloud: 9 occurrences (1.45% density) - Secondary\n6. partnered: 8 occurrences (1.29% density) - Supporting\n7. intelligent: 6 occurrences (0.96% density) - Supporting\n8. app: 6 occurrences (0.96% density) - Supporting\n9. software: 6 occurrences (0.96% density) - Supporting\n10. performance: 6 occurrences (0.96% density) - Supporting\n11. infrastructure: 5 occurrences (0.8% density) - Supporting\n12. banking: 5 occurrences (0.8% density) - Supporting\n13. enhancing: 5 occurrences (0.8% density) - Supporting\n14. strategy: 4 occurrences (0.64% density) - Supporting\n15. designsoftware: 4 occurrences (0.64% density) - Supporting\n16. engineeringproduct: 4 occurrences (0.64% density) - Supporting\n17. managementai: 4 occurrences (0.64% density) - Supporting\n18. datacloud: 4 occurrences (0.64% density) - Supporting\n19. financeinsurancetravel: 4 occurrences (0.64% density) - Supporting\n20. airlinesretail: 4 occurrences (0.64% density) - Supporting\n\n📊 AUDIT SUMMARY:\n- Total Checks Performed: 9\n- Passed Tests: 4\n- Failed Tests: 5\n- Warnings: 0\n\n🚨 SEO ISSUES FOUND (Each as individual bullet):\n• Meta description too long (164 characters)\n• Multiple H1 tags (3 count)\n• Paragraphs too short (average 13.7 words)\n• 'commencis' keyword too dense (3.7%)\n• 'digital' keyword too dense (3.38%)\n• 'experience' keyword too dense (3.22%)\n• Internal links count low (1 count)\n\n✅ PASSED SEO TESTS (Each as individual bullet):\n• Title tag length optimal (48 characters) - Within recommended 30-60 character range\n• H1 tag contains content - Good for topical relevance\n• Images with alt text (60 out of 65) - Meets accessibility and SEO requirements\n• Content length sufficient (1239 words) - Meets minimum content requirements\n\n💡 OPTIMIZATION RECOMMENDATIONS (Prioritized):\n• HIGH PRIORITY: Write meta description (120-160 characters) including primary keyword 'commencis' and compelling CTA\n• HIGH PRIORITY: Page should have only one H1 tag\n• MEDIUM PRIORITY: Paragraphs should contain at least 20 words\n• MEDIUM PRIORITY: Keep keyword density between 1-3%\n• LOW PRIORITY: Add at least 3 internal links\n\n📝 TECHNICAL DETAILS:\n- Title: Present - 48 characters - Contains primary keyword 'commencis'\n- Meta Description: Present - 164 characters - Contains primary keyword 'commencis'\n- H1 Tags: 3 count - Issue: 3\n- H2-H6 Tags: H2(13), H3(16), H4(0), H5(0), H6(0)\n- Images: 65 total, 60 with alt text (92.3% coverage)\n- Internal Links: 1 count - Insufficient: <3\n- Content Length: 1239 words - Sufficient: 300+\n- Keyword Density: Primary 'commencis' (3.7%), Secondary 'digital' (3.38%)", "page_info": {"title": "Commence your next digital evolution - Commencis", "meta_description": "Commencis drives AI-powered digital transformation for enterprises through experience design, intelligent custom software development, and scalable cloud solutions.", "word_count": 1239, "headings_count": {"h1": 3, "h2": 13, "h3": 16, "h4": 0}, "images_total": 65, "images_with_alt": 60}}
      onMessage(response);
      onComplete();
      return;
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
