# PubTender - SEO Analysis Tool

PubTender, Google Agent Development Kit (ADK) kullanarak geliştirilmiş kapsamlı bir SEO analiz aracıdır. Web sitelerini analiz ederek SEO uyumluluğunu kontrol eder, içerik önerilerinde bulunur ve görsel optimizasyonu sağlar.

## 🚀 Özellikler

- **Web Crawler**: Web sitelerinden HTML içerik çıkarımı
- **Content Analyzer**: SEO analizi ve anahtar kelime çıkarımı  
- **Competitor Analysis**: Görsel optimizasyonu ve alt metin önerileri
- **Real-time Chat**: Analiz sonuçları hakkında sohbet edebilme
- **Modern UI**: React + TypeScript ile geliştirilmiş kullanıcı dostu arayüz

## 📋 Gereksinimler

- Python 3.9+
- Node.js 18+
- Google Cloud Project (ADK için)
- uv package manager

## 🛠️ Kurulum

### 1. Python Dependencies (Backend)
```bash
make install
```

### 2. Client Dependencies (Frontend)
```bash
make install-client
```

### 3. Environment Variables
`.env` dosyası oluşturun:
```env
APP_NAME=pubtender
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## 🏃‍♂️ Çalıştırma

### Tam Stack (Önerilen)
```bash
make dev
```
Bu komut hem backend (port 8000) hem de frontend (port 3000) servislerini başlatır.

### Sadece Backend
```bash
make server
```

### Sadece Frontend
```bash
make client
```

### Google ADK Playground (Orijinal)
```bash
make playground
```

## 🏗️ Proje Yapısı

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
├── server/                # FastAPI Backend
│   ├── main.py           # FastAPI server
│   └── requirements.txt
└── deployment/           # Terraform configurations
```

## 🔧 API Endpoints

### WebSocket
- `ws://localhost:8000/ws/{user_id}` - Real-time communication

### REST
- `GET /` - API information
- `GET /health` - Health check

## 💬 Kullanım

1. **New Analysis** butonuna tıklayın
2. Analiz etmek istediğiniz web sitesinin URL'sini girin
3. Analiz adımlarını takip edin:
   - Web Crawler: HTML içerik çıkarımı
   - Content Analyzer: SEO analizi
   - Competitor Analysis: Görsel optimizasyonu
4. Analiz tamamlandığında sonuçları görüntüleyin
5. Chat arayüzü ile agent'a sorular sorun

## 🧪 Test

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

PubTender, Google ADK'nın agent-based architecture'ını kullanır:

- **Root Agent**: Ana koordinatör agent
- **HTML Content Extractor**: Web sayfalarından içerik çıkarır
- **Image Generator**: Görsel optimizasyonu ve alt metin üretimi
- **Content SEO Ruler**: SEO kuralları kontrolü (geliştirme aşamasında)

Frontend, WebSocket üzerinden real-time olarak backend ile iletişim kurar ve analiz adımlarını takip eder.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🆘 Support

Issues ve feature requests için GitHub Issues kullanın.