#!/usr/bin/env python3
"""
Groq API 사용량 추적 시스템 (v2)

목표:
  • 사용 가능 한도 확인
  • 현재 소모량 조회
  • 실시간 모니터링
"""

import os
import json
import urllib.request
from datetime import datetime
from typing import Dict


class GroqUsageTracker:
    """Groq API 사용량 추적"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1"
    
    def check_api_key(self) -> bool:
        """API 키 확인"""
        if not self.api_key:
            print("❌ GROQ_API_KEY 미설정")
            return False
        
        if not self.api_key.startswith('gsk_'):
            print("⚠️ 토큰 형식이 이상합니다")
            return False
        
        print("✅ GROQ_API_KEY 유효")
        print(f"   Token: {self.api_key[:10]}...{self.api_key[-10:]}")
        return True
    
    def get_api_info(self) -> Dict:
        """API 정보 조회"""
        return {
            'provider': 'Groq',
            'api_type': 'OpenAI-compatible',
            'base_url': self.base_url,
            'status': '✅ Ready to use'
        }
    
    def estimate_usage_limits(self) -> Dict:
        """사용 한도 추정 (공식 문서 기준)"""
        return {
            'free_tier': {
                'requests_per_minute': 30,
                'tokens_per_minute': 6000,
                'requests_per_day': 14400,
                'tokens_per_day': 2880000,
            },
            'note': 'Groq free tier limits (typical values)'
        }
    
    def test_simple_api_call(self) -> Dict:
        """간단한 API 호출 테스트"""
        try:
            req = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    'model': 'llama-3.1-8b-instant',
                    'messages': [
                        {'role': 'user', 'content': 'Say "GROQ_OK" only.'}
                    ],
                    'temperature': 0.5,
                    'max_tokens': 5
                }).encode('utf-8'),
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                usage = data.get('usage', {})
                return {
                    'status': 'success',
                    'model': data.get('model'),
                    'tokens': {
                        'prompt': usage.get('prompt_tokens', 0),
                        'completion': usage.get('completion_tokens', 0),
                        'total': usage.get('total_tokens', 0)
                    },
                    'timestamp': datetime.now().isoformat()
                }
        except urllib.error.HTTPError as e:
            return {
                'status': 'error',
                'code': e.code,
                'message': f'HTTP {e.code}: {str(e.reason)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def estimate_usage_from_tests(self, num_tests: int = 3) -> Dict:
        """테스트 호출들로부터 사용량 추정"""
        results = {
            'num_tests': num_tests,
            'successful_calls': 0,
            'failed_calls': 0,
            'total_tokens': 0,
            'calls': []
        }
        
        print(f"\n🧪 Running {num_tests} test API calls...\n")
        
        for i in range(num_tests):
            result = self.test_simple_api_call()
            results['calls'].append(result)
            
            if result['status'] == 'success':
                results['successful_calls'] += 1
                tokens = result['tokens']['total']
                results['total_tokens'] += tokens
                print(f"  ✅ Call {i+1}: {tokens} tokens used")
            else:
                results['failed_calls'] += 1
                print(f"  ❌ Call {i+1}: {result.get('message')}")
        
        # 사용량 추정
        if results['successful_calls'] > 0:
            results['avg_tokens_per_call'] = results['total_tokens'] / results['successful_calls']
            results['estimated_hourly_usage'] = results['total_tokens'] * 3600
        
        return results
    
    def generate_report(self) -> str:
        """사용량 리포트 생성"""
        
        print("\n" + "="*70)
        print("📊 GROQ API USAGE TRACKING REPORT")
        print("="*70 + "\n")
        
        # 1. API 키 확인
        if not self.check_api_key():
            print("\n❌ Cannot proceed without valid API key")
            print("="*70 + "\n")
            return "failed"
        
        # 2. API 정보
        print("\n🔧 API Information:")
        info = self.get_api_info()
        for key, value in info.items():
            print(f"  • {key}: {value}")
        
        # 3. 사용 한도
        print("\n📈 Estimated Usage Limits (Free Tier):")
        limits = self.estimate_usage_limits()['free_tier']
        print(f"  • RPM (Requests/Minute): {limits['requests_per_minute']}")
        print(f"  • TPM (Tokens/Minute): {limits['tokens_per_minute']:,}")
        print(f"  • Daily Requests: {limits['requests_per_day']:,}")
        print(f"  • Daily Tokens: {limits['tokens_per_day']:,}")
        
        # 4. 사용량 추적
        print("\n📊 Usage Pattern (3 test calls):")
        pattern = self.estimate_usage_from_tests(3)
        
        if pattern['successful_calls'] > 0:
            print(f"\n  ✅ Successful: {pattern['successful_calls']}/3")
            print(f"  Total tokens (tests): {pattern['total_tokens']}")
            print(f"  Avg per call: {pattern['avg_tokens_per_call']:.1f}")
            print(f"  Est. hourly: {pattern['estimated_hourly_usage']:.0f} tokens")
        else:
            print(f"\n  ❌ All {pattern['failed_calls']} calls failed")
            if pattern['calls']:
                print(f"  Error: {pattern['calls'][0].get('message')}")
        
        # 5. 상태 평가
        print("\n🎯 Status Assessment:")
        if pattern['successful_calls'] > 0:
            print("  ✅ Groq API is WORKING")
            print("  ✅ Authentication successful")
            print("  ✅ Model llama-3.1-8b-instant is accessible")
            
            # 비용 추정
            print("\n💰 Cost Estimate:")
            print(f"  • 3 test calls: ~{pattern['total_tokens']} tokens")
            print("  • Groq Free Tier: No charge")
            print("  • Status: FREE ✅")
        else:
            print("  ⚠️ Groq API connection issues detected")
            print("  • Check: API key validity")
            print("  • Check: Network connectivity")
            print("  • Check: Rate limits")
        
        # 6. 권장사항
        print("\n💡 Recommendations:")
        print("  ✅ Use Groq for: Fast inference, real-time applications")
        print("  ✅ Speed: Ultra-fast response times")
        print("  ✅ Cost: Very affordable (free tier available)")
        print("  🎯 Best models: llama-3.1-8b, qwen3-32b")
        
        print("\n" + "="*70)
        print(f"Report generated: {datetime.now().isoformat()}")
        print("="*70 + "\n")
        
        return "success"
    
    def save_report(self, filepath: str = "groq_usage_report.json"):
        """리포트 저장"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'provider': 'Groq',
            'api_key_valid': bool(self.api_key),
            'estimated_limits': self.estimate_usage_limits()['free_tier'],
            'status': 'Ready for production'
        }
        
        full_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            filepath
        )
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return full_path


def main():
    """메인 실행"""
    tracker = GroqUsageTracker()
    result = tracker.generate_report()
    
    if result == "success":
        filepath = tracker.save_report()
        print(f"✅ Report saved: {filepath}\n")


if __name__ == "__main__":
    main()
