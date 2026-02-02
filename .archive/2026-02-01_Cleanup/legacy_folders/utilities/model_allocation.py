#!/usr/bin/env python3
"""
모든 API 모델 + 작업별 최적 분배

박사님의 모든 API에서 사용 가능한 모델들을:
  1. 카테고리별로 분류
  2. 작업별로 최적 배분
  3. 사용량/성능 함께 표시
"""

MODEL_ALLOCATION = {
    "🟢 **Gemini API (Pro 요금제)**": {
        "최고 성능 (연구/논문/복잡 분석)": [
            ("gemini-2.5-pro", "Gemini 2.5 Pro", "[TPM: 2.06K/2M = 0.1%] ⭐⭐⭐"),
            ("gemini-3-pro-preview", "Gemini 3 Pro Preview", "[프리뷰] 최신 최고성능"),
        ],
        "고성능 코딩 (알고리즘/복잡 로직)": [
            ("gemini-2.5-flash", "Gemini 2.5 Flash", "[TPM: 973K/1M = 97.3%] ⚠️ 거의 도달"),
            ("gemini-2.0-flash", "Gemini 2.0 Flash", "[TPM: 437K/4M = 10.9%] ✅ 여유충분"),
        ],
        "빠른 응답 (일상적 작업)": [
            ("gemini-2.0-flash-lite", "Gemini 2.0 Flash-Lite", "[TPM: 360K/4M = 9.0%] ✅ 매우빠름"),
            ("gemini-2.5-flash-lite", "Gemini 2.5 Flash-Lite", "[빠른 응답] 경량"),
            ("gemini-flash-latest", "Gemini Flash Latest", "[최신] 항상 최신"),
        ],
        "특수 작업": [
            ("gemini-2.5-computer-use-preview-10-2025", "Gemini 2.5 Computer Use", "[프리뷰] 컴퓨터 제어"),
            ("deep-research-pro-preview-12-2025", "Deep Research Pro", "[프리뷰] 심화 연구"),
            ("gemini-2.5-flash-preview-tts", "Gemini 2.5 Flash TTS", "[오디오] 음성 합성"),
            ("gemini-2.5-pro-preview-tts", "Gemini 2.5 Pro TTS", "[오디오] 고품질 음성"),
        ],
        "이미지 생성": [
            ("imagen-4.0-generate-001", "Imagen 4", "[이미지] 표준"),
            ("imagen-4.0-ultra-generate-001", "Imagen 4 Ultra", "[이미지] 최고품질"),
            ("imagen-4.0-fast-generate-001", "Imagen 4 Fast", "[이미지] 빠름"),
            ("veo-3.1-generate-preview", "Veo 3.1", "[영상] 프리뷰"),
        ],
        "경량 모델": [
            ("gemma-3-27b-it", "Gemma 3 27B", "[경량] 가장강함"),
            ("gemma-3-12b-it", "Gemma 3 12B", "[경량] 균형"),
            ("gemma-3-4b-it", "Gemma 3 4B", "[경량] 가장빠름"),
        ],
    },

    "🔵 **Claude API (Pro 요금제)**": {
        "최고 성능 (연구/전략/복잡분석)": [
            ("claude-opus-4-5-20251101", "Claude Opus 4.5", "[사용: 추적중] ⭐⭐⭐ 최신최고"),
            ("claude-opus-4-1-20250805", "Claude Opus 4.1", "[사용: 추적중] ⭐⭐ 안정"),
        ],
        "균형 (일반적인 대부분 작업)": [
            ("claude-sonnet-4-5-20250929", "Claude Sonnet 4.5", "[사용: 추적중] ⭐⭐ 최신"),
            ("claude-sonnet-4-20250514", "Claude Sonnet 4", "[사용: 추적중] ⭐⭐ 안정"),
        ],
        "빠른 응답 (간단한 작업)": [
            ("claude-haiku-4-5-20251001", "Claude Haiku 4.5", "[사용: 추적중] ⭐ 최신 빠름"),
            ("claude-3-haiku-20240307", "Claude Haiku 3", "[사용: 추적중] ⭐ 레거시"),
        ],
    },

    "🟡 **GitHub Copilot (Pro 요금제 무제한)**": {
        "최고 성능": [
            ("github-copilot/claude-opus-4.5", "Copilot Opus 4.5", "[Pro/무제한] ⭐⭐⭐"),
        ],
        "균형 (추천)": [
            ("github-copilot/claude-sonnet-4", "Copilot Sonnet 4", "[Pro/무제한] ⭐⭐ 코딩최고"),
        ],
        "빠른 응답": [
            ("github-copilot/claude-haiku-4.5", "Copilot Haiku 4.5", "[Pro/무제한] ⭐ 기본"),
        ],
        "특수": [
            ("github-copilot/gpt-4o", "Copilot GPT-4o", "[Pro/무제한] 특수작업"),
        ],
    },

    "⚡ **Groq API (빠른 응답)**": {
        "최고 성능": [
            ("qwen/qwen3-32b", "Qwen3 32B", "[매우빠름] ⭐⭐ Alibaba"),
            ("meta-llama/llama-4-maverick-17b-128e-instruct", "Llama 4 Maverick 17B", "[매우빠름] ⭐⭐ Meta"),
        ],
        "빠른 응답": [
            ("llama-3.3-70b-versatile", "Llama 3.3 70B", "[빠름] ⭐ 다재다능"),
            ("llama-3.1-8b-instant", "Llama 3.1 8B", "[초고속] ⭐ 가벼움"),
        ],
        "특수": [
            ("groq/compound-mini", "Groq Compound Mini", "[Groq전용] 빠름"),
        ],
    },
}

