"""
Tests - SHawn-Brain 자동화 테스트

테스트 구조:
- Unit Tests: 각 카트리지별 테스트
- Integration Tests: API 엔드포인트 테스트
- E2E Tests: 전체 흐름 테스트
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


# ============================================================================
# 1. Fixtures
# ============================================================================

@pytest.fixture
def api_client():
    """API 테스트 클라이언트"""
    from ddc.web.app import app
    return TestClient(app)


# ============================================================================
# 2. Unit Tests - Bio Cartridge
# ============================================================================

class TestBioCartridge:
    """Bio Cartridge 테스트"""
    
    def test_bio_interface_import(self):
        """Bio Interface import 테스트"""
        from ddc.cartridges.bio import bio_interface
        assert bio_interface is not None
    
    def test_analyze_cell_image(self):
        """세포 이미지 분석 테스트"""
        from ddc.cartridges.bio.bio_interface import BioCartridgeInterface
        
        interface = BioCartridgeInterface()
        result = interface.analyze_cell_image_with_neocortex(
            image_path="/path/to/image.jpg"
        )
        
        assert 'bio_analysis' in result
        assert 'neocortex_integration' in result


# ============================================================================
# 3. Unit Tests - Inv Cartridge
# ============================================================================

class TestInvCartridge:
    """Inv Cartridge 테스트"""
    
    def test_inv_interface_import(self):
        """Inv Interface import 테스트"""
        from ddc.cartridges.inv import inv_interface
        assert inv_interface is not None
    
    def test_analyze_stock(self):
        """주식 분석 테스트"""
        from ddc.cartridges.inv.inv_interface import InvCartridgeInterface
        
        interface = InvCartridgeInterface()
        result = interface.analyze_stock_with_neocortex(
            ticker="TSLA",
            analysis_data={}
        )
        
        assert 'ticker' in result
        assert 'basic_analysis' in result


# ============================================================================
# 4. Integration Tests - API Endpoints
# ============================================================================

class TestAPIEndpoints:
    """API 엔드포인트 테스트"""
    
    def test_root_endpoint(self, api_client):
        """루트 엔드포인트 테스트"""
        response = api_client.get("/")
        assert response.status_code == 200
        assert "SHawn-Brain API" in response.json()["name"]
    
    def test_health_check(self, api_client):
        """헬스 체크 테스트"""
        response = api_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "🟢 healthy"
    
    def test_system_status(self, api_client):
        """시스템 상태 테스트"""
        response = api_client.get("/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "version" in data
        assert "uptime" in data
        assert "neural_health" in data
    
    @patch('ddc.cartridges.bio.bio_interface.BioCartridgeInterface')
    def test_bio_analyze_endpoint(self, mock_bio, api_client):
        """Bio 분석 엔드포인트 테스트"""
        response = api_client.post(
            "/api/bio/analyze_image",
            json={
                "image_path": "/test/image.jpg",
                "use_neocortex": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "cell_type" in data
    
    @patch('ddc.cartridges.inv.inv_interface.InvCartridgeInterface')
    def test_inv_analyze_endpoint(self, mock_inv, api_client):
        """Inv 분석 엔드포인트 테스트"""
        response = api_client.post(
            "/api/inv/analyze_stock",
            json={
                "ticker": "TSLA",
                "use_neocortex": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "ticker" in data
    
    def test_neural_health_endpoint(self, api_client):
        """신경계 건강도 엔드포인트 테스트"""
        response = api_client.get("/api/neural/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "neural_levels" in data
        assert "average_health" in data


# ============================================================================
# 5. Performance Tests
# ============================================================================

class TestPerformance:
    """성능 테스트"""
    
    def test_api_response_time(self, api_client):
        """API 응답 시간 테스트"""
        import time
        
        start = time.time()
        response = api_client.get("/health")
        duration = (time.time() - start) * 1000  # ms
        
        assert response.status_code == 200
        assert duration < 100, f"Response time {duration}ms exceeds 100ms limit"
    
    def test_concurrent_requests(self, api_client):
        """동시 요청 테스트"""
        from concurrent.futures import ThreadPoolExecutor
        
        def make_request():
            return api_client.get("/health")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [f.result() for f in futures]
        
        assert all(r.status_code == 200 for r in results)


# ============================================================================
# 6. Monitoring Tests
# ============================================================================

class TestMonitoring:
    """모니터링 테스트"""
    
    def test_monitoring_dashboard(self):
        """모니터링 대시보드 테스트"""
        from ddc.web.monitoring_dashboard import monitor
        
        # 테스트 데이터 기록
        monitor.record_neural_activity('L1_Brainstem', 0.95, 5.0, 1000)
        
        # 대시보드 데이터 조회
        data = monitor.get_dashboard_data()
        
        assert 'neural_system' in data
        assert 'cartridges' in data
        assert 'performance' in data
    
    def test_monitoring_report(self):
        """모니터링 리포트 생성 테스트"""
        from ddc.web.monitoring_dashboard import get_monitoring_report
        
        report = get_monitoring_report()
        
        assert "SHawn-Brain 모니터링" in report
        assert "신경계 상태" in report


# ============================================================================
# 7. Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """에러 처리 테스트"""
    
    def test_invalid_endpoint(self, api_client):
        """잘못된 엔드포인트 테스트"""
        response = api_client.get("/invalid")
        assert response.status_code == 404
    
    def test_missing_required_field(self, api_client):
        """필수 필드 누락 테스트"""
        response = api_client.post(
            "/api/bio/analyze_image",
            json={}  # image_path 필수
        )
        assert response.status_code in [400, 422]


# ============================================================================
# 8. E2E Tests
# ============================================================================

class TestE2E:
    """엔드투엔드 테스트"""
    
    def test_full_bio_workflow(self, api_client):
        """Bio 전체 워크플로우"""
        # 1. 헬스 체크
        assert api_client.get("/health").status_code == 200
        
        # 2. Bio 분석 요청
        response = api_client.post(
            "/api/bio/analyze_image",
            json={"image_path": "/test/image.jpg"}
        )
        assert response.status_code == 200
        
        # 3. 신경계 상태 확인
        assert api_client.get("/api/neural/health").status_code == 200
    
    def test_full_inv_workflow(self, api_client):
        """Inv 전체 워크플로우"""
        # 1. 헬스 체크
        assert api_client.get("/health").status_code == 200
        
        # 2. Inv 분석 요청
        response = api_client.post(
            "/api/inv/analyze_stock",
            json={"ticker": "TSLA"}
        )
        assert response.status_code == 200
        
        # 3. 신경계 상태 확인
        assert api_client.get("/api/neural/cartridges").status_code == 200


# ============================================================================
# 9. Limbic System Tests (L2)
# ============================================================================

class TestLimbicSystem:
    """변린계 테스트"""

    def test_emotion_processor(self):
        """감정 프로세서 테스트"""
        from ddc.brain.brain_core.limbic_system.emotion_processor import EmotionProcessor

        processor = EmotionProcessor()

        # 감정 설정
        processor.set_emotion("happiness", 0.8)
        report = processor.get_emotional_state_report()

        assert report['current_state']['dominant_emotion'] == 'happiness'
        assert report['current_state']['intensity'] == 0.8
        assert report['stability_index'] >= 0.0
        assert report['stability_index'] <= 1.0

    def test_emotion_propagation(self):
        """감정 전파 테스트"""
        from ddc.brain.brain_core.limbic_system.emotion_processor import EmotionProcessor

        processor = EmotionProcessor()
        processor.set_emotion("happiness", 0.9)

        report = processor.get_emotional_state_report()
        # 행복은 놀람을 증가시켜야 함
        assert report['all_emotions']['surprise'] > 0.0

    def test_value_assessment(self):
        """가치 평가 테스트"""
        from ddc.brain.brain_core.limbic_system.value_assessment import ValueAssessment

        assessor = ValueAssessment()

        # 좋은 결정 평가
        result = assessor.assess_decision(
            domain="biology",
            decision="Research",
            action_description="rigorous verification honest accurate"
        )

        assert result['overall_alignment'] > 0.0
        assert 'value_influences' in result

    def test_emotional_diversity(self):
        """감정 다양성 테스트"""
        from ddc.brain.brain_core.limbic_system.emotion_processor import EmotionProcessor

        processor = EmotionProcessor()
        processor.set_emotion("happiness", 0.5)
        processor.set_emotion("surprise", 0.3)
        processor.set_emotion("fear", 0.2)

        report = processor.get_emotional_state_report()
        assert report['diversity_index'] > 0.3  # 여러 감정이 활성화됨


# ============================================================================
# 10. Neocortex Tests - Parietal (L3)
# ============================================================================

class TestParietalCortex:
    """두정엽 테스트"""

    def test_innovation_engine(self):
        """혁신 엔진 테스트"""
        from ddc.brain.neocortex.parietal.innovation_engine import InnovationEngine

        engine = InnovationEngine()

        # 개념 교배
        idea = engine.cross_domain_synthesis(
            concept1="adaptation",
            domain1="biology",
            concept2="diversification",
            domain2="finance"
        )

        assert idea.novelty_score >= 0.3
        assert idea.feasibility_score >= 0.3
        assert idea.impact_score >= 0.4

    def test_conceptual_similarity(self):
        """개념적 유사성 테스트"""
        from ddc.brain.neocortex.parietal.innovation_engine import InnovationEngine

        engine = InnovationEngine()

        # 같은 개념
        sim1 = engine._calculate_conceptual_similarity(
            "adaptation", "biology", "adaptation", "biology"
        )
        assert sim1 >= 0.7

        # 다른 개념
        sim2 = engine._calculate_conceptual_similarity(
            "adaptation", "biology", "divergent", "finance"
        )
        assert sim2 >= 0.0
        assert sim2 <= 1.0

    def test_idea_evaluation(self):
        """아이디어 평가 테스트"""
        from ddc.brain.neocortex.parietal.innovation_engine import InnovationEngine

        engine = InnovationEngine()
        idea = engine.cross_domain_synthesis(
            "evolution", "biology", "optimization", "technology"
        )

        evaluation = engine.evaluate_idea(idea)

        assert 'overall_score' in evaluation
        assert 'viability' in evaluation
        assert evaluation['overall_score'] >= 0.0
        assert evaluation['overall_score'] <= 1.0


# ============================================================================
# 11. Edge Cases & Stress Tests
# ============================================================================

class TestEdgeCases:
    """엣지 케이스 테스트"""

    def test_empty_input(self, api_client):
        """빈 입력 테스트"""
        response = api_client.post(
            "/api/bio/analyze_image",
            json={"image_path": ""}
        )
        assert response.status_code in [200, 400, 422]

    def test_large_payload(self, api_client):
        """큰 페이로드 테스트"""
        large_data = "x" * 10000
        response = api_client.post(
            "/api/bio/analyze_image",
            json={"image_path": large_data}
        )
        assert response.status_code in [200, 400, 413]

    def test_special_characters(self, api_client):
        """특수 문자 테스트"""
        response = api_client.post(
            "/api/inv/analyze_stock",
            json={"ticker": "TS@#$%"}
        )
        assert response.status_code in [200, 400, 422]

    def test_emotion_boundary_values(self):
        """감정 경계값 테스트"""
        from ddc.brain.brain_core.limbic_system.emotion_processor import EmotionProcessor

        processor = EmotionProcessor()

        # 최대값
        processor.set_emotion("happiness", 1.0)
        assert processor.current_state.emotions['happiness'] == 1.0

        # 최소값
        processor.set_emotion("sadness", 0.0)
        assert processor.current_state.emotions['sadness'] == 0.0

        # 범위 초과
        processor.set_emotion("anger", 1.5)
        assert processor.current_state.emotions['anger'] == 1.0


# ============================================================================
# 12. Integration Tests - Neural System
# ============================================================================

class TestNeuralSystemIntegration:
    """신경계 통합 테스트"""

    def test_neural_signal_flow(self):
        """신경 신호 흐름 테스트"""
        from ddc.brain.brain_core.limbic_system.emotion_processor import EmotionProcessor
        from ddc.brain.neocortex.parietal.innovation_engine import InnovationEngine

        # L2 감정 설정
        processor = EmotionProcessor()
        processor.set_emotion("surprise", 0.7)
        emotion_state = processor.get_emotional_state_report()

        # L3 창의성 엔진
        engine = InnovationEngine()
        idea = engine.cross_domain_synthesis(
            "emergence", "biology", "scalability", "technology"
        )

        # 둘 다 정상 작동
        assert emotion_state['current_state']['intensity'] > 0.0
        assert idea.novelty_score >= 0.3

    def test_multi_level_processing(self, api_client):
        """다층 처리 테스트"""
        # L1: 기본 기능
        health = api_client.get("/health")
        assert health.status_code == 200

        # L2: 감정/주의
        neural_health = api_client.get("/api/neural/health")
        assert neural_health.status_code == 200

        # L3: 분석
        bio_response = api_client.post(
            "/api/bio/analyze_image",
            json={"image_path": "/test.jpg"}
        )
        assert bio_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
