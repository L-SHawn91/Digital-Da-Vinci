#!/usr/bin/env python3
"""
일일 테스트 결과 기반 TOOLS.md 자동 생성

기능:
1. daily_test_results.json 읽기
2. 점수에 따라 분배표 정렬
3. TOOLS.md 자동 생성 (날짜 포함)
4. 분배표 동적 업데이트
"""

import json
from datetime import datetime

class DailyAllocationUpdater:
    """일일 테스트 결과 기반 분배표 자동 업데이트"""
    
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M:%S")
    
    def load_test_results(self):
        """일일 테스트 결과 로드"""
        
        try:
            with open("/Users/soohyunglee/.openclaw/workspace/daily_test_results.json", "r") as f:
                return json.load(f)
        except:
            print("❌ 테스트 결과 파일 없음")
            return None
    
    def generate_tools_md(self, test_results):
        """TOOLS.md 자동 생성"""
        
        if not test_results:
            return None
        
        models = test_results.get("models", [])
        adjustments = test_results.get("allocation_adjustments", {})
        report = test_results.get("report", {})
        
        # 모델 순위 생성
        ranked = sorted(models, key=lambda x: x["overall_score"], reverse=True)
        
        md_content = f"""# TOOLS.md - 일일 자동 업데이트 분배표 ({self.date})
## ✅ 매일 아침 자동 테스트 후 수정됨 ({self.time})

---

## 🌅 **오늘 테스트 결과**

```
📊 평균 점수: {report.get('average_score', 0)}/10
✅ 정상 API: {report.get('total_tests', 0)}/10
🥇 최고: {report.get('best_api', 'N/A')} ({report.get('best_score', 0)}/10)
🥉 최저: {report.get('worst_api', 'N/A')} ({report.get('worst_score', 0)}/10)
```

---

## 🏆 **오늘 API 순위**

"""
        
        for i, model in enumerate(ranked, 1):
            emoji = ["🥇", "🥈", "🥉"] + ["🏅"] * 10
            md_content += f"""
{emoji[i-1]} **{i}. {model['api']}** - {model['overall_score']}/10
   • 응답시간: {model['response_time_ms']}ms
   • 품질: {model['quality_score']}/10
   • 안정성: {model['reliability_score']}/10
   • 효율성: {model['cost_efficiency']}/10
   • 상태: {model['status']}
   • 메모: {model['note']}
"""
        
        md_content += """
---

## 📊 **동적 조정된 분배표 (점수 기반)**

### **📚 연구/분석**
"""
        
        if adjustments:
            research = adjustments.get("research", {})
            for key, value in research.items():
                md_content += f"\n   {key}: {value}"
        
        md_content += """

### **💻 코딩/복잡작업**
"""
        
        if adjustments:
            coding = adjustments.get("coding", {})
            for key, value in coding.items():
                md_content += f"\n   {key}: {value}"
        
        md_content += """

### **⚡ 긴급/빠른응답**
"""
        
        if adjustments:
            urgent = adjustments.get("urgent", {})
            for key, value in urgent.items():
                md_content += f"\n   {key}: {value}"
        
        md_content += """

### **📞 일반대화**
"""
        
        if adjustments:
            chat = adjustments.get("chat", {})
            for key, value in chat.items():
                md_content += f"\n   {key}: {value}"
        
        md_content += """

### **🧬 생물학/이미지**
"""
        
        if adjustments:
            image = adjustments.get("image", {})
            for key, value in image.items():
                md_content += f"\n   {key}: {value}"
        
        md_content += """

### **📊 데이터분석**
"""
        
        if adjustments:
            data = adjustments.get("data", {})
            for key, value in data.items():
                md_content += f"\n   {key}: {value}"
        
        md_content += f"""

---

## 📝 **점수 반영 기준**

```
🥇 순위 1-3: 최우선 (60-70%)
🏅 순위 4-6: 주요 (20-30%)
🏅 순위 7-10: 보조 (5-15%)

점수 자동 반영:
  • 매일 08:00 테스트 실행
  • 점수 기반 순위 변동
  • 분배표 자동 수정
  • TOOLS.md 자동 업데이트
```

---

**🔄 업데이트 자동화**

• 매일 아침 {self.time} 테스트 완료
• 전날 결과물 점수 반영
• 분배표 동적 조정
• 일일 리포트 생성

**다음 업데이트: 내일 08:00**
"""
        
        return md_content
    
    def save_tools_md(self, content):
        """TOOLS.md 저장"""
        
        if not content:
            return False
        
        try:
            with open("/Users/soohyunglee/.openclaw/workspace/TOOLS.md", "w") as f:
                f.write(content)
            print(f"✅ TOOLS.md 업데이트 완료 ({self.date})")
            return True
        except Exception as e:
            print(f"❌ TOOLS.md 저장 실패: {e}")
            return False
    
    def create_daily_report_file(self, test_results):
        """일일 리포트 파일 생성"""
        
        if not test_results:
            return False
        
        filename = f"/Users/soohyunglee/.openclaw/workspace/daily_reports/{self.date}_report.json"
        
        try:
            import os
            os.makedirs("/Users/soohyunglee/.openclaw/workspace/daily_reports", exist_ok=True)
            
            with open(filename, "w") as f:
                json.dump(test_results, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 일일 리포트 저장: {filename}")
            return True
        except Exception as e:
            print(f"❌ 리포트 저장 실패: {e}")
            return False
    
    def run(self):
        """전체 실행"""
        
        print("\n" + "="*100)
        print(f"🔄 일일 분배표 자동 업데이트 ({self.date})")
        print("="*100 + "\n")
        
        # Step 1: 테스트 결과 로드
        test_results = self.load_test_results()
        
        if not test_results:
            print("⚠️ 테스트 결과 없음, 스킵합니다")
            return
        
        # Step 2: TOOLS.md 생성
        print("📝 TOOLS.md 생성 중...")
        tools_md = self.generate_tools_md(test_results)
        
        # Step 3: TOOLS.md 저장
        if tools_md:
            self.save_tools_md(tools_md)
        
        # Step 4: 일일 리포트 저장
        self.create_daily_report_file(test_results)
        
        # Step 5: 완료 메시지
        print("\n" + "="*100)
        print("✅ 분배표 자동 업데이트 완료!")
        print("="*100)
        print(f"""
📊 업데이트 내용:
   • TOOLS.md: 점수 기반 재정렬
   • 분배표: {test_results.get('report', {}).get('best_api', 'N/A')} 최우선
   • 리포트: {self.date}_report.json 저장

🔄 다음 업데이트: 내일 08:00
""")

if __name__ == "__main__":
    updater = DailyAllocationUpdater()
    updater.run()
