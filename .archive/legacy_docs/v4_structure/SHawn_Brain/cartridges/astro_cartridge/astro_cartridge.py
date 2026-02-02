"""
AstroCartridge: 우주과학 전문 카트리지 (Groq 초고속 개발자판)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

이 모듈은 우주과학의 핵심 개념들을 다룹니다:
- 별 분류 및 특성
- 행성계 및 외계행성
- 우주 탐사 임무 정보
- 천체역학 및 궤도 계산

작성자: Groq API 초고속 개발자
버전: 1.0.0
라이선스: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import math
import json


# ════════════════════════════════════════════════════════════════
# 1️⃣  ENUMS: 우주과학 분류 체계
# ════════════════════════════════════════════════════════════════

class SpectralType(Enum):
    """별의 분광형 분류 (OBAFGKM)"""
    O = ("초거대질량별", 30000, 100, 25000)  # (이름, 표면온도K, 질량배(태양), 수명억년)
    B = ("대질량별", 10000, 17, 300)
    A = ("중간질량별", 7500, 3.2, 1000)
    F = ("황색별", 6000, 1.6, 3000)
    G = ("태양형별", 5800, 1.0, 10000)  # 우리 태양
    K = ("주황색별", 3700, 0.8, 17000)
    M = ("적색왜성", 2400, 0.3, 56000)

    def info(self) -> Dict[str, any]:
        """분광형 정보 반환"""
        name, temp, mass, lifetime = self.value
        return {
            "name": name,
            "surface_temp_k": temp,
            "mass_solar": mass,
            "lifetime_million_years": lifetime
        }


class PlanetType(Enum):
    """행성 분류"""
    TERRESTRIAL = "암석형 행성"
    SUPER_EARTH = "슈퍼 지구"
    NEPTUNE_LIKE = "해왕성형"
    JOVIAN = "목성형"
    PULSAR = "펄서 행성"


class MissionStatus(Enum):
    """우주 탐사 임무 상태"""
    PLANNED = "계획 중"
    ACTIVE = "진행 중"
    COMPLETED = "완료"
    FAILED = "실패"
    RETIRED = "은퇴"


# ════════════════════════════════════════════════════════════════
# 2️⃣  DATACLASSES: 우주 객체 표현
# ════════════════════════════════════════════════════════════════

@dataclass
class CelestialBody:
    """천체 기본 정보"""
    name: str
    mass_kg: float  # 질량 (kg)
    radius_km: float  # 반경 (km)
    distance_from_sun_au: Optional[float] = None  # 태양으로부터의 거리 (AU)
    
    def gravity(self) -> float:
        """표면 중력 가속도 (m/s²) 계산"""
        G = 6.674e-11  # 만유인력상수
        try:
            radius_m = self.radius_km * 1000
            return (G * self.mass_kg) / (radius_m ** 2)
        except (ZeroDivisionError, ValueError):
            return 0.0
    
    def escape_velocity(self) -> float:
        """탈출속도 (km/s) 계산"""
        try:
            g = self.gravity()
            radius_m = self.radius_km * 1000
            return math.sqrt(2 * g * radius_m) / 1000
        except (ValueError, ZeroDivisionError):
            return 0.0
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            "name": self.name,
            "mass_kg": self.mass_kg,
            "radius_km": self.radius_km,
            "distance_au": self.distance_from_sun_au,
            "surface_gravity_ms2": round(self.gravity(), 2),
            "escape_velocity_kms": round(self.escape_velocity(), 2)
        }


@dataclass
class Star:
    """별 정보"""
    name: str
    spectral_type: SpectralType
    magnitude: float  # 겉보기 등급
    distance_ly: float  # 거리 (광년)
    mass_solar: float  # 태양질량 단위
    radius_solar: float  # 태양반경 단위
    luminosity_solar: float  # 태양광도 단위
    
    def info(self) -> Dict:
        """별의 상세 정보"""
        spec_info = self.spectral_type.info()
        return {
            "name": self.name,
            "spectral_type": self.spectral_type.name,
            "spectral_info": spec_info,
            "apparent_magnitude": self.magnitude,
            "distance_light_years": self.distance_ly,
            "mass_solar_masses": self.mass_solar,
            "radius_solar_radii": self.radius_solar,
            "luminosity_solar_luminosities": self.luminosity_solar,
            "surface_temp_k": spec_info["surface_temp_k"],
            "lifetime_million_years": spec_info["lifetime_million_years"]
        }
    
    def absolute_magnitude(self) -> float:
        """절대등급 계산"""
        # 겉보기 등급과 절대등급의 거리계수 공식
        try:
            distance_pc = self.distance_ly / 3.26156
            distance_modulus = 5 * math.log10(distance_pc) - 5
            return self.magnitude - distance_modulus
        except (ValueError, ZeroDivisionError):
            return self.magnitude


@dataclass
class ExoplanetSystem:
    """외계행성계 정보"""
    name: str
    star: Star
    planets: List[Dict] = field(default_factory=list)
    discovery_year: int = 0
    discovery_method: str = "Unknown"
    
    def add_planet(self, planet_name: str, planet_type: PlanetType, 
                   orbital_period_days: float, semi_major_axis_au: float) -> None:
        """행성 추가"""
        try:
            planet = {
                "name": planet_name,
                "type": planet_type.value,
                "orbital_period_days": orbital_period_days,
                "semi_major_axis_au": semi_major_axis_au,
                "orbital_velocity_kms": self._calculate_orbital_velocity(semi_major_axis_au)
            }
            self.planets.append(planet)
        except Exception as e:
            raise ValueError(f"행성 추가 실패: {e}")
    
    def _calculate_orbital_velocity(self, semi_major_axis_au: float) -> float:
        """궤도 속도 계산 (km/s)"""
        try:
            # 케플러 법칙 적용
            M = self.star.mass_solar
            a = semi_major_axis_au * 1.496e8  # AU -> km
            G = 6.674e-11
            sun_mass_kg = 1.989e30
            return math.sqrt(G * M * sun_mass_kg / a) / 1000
        except (ValueError, ZeroDivisionError):
            return 0.0
    
    def habitable_zone(self) -> Tuple[float, float]:
        """거주가능 영역 (AU) 반환: (내부경계, 외부경계)"""
        try:
            L = self.star.luminosity_solar
            inner = math.sqrt(L / 1.1)  # 근사값
            outer = math.sqrt(L / 0.53)
            return (round(inner, 3), round(outer, 3))
        except (ValueError, ZeroDivisionError):
            return (0.0, 0.0)
    
    def to_dict(self) -> Dict:
        """시스템 정보 딕셔너리"""
        hz_inner, hz_outer = self.habitable_zone()
        return {
            "system_name": self.name,
            "star": self.star.info(),
            "planets": self.planets,
            "planet_count": len(self.planets),
            "discovery_year": self.discovery_year,
            "discovery_method": self.discovery_method,
            "habitable_zone_au": {
                "inner_boundary": hz_inner,
                "outer_boundary": hz_outer
            }
        }


@dataclass
class SpaceMission:
    """우주 탐사 임무 정보"""
    name: str
    agency: str  # 우주기관
    launch_date: str  # YYYY-MM-DD
    status: MissionStatus
    target: str  # 목표
    instruments: List[str] = field(default_factory=list)
    discoveries: List[str] = field(default_factory=list)
    
    def mission_duration_days(self) -> Optional[int]:
        """임무 기간 (일수)"""
        try:
            launch = datetime.strptime(self.launch_date, "%Y-%m-%d")
            duration = datetime.now() - launch
            return duration.days if self.status != MissionStatus.PLANNED else None
        except ValueError:
            return None
    
    def summary(self) -> Dict:
        """임무 요약"""
        return {
            "mission_name": self.name,
            "agency": self.agency,
            "launch_date": self.launch_date,
            "status": self.status.value,
            "target": self.target,
            "instrument_count": len(self.instruments),
            "instruments": self.instruments[:5],  # 처음 5개만
            "discoveries": len(self.discoveries),
            "mission_duration_days": self.mission_duration_days()
        }


# ════════════════════════════════════════════════════════════════
# 3️⃣  MAIN CARTRIDGE: AstroCartridge 클래스
# ════════════════════════════════════════════════════════════════

class AstroCartridge:
    """
    우주과학 전문 카트리지
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    별, 행성계, 우주 탐사에 대한 정보와 분석을 제공합니다.
    """
    
    def __init__(self) -> None:
        """카트리지 초기화"""
        self.stars: Dict[str, Star] = {}
        self.exoplanet_systems: Dict[str, ExoplanetSystem] = {}
        self.missions: Dict[str, SpaceMission] = {}
        self.version = "1.0.0"
        self._load_sample_data()
    
    def _load_sample_data(self) -> None:
        """기본 우주 객체 로드"""
        # 우리 태양
        sun = Star(
            name="Sun",
            spectral_type=SpectralType.G,
            magnitude=-26.74,
            distance_ly=0,
            mass_solar=1.0,
            radius_solar=1.0,
            luminosity_solar=1.0
        )
        self.stars["Sun"] = sun
        
        # 시리우스 (밤하늘에서 가장 밝은 별)
        sirius = Star(
            name="Sirius",
            spectral_type=SpectralType.A,
            magnitude=-1.46,
            distance_ly=8.6,
            mass_solar=2.02,
            radius_solar=1.71,
            luminosity_solar=25.4
        )
        self.stars["Sirius"] = sirius
        
        # Proxima Centauri (태양에서 가장 가까운 별)
        proxima = Star(
            name="Proxima Centauri",
            spectral_type=SpectralType.M,
            magnitude=11.05,
            distance_ly=4.24,
            mass_solar=0.12,
            radius_solar=0.14,
            luminosity_solar=0.0017
        )
        self.stars["Proxima Centauri"] = proxima
        
        # TRAPPIST-1 행성계 (잘 알려진 외계행성계)
        trappist1 = Star(
            name="TRAPPIST-1",
            spectral_type=SpectralType.M,
            magnitude=18.8,
            distance_ly=39,
            mass_solar=0.089,
            radius_solar=0.117,
            luminosity_solar=0.000546
        )
        self.stars["TRAPPIST-1"] = trappist1
        
        # TRAPPIST-1 행성계 생성
        trappist_system = ExoplanetSystem(
            name="TRAPPIST-1 System",
            star=trappist1,
            discovery_year=2017,
            discovery_method="Transit"
        )
        
        # 7개 행성 추가
        planets_data = [
            ("TRAPPIST-1b", PlanetType.TERRESTRIAL, 1.51, 0.01154),
            ("TRAPPIST-1c", PlanetType.TERRESTRIAL, 2.42, 0.01581),
            ("TRAPPIST-1d", PlanetType.TERRESTRIAL, 4.05, 0.02227),
            ("TRAPPIST-1e", PlanetType.TERRESTRIAL, 6.10, 0.02925),  # 거주가능 영역
            ("TRAPPIST-1f", PlanetType.TERRESTRIAL, 9.21, 0.03853),  # 거주가능 영역
            ("TRAPPIST-1g", PlanetType.TERRESTRIAL, 12.35, 0.04680),  # 거주가능 영역
            ("TRAPPIST-1h", PlanetType.TERRESTRIAL, 18.77, 0.06193),
        ]
        
        for name, ptype, period, axis in planets_data:
            trappist_system.add_planet(name, ptype, period, axis)
        
        self.exoplanet_systems["TRAPPIST-1"] = trappist_system
        
        # 유명 우주 탐사 임무들
        missions_data = [
            SpaceMission(
                name="Hubble Space Telescope",
                agency="NASA/ESA",
                launch_date="1990-04-25",
                status=MissionStatus.ACTIVE,
                target="Universe",
                instruments=["Wide Field Camera 3", "Spectrograph", "Photometer"],
                discoveries=["Dark Energy", "Hubble Constant", "Black Holes"]
            ),
            SpaceMission(
                name="James Webb Space Telescope",
                agency="NASA/ESA/CSA",
                launch_date="2021-12-25",
                status=MissionStatus.ACTIVE,
                target="Early Universe",
                instruments=["NIRCam", "NIRSpec", "MIRI"],
                discoveries=["Earliest Galaxies", "Exoplanet Atmospheres"]
            ),
            SpaceMission(
                name="Mars Rover Perseverance",
                agency="NASA",
                launch_date="2020-07-30",
                status=MissionStatus.ACTIVE,
                target="Mars",
                instruments=["SAM", "RAMAN", "Microphones"],
                discoveries=["Organic Compounds", "Methane Variations", "Ancient Streambeds"]
            ),
        ]
        
        for mission in missions_data:
            self.missions[mission.name] = mission
    
    def get_star(self, name: str) -> Optional[Dict]:
        """별 정보 조회"""
        if name not in self.stars:
            raise ValueError(f"별을 찾을 수 없음: {name}")
        return self.stars[name].info()
    
    def list_stars(self) -> List[str]:
        """모든 별 목록"""
        return list(self.stars.keys())
    
    def get_exoplanet_system(self, name: str) -> Optional[Dict]:
        """외계행성계 정보 조회"""
        if name not in self.exoplanet_systems:
            raise ValueError(f"행성계를 찾을 수 없음: {name}")
        return self.exoplanet_systems[name].to_dict()
    
    def list_exoplanet_systems(self) -> List[str]:
        """모든 외계행성계 목록"""
        return list(self.exoplanet_systems.keys())
    
    def get_mission(self, name: str) -> Optional[Dict]:
        """우주 탐사 임무 정보 조회"""
        if name not in self.missions:
            raise ValueError(f"임무를 찾을 수 없음: {name}")
        return self.missions[name].summary()
    
    def list_missions(self) -> List[str]:
        """모든 우주 탐사 임무 목록"""
        return list(self.missions.keys())
    
    def calculate_distance_modulus(self, apparent_mag: float, distance_ly: float) -> float:
        """거리계수를 이용한 절대등급 계산"""
        try:
            distance_pc = distance_ly / 3.26156
            return apparent_mag - (5 * math.log10(distance_pc) - 5)
        except (ValueError, ZeroDivisionError):
            raise ValueError("유효하지 않은 겉보기 등급 또는 거리")
    
    def find_habitable_planets(self) -> List[Dict]:
        """거주가능 영역에 있는 행성 찾기"""
        habitable_planets = []
        
        for system_name, system in self.exoplanet_systems.items():
            hz_inner, hz_outer = system.habitable_zone()
            
            for planet in system.planets:
                axis = planet["semi_major_axis_au"]
                if hz_inner <= axis <= hz_outer:
                    habitable_planets.append({
                        "system": system_name,
                        "planet": planet["name"],
                        "star": system.star.name,
                        "semi_major_axis_au": axis,
                        "habitable_zone_inner_au": hz_inner,
                        "habitable_zone_outer_au": hz_outer,
                        "habitable_index": round((axis - hz_inner) / (hz_outer - hz_inner), 2)
                    })
        
        return habitable_planets
    
    def compare_stars(self, star1_name: str, star2_name: str) -> Dict:
        """두 별 비교"""
        if star1_name not in self.stars or star2_name not in self.stars:
            raise ValueError("비교할 별을 찾을 수 없음")
        
        s1 = self.stars[star1_name]
        s2 = self.stars[star2_name]
        
        return {
            "star1": s1.name,
            "star2": s2.name,
            "comparison": {
                "temperature": f"{s1.spectral_type.info()['surface_temp_k']}K vs {s2.spectral_type.info()['surface_temp_k']}K",
                "mass_ratio": f"1 : {round(s2.mass_solar / s1.mass_solar, 2)}",
                "luminosity_ratio": f"1 : {round(s2.luminosity_solar / s1.luminosity_solar, 2)}",
                "distance_ratio": f"1 : {round(s2.distance_ly / s1.distance_ly if s1.distance_ly > 0 else 0, 2)}",
                "magnitude_difference": f"{s2.magnitude - s1.magnitude:.2f} (밝음)"
            }
        }
    
    def get_statistics(self) -> Dict:
        """카트리지 통계"""
        return {
            "version": self.version,
            "stars_count": len(self.stars),
            "exoplanet_systems_count": len(self.exoplanet_systems),
            "total_exoplanets": sum(len(sys.planets) for sys in self.exoplanet_systems.values()),
            "missions_count": len(self.missions),
            "active_missions": sum(1 for m in self.missions.values() if m.status == MissionStatus.ACTIVE),
            "habitable_candidates": len(self.find_habitable_planets())
        }


# ════════════════════════════════════════════════════════════════
# 4️⃣  TESTS: 단위 테스트
# ════════════════════════════════════════════════════════════════

def run_tests() -> Dict:
    """모든 테스트 실행"""
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "tests_passed": 0,
        "tests_failed": 0,
        "details": []
    }
    
    try:
        # 테스트 1: 카트리지 초기화
        cartridge = AstroCartridge()
        test_results["tests_passed"] += 1
        test_results["details"].append("✅ 카트리지 초기화 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 카트리지 초기화 실패: {e}")
        return test_results
    
    # 테스트 2: 별 정보 조회
    try:
        sun_info = cartridge.get_star("Sun")
        assert sun_info["name"] == "Sun"
        assert sun_info["spectral_type"] == "G"
        test_results["tests_passed"] += 1
        test_results["details"].append("✅ 별 정보 조회 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 별 정보 조회 실패: {e}")
    
    # 테스트 3: 외계행성계 조회
    try:
        trappist_info = cartridge.get_exoplanet_system("TRAPPIST-1")
        assert trappist_info["planet_count"] == 7
        assert "habitable_zone_au" in trappist_info
        test_results["tests_passed"] += 1
        test_results["details"].append("✅ 외계행성계 조회 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 외계행성계 조회 실패: {e}")
    
    # 테스트 4: 거주가능 행성 찾기
    try:
        habitable = cartridge.find_habitable_planets()
        assert len(habitable) > 0
        assert "planet" in habitable[0]
        test_results["tests_passed"] += 1
        test_results["details"].append(f"✅ 거주가능 행성 발견: {len(habitable)}개")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 거주가능 행성 찾기 실패: {e}")
    
    # 테스트 5: 별 비교
    try:
        comparison = cartridge.compare_stars("Sun", "Sirius")
        assert "comparison" in comparison
        assert "mass_ratio" in comparison["comparison"]
        test_results["tests_passed"] += 1
        test_results["details"].append("✅ 별 비교 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 별 비교 실패: {e}")
    
    # 테스트 6: 우주 탐사 임무 조회
    try:
        mission = cartridge.get_mission("Hubble Space Telescope")
        assert mission["mission_name"] == "Hubble Space Telescope"
        assert mission["status"] == "진행 중"
        test_results["tests_passed"] += 1
        test_results["details"].append("✅ 우주 탐사 임무 조회 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 우주 탐사 임무 조회 실패: {e}")
    
    # 테스트 7: 거리 계산
    try:
        abs_mag = cartridge.calculate_distance_modulus(-1.46, 8.6)
        assert isinstance(abs_mag, float)
        test_results["tests_passed"] += 1
        test_results["details"].append("✅ 거리 계산 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 거리 계산 실패: {e}")
    
    # 테스트 8: 통계
    try:
        stats = cartridge.get_statistics()
        assert stats["stars_count"] > 0
        assert stats["exoplanet_systems_count"] > 0
        assert stats["habitable_candidates"] > 0
        test_results["tests_passed"] += 1
        test_results["details"].append("✅ 통계 계산 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 통계 계산 실패: {e}")
    
    # 테스트 9: 에러 처리
    try:
        try:
            cartridge.get_star("NonexistentStar")
            test_results["tests_failed"] += 1
            test_results["details"].append("❌ 에러 처리 실패: 예외가 발생하지 않음")
        except ValueError:
            test_results["tests_passed"] += 1
            test_results["details"].append("✅ 에러 처리 성공")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 에러 처리 테스트 실패: {e}")
    
    # 테스트 10: 모든 목록 조회
    try:
        stars = cartridge.list_stars()
        systems = cartridge.list_exoplanet_systems()
        missions = cartridge.list_missions()
        assert len(stars) > 0
        assert len(systems) > 0
        assert len(missions) > 0
        test_results["tests_passed"] += 1
        test_results["details"].append(f"✅ 모든 목록 조회 성공: {len(stars)} 별, {len(systems)} 행성계, {len(missions)} 임무")
    except Exception as e:
        test_results["tests_failed"] += 1
        test_results["details"].append(f"❌ 모든 목록 조회 실패: {e}")
    
    test_results["total_tests"] = test_results["tests_passed"] + test_results["tests_failed"]
    test_results["success_rate"] = round(
        (test_results["tests_passed"] / test_results["total_tests"] * 100) 
        if test_results["total_tests"] > 0 else 0, 
        1
    )
    
    return test_results


# ════════════════════════════════════════════════════════════════
# 5️⃣  MAIN: 데모 및 테스트 실행
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 AstroCartridge v1.0.0 - Groq 초고속 우주과학 카트리지")
    print("=" * 70)
    
    # 카트리지 초기화
    astro = AstroCartridge()
    
    # 통계 출력
    print("\n📊 시스템 통계:")
    stats = astro.get_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # 거주가능 행성 조회
    print("\n🌍 거주가능 영역 행성:")
    habitable = astro.find_habitable_planets()
    for planet in habitable:
        print(f"  - {planet['planet']} ({planet['system']})")
    
    # 테스트 실행
    print("\n🧪 테스트 실행:")
    print("=" * 70)
    test_results = run_tests()
    print(json.dumps(test_results, indent=2, ensure_ascii=False))
    
    print("\n✨ AstroCartridge 준비 완료!")
