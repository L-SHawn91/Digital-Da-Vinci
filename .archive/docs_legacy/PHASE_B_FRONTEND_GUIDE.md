# 🎨 Phase B Frontend 구현 가이드 (병렬 진행)

## 📋 개요

DCRS 모델 테스트 진행 중 **병렬로 Frontend 개발** 진행합니다.

- **Backend**: 2-3시간 예상
- **Frontend**: 1.5-2시간 예상  
- **병렬 진행**: 4-5시간 (순차 대비 40% 시간 절감)

---

## 🎨 Component 1: Header (15분)

### 목표
대시보드 상단 헤더 - 로고, 제목, 상태 표시기

### 파일 위치
`src/components/Header.tsx`

### 구현 코드
```tsx
import React, { useState, useEffect } from 'react';
import { Box, Typography, Chip } from '@mui/material';

export const Header: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [status, setStatus] = useState('🟢 Live');
  
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);
  
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        p: 2,
        bgcolor: '#1a1a2e',
        color: '#eee',
        borderBottom: '2px solid #00d4ff'
      }}
    >
      {/* 좌측: 로고 */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#00d4ff' }}>
          🧠 SHawn-Brain
        </Typography>
      </Box>
      
      {/* 중앙: 제목 */}
      <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
        Neural System Dashboard
      </Typography>
      
      {/* 우측: 상태 표시기 + 시간 */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Chip
          label={status}
          sx={{ bgcolor: '#00d4ff', color: '#000', fontWeight: 'bold' }}
        />
        <Typography sx={{ fontSize: '0.9rem', color: '#aaa' }}>
          {currentTime.toLocaleTimeString()}
        </Typography>
      </Box>
    </Box>
  );
};
```

