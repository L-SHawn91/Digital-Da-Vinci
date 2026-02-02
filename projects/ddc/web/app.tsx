"""
React Frontend - SHawn-Brain 대시보드

파일: ddc/web/frontend/app.tsx

구조:
- Header: 제목 & 신경계 상태
- Sidebar: 카트리지 네비게이션
- MainContent: 분석 결과 표시
- RightPanel: 통계 & 모니터링
- Footer: 정보

설치:
npm create vite@latest shawn-brain-web -- --template react-ts
cd shawn-brain-web
npm install axios react-router-dom zustand

실행:
npm run dev
"""

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

// ============================================================================
// 1. API 클라이언트
// ============================================================================

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

// ============================================================================
// 2. 타입 정의
// ============================================================================

interface NeuralHealth {
  brainstem: number;
  limbic: number;
  neocortex: number;
  neuronet: number;
  avg: number;
}

interface BioAnalysis {
  status: string;
  cell_type: string;
  health_status: string;
  confidence: number;
  neocortex_features: Record<string, number>;
  timestamp: string;
}

interface InvAnalysis {
  status: string;
  ticker: string;
  technical_score: number;
  fundamental_score: number;
  recommendation: string;
  neocortex_decision: Record<string, number>;
  timestamp: string;
}

// ============================================================================
// 3. Header 컴포넌트
// ============================================================================

const Header: React.FC<{ neuralHealth: NeuralHealth }> = ({ neuralHealth }) => (
  <header className="header">
    <div className="header-content">
      <h1>🧠 SHawn-Brain</h1>
      <p>Digital Leonardo da Vinci Project</p>
    </div>
    <div className="neural-status">
      <div className="status-badge">
        <span className="status-light">🟢</span>
        <span className="status-text">신경계 정상</span>
      </div>
      <div className="health-bar">
        <div 
          className="health-fill" 
          style={{ width: `${neuralHealth.avg * 100}%` }}
        >
          {Math.round(neuralHealth.avg * 100)}%
        </div>
      </div>
    </div>
  </header>
);

// ============================================================================
// 4. Sidebar 컴포넌트
// ============================================================================

const Sidebar: React.FC<{
  activeCartridge: string;
  onSelectCartridge: (name: string) => void;
}> = ({ activeCartridge, onSelectCartridge }) => (
  <aside className="sidebar">
    <nav className="cartridge-menu">
      <h3>📦 카트리지</h3>
      {[
        { name: 'bio', icon: '🧬', label: 'Bio (생물)' },
        { name: 'inv', icon: '💰', label: 'Inv (투자)' },
        { name: 'lit', icon: '📚', label: 'Lit (문학)' },
        { name: 'quant', icon: '📊', label: 'Quant (정량)' },
        { name: 'astro', icon: '🌌', label: 'Astro (천문)' }
      ].map(cartridge => (
        <button
          key={cartridge.name}
          className={`menu-item ${activeCartridge === cartridge.name ? 'active' : ''}`}
          onClick={() => onSelectCartridge(cartridge.name)}
        >
          <span className="icon">{cartridge.icon}</span>
          <span className="label">{cartridge.label}</span>
          <span className="status">🟢</span>
        </button>
      ))}
    </nav>
    
    <div className="sidebar-info">
      <h4>신경계 레벨</h4>
      <div className="level-item">
        <span>L1 뇌간</span>
        <span className="level-value">95%</span>
      </div>
      <div className="level-item">
        <span>L2 변린계</span>
        <span className="level-value">93%</span>
      </div>
      <div className="level-item">
        <span>L3 신피질</span>
        <span className="level-value">94%</span>
      </div>
      <div className="level-item">
        <span>L4 신경망</span>
        <span className="level-value">98%</span>
      </div>
    </div>
  </aside>
);

// ============================================================================
// 5. MainContent 컴포넌트
// ============================================================================

