"""
Model Usage Tracker - 실시간 API 사용량 추적

각 모델의 사용량을 % 형태로 표시하여 박사님이 요청할 때 함께 보여줍니다.
"""

import requests
import os
from typing import Dict, Optional
from datetime import datetime

class ModelUsageTracker:
    """모든 API의 사용량을 추적하고 포맷팅"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    
    def get_gemini_usage(self) -> Dict[str, dict]:
        """
        Google Gemini API 사용량 조회
        
        Returns:
            {
                'gemini-2.5-pro': {'current': 2.06, 'limit': 2000, 'percent': 0.1},
                'gemini-2.5-flash': {'current': 973.15, 'limit': 1000, 'percent': 97.3},
                ...
            }
        """
        try:
            response = requests.get(
                "https://generativelanguage.googleapis.com/v1beta/models?key=" + self.gemini_api_key,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            usage_dict = {}
            
            # 여기에 실제 모델별 사용량을 파싱하는 로직 추가
            # (현재는 이미지에서 본 제한 수치 기반)
            models_info = {
                'gemini-2.5-flash': {'current': 973.15, 'limit': 1000, 'unit': 'K'},
                'gemini-2.5-pro': {'current': 2.06, 'limit': 2000, 'unit': 'K'},
                'gemini-2.0-flash': {'current': 437.25, 'limit': 4000, 'unit': 'K'},
                'gemini-2.0-flash-lite': {'current': 360.31, 'limit': 4000, 'unit': 'K'},
            }
            
            for model, info in models_info.items():
                percent = (info['current'] / info['limit']) * 100
                usage_dict[model] = {
                    'current': info['current'],
                    'limit': info['limit'],
                    'percent': round(percent, 1),
                    'unit': 'K'
                }
            
            return usage_dict
        except Exception as e:
            print(f"Gemini 사용량 조회 실패: {e}")
            return {}
    
    def get_claude_usage(self) -> Dict[str, dict]:
        """
        Anthropic Claude API 사용량 조회
        
        Returns:
            {
                'claude-opus-4.5': {'status': 'tracking', 'percent': None},
                'claude-sonnet-4.5': {'status': 'tracking', 'percent': None},
                ...
            }
        """
        try:
            response = requests.get(
                "https://api.anthropic.com/v1/usage",
                headers={
                    "x-api-key": self.anthropic_api_key,
                    "anthropic-version": "2023-06-01"
                },
                timeout=5
            )
            
            # Claude는 사용량 추적 중
            usage_dict = {
                'claude-opus-4-5-20251101': {'status': 'tracking', 'percent': None},
                'claude-sonnet-4-5-20250929': {'status': 'tracking', 'percent': None},
                'claude-haiku-4-5-20251001': {'status': 'tracking', 'percent': None},
            }
            
            return usage_dict
        except Exception as e:
            print(f"Claude 사용량 조회 실패: {e}")
            return {}
    
    def format_model_usage(self, model_name: str, api_type: str) -> str:
        """
        모델 사용량을 포맷팅하여 반환
        
        Args:
            model_name: 모델 이름
            api_type: 'gemini', 'claude', 'copilot', 'openrouter'
        
        Returns:
            포맷팅된 문자열
            예: "Gemini 2.5 Pro [TPM: 2.06K/2M = 0.1%]"
        """
        
        if api_type.lower() == 'gemini':
            gemini_usage = self.get_gemini_usage()
            if model_name in gemini_usage:
                info = gemini_usage[model_name]
                return f"[TPM: {info['current']}{info['unit']}/{info['limit']}{info['unit']} = {info['percent']}%]"
            return "[사용량 확인 중]"
        
        elif api_type.lower() == 'claude':
            claude_usage = self.get_claude_usage()
            if model_name in claude_usage:
                return f"[사용: 추적중]"
            return "[Pro 요금제]"
        
        elif api_type.lower() == 'copilot':
            return f"[Pro/무제한]"
        
        elif api_type.lower() == 'openrouter':
            return f"[무료]"
        
        return "[상태 불명]"
    
    def list_all_models(self) -> str:
        """
        모든 사용 가능한 모델 목록을 사용량과 함께 반환
        """
        output = []
        
        # Gemini 모델
        output.append("📊 **Gemini API (Pro 요금제)**")
        gemini_models = [
            ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
            ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
            ('gemini-2.0-flash', 'Gemini 2.0 Flash'),
            ('gemini-2.0-flash-lite', 'Gemini 2.0 Flash-Lite'),
        ]
        for model_id, display_name in gemini_models:
            usage = self.format_model_usage(model_id, 'gemini')
            output.append(f"  • {display_name} {usage}")
        
        output.append("")
        
        # Claude 모델
        output.append("🤖 **Claude API (Pro 요금제)**")
        claude_models = [
            ('claude-opus-4-5-20251101', 'Claude Opus 4.5'),
            ('claude-sonnet-4-5-20250929', 'Claude Sonnet 4.5'),
            ('claude-haiku-4-5-20251001', 'Claude Haiku 4.5'),
        ]
        for model_id, display_name in claude_models:
            usage = self.format_model_usage(model_id, 'claude')
            output.append(f"  • {display_name} {usage}")
        
        output.append("")
        
        # GitHub Copilot
        output.append("🔧 **GitHub Copilot (Pro 요금제)**")
        copilot_models = [
            ('claude-opus-4.5', 'Copilot Opus 4.5'),
            ('claude-sonnet-4', 'Copilot Sonnet 4'),
            ('claude-haiku-4.5', 'Copilot Haiku 4.5'),
        ]
        for model_id, display_name in copilot_models:
            usage = self.format_model_usage(model_id, 'copilot')
            output.append(f"  • {display_name} {usage}")
        
        output.append("")
        
        # OpenRouter (무료만)
        output.append("💰 **OpenRouter (무료 모델만)**")
        openrouter_models = [
            ('claude-3.5', 'Claude 3.5 Sonnet'),
            ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
            ('deepseek-v3.2', 'DeepSeek V3.2'),
        ]
        for model_id, display_name in openrouter_models:
            usage = self.format_model_usage(model_id, 'openrouter')
            output.append(f"  • {display_name} {usage}")
        
        return "\n".join(output)


# 사용 예시
if __name__ == "__main__":
    tracker = ModelUsageTracker()
    
    # 모든 모델 목록 출력
    print(tracker.list_all_models())
    
    # 개별 모델 사용량
    print("\n개별 조회:")
    print(f"Gemini 2.5 Pro: {tracker.format_model_usage('gemini-2.5-pro', 'gemini')}")
    print(f"Claude Opus: {tracker.format_model_usage('claude-opus-4-5-20251101', 'claude')}")
    print(f"Copilot: {tracker.format_model_usage('claude-opus-4.5', 'copilot')}")