### 스타일 포인트
- 어두운 배경 (#1a1a2e)
- 시안색 하이라이트 (#00d4ff)
- 반응형: `justifyContent: 'space-between'`

---

## 🎨 Component 2: Sidebar (20분)

### 목표
왼쪽 네비게이션 + 빠른 통계

### 파일 위치
`src/components/Sidebar.tsx`

### 구현 코드
```tsx
import React, { useState } from 'react';
import { Drawer, Box, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

interface SidebarProps {
  onMenuClick: (page: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onMenuClick }) => {
  const [selectedMenu, setSelectedMenu] = useState('overview');
  
  const menuItems = [
    { icon: '🏠', label: 'Overview', path: 'overview' },
    { icon: '🧠', label: 'Neural Activity', path: 'neural' },
    { icon: '📊', label: 'Performance', path: 'performance' },
    { icon: '🔧', label: 'Models', path: 'models' },
    { icon: '📈', label: 'Analytics', path: 'analytics' },
    { icon: '⚙️', label: 'Settings', path: 'settings' }
  ];
  
  const quickStats = [
    { label: 'Total APIs', value: '10/10', color: '#00ff00' },
    { label: 'Avg Score', value: '9.09/10', color: '#ffd700' },
    { label: 'Active', value: '100%', color: '#00d4ff' }
  ];
  
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 280,
        '& .MuiDrawer-paper': {
          width: 280,
          bgcolor: '#0f3460',
          color: '#eee'
        }
      }}
    >
      {/* 네비게이션 */}
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: '#00d4ff' }}>
          📋 Navigation
        </Typography>
        
        <List>
          {menuItems.map(item => (
            <ListItem
              button
              key={item.path}
              selected={selectedMenu === item.path}
              onClick={() => {
                setSelectedMenu(item.path);
                onMenuClick(item.path);
              }}
              sx={{
                mb: 1,
                borderRadius: 1,
                '&.Mui-selected': {
                  bgcolor: '#00d4ff',
                  color: '#000'
                }
              }}
            >
              <ListItemText primary={`${item.icon} ${item.label}`} />
            </ListItem>
          ))}
        </List>
      </Box>
      
      <Divider sx={{ bgcolor: '#444' }} />
      
      {/* 빠른 통계 */}
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2, color: '#00d4ff' }}>
          📊 Quick Stats
        </Typography>
        
        {quickStats.map(stat => (
          <Box key={stat.label} sx={{ mb: 1.5 }}>
            <Typography sx={{ fontSize: '0.85rem', color: '#aaa' }}>
              {stat.label}
            </Typography>
            <Typography sx={{ fontWeight: 'bold', color: stat.color }}>
              {stat.value}
            </Typography>
          </Box>
        ))}
      </Box>
    </Drawer>
  );
};
```

---

## 🎨 Component 3: Main Cards (25분)

### 목표
4개 통계 카드 (2x2 그리드)

### 파일 위치
`src/components/MainCards.tsx`

### 구현 코드
```tsx
import React from 'react';
import { Grid, Card, CardContent, Typography, Box } from '@mui/material';

interface CardData {
  title: string;
  value: string;
  icon: string;
  color: string;
  bgColor: string;
}

export const MainCards: React.FC = () => {
  const cards: CardData[] = [
    {
      title: '🥇 Best Model',
      value: 'Gemini',
      icon: '9.9/10',
      color: '#ffd700',
      bgColor: 'rgba(255, 215, 0, 0.1)'
    },
    {
      title: 'Status Summary',
      value: '10/10',
      icon: 'APIs Online',
      color: '#00ff00',
      bgColor: 'rgba(0, 255, 0, 0.1)'
    },
    {
      title: '📊 Avg Score',
      value: '9.09/10',
      icon: 'All Models',
      color: '#00d4ff',
      bgColor: 'rgba(0, 212, 255, 0.1)'
    },
    {
      title: '⏱️ System Health',
      value: '95%',
      icon: 'Healthy',
      color: '#ff6b9d',
      bgColor: 'rgba(255, 107, 157, 0.1)'
    }
  ];
  
  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      {cards.map((card, index) => (
        <Grid item xs={12} sm={6} key={index}>
          <Card
            sx={{
              bgcolor: card.bgColor,
              border: `2px solid ${card.color}`,
              boxShadow: `0 0 10px ${card.color}33`
            }}
          >
            <CardContent>
              <Typography sx={{ color: card.color, fontWeight: 'bold' }}>
                {card.title}
              </Typography>
              
              <Typography
                variant="h4"
                sx={{ my: 1, fontWeight: 'bold', color: card.color }}
              >
                {card.value}
              </Typography>
              
              <Typography sx={{ fontSize: '0.9rem', color: '#aaa' }}>
                {card.icon}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};
```

---

## 🎨 Component 4: Real-time Charts (35분)

### 목표
3개 차트 - 라인, 막대, 파이

### 파일 위치
`src/components/Charts.tsx`

### 구현 코드
```tsx
import React, { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface ChartData {
  labels: string[];
  datasets: any[];
}

export const Charts: React.FC = () => {
  const [performanceData, setPerformanceData] = useState<ChartData | null>(null);
  
  useEffect(() => {
    // WebSocket 연결 시뮬레이션 - 실제로는 WebSocket에서 받음
    const data: ChartData = {
      labels: ['08:00', '08:15', '08:30', '08:45', '09:00'],
      datasets: [
        {
          label: 'Gemini',
          data: [9.9, 9.8, 9.9, 9.9, 9.9],
          borderColor: '#ffd700',
          backgroundColor: 'rgba(255, 215, 0, 0.1)',
          borderWidth: 2,
          tension: 0.4
        },
        {
          label: 'Groq',
          data: [9.7, 9.6, 9.7, 9.7, 9.8],
          borderColor: '#00d4ff',
          backgroundColor: 'rgba(0, 212, 255, 0.1)',
          borderWidth: 2,
          tension: 0.4
        }
      ]
    };
    
    setPerformanceData(data);
  }, []);
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        labels: {
          color: '#eee'
        }
      }
    },
    scales: {
      y: {
        min: 8,
        max: 10,
        ticks: {
          color: '#aaa'
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      },
      x: {
        ticks: {
          color: '#aaa'
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      }
    }
  };
  
  return (
    <Box>
      {/* 라인 차트 */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'rgba(255, 255, 255, 0.05)', borderRadius: 2 }}>
        <Typography sx={{ fontWeight: 'bold', mb: 2, color: '#00d4ff' }}>
          📈 Model Performance (24h)
        </Typography>
        {performanceData && <Line data={performanceData} options={chartOptions} />}
      </Box>
      
      {/* 막대 그래프 */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'rgba(255, 255, 255, 0.05)', borderRadius: 2 }}>
        <Typography sx={{ fontWeight: 'bold', mb: 2, color: '#00d4ff' }}>
          ⏱️ Response Time
        </Typography>
        {performanceData && <Bar data={performanceData} options={chartOptions} />}
      </Box>
    </Box>
  );
};
```

### Chart.js 설치
```bash
npm install chart.js react-chartjs-2
```

---

## 🎨 Component 5: Right Sidebar (15분)

### 목표
알림, 최근 활동, 시스템 정보

### 파일 위치
`src/components/RightSidebar.tsx`

### 구현 코드
```tsx
import React from 'react';
import { Box, Typography, Paper, Divider, List, ListItem } from '@mui/material';

export const RightSidebar: React.FC = () => {
  const activities = [
    { time: '08:00', text: 'DCRS 자동 실행 완료 ✅' },
    { time: '08:05', text: 'Gemini: 9.9/10 최우선 🥇' },
    { time: '08:10', text: 'Daily Report 생성됨' }
  ];
  
  const alerts = [];
  
  const systemInfo = [
    { label: 'Version', value: 'v1.0.0' },
    { label: 'Uptime', value: '99.7%' },
    { label: 'Last Update', value: '08:00' }
  ];
  
  return (
    <Box
      sx={{
        width: 300,
        overflowY: 'auto',
        bgcolor: '#0f3460',
        color: '#eee',
        p: 2
      }}
    >
      {/* 최근 활동 */}
      <Paper sx={{ mb: 2, bgcolor: 'rgba(0, 212, 255, 0.1)', p: 2, border: '1px solid #00d4ff' }}>
        <Typography sx={{ fontWeight: 'bold', mb: 1, color: '#00d4ff' }}>
          🔔 Recent Activities
        </Typography>
        <List dense>
          {activities.map((activity, idx) => (
            <ListItem key={idx} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
              <Typography sx={{ fontSize: '0.8rem', color: '#aaa' }}>
                {activity.time}
              </Typography>
              <Typography sx={{ fontSize: '0.9rem' }}>
                {activity.text}
              </Typography>
            </ListItem>
          ))}
        </List>
      </Paper>
      
      <Divider sx={{ bgcolor: '#444', my: 1 }} />
      
      {/* 알림 */}
      <Paper sx={{ mb: 2, bgcolor: 'rgba(255, 107, 157, 0.1)', p: 2, border: '1px solid #ff6b9d' }}>
        <Typography sx={{ fontWeight: 'bold', mb: 1, color: '#ff6b9d' }}>
          ⚠️ Alerts
        </Typography>
        {alerts.length === 0 ? (
          <Typography sx={{ fontSize: '0.9rem', color: '#00ff00' }}>
            No alerts ✅
          </Typography>
        ) : (
          alerts.map((alert, idx) => (
            <Typography key={idx} sx={{ fontSize: '0.9rem' }}>
              {alert}
            </Typography>
          ))
        )}
      </Paper>
      
      <Divider sx={{ bgcolor: '#444', my: 1 }} />
      
      {/* 시스템 정보 */}
      <Paper sx={{ bgcolor: 'rgba(0, 255, 0, 0.1)', p: 2, border: '1px solid #00ff00' }}>
        <Typography sx={{ fontWeight: 'bold', mb: 1, color: '#00ff00' }}>
          ℹ️ System Information
        </Typography>
        {systemInfo.map((info, idx) => (
          <Box key={idx} sx={{ mb: 0.5 }}>
            <Typography sx={{ fontSize: '0.85rem', color: '#aaa' }}>
              {info.label}
            </Typography>
            <Typography sx={{ fontWeight: 'bold', color: '#00d4ff' }}>
              {info.value}
            </Typography>
          </Box>
        ))}
      </Paper>
    </Box>
  );
};
```

---

## 🔌 Main App Layout

### 파일 위치
`src/App.tsx`

### 구현 코드
```tsx
import React, { useState } from 'react';
import { Box } from '@mui/material';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { MainCards } from './components/MainCards';
import { Charts } from './components/Charts';
import { RightSidebar } from './components/RightSidebar';

export const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState('overview');
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', bgcolor: '#1a1a2e' }}>
      {/* Header */}
      <Header />
      
      {/* Main Content */}
      <Box sx={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        {/* Left Sidebar */}
        <Sidebar onMenuClick={setCurrentPage} />
        
        {/* Main Area */}
        <Box sx={{ flex: 1, overflowY: 'auto', p: 3 }}>
          {currentPage === 'overview' && (
            <>
              <MainCards />
              <Charts />
            </>
          )}
          {/* 다른 페이지 콘텐츠... */}
        </Box>
        
        {/* Right Sidebar */}
        <RightSidebar />
      </Box>
    </Box>
  );
};

export default App;
```

---

## 🚀 프로젝트 설정

### React 프로젝트 생성
```bash
npm create vite@latest shawn-web-dashboard -- --template react-ts
cd shawn-web-dashboard
npm install
```

### 필수 라이브러리 설치
```bash
npm install @mui/material @emotion/react @emotion/styled
npm install chart.js react-chartjs-2
npm install axios
npm install socket.io-client
```

### 실행
```bash
npm run dev
```

---

## 📊 폴더 구조
```
src/
├── components/
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── MainCards.tsx
│   ├── Charts.tsx
│   └── RightSidebar.tsx
├── hooks/
│   └── useWebSocket.ts
├── services/
│   └── api.ts
├── App.tsx
└── index.css
```

---

## ⏱️ 구현 타임라인

```
08:05-08:20: Component 1 (Header) - 15분 ✅
08:20-08:40: Component 2 (Sidebar) - 20분 ✅
08:40-09:05: Component 3 (Cards) - 25분 ✅
09:05-09:40: Component 4 (Charts) - 35분 ✅
09:40-09:55: Component 5 (RightSidebar) - 15분 ✅
09:55-10:30: Layout 통합 - 35분
10:30-11:00: WebSocket 통합 - 30분

총 3시간 (예상: 1.5-2시간 설계 + 1.5시간 구현)
```

---

## 🎯 다음 단계

1. ✅ 5개 컴포넌트 설계
2. 🔄 React 코드 구현 (1-1.5시간)
3. WebSocket 실시간 데이터 연결
4. 차트 애니메이션 추가
5. 반응형 레이아웃 최적화
6. 성능 튜닝

**병렬 진행으로 효율성 극대화!** 🚀
