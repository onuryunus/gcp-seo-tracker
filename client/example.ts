// Generate a unique GUID for session
export const generateGUID = (): string => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  };
  
  // API configuration
  const API_BASE_URL = '/flywithme/api';
  const API_AUTH = 'Basic Y29tbWVuY2lzOkNWVUJBYTZJM0RYTVd0ag==';
  
  export const createSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/apps/travel_concierge/users/user/sessions`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Accept-Language': 'tr,tr-TR',
          'Authorization': API_AUTH,
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
  
  export interface ChatResponse {
    content?: {
      parts: Array<{ text?: string; functionCall?: { args: { agent_name?: string }, name: string } }>;
      role: string;
    };
    partial: boolean;
    invocationId?: string;
    author?: string;
    error?: string;
  }
  
  export interface StreamingChatService {
    sendMessage: (
      message: string,
      sessionId: string,
      onMessage: (response: string) => void,
      onComplete: () => void,
      onError: (error: string) => void,
      onAgentChange: (agentName: string) => void
    ) => void;
  }
  
  export const createStreamingChatService = (): StreamingChatService => {
    const sendMessage = async (
      message: string,
      sessionId: string,
      onMessage: (response: string) => void,
      onComplete: () => void,
      onError: (error: string) => void,
      onAgentChange: (agentName: string) => void
    ) => {
      try {
        const requestBody = {
          appName: "travel_concierge",
          userId: "user",
          sessionId: sessionId,
          newMessage: {
            role: "user",
            parts: [{ text: message }]
          },
          streaming: false
        };
  
        const response = await fetch(`${API_BASE_URL}/run_sse`, {
          method: 'POST',
          headers: {
            'Accept': 'text/event-stream',
            'Accept-Language': 'tr,tr-TR;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
            'Authorization': API_AUTH,
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody)
        });
  
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
  
        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error('Response body is not readable');
        }
  
        const decoder = new TextDecoder();
        let buffer = '';
  
        let lastMessageText = '';
        try {
          while (true) {
            const { done, value } = await reader.read();
  
            if (done) {
              onComplete();
              break;
            }
  
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';
  
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const jsonData = line.slice(6); // Remove 'data: ' prefix
                  const parsedData: ChatResponse = JSON.parse(jsonData);
  
                  // If the stream sends an error payload, surface it and stop processing
                  console.log('Parsed SSE data:', parsedData);
                  if ((parsedData as any).error || (parsedData as any).error === '') {
                    throw new Error((parsedData as any).error);
                  }
  
                  if (parsedData.content && parsedData.content.parts) {
                    for (const part of parsedData.content.parts) {
                      // Check for agent change
                      if (part.functionCall && part.functionCall.args && (part.functionCall.args.agent_name || part.functionCall.name)) {
                        onAgentChange(part.functionCall.args.agent_name || part.functionCall.name);
                      }
  
                      // Check if this is a message with text content
                      if (part.text) {
                        const messageText = part.text;
  
                        if (messageText && messageText.trim()) {
                          // Only send the new part (difference) if messageText is an extension of lastMessageText
                          if (messageText.startsWith(lastMessageText)) {
                            const newPart = messageText.slice(lastMessageText.length);
  
                            if (newPart) {
                              onMessage(newPart);
                            }
                          } else if (messageText !== lastMessageText) {
                            // If it's completely different content, send it
                            onMessage(messageText);
                          }
                          lastMessageText = messageText;
                        }
                      }
                    }
                  }
                } catch (parseError) {
                  console.warn('Failed to parse SSE data:', parseError);
                  const errMsg = parseError instanceof Error ? parseError.message : 'Failed to parse SSE data';
                  throw new Error(errMsg);
                }
              }
            }
          }
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
   