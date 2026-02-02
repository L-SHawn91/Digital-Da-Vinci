#!/usr/bin/env python3
"""
🧠 SHawn-Brain 디지털 신경계 시각화
디지털 다빈치 프로젝트 전체 구조도

박사님의 요청: "전체 숀두뇌를 크게 그리고 세부 조직들 표시하고 
세부 옆이나 신경계까지 그린 그림 - 눈에 세부적인 내용까지 잘 들어오게"

생성: matplotlib + graphviz 활용
출력: 고해상도 PNG + PDF
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, FancyArrowPatch, Rectangle
import numpy as np
from matplotlib import font_manager as fm
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# 한글 폰트 설정
plt.rcParams['font.sans-serif'] = ['Apple Color Emoji', 'DejaVu Sans']

def create_shawn_brain_visualization():
    """SHawn-Brain 전체 구조 시각화"""
    
    # Figure 생성 (매우 큼 - 고해상도)
    fig = plt.figure(figsize=(24, 16), dpi=300, facecolor='white')
    
    # 메인 축
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 제목
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ax.text(5, 9.7, '🧠 SHawn-Brain: Digital Leonardo da Vinci Project', 
            fontsize=32, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFE5B4', edgecolor='black', linewidth=3))
    
    ax.text(5, 9.2, 'Complete Digital Nervous System Architecture', 
            fontsize=16, ha='center', style='italic', color='#333333')
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 중앙: 뇌 구조 (Brain Silhouette)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # 전체 뇌 배경 (회색)
    brain_circle = Circle((5, 4.5), 2.2, color='#E8E8E8', ec='black', linewidth=3, zorder=1)
    ax.add_patch(brain_circle)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 신피질 영역 (4개 엽)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # 색상 정의
    colors = {
        'prefrontal': '#FF6B6B',      # 빨강
        'temporal': '#4ECDC4',         # 청록
        'parietal': '#45B7D1',         # 파랑
        'occipital': '#96CEB4'         # 초록
    }
    
    # 1. 전전두엽 (좌상단)
    prefrontal = Wedge((5, 4.5), 2.0, 90, 150, width=0.6, 
                       facecolor=colors['prefrontal'], edgecolor='black', linewidth=2, zorder=2)
    ax.add_patch(prefrontal)
    ax.text(4.0, 5.8, 'Prefrontal\n(Gemini)\nPlanning', fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white', zorder=3)
    
    # 2. 측두엽 (우상단)
    temporal = Wedge((5, 4.5), 2.0, 30, 90, width=0.6, 
                     facecolor=colors['temporal'], edgecolor='black', linewidth=2, zorder=2)
    ax.add_patch(temporal)
    ax.text(6.0, 5.8, 'Temporal\n(Anthropic)\nMemory', fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white', zorder=3)
    
    # 3. 두정엽 (좌하단)
    parietal = Wedge((5, 4.5), 2.0, 210, 270, width=0.6, 
                     facecolor=colors['parietal'], edgecolor='black', linewidth=2, zorder=2)
    ax.add_patch(parietal)
    ax.text(4.0, 3.2, 'Parietal\n(DeepSeek)\nIntegration', fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white', zorder=3)
    
    # 4. 후두엽 (우하단)
    occipital = Wedge((5, 4.5), 2.0, 270, 330, width=0.6, 
                      facecolor=colors['occipital'], edgecolor='black', linewidth=2, zorder=2)
    ax.add_patch(occipital)
    ax.text(6.0, 3.2, 'Occipital\n(Groq)\nAnalysis', fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white', zorder=3)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 변연계 (내부 원)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    limbic = Circle((5, 4.5), 1.3, color='#FFA07A', ec='black', linewidth=2.5, zorder=4)
    ax.add_patch(limbic)
    ax.text(5, 4.8, 'Limbic\nSystem', fontsize=11, fontweight='bold', ha='center', 
            color='white', zorder=5)
    ax.text(5, 4.2, '(Gemini 60%)', fontsize=8, ha='center', color='white', zorder=5)
    ax.text(5, 3.9, 'Decision\nMaking', fontsize=8, ha='center', color='white', zorder=5)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 뇌간 (중심)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    brainstem = Circle((5, 4.5), 0.7, color='#FF4500', ec='black', linewidth=2.5, zorder=6)
    ax.add_patch(brainstem)
    ax.text(5, 4.7, 'Brainstem', fontsize=9, fontweight='bold', ha='center', 
            color='white', zorder=7)
    ax.text(5, 4.3, '(Groq 50%)', fontsize=7, ha='center', color='white', zorder=7)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 신경망 (NeuroNet) - 외부 원
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    neuronet = Circle((5, 4.5), 2.8, fill=False, ec='#9370DB', 
                      linewidth=3, linestyle='--', zorder=8)
    ax.add_patch(neuronet)
    ax.text(7.8, 7.0, 'NeuroNet', fontsize=11, fontweight='bold', color='#9370DB', zorder=8)
    ax.text(7.8, 6.7, '(100ms routing)', fontsize=8, color='#9370DB', zorder=8)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 좌측: Level 1-4 상세 정보
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Level 1: Brainstem
    level1_box = FancyBboxPatch((0.2, 6.5), 2.0, 1.8, boxstyle="round,pad=0.1",
                               facecolor='#FFE5E5', edgecolor='#FF4500', linewidth=2.5)
    ax.add_patch(level1_box)
    ax.text(1.2, 8.0, 'Level 1', fontsize=11, fontweight='bold', ha='center', color='#FF4500')
    ax.text(1.2, 7.7, 'Brainstem', fontsize=10, fontweight='bold', ha='center')
    ax.text(1.2, 7.3, 'Diagnosis', fontsize=8, ha='center', style='italic')
    ax.text(1.2, 6.95, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(1.2, 6.65, 'Groq 50%', fontsize=7, ha='center', color='#FF4500')
    
    # Level 2: Limbic
    level2_box = FancyBboxPatch((0.2, 4.2), 2.0, 1.8, boxstyle="round,pad=0.1",
                               facecolor='#FFE0D5', edgecolor='#FFA07A', linewidth=2.5)
    ax.add_patch(level2_box)
    ax.text(1.2, 5.7, 'Level 2', fontsize=11, fontweight='bold', ha='center', color='#FFA07A')
    ax.text(1.2, 5.4, 'Limbic', fontsize=10, fontweight='bold', ha='center')
    ax.text(1.2, 5.0, 'Decision', fontsize=8, ha='center', style='italic')
    ax.text(1.2, 4.65, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(1.2, 4.35, 'Gemini 60%', fontsize=7, ha='center', color='#FFA07A')
    
    # Level 3: Neocortex
    level3_box = FancyBboxPatch((0.2, 1.9), 2.0, 1.8, boxstyle="round,pad=0.1",
                               facecolor='#E5F5FF', edgecolor='#4ECDC4', linewidth=2.5)
    ax.add_patch(level3_box)
    ax.text(1.2, 3.4, 'Level 3', fontsize=11, fontweight='bold', ha='center', color='#4ECDC4')
    ax.text(1.2, 3.1, 'Neocortex', fontsize=10, fontweight='bold', ha='center')
    ax.text(1.2, 2.7, 'Learning', fontsize=8, ha='center', style='italic')
    ax.text(1.2, 2.35, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(1.2, 2.05, '4 Lobes', fontsize=7, ha='center', color='#4ECDC4')
    
    # Level 4: NeuroNet
    level4_box = FancyBboxPatch((0.2, -0.4), 2.0, 1.8, boxstyle="round,pad=0.1",
                               facecolor='#F0E5FF', edgecolor='#9370DB', linewidth=2.5)
    ax.add_patch(level4_box)
    ax.text(1.2, 1.1, 'Level 4', fontsize=11, fontweight='bold', ha='center', color='#9370DB')
    ax.text(1.2, 0.8, 'NeuroNet', fontsize=10, fontweight='bold', ha='center')
    ax.text(1.2, 0.4, 'Routing', fontsize=8, ha='center', style='italic')
    ax.text(1.2, 0.05, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(1.2, -0.25, '100ms⚡', fontsize=7, ha='center', color='#9370DB')
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 우측: 카트리지와 시스템 정보
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Bio-Cartridge
    bio_box = FancyBboxPatch((7.8, 6.5), 2.0, 1.8, boxstyle="round,pad=0.1",
                            facecolor='#E8F5E9', edgecolor='#4CAF50', linewidth=2.5)
    ax.add_patch(bio_box)
    ax.text(8.8, 8.0, 'Bio', fontsize=11, fontweight='bold', ha='center', color='#4CAF50')
    ax.text(8.8, 7.7, 'Cartridge', fontsize=10, fontweight='bold', ha='center')
    ax.text(8.8, 7.3, 'Stem Cell', fontsize=8, ha='center', style='italic')
    ax.text(8.8, 6.95, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(8.8, 6.65, 'Analysis', fontsize=7, ha='center', color='#4CAF50')
    
    # Investment-Cartridge
    inv_box = FancyBboxPatch((7.8, 4.2), 2.0, 1.8, boxstyle="round,pad=0.1",
                            facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=2.5)
    ax.add_patch(inv_box)
    ax.text(8.8, 5.7, 'Investment', fontsize=11, fontweight='bold', ha='center', color='#FF9800')
    ax.text(8.8, 5.35, 'Cartridge', fontsize=10, fontweight='bold', ha='center')
    ax.text(8.8, 4.95, 'Finance', fontsize=8, ha='center', style='italic')
    ax.text(8.8, 4.6, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(8.8, 4.3, 'Trading', fontsize=7, ha='center', color='#FF9800')
    
    # 효율성 지표
    eff_box = FancyBboxPatch((7.8, 1.9), 2.0, 1.8, boxstyle="round,pad=0.1",
                            facecolor='#FCE4EC', edgecolor='#E91E63', linewidth=2.5)
    ax.add_patch(eff_box)
    ax.text(8.8, 3.4, 'Efficiency', fontsize=11, fontweight='bold', ha='center', color='#E91E63')
    ax.text(8.8, 3.0, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(8.8, 2.65, 'Avg: 9.58/10', fontsize=8, ha='center', color='#E91E63', fontweight='bold')
    ax.text(8.8, 2.3, 'Cost: -99.98%', fontsize=8, ha='center', color='#E91E63', fontweight='bold')
    ax.text(8.8, 1.95, '10K routes/sec', fontsize=7, ha='center', color='#E91E63')
    
    # DCRS 시스템
    dcrs_box = FancyBboxPatch((7.8, -0.4), 2.0, 1.8, boxstyle="round,pad=0.1",
                             facecolor='#E3F2FD', edgecolor='#2196F3', linewidth=2.5)
    ax.add_patch(dcrs_box)
    ax.text(8.8, 1.1, 'DCRS', fontsize=11, fontweight='bold', ha='center', color='#2196F3')
    ax.text(8.8, 0.7, 'Daily Neural', fontsize=8, ha='center', color='#2196F3')
    ax.text(8.8, 0.4, 'Recalibration', fontsize=8, ha='center', color='#2196F3')
    ax.text(8.8, 0.05, '━━━━━━━━━━━', fontsize=7, ha='center')
    ax.text(8.8, -0.25, '@08:00 UTC+9', fontsize=7, ha='center', color='#2196F3')
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 하단: 데이터 흐름 및 신경 경로
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # 입력 화살표
    arrow_in = FancyArrowPatch((0.5, -1.2), (3, 4.5),
                              arrowstyle='->', mutation_scale=30, 
                              linewidth=3, color='#4CAF50', zorder=10)
    ax.add_patch(arrow_in)
    ax.text(1.2, -1.5, 'Input', fontsize=9, fontweight='bold', color='#4CAF50')
    
    # 출력 화살표
    arrow_out = FancyArrowPatch((7, 4.5), (9.5, -1.2),
                               arrowstyle='->', mutation_scale=30,
                               linewidth=3, color='#FF5722', zorder=10)
    ax.add_patch(arrow_out)
    ax.text(8.8, -1.5, 'Output', fontsize=9, fontweight='bold', color='#FF5722')
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 범례 및 설명
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    legend_y = 0.2
    ax.text(3.5, legend_y + 0.3, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 
            fontsize=8, ha='center', color='gray')
    ax.text(3.5, legend_y - 0.1, 'Key Metrics:', fontsize=9, fontweight='bold', ha='center')
    ax.text(3.5, legend_y - 0.5, '• Efficiency: 9.58/10 avg  • Cost: ~$5/month  • Latency: 100ms (L4)', 
            fontsize=8, ha='center', color='#333333')
    ax.text(3.5, legend_y - 0.85, '• Processing: 10K routes/sec  • Learning: +0.5-1% daily  • Models: 10 APIs', 
            fontsize=8, ha='center', color='#333333')
    
    plt.tight_layout()
    return fig

# 생성 및 저장
print("🧠 Generating SHawn-Brain Visualization...")
fig = create_shawn_brain_visualization()

# PNG로 저장 (고해상도)
png_path = '/Users/soohyunglee/.openclaw/workspace/SHawn-Brain_Architecture.png'
fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ PNG saved: {png_path}")

# PDF로도 저장
pdf_path = '/Users/soohyunglee/.openclaw/workspace/SHawn-Brain_Architecture.pdf'
fig.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor='white')
print(f"✅ PDF saved: {pdf_path}")

plt.close(fig)

print("\n✨ 시각화 완료!")
print(f"📊 이미지 크기: 24x16 inches, 300 DPI (매우 고해상도)")
print(f"📁 저장된 파일: PNG + PDF")