def print_allocation():
    """모든 모델을 작업별로 출력"""
    
    print("=" * 90)
    print("📊 모든 API 모델 + 작업별 최적 분배")
    print("=" * 90)
    print()
    
    for api_name, categories in MODEL_ALLOCATION.items():
        print(api_name)
        print()
        
        for category, models in categories.items():
            print(f"  ### {category}")
            for model_id, display_name, usage_info in models:
                print(f"    • {display_name:40} {usage_info}")
            print()
    
    print("=" * 90)
    print("🎯 작업별 최적 모델 선택")
    print("=" * 90)
    print()
    
    recommendations = {
        "📚 연구/논문/심화분석": [
            "1순위: Gemini 2.5 Pro [0.1% 사용] ⭐⭐⭐",
            "2순위: Claude Opus 4.5 [추적중]",
            "3순위: Copilot Opus 4.5 [무제한]",
        ],
        "💻 코딩 (복잡한 알고리즘)": [
            "1순위: Copilot Sonnet 4 [무제한] ⭐⭐",
            "2순위: Gemini 2.5 Flash [97.3%] ⚠️",
            "3순위: Claude Sonnet 4.5 [추적중]",
        ],
        "🚀 빠른 응답 필요": [
            "1순위: Groq Llama 3.1 8B [초고속]",
            "2순위: Gemini 2.0 Flash-Lite [9.0%]",
            "3순위: Copilot Haiku [무제한]",
        ],
        "🎨 이미지/영상 생성": [
            "1순위: Gemini Imagen 4 Ultra [고품질]",
            "2순위: Gemini Veo 3.1 [영상]",
            "3순위: Gemini Imagen 4 Fast [빠름]",
        ],
        "🔊 음성 생성": [
            "1순위: Gemini 2.5 Flash TTS [프리뷰]",
            "2순위: Gemini 2.5 Pro TTS [고품질]",
        ],
        "📞 일반 대화": [
            "1순위: Gemini 2.0 Flash [10.9% 여유]",
            "2순위: Claude Sonnet 4.5 [균형]",
            "3순위: Copilot Haiku [무제한]",
        ],
        "🤖 자동화/스크립트": [
            "1순위: Copilot Sonnet 4 [무제한] ⭐",
            "2순위: Gemini 2.5 Flash-Lite [빠름]",
            "3순위: Groq Llama [초고속]",
        ],
        "🧬 전문분야 (생물학)": [
            "1순위: Gemini 2.5 Pro [0.1%] 전문성",
            "2순위: Claude Opus 4.5 [추적중]",
        ],
    }
    
    for task, models in recommendations.items():
        print(f"{task}")
        for model in models:
            print(f"  {model}")
        print()
    
    print("=" * 90)
    print("💡 사용 전략")
    print("=" * 90)
    print()
    print("✅ 메인 모델 선택 기준:")
    print("  1. 작업 성격 파악")
    print("  2. 위 표에서 추천 순서대로 선택")
    print("  3. 사용량/비용 확인")
    print()
    print("⚡ Groq 활용:")
    print("  • 매우 빠른 응답 필요할 때")
    print("  • 토큰 비용 절감 필요할 때")
    print("  • 비용 제한 없음 (매우 저렴)")
    print()
    print("🎯 Gemini 2.5 Flash 주의:")
    print("  • 현재 TPM 97.3% 사용 (거의 도달)")
    print("  • 다른 모델로 전환 권장")
    print("  • Gemini 2.0 Flash로 대체 가능")
    print()
    print("=" * 90)


if __name__ == "__main__":
    print_allocation()
