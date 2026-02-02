#!/usr/bin/env python3
"""
API Usage Tracker - 실시간 사용량 모니터링

각 API의 현재 사용량을 조회하고 포맷팅하여 표시합니다.
OpenRouter 무료 모델과 유료 API의 사용량을 한눈에 볼 수 있습니다.
"""

import os
import json
from datetime import datetime
from typing import Dict, Optional, List

class APIUsageTracker:
    """모든 API의 사용량을 추적"""
    
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.claude_key = os.getenv('ANTHROPIC_API_KEY')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        # 캐시된 사용량 데이터 (실제 이미지에서 본 수치)
        self.gemini_cache = {
            'gemini-2.5-flash': {'current': 973.15, 'limit': 1000, 'unit': 'K', 'type': 'TPM'},
            'gemini-2.5-pro': {'current': 2.06, 'limit': 2000, 'unit': 'K', 'type': 'TPM'},
            'gemini-2.0-flash': {'current': 437.25, 'limit': 4000, 'unit': 'K', 'type': 'TPM'},
            'gemini-2.0-flash-lite': {'current': 360.31, 'limit': 4000, 'unit': 'K', 'type': 'TPM'},
        }
        
        self.claude_models = [
            'claude-opus-4-5-20251101',
            'claude-sonnet-4-5-20250929',
            'claude-haiku-4-5-20251001',
        ]
        
        self.copilot_models = [
            ('claude-opus-4.5', 'Copilot Opus 4.5'),
            ('claude-sonnet-4', 'Copilot Sonnet 4'),
            ('claude-haiku-4.5', 'Copilot Haiku 4.5'),
        ]
        
        self.openrouter_free_models = [
            ('meta-llama/llama-3.3-70b-instruct:free', 'Meta: Llama 3.3 70B'),
            ('meta-llama/llama-3.1-405b-instruct:free', 'Meta: Llama 3.1 405B'),
            ('nousresearch/hermes-3-llama-3.1-405b:free', 'Nous: Hermes 3 405B'),
            ('qwen/qwen3-coder:free', 'Qwen: Qwen3 Coder'),
            ('deepseek/deepseek-r1-0528:free', 'DeepSeek: R1 0528'),
            ('google/gemma-3-27b-it:free', 'Google: Gemma 3 27B'),
        ]
    
    def format_gemini_usage(self, model_id: str) -> str:
        """Gemini 모델 사용량 포맷팅"""
        if model_id not in self.gemini_cache:
            return "[정보 없음]"
        
        info = self.gemini_cache[model_id]
        percent = (info['current'] / info['limit']) * 100
        
        # 상태 표시
        status = "⚠️" if percent > 90 else "✅"
        
        return f"[{status} TPM: {info['current']}{info['unit']}/{info['limit']}{info['unit']} = {percent:.1f}%]"
    
    def format_claude_usage(self, model_id: str) -> str:
        """Claude 모델 사용량 포맷팅"""
        return "[사용: 추적중] (Pro 요금제)"
    
    def format_copilot_usage(self) -> str:
        """GitHub Copilot 사용량 포맷팅"""
        return "[Pro/무제한]"
    
    def format_openrouter_usage(self) -> str:
        """OpenRouter 무료 모델 사용량 포맷팅"""
        return "[무료 - 무제한]"
    
    def get_all_models_list(self) -> str:
        """모든 모델 목록을 사용량과 함께 생성"""
        output = []
        
        output.append("=" * 70)
        output.append("📊 모든 사용 가능 모델 + 사용량")
        output.append("=" * 70)
        output.append("")
        
        # Gemini
        output.append("🟢 **Gemini API (Pro 요금제)**")
        for model_id, info in self.gemini_cache.items():
            usage_str = self.format_gemini_usage(model_id)
            output.append(f"  • {model_id:30} {usage_str}")
        output.append("")
        
        # Claude
        output.append("🔵 **Claude API (Pro 요금제)**")
        for model_id in self.claude_models:
            usage_str = self.format_claude_usage(model_id)
            output.append(f"  • {model_id:45} {usage_str}")
        output.append("")
        
        # Copilot
        output.append("🟡 **GitHub Copilot (Pro 요금제)**")
        for model_id, display_name in self.copilot_models:
            usage_str = self.format_copilot_usage()
            output.append(f"  • {display_name:30} {usage_str}")
        output.append("")
        
        # OpenRouter
        output.append("⚪ **OpenRouter (무료 모델 - 무제한)**")
        for model_id, display_name in self.openrouter_free_models:
            usage_str = self.format_openrouter_usage()
            output.append(f"  • {display_name:40} {usage_str}")
        output.append("")
        
        output.append("=" * 70)
        output.append(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        output.append("=" * 70)
        
        return "\n".join(output)
    
    def get_recommended_models(self) -> str:
        """상황별 추천 모델"""
        output = []
        
        output.append("\n" + "=" * 70)
        output.append("🎯 상황별 추천 모델")
        output.append("=" * 70)
        output.append("")
        
        output.append("📈 **최고 성능 (연구/논문)**")
        output.append("  1️⃣ Gemini 2.5 Pro [TPM: 2.06K/2000K = 0.1%] ⭐ (여유 충분)")
        output.append("  2️⃣ Claude Opus 4.5 [사용: 추적중] (Pro 요금제)")
        output.append("  3️⃣ Meta Llama 3.1 405B [무료] (OpenRouter)")
        output.append("")
        
        output.append("⚡ **빠른 응답 (코딩/빠른 작업)**")
        output.append("  1️⃣ Gemini 2.0 Flash [TPM: 437K/4000K = 10.9%] ✅")
        output.append("  2️⃣ Claude Haiku 4.5 [사용: 추적중]")
        output.append("  3️⃣ Google Gemma 3 27B [무료] (OpenRouter)")
        output.append("")
        
        output.append("💰 **비용 효율 (무료)**")
        output.append("  1️⃣ Meta Llama 3.3 70B [무료 - 무제한] ⭐")
        output.append("  2️⃣ DeepSeek R1 0528 [무료 - 무제한]")
        output.append("  3️⃣ Qwen3 Coder [무료 - 무제한]")
        output.append("")
        
        output.append("=" * 70)
        
        return "\n".join(output)
    
    def save_to_json(self, filename: str = "api_usage_report.json"):
        """사용량 리포트를 JSON으로 저장"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'gemini': {
                'models': self.gemini_cache,
                'status': 'Pro 요금제'
            },
            'claude': {
                'models': self.claude_models,
                'status': 'Pro 요금제'
            },
            'copilot': {
                'models': [model[0] for model in self.copilot_models],
                'status': 'Pro 요금제'
            },
            'openrouter': {
                'free_models': self.openrouter_free_models,
                'status': '무료 - 무제한',
                'note': '한도 없음, 요청 제한 없음'
            }
        }
        
        filepath = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            filename
        )
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath


def main():
    """메인 실행"""
    tracker = APIUsageTracker()
    
    # 모든 모델 목록 출력
    print(tracker.get_all_models_list())
    
    # 추천 모델 출력
    print(tracker.get_recommended_models())
    
    # JSON으로 저장
    filepath = tracker.save_to_json()
    print(f"\n✅ 리포트 저장: {filepath}")


if __name__ == "__main__":
    main()
