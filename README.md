# PubTender - SEO Analysis Tool

PubTender is a comprehensive SEO analysis tool developed using Google Agent Development Kit (ADK). It analyzes websites to check SEO compliance, provides content recommendations, and offers visual optimization.

## 🚀 Features

- **Web Crawler**: HTML content extraction from websites
- **Content Analyzer**: SEO analysis and keyword extraction  
- **Competitor Analysis**: Visual optimization and alt text suggestions
- **Real-time Chat**: Interactive chat about analysis results
- **Modern UI**: User-friendly interface built with React + TypeScript

## 📋 Requirements

- Python 3.9+
- Node.js 18+
- Google Cloud Project (for ADK)
- uv package manager

## 🛠️ Installation

### 1. Python Dependencies (Backend)
```bash
make install
```

### 2. Client Dependencies (Frontend)
```bash
make install-client
```

### 3. Environment Variables
Create a `.env` file:
```env
APP_NAME=pubtender
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## 🏃‍♂️ Running

### Full Stack (Recommended)
```bash
make dev
```
This command starts both backend (port 8000) and frontend (port 3000) services.

### Backend Only
```bash
make playground
```

### Frontend Only
```bash
cd client & npm run dev
```

## 🏗️ Project Structure

```
pubtender/
├── app/                    # Agent definitions (Google ADK)
│   ├── agent.py           # Root agent
│   ├── sub_agents/        # Sub-agents
│   │   ├── html_content_extractor/
│   │   ├── image_generator/
│   │   └── content_seo_ruler/
│   └── utils/             # Utility functions
├── client/                # React TypeScript Frontend
│   ├── src/
│   │   ├── components/    # UI Components
│   │   ├── hooks/         # Custom hooks
│   │   ├── types/         # TypeScript definitions
│   │   └── utils/         # Utility functions
│   └── package.json
└── deployment/           # Terraform configurations
```

## 🔧 API Endpoints

### WebSocket
- `ws://localhost:8000/ws/{user_id}` - Real-time communication

### REST
- `GET /` - API information
- `GET /health` - Health check

## 💬 Usage

1. Click the **New Analysis** button
2. Enter the URL of the website you want to analyze
3. Follow the analysis steps:
   - Web Crawler: HTML content extraction
   - Content Analyzer: SEO analysis
   - Competitor Analysis: Visual optimization
4. View the results when analysis is complete
5. Ask questions to the agent through the chat interface

## 🧪 Testing

```bash
make test
```

## 🔍 Code Quality

```bash
make lint
```

## 🚀 Deployment

### Development Environment
```bash
make setup-dev-env
```

### Production
```bash
make backend
```

## 🏗️ Architecture

PubTender uses Google ADK's agent-based architecture:

- **Root Agent**: Main coordinator agent
- **HTML Content Extractor**: Extracts content from web pages
- **Image Generator**: Visual optimization and alt text generation
- **Content SEO Ruler**: SEO rules checking (in development)

The frontend communicates with the backend in real-time via WebSocket and tracks analysis steps.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🆘 Support

Use GitHub Issues for issues and feature requests.