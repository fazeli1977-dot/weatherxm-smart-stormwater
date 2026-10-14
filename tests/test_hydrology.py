import pytest
from weatherxm_smart_stormwater.hydrology import HydrologyEngine
from weatherxm_smart_stormwater.models import CatchmentParameters, FloodRiskLevel

def test_rational_method_discharge():
    # Q = 0.00278 * 0.8 * 50.0 * 20.0 = 2.224 m3/s
    q = HydrologyEngine.calculate_peak_discharge(c=0.8, intensity_mm_h=50.0, area_ha=20.0)
    assert pytest.approx(q, 0.01) == 2.224

def test_flood_risk_critical():
    catchment = CatchmentParameters(
        catchment_id="Urban-Zone-1",
        area_hectares=30.0,
        runoff_coefficient=0.85,
        stormwater_network_capacity_m3_s=2.0
    )
    # Intensity: 40 mm/h -> Q = 0.00278 * 0.85 * 40 * 30 = 2.8356 m3/s (> 2.0 m3/s -> CRITICAL)
    assessment = HydrologyEngine.evaluate_catchment(catchment, precipitation_rate_mm_h=40.0)
    assert assessment.risk_level == FloodRiskLevel.CRITICAL
    assert assessment.capacity_saturation_pct > 100.0

def test_flood_risk_normal():
    catchment = CatchmentParameters(
        catchment_id="Urban-Zone-2",
        area_hectares=10.0,
        runoff_coefficient=0.3,
        stormwater_network_capacity_m3_s=5.0
    )
    assessment = HydrologyEngine.evaluate_catchment(catchment, precipitation_rate_mm_h=5.0)
    assert assessment.risk_level == FloodRiskLevel.NORMAL
    assert assessment.capacity_saturation_pct < 50.0