const MainContent: React.FC<{ activeCartridge: string }> = ({ activeCartridge }) => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<BioAnalysis | InvAnalysis | null>(null);
  const [input, setInput] = useState('');

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      if (activeCartridge === 'bio') {
        const response = await api.post<BioAnalysis>('/api/bio/analyze_image', {
          image_path: input,
          use_neocortex: true
        });
        setResult(response.data);
      } else if (activeCartridge === 'inv') {
        const response = await api.post<InvAnalysis>('/api/inv/analyze_stock', {
          ticker: input,
          use_neocortex: true
        });
        setResult(response.data);
      }
    } catch (error) {
      console.error('분석 오류:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="main-content">
      <div className="analysis-panel">
        <h2>{activeCartridge === 'bio' ? '🧬 세포 분석' : '💰 주식 분석'}</h2>
        
        <div className="input-group">
          <input
            type="text"
            placeholder={activeCartridge === 'bio' ? '이미지 경로 입력' : '종목 코드 입력 (TSLA, 005930)'}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
            className="input-field"
          />
          <button 
            onClick={handleAnalyze} 
            disabled={loading}
            className="analyze-button"
          >
            {loading ? '분석 중...' : '분석'}
          </button>
        </div>

        {result && (
          <div className="result-panel">
            <h3>📊 분석 결과</h3>
            
            {'cell_type' in result ? (
              // Bio 결과
              <div className="bio-result">
                <div className="result-item">
                  <span>세포 종류:</span>
                  <span className="value">{result.cell_type}</span>
                </div>
                <div className="result-item">
                  <span>건강 상태:</span>
                  <span className="value">{result.health_status}</span>
                </div>
                <div className="result-item">
                  <span>신뢰도:</span>
                  <span className="value">{(result.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="neocortex-features">
                  <h4>신피질 특성</h4>
                  {Object.entries(result.neocortex_features).map(([key, val]) => (
                    <div key={key} className="feature-bar">
                      <span>{key}: {(val * 100).toFixed(1)}%</span>
                      <div className="bar">
                        <div className="fill" style={{ width: `${val * 100}%` }}></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              // Inv 결과
              <div className="inv-result">
                <div className="result-item">
                  <span>종목:</span>
                  <span className="value">{result.ticker}</span>
                </div>
                <div className="result-item">
                  <span>기술 점수:</span>
                  <span className="value">{(result.technical_score * 100).toFixed(1)}</span>
                </div>
                <div className="result-item">
                  <span>기본 점수:</span>
                  <span className="value">{(result.fundamental_score * 100).toFixed(1)}</span>
                </div>
                <div className="result-item">
                  <span>추천:</span>
                  <span className="value recommendation">{result.recommendation}</span>
                </div>
                <div className="neocortex-decision">
                  <h4>신피질 의사결정</h4>
                  {Object.entries(result.neocortex_decision).map(([key, val]) => (
                    <div key={key} className="decision-item">
                      <span>{key}: {(val * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            <div className="timestamp">
              {new Date(result.timestamp).toLocaleString('ko-KR')}
            </div>
          </div>
        )}
      </div>
    </main>
  );
};

// ============================================================================
// 6. RightPanel 컴포넌트
// ============================================================================

const RightPanel: React.FC = () => {
  const [stats, setStats] = useState({ api_calls: 0, avg_health: 0 });
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // WebSocket 연결
    wsRef.current = new WebSocket('ws://localhost:8000/ws/neural_stream');
    
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStats({
        api_calls: data.api_calls.total || 0,
        avg_health: data.levels.avg || 0
      });
    };

    return () => wsRef.current?.close();
  }, []);

  return (
    <aside className="right-panel">
      <div className="stats-card">
        <h3>📈 통계</h3>
        <div className="stat-item">
          <span>API 호출</span>
          <span className="stat-value">{stats.api_calls}</span>
        </div>
        <div className="stat-item">
          <span>신경 건강도</span>
          <span className="stat-value">{(stats.avg_health * 100).toFixed(1)}%</span>
        </div>
      </div>

      <div className="models-card">
        <h3>🤖 활용 모델</h3>
        <div className="model-list">
          <div className="model-item">Gemini 2.5</div>
          <div className="model-item">Groq Llama</div>
          <div className="model-item">Claude 3.5</div>
          <div className="model-item">DeepSeek</div>
          <div className="model-item">OpenRouter</div>
        </div>
      </div>

      <div className="info-card">
        <h3>ℹ️ 정보</h3>
        <div className="info-text">
          <p><strong>프로젝트:</strong></p>
          <p>Digital Leonardo da Vinci</p>
          <p><strong>버전:</strong> v5.1.0</p>
          <p><strong>상태:</strong> 🟢 Active</p>
        </div>
      </div>
    </aside>
  );
};

// ============================================================================
// 7. Footer 컴포넌트
// ============================================================================

const Footer: React.FC = () => (
  <footer className="footer">
    <div className="footer-content">
      <p>🧠 SHawn-Brain | Digital Leonardo da Vinci Project</p>
      <p>© 2026 Dr. SHawn Lee | MoltBot Assistant</p>
    </div>
  </footer>
);

// ============================================================================
// 8. App 메인 컴포넌트
// ============================================================================

export default function App() {
  const [activeCartridge, setActiveCartridge] = useState('bio');
  const [neuralHealth, setNeuralHealth] = useState<NeuralHealth>({
    brainstem: 0.95,
    limbic: 0.93,
    neocortex: 0.94,
    neuronet: 0.98,
    avg: 0.95
  });

  useEffect(() => {
    // 신경계 상태 주기적 업데이트
    const interval = setInterval(async () => {
      try {
        const response = await api.get('/api/neural/health');
        const levels = response.data.neural_levels;
        setNeuralHealth({
          brainstem: levels.L1_Brainstem.health,
          limbic: levels.L2_Limbic.health,
          neocortex: levels.L3_Neocortex.health,
          neuronet: levels.L4_NeuroNet.health,
          avg: response.data.average_health
        });
      } catch (error) {
        console.error('상태 업데이트 오류:', error);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <Header neuralHealth={neuralHealth} />
      <div className="app-layout">
        <Sidebar activeCartridge={activeCartridge} onSelectCartridge={setActiveCartridge} />
        <MainContent activeCartridge={activeCartridge} />
        <RightPanel />
      </div>
      <Footer />
    </div>
  );
}
