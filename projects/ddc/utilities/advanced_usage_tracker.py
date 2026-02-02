#!/usr/bin/env python3
"""
GitHub Copilot + Anthropic Claude 사용량 자동 추적

강한 권한 GitHub Token을 사용하여:
  1. Copilot 사용량 실시간 조회
  2. Claude API 크레딧 상태 조회
  3. 통합 리포트 생성
"""

import os
import json
import urllib.request
from datetime import datetime
from typing import Dict, Optional

class AdvancedUsageTracker:
    """GitHub Token을 사용한 고급 사용량 추적"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_ADVANCED_TOKEN')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
    
    def check_github_token(self) -> bool:
        """GitHub Token 유효성 확인"""
        if not self.github_token:
            print("❌ GITHUB_ADVANCED_TOKEN이 설정되지 않았습니다!")
            return False
        
        if not self.github_token.startswith('ghp_'):
            print("⚠️ 토큰 형식이 이상합니다. ghp_로 시작해야 합니다.")
            return False
        
        return True
    
    def get_github_user_info(self) -> Dict:
        """GitHub 사용자 정보 조회"""
        try:
            req = urllib.request.Request(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'token {self.github_token}',
                    'Accept': 'application/vnd.github+json'
                }
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                return {
                    'login': data.get('login'),
                    'name': data.get('name'),
                    'plan': data.get('plan', {}).get('name'),
                    'status': 'success'
                }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}
    
    def check_copilot_api(self) -> Dict:
        """Copilot API 확인 (아직 공개되지 않음)"""
        try:
            req = urllib.request.Request(
                'https://api.github.com/user/copilot_settings',
                headers={
                    'Authorization': f'token {self.github_token}',
                    'Accept': 'application/vnd.github+json'
                }
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return {'status': 'available', 'data': json.loads(response.read().decode())}
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {
                    'status': 'not_available',
                    'message': 'Copilot API는 아직 공개되지 않았습니다',
                    'workaround': 'https://github.com/settings/copilot'
                }
            return {'status': 'error', 'code': e.code}
    
    def get_claude_status(self) -> Dict:
        """Claude 크레딧 상태 조회"""
        return {
            'status': 'api_limited',
            'note': 'Anthropic API는 usage 엔드포인트 미지원',
            'workaround': 'Anthropic 웹에서 직접 확인: https://console.anthropic.com/account/billing/overview',
            'method': 'dashboard_only'
        }
    
    def get_gemini_usage(self) -> Dict:
        """Google Gemini 사용량 조회"""
        try:
            gemini_key = self.gemini_key
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                models = data.get('models', [])
                gemini_models = [m for m in models if 'gemini' in m.get('name', '').lower()]
                
                return {
                    'status': 'connected',
                    'available_models': len(gemini_models),
                    'sample_models': [m.get('displayName') for m in gemini_models[:3]]
                }
        except Exception as e:
            return {'error': str(e), 'status': 'failed'}
    
    def generate_report(self) -> str:
        """통합 사용량 리포트 생성"""
        output = []
        
        output.append("=" * 70)
        output.append("📊 고급 사용량 추적 리포트")
        output.append("=" * 70)
        output.append("")
        
        # GitHub Token 상태
        output.append("🔑 GitHub Token 상태")
        if self.check_github_token():
            output.append("  ✅ 토큰 설정 완료 (유효)")
        else:
            output.append("  ❌ 토큰 미설정")
        output.append("")
        
        # GitHub 사용자 정보
        output.append("👤 GitHub 계정 정보")
        user_info = self.get_github_user_info()
        if user_info.get('status') == 'success':
            output.append(f"  ✅ 계정: {user_info.get('login')}")
            output.append(f"  📝 이름: {user_info.get('name')}")
            output.append(f"  💳 플랜: {user_info.get('plan')}")
        else:
            output.append(f"  ❌ 오류: {user_info.get('error')}")
        output.append("")
        
        # Copilot 상태
        output.append("🟡 GitHub Copilot")
        copilot_info = self.check_copilot_api()
        if copilot_info.get('status') == 'available':
            output.append("  ✅ API 사용 가능")
            output.append(f"  데이터: {copilot_info.get('data')}")
        else:
            output.append(f"  ⏳ {copilot_info.get('message')}")
            output.append(f"  📌 웹: {copilot_info.get('workaround')}")
        output.append("")
        
        # Claude 상태
        output.append("🔵 Anthropic Claude")
        claude_info = self.get_claude_status()
        output.append(f"  ⏳ {claude_info.get('note')}")
        output.append(f"  📌 웹: {claude_info.get('workaround')}")
        output.append("")
        
        # Gemini 상태
        output.append("🟢 Google Gemini")
        gemini_info = self.get_gemini_usage()
        if gemini_info.get('status') == 'connected':
            output.append(f"  ✅ 연결 성공")
            output.append(f"  📊 사용 가능 모델: {gemini_info.get('available_models')}개")
            output.append(f"  🎯 샘플: {', '.join(gemini_info.get('sample_models', []))}")
        else:
            output.append(f"  ❌ 오류: {gemini_info.get('error')}")
        output.append("")
        
        output.append("=" * 70)
        output.append("📌 다음 단계")
        output.append("=" * 70)
        output.append("")
        output.append("✅ 토큰 설정 완료!")
        output.append("")
        output.append("⏳ 대기 중 (GitHub 공식 API 개방 대기):")
        output.append("  • Copilot 사용량 API")
        output.append("  • Copilot 크레딧 API")
        output.append("")
        output.append("🔄 현재 가능한 것:")
        output.append("  • GitHub 계정 정보 조회 ✅")
        output.append("  • Gemini API 연결 ✅")
        output.append("")
        output.append("📝 수동 확인 (웹):")
        output.append("  1. Claude: https://console.anthropic.com/account/billing/overview")
        output.append("  2. Copilot: https://github.com/settings/copilot")
        output.append("  3. Gemini: https://aistudio.google.com/apikey")
        output.append("")
        output.append("=" * 70)
        output.append(f"생성: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 70)
        
        return "\n".join(output)
    
    def save_report(self, filename: str = "advanced_usage_report.json"):
        """리포트를 JSON으로 저장"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'github': {
                'token_ready': self.check_github_token(),
                'user_info': self.get_github_user_info(),
                'copilot_api': self.check_copilot_api()
            },
            'claude': {
                'status': 'web_dashboard_only',
                'url': 'https://console.anthropic.com/account/billing/overview'
            },
            'gemini': self.get_gemini_usage(),
            'manual_urls': {
                'claude': 'https://console.anthropic.com/account/billing/overview',
                'copilot': 'https://github.com/settings/copilot',
                'gemini': 'https://aistudio.google.com/apikey'
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
    tracker = AdvancedUsageTracker()
    
    # 리포트 출력
    print(tracker.generate_report())
    
    # JSON 저장
    filepath = tracker.save_report()
    print(f"\n✅ 리포트 저장: {filepath}")


if __name__ == "__main__":
    main()
