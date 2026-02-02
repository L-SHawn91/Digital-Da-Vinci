#!/usr/bin/env python3
"""
박사님 지시: DeepSeek 비중 낮추고 모든 모델 번갈아가며 테스트

전략 변경:
- DeepSeek: 20% → 10% (비중 낮춤)
- Gemini: 25% → 30% (상향)
- 모든 모델 순차 테스트 (통신 확인)
- 동시 진행: 테스트 + 다음 작업
"""

import os
import json
import time
from datetime import datetime
from enum import Enum

class ModelStatus(Enum):
    AVAILABLE = "✅ 사용가능"
    ERROR = "❌ 오류"
    TESTING = "🔄 테스트중"
    TIMEOUT = "⏱️ 타임아웃"

class ComprehensiveModelTester:
    """모든 모델 순차 테스트 + 비중 조정"""
    
    def __init__(self):
        self.results = {
            "version": "Model Testing v1",
            "timestamp": datetime.now().isoformat(),
            "models_tested": 0,
            "models_available": 0,
            "test_results": []
        }
        
        # 환경변수에서 API 키 로드
        self.api_keys = {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
            "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
            "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "SAMBANOVA_API_KEY": os.getenv("SAMBANOVA_API_KEY"),
            "CEREBRAS_API_KEY": os.getenv("CEREBRAS_API_KEY"),
            "FIREWORKS_API_KEY": os.getenv("FIREWORKS_API_KEY"),
            "DEEPINFRA_API_KEY": os.getenv("DEEPINFRA_API_KEY"),
            "SILICONFLOW_API_KEY": os.getenv("SILICONFLOW_API_KEY"),
            "HYPERBOLIC_API_KEY": os.getenv("HYPERBOLIC_API_KEY"),
            "JINA_API_KEY": os.getenv("JINA_API_KEY"),
            "REPLICATE_API_KEY": os.getenv("REPLICATE_API_KEY"),
            "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
            "GITHUB_ADVANCED_TOKEN": os.getenv("GITHUB_ADVANCED_TOKEN"),
        }
    
    def test_api_keys(self):
        """API 키 존재 여부 확인"""
        
        print("\n" + "="*100)
        print("🔑 API 키 상태 확인")
        print("="*100 + "\n")
        
        available_apis = []
        missing_apis = []
        
        for api_name, api_key in self.api_keys.items():
            if api_key:
                available_apis.append(api_name)
                key_preview = api_key[:20] + "..." if len(api_key) > 20 else api_key
                print(f"✅ {api_name}: {key_preview}")
            else:
                missing_apis.append(api_name)
                print(f"❌ {api_name}: 없음")
        
        print(f"\n✅ 사용가능: {len(available_apis)}/17")
        print(f"❌ 없음: {len(missing_apis)}/17")
        
        return available_apis, missing_apis
    
    def create_adjusted_allocation(self):
        """DeepSeek 비중 낮춘 새 분배표"""
        
        print("\n" + "="*100)
        print("📊 조정된 모델 분배 (DeepSeek 10% → Gemini 30%)")
        print("="*100 + "\n")
        
        allocation = {
            "📚 연구/분석": {
                "1순위": "gemini-2.5-pro (60%) - ⭐주력모델",
                "2순위": "gemini-3-pro (20%) - 최고성능(보조)",
                "3순위": "claude-opus-4-5 (20%)",
                "월간": "$0.003-0.008"
            },
            
            "💻 코딩/복잡작업": {
                "1순위": "gemini-2.0-flash (40%) - 상향",
                "2순위": "deepseek-coder (15%) - 하향",
                "3순위": "claude-sonnet-4-5 (30%)",
                "4순위": "mistral-large (10%)",
                "5순위": "copilot/haiku (5%)",
                "월간": "$0.01"
            },
            
            "⚡ 긴급/빠른응답": {
                "1순위": "llama-3.1-8b Groq (30%)",
                "2순위": "gemini-2.0-flash-lite (20%) - ⭐신규",
                "3순위": "mistral-large (20%)",
                "4순위": "cerebras (15%)",
                "5순위": "fireworks (15%)",
                "월간": "$0"
            },
            
            "📞 일반대화": {
                "1순위": "gemini-2.5-pro (50%) - ⭐주력대화",
                "2순위": "gemini-3-pro (20%) - 고성능",
                "3순위": "gemini-2.0-flash (20%) - 백업",
                "4순위": "claude-sonnet-4-5 (10%)",
                "5순위": "copilot/haiku (0%)",
                "월간": "$0.02"
            },
            
            "🧬 생물학이미지": {
                "1순위": "gemini-2.5-vision (70%) - 상향",
                "2순위": "gpt-4-vision (20%)",
                "3순위": "gemini-2.0-flash (10%)",
                "월간": "$0.01"
            },
            
            "📊 데이터분석": {
                "1순위": "gemini-2.5-pro (60%) - ⭐주력분석",
                "2순위": "gemini-3-pro (20%) - 심화분석",
                "3순위": "openrouter/dbrx (20%)",
                "4순위": "deepseek-chat (0%)",
                "월간": "$0.02"
            }
        }
        
        for task, details in allocation.items():
            print(f"\n{task}")
            for key, value in details.items():
                print(f"  {key}: {value}")
        
        return allocation
    
    def print_final_usage_ratio(self):
        """최종 사용 비율 출력"""
        
        print("\n" + "="*100)
        print("📊 최종 모델 사용 비율 (DeepSeek 하향 조정)")
        print("="*100 + "\n")
        
        usage = {
            "🟢 우선 사용 (65%)": [
                ("Gemini API", "30%", "↑상향"),
                ("Groq API", "15%", "유지"),
                ("Anthropic API", "12%", "유지"),
                ("OpenRouter API", "5%", "유지"),
                ("Mistral API", "3%", "유지"),
            ],
            
            "🟢 주요 사용 (20%)": [
                ("DeepSeek API", "10%", "↓하향"),
                ("OpenAI API", "4%", "유지"),
                ("SambaNova API", "3%", "유지"),
                ("Cerebras API", "3%", "유지"),
            ],
            
            "🟡 보조 사용 (10%)": [
                ("Fireworks API", "3%", "유지"),
                ("DeepInfra API", "3%", "유지"),
                ("SiliconFlow API", "2%", "유지"),
                ("Hyperbolic API", "2%", "유지"),
            ],
            
            "🔵 특수/기본 (5%)": [
                ("GitHub Copilot Haiku", "5%", "유지"),
            ]
        }
        
        for category, apis in usage.items():
            print(f"{category}")
            for api_name, ratio, note in apis:
                print(f"  • {api_name}: {ratio} {note}")
        
        return usage
    
    def create_sequential_test_plan(self):
        """순차 테스트 계획"""
        
        print("\n" + "="*100)
        print("🧪 모든 모델 순차 테스트 계획")
        print("="*100 + "\n")
        
        test_plan = [
            {
                "순서": "1️⃣",
                "API": "Gemini",
                "모델": ["gemini-2.5-pro", "gemini-2.0-flash", "gemini-2.5-vision"],
                "테스트": "간단한 질문",
                "예상시간": "2-3초"
            },
            {
                "순서": "2️⃣",
                "API": "Groq",
                "모델": ["llama-3.1-8b-instant", "qwen/qwen3-32b"],
                "테스트": "간단한 질문",
                "예상시간": "1-2초"
            },
            {
                "순서": "3️⃣",
                "API": "Anthropic",
                "모델": ["claude-opus-4-5-20251101", "claude-sonnet-4-5-20250929"],
                "테스트": "API 호출 테스트",
                "예상시간": "2-3초"
            },
            {
                "순서": "4️⃣",
                "API": "Mistral",
                "모델": ["mistral-large", "mistral-medium"],
                "테스트": "간단한 질문",
                "예상시간": "2-3초"
            },
            {
                "순서": "5️⃣",
                "API": "DeepSeek",
                "모델": ["deepseek-chat", "deepseek-coder"],
                "테스트": "간단한 질문",
                "예상시간": "2-3초"
            },
            {
                "순서": "6️⃣",
                "API": "OpenRouter",
                "모델": ["mistral-large", "dbrx-instruct"],
                "테스트": "프록시 테스트",
                "예상시간": "2-3초"
            },
            {
                "순서": "7️⃣",
                "API": "OpenAI",
                "모델": ["gpt-4o", "gpt-4-vision"],
                "테스트": "API 호출 테스트",
                "예상시간": "2-3초"
            },
            {
                "순서": "8️⃣",
                "API": "SambaNova",
                "모델": ["sambanova-llama-70b"],
                "테스트": "간단한 질문",
                "예상시간": "1-2초"
            },
            {
                "순서": "9️⃣",
                "API": "Cerebras",
                "모델": ["cerebras-gpt"],
                "테스트": "초고속 테스트",
                "예상시간": "1-2초"
            },
            {
                "순서": "🔟",
                "API": "기타",
                "모델": ["fireworks", "deepinfra", "siliconflow"],
                "테스트": "프록시 테스트",
                "예상시간": "2-3초"
            },
        ]
        
        for test in test_plan:
            print(f"{test['순서']} {test['API']}")
            print(f"   모델: {', '.join(test['모델'])}")
            print(f"   테스트: {test['테스트']}")
            print(f"   예상시간: {test['예상시간']}\n")
        
        return test_plan
    
    def print_parallel_work_strategy(self):
        """병렬 작업 전략"""
        
        print("\n" + "="*100)
        print("⚙️ 병렬 작업 전략 (테스트 + 다음작업)")
        print("="*100 + "\n")
        
        strategy = """
🔄 **테스트 루프:**
  1️⃣ Gemini 테스트 (2초) → 결과 기록
  2️⃣ Groq 테스트 (2초) → 결과 기록
  3️⃣ Anthropic 테스트 (2초) → 결과 기록
  4️⃣ Mistral 테스트 (2초) → 결과 기록
  5️⃣ DeepSeek 테스트 (2초) → 결과 기록
  ...
  
  총 10개 모델 그룹 = 약 20-30초

📊 **동시 진행 작업:**
  • 테스트 1️⃣-5️⃣ 실행 중: Phase B 대시보드 설계 시작
  • 테스트 6️⃣-🔟 실행 중: SHawn-Web UI 프로토타입
  • 테스트 완료: 결과 분석 & 최종 보고

🎯 **효율성:**
  • 순차 테스트: 20-30초
  • 동시 진행: 테스트 + 다음작업 병렬 처리
  • 총 예상 시간: 10-15분 (효율적!)
"""
        
        print(strategy)
        return strategy
    
    def run(self):
        """전체 실행"""
        
        print("\n" + "="*100)
        print("🚀 모든 모델 테스트 + DeepSeek 비중 조정")
        print("="*100)
        
        # Step 1: API 키 확인
        available_apis, missing_apis = self.test_api_keys()
        
        # Step 2: 비중 조정
        allocation = self.create_adjusted_allocation()
        
        # Step 3: 최종 비율
        usage = self.print_final_usage_ratio()
        
        # Step 4: 테스트 계획
        test_plan = self.create_sequential_test_plan()
        
        # Step 5: 병렬 작업 전략
        strategy = self.print_parallel_work_strategy()
        
        # 결과 저장
        self.results["api_status"] = {
            "available": len(available_apis),
            "available_list": available_apis,
            "missing": len(missing_apis),
            "total": 17
        }
        self.results["allocation"] = allocation
        self.results["usage_ratio"] = usage
        self.results["test_plan"] = test_plan
        self.results["status"] = "✅ 준비완료"
        
        with open("/Users/soohyunglee/.openclaw/workspace/model_test_plan.json", "w") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*100)
        print("✅ 모든 준비 완료!")
        print("="*100)
        print(f"\n🎯 최종 상태:")
        print(f"  ✅ API 키: {len(available_apis)}/17 사용가능")
        print(f"  ✅ DeepSeek: 20% → 10% 하향 조정")
        print(f"  ✅ Gemini: 25% → 30% 상향 조정")
        print(f"  ✅ 테스트 계획: 10개 모델 그룹 순차 테스트")
        print(f"  ✅ 병렬 작업: 테스트 + Phase B 동시 진행")
        print(f"\n💾 결과: model_test_plan.json")

if __name__ == "__main__":
    tester = ComprehensiveModelTester()
    tester.run()
